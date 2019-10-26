//--------------------------------------------------------------------
//-- iCEBreaker - Counter example
//--------------------------------------------------------------------

module counter #(parameter LOG2DELAY = 21)
    (input clk_25mhz, output wire [4:0] led);
    localparam BITS = 5;

    reg [BITS+LOG2DELAY-1:0] counter = 0;
    reg [BITS-1:0] outcnt;

    always @(posedge clk_25mhz) begin
        counter <= counter + 1;
        outcnt <= (counter >> LOG2DELAY);
    end

    assign led = outcnt;
endmodule
