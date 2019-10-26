//--------------------------------------------------------------------
//-- iCEBreaker - Leds and buttons example
//--------------------------------------------------------------------

module leds_and_buttons(input [2:0] btn, output wire [4:0] led);
    assign led = { 2'b10, btn };
endmodule