//-------------------------------------------------------------------
//-- leds_and_buttons_tb.v
//-- Testbench
//-------------------------------------------------------------------
`default_nettype none
`timescale 100 ns / 10 ns

module leds_and_buttons_tb();
  reg clk = 0;
  always #1 clk = ~clk;

  reg  [2:0] btn = 0;
  wire [4:0] led;

  leds_and_buttons UUT (.btn(btn), .led(led));

  initial begin
    // filename is propagated by platformio
    $dumpfile(``VCD_OUTPUT);
    $dumpvars(0, leds_and_buttons_tb);
    
    btn = 3'b001;
    #20
    btn = 3'b010;
    #20
    btn = 3'b100;
    #20
    btn = 3'b101;
    #20
    btn = 3'b111;
    #20
    
    $display("End of simulation");
    $finish;
  end

endmodule
