module shift_mode
    #(
        parameter NB_LED = 4
    )
    (
        output [NB_LED-1:0] o_led   ,
        input               i_valid ,
        input               i_sw    ,
        input               i_reset ,
        input               clock
    );

    //VARIABLES
    reg [(NB_LED+2)-1:0] o_led_signal;
    
    // RUN
    always @(posedge clock) begin
        if (i_reset) begin
            o_led_signal <= {1'b1, {NB_LED{1'b0}}, 1'b1};
        end
        else if(i_valid) begin
            if (i_sw) begin
                o_led_signal[NB_LED-2:0]            <= o_led_signal[NB_LED-2:0] << 1            ;
                o_led_signal[0]                     <= o_led_signal[NB_LED-2]                   ;

                o_led_signal[NB_LED+1:NB_LED-1]     <= o_led_signal[NB_LED+1:NB_LED-1] >> 1     ;
                o_led_signal[NB_LED+1]              <= o_led_signal[NB_LED-1]                   ;
            end
            else begin
                o_led_signal[NB_LED-2:0]            <= o_led_signal[NB_LED-2:0] >> 1            ;
                o_led_signal[NB_LED-2]              <= o_led_signal[0]                          ;

                o_led_signal[NB_LED+1:NB_LED-1]     <= o_led_signal[NB_LED+1:NB_LED-1] << 1     ;
                o_led_signal[NB_LED-1]              <= o_led_signal[NB_LED+1]                   ;  
            end
        end
        else begin 
            o_led_signal <= o_led_signal;
        end
    end

    assign o_led = o_led_signal[NB_LED:1];
endmodule