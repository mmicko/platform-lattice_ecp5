//--------------------------------------------------------------------
//-- iCEstick test
//-- Counter example
//--------------------------------------------------------------------
//-- March 2016. Written by Juan Gonzalez (obijuan)
//--------------------------------------------------------------------
//-- Releases under the GPL v2+ license
//--------------------------------------------------------------------

module counter #(
        parameter N = 29          //-- Counter bits lentgh
  )(
        input wire clk_25mhz,
        output wire [4:0] led
);

reg [N-1:0] cont;
reg rstn = 0;

//-- Initialization
always @(posedge clk_25mhz)
  rstn <= 1;

//-- counter, with synchronous reset
always @(posedge clk_25mhz)
  if (!rstn)
    cont <= 0;
  else
    cont <= cont + 1;

//-- Connect the 5 most significant bits to the leds
assign led = cont[N-1: N-6];

endmodule
