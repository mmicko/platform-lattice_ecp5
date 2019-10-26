# -*- coding: utf-8 -*-
# Copyright 2014-present PlatformIO <contact@platformio.org>
# Copyright 2016-present Juan González <juan@iearobotics.com>
#                        Jesús Arroyo Torrens <jesus.jkhlg@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    Build script for Lattice iCE40 FPGAs
"""

import os
from os.path import join
from platform import system

from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default,
                          DefaultEnvironment, Exit, GetOption,
                          Glob)

env = DefaultEnvironment()
pioPlatform = env.PioPlatform()

env.Replace(
    PROGNAME='hardware',
    UPLOADER=env.BoardConfig().get('upload.command', ''),
    UPLOADERFLAGS=env.BoardConfig().get('upload.args', ''),
    UPLOADBINCMD='$UPLOADER $UPLOADERFLAGS $SOURCES')
env.Append(SIMULNAME='simulation')

# -- Target name for synthesis
TARGET = join(env['BUILD_DIR'], env['PROGNAME'])

# -- Resources paths
IVL_PATH = join(
    pioPlatform.get_package_dir('toolchain-iverilog'), 'lib', 'ivl')
VLIB_PATH = join(
    pioPlatform.get_package_dir('toolchain-iverilog'), 'vlib')
YOSYS_PATH = join(
    pioPlatform.get_package_dir('toolchain-yosys'), 'share', 'yosys')
DATABASE_PATH = join(
    pioPlatform.get_package_dir('toolchain-ecp5'), 'share', 'trellis', 'database')

VLIB_FILES = ' '.join([
    '"{}"'.format(f) for f in Glob(join(VLIB_PATH, '*.v'))
    ]) if VLIB_PATH else ''

isWindows = 'Windows' == system()
VVP_PATH = '' if isWindows else '-M "{0}"'.format(IVL_PATH)
IVER_PATH = '' if isWindows else '-B "{0}"'.format(IVL_PATH)

# -- Get a list of all the verilog files in the src folfer, in ASCII, with
# -- the full path. All these files are used for the simulation
v_nodes = Glob(join(env['PROJECTSRC_DIR'], '*.v'))
src_sim = [str(f) for f in v_nodes]

# --- Get the Testbench file (there should be only 1)
# -- Create a list with all the files finished in _tb.v. It should contain
# -- the test bench
list_tb = [f for f in src_sim if f[-5:].upper() == '_TB.V']

if len(list_tb) > 1:
    print('---> WARNING: More than one testbenches used')

# -- Error checking
try:
    testbench = list_tb[0]

# -- there is no testbench
except IndexError:
    testbench = None

SIMULNAME = ''
TARGET_SIM = ''

# clean
if len(COMMAND_LINE_TARGETS) == 0:
    if testbench is not None:
        # -- Simulation name
        testbench_file = os.path.split(testbench)[-1]
        SIMULNAME, ext = os.path.splitext(testbench_file)
# sim
elif 'sim' in COMMAND_LINE_TARGETS:
    if testbench is None:
        print('---> ERROR: NO testbench found for simulation')
        Exit(1)

    # -- Simulation name
    testbench_file = os.path.split(testbench)[-1]
    SIMULNAME, ext = os.path.splitext(testbench_file)

# -- Target sim name
if SIMULNAME:
    TARGET_SIM = join(env.subst('$BUILD_DIR'), SIMULNAME).replace('\\', '\\\\')

# --- Get the synthesis files. They are ALL the files except the testbench
src_synth = [f for f in src_sim if f not in list_tb]

# -- Get the PCF file
src_dir = env.subst('$PROJECTSRC_DIR')
LPFs = join(src_dir, '*.lpf')
LPF_list = Glob(LPFs)
LPF = ''

try:
    LPF = LPF_list[0]
except IndexError:
    print('---> WARNING: no .lpf file found')

#
# Builder: Yosys (.v --> .json)
#
synth = Builder(
    action='yosys -p \"synth_ecp5 -json $TARGET\" -q $SOURCES',
    suffix='.json',
    src_suffix='.v')

#
# Builder: Arachne-pnr (.json --> .asc)
#
pnr = Builder(
    action='nextpnr-ecp5 --{1} --package {2} --json $SOURCE --lpf {3} --textcfg $TARGET --quiet --lpf-allow-unconstrained'.format(
        env.BoardConfig().get('build.type', ''),
        env.BoardConfig().get('build.size', '25k'),
        env.BoardConfig().get('build.pack', 'CABGA381'),
        LPF
    ),
    suffix='.asc',
    src_suffix='.json')

#
# Builder: ecppack (.config --> .bin)
#
bitstream = Builder(
    action='ecppack --db {0} {1} $SOURCE $TARGET'.format(DATABASE_PATH, env.BoardConfig().get('build.idcode', '')),
    suffix='.bin',
    src_suffix='.config')


env.Append(BUILDERS={
    'Synth': synth, 'PnR': pnr, 'Bin': bitstream})

blif = env.Synth(TARGET, [src_synth])
asc = env.PnR(TARGET, [blif, LPF])
binf = env.Bin(TARGET, asc)

#
# Target: Upload bitstream
#
target_upload = env.Alias('upload', binf, '$UPLOADBINCMD')
AlwaysBuild(target_upload)

#
# Builders: Icarus Verilog
#
iverilog = Builder(
    action='iverilog {0} -o $TARGET -D VCD_OUTPUT={1} {2} $SOURCES'.format(
        IVER_PATH, TARGET_SIM + '.vcd' if TARGET_SIM else '', VLIB_FILES),
    suffix='.out',
    src_suffix='.v')
vcd = Builder(
    action='vvp {0} $SOURCE'.format(
        VVP_PATH),
    suffix='.vcd',
    src_suffix='.out')
# NOTE: output file name is defined in the
#       iverilog call using VCD_OUTPUT macro

env.Append(BUILDERS={'IVerilog': iverilog, 'VCD': vcd})

#
# Target: Verify verilog code
#
vout = env.IVerilog(TARGET, src_synth)

target_verify = env.Alias('verify', vout)
AlwaysBuild(target_verify)

#
# Target: Simulate testbench
#
sout = env.IVerilog(TARGET_SIM, src_sim)
vcd_file = env.VCD(sout)

target_sim = env.Alias('sim', vcd_file, 'gtkwave {0} {1}.gtkw'.format(
    vcd_file[0], join(env['PROJECTSRC_DIR'], SIMULNAME)))
AlwaysBuild(target_sim)

# -- Verilator builder
verilator = Builder(
    action='verilator --lint-only -v {0}/ecp5/cells_sim.v -DNO_INCLUDES {1} {2} {3} {4} $SOURCES'.format(
        YOSYS_PATH,
        '-Wall',
        '-Wno-style',
        '',
        ''),
    src_suffix='.v')

env.Append(BUILDERS={'Verilator': verilator})

# --- Lint
lout = env.Verilator(TARGET, src_synth)

lint = env.Alias('lint', lout)
AlwaysBuild(lint)

#
# Setup default targets
#
Default([binf])

#
# Target: Clean generated files
#
if GetOption('clean'):
    env.Default([t, vout, sout, vcd_file])
