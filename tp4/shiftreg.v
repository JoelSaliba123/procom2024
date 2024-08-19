module shiftreg
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
    reg [NB_LED-1:0] shift_register;
    
    // RUN
    always @(posedge clock) begin
        if (i_reset) begin
            shift_register <= {{(NB_LED-1){1'b0}},1'b1};
        end
        else if(i_valid) begin
            
            if (i_sw) begin
                shift_register       <= shift_register << 1         ;
                shift_register[0]    <= shift_register[NB_LED-1]    ;
            end
            else begin
                shift_register              <= shift_register >> 1  ;
                shift_register[NB_LED-1]    <= shift_register[0]    ;    
            end
        end
        else begin 
            shift_register <= shift_register;
        end
    end

    assign o_led = shift_register;
endmodule