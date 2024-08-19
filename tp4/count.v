module count 
    #(
        parameter NB_SW   = 3,
        parameter NB_CNT  = 32
    )
    (
        output              o_valid ,
        input [NB_SW-1:0]   i_sw    ,
        input               i_reset ,
        input               clock
    );

    // LOCAL PARAMETERS
    localparam [NB_CNT-1:0]  R0 = 2**(NB_CNT-10)-1;
    localparam [NB_CNT-1:0]  R1 = 2**(NB_CNT-12)-1;
    localparam [NB_CNT-1:0]  R2 = 2**(NB_CNT-14)-1;
    localparam [NB_CNT-1:0]  R3 = 2**(NB_CNT-16)-1;

    // VARIABLES
    wire    [NB_CNT:0]      limit_ref;
    reg     [NB_CNT-1:0]    cnt;
    reg                     valid;

    // RUN
    assign limit_ref =  i_sw[2:1] == 0 ? R0:
                        i_sw[2:1] == 1 ? R1:
                        i_sw[2:1] == 2 ? R2: R3;

                
    always @(posedge clock) begin
        if (i_reset) begin
            valid   <= 1'b0             ;
            cnt     <= {NB_CNT{1'b0}}   ;     
        end 
        else if(i_sw[0]) begin
            if (cnt<limit_ref) begin
                valid   <= 1'b0         ;
                cnt     <= cnt + 1      ; 
            end
            else begin
                valid   <= 1'b1             ;
                cnt     <= {NB_CNT{1'b0}}   ;     
            end
        end
        else begin
            valid <= valid  ;
            cnt   <= cnt    ; 
        end
    end

    assign o_valid = valid ;

endmodule