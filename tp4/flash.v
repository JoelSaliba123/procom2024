module flash
    #(
        parameter NB_LED = 4
    )
    (
        output [NB_LED-1:0] o_led   ,
        input               i_valid ,
        input               i_reset ,
        input               clock
    );

    //VARIABLES
    reg [NB_LED-1:0] flash_leds;
    
    // RUN
    always @(posedge clock) begin
        if (i_reset) begin
            flash_leds <= {(NB_LED){1'b0}};
        end
        else if(i_valid) begin
            flash_leds <= ~flash_leds;
        end
        else begin 
            flash_leds <= flash_leds;
        end
    end

    assign o_led = flash_leds;
endmodule