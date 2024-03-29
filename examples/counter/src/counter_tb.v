//-------------------------------------------------------------------
//-- counter_tb.v
//-- Testbench
//-------------------------------------------------------------------
`default_nettype none
`timescale 100 ns / 10 ns

module counter_tb();
  reg clk = 0;
  always #1 clk = ~clk;

  wire [4:0] led;

  counter #(.LOG2DELAY(1)) UUT (.clk_25mhz(clk), .led(led));

  initial begin
    // filename is propagated by platformio
    $dumpfile(``VCD_OUTPUT);
    $dumpvars(0, counter_tb);    
    // simulation lasts 1000 clocks
    #1000 $display("End of simulation");
    $finish;
  end

endmodule
