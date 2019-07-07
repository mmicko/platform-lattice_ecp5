# Lattice ECP5: development platform for [PlatformIO](http://platformio.org)

Lattice ECP5 FPGAs are fully usable by open source tools.

* [Home](http://platformio.org/platforms/lattice_ecp5) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/lattice_ecp5.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = lattice_ecp5
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-lattice_ecp5.git
board = ...
...
```

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/lattice_ecp5.html).


# Credits

* [Prjtrellis](https://github.com/SymbiFlow/prjtrellis/)
* [NextPnR](https://github.com/YosysHQ/nextpnr/)
* [Icarus Verilog](http://iverilog.icarus.com/)
