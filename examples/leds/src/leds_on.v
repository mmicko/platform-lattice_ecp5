//--------------------------------------------------------------------
//-- IceZUM Alhambra test
//-- Hello world example
//-- Turn on all the yellow leds
//--------------------------------------------------------------------
//-- March 2016. Written by Juan Gonzalez (obijuan)
//--------------------------------------------------------------------
//-- Releases under the GPL v2+ license
//--------------------------------------------------------------------

module leds_on(output wire [6:0] led);

//-- Turn on all the leds
assign led = 8'hFF;

endmodule
