
`timescale 1ns/100ps

module tb_top_ej2 ();


    parameter NB_BUTTONS    = 4 ;    
    parameter NB_SW         = 4 ;
    parameter NB_COUNTER    = 16;
    parameter NB_LED        = 4 ;

    wire [NB_LED - 1 : 0] o_led  ; 
    wire [NB_LED - 1 : 0] o_led_b;
    wire [NB_LED - 1 : 0] o_led_g;
    wire [NB_LED - 1 : 0] o_led_r;

    reg  [NB_SW   - 1 : 0]      i_sw   ;
    reg  [NB_BUTTONS   - 1 : 0] i_btn  ;
    reg                         i_reset;
    reg                         clock  ;
    
    initial begin
        clock   = 1'b0;
        i_sw    = 4'b0000;
        i_btn   = 4'b0000;

        //Reset system
        i_reset = 1'b0;
        #100;
        @(posedge clock);
        i_reset = 1'b1;
        #100;

        //Mode 3 - RED  
        @(posedge clock);
        i_sw    = 4'b0001;
        #10
        @(posedge clock);
        i_btn   = 4'b0011;
        #10
        @(posedge clock);
        i_btn   = 4'b0000;
        #10
        @(posedge clock);
        i_btn   = 4'b0001;
        #10
        @(posedge clock);
        i_btn   = 4'b0000;
        #10
        

        //Change Speed
        @(posedge clock);
        i_sw    = 4'b0001;
        #3000;
        @(posedge clock);
        i_sw    = 4'b0011;
        #1000;
        @(posedge clock);
        i_sw    = 4'b0101;
        #500;
        @(posedge clock);
        i_sw    = 4'b0111;
        #70;

        //Change Speed
        @(posedge clock);
        i_sw    = 4'b1001;
        #3000;
        @(posedge clock);
        i_sw    = 4'b1011;
        #1000;
        @(posedge clock);
        i_sw    = 4'b1101;
        #500;
        @(posedge clock);
        i_sw    = 4'b1111;
        #70;

    
        $finish;
    end

    always #5 clock = ~clock;

    top_ej2 
        #(
            .NB_LED       (NB_LED       ),
            .NB_CNT       (NB_COUNTER   ),
            .NB_BUTTONS   (NB_BUTTONS   ),
            .NB_SW        (NB_SW        )
        ) 
        u_top
        (
            .o_led_r (o_led_r   ),
            .o_led_g (o_led_g   ),
            .o_led_b (o_led_b   ),
            .o_led   (o_led     ),
            .i_sw    (i_sw      ),
            .i_btn   (i_btn     ),
            .i_reset (i_reset   ),
            .clock   (clock     )
        );



endmodule