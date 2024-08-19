module top
    #(
        parameter  NB_LED       = 4 ,
        parameter  NB_CNT       = 32,
        parameter  NB_BUTTONS   = 4 ,
        parameter  NB_SW        = 4
    )

    (
        // output [NB_LED-1:0]     o_led_r ,
        // output [NB_LED-1:0]     o_led_g ,
        // output [NB_LED-1:0]     o_led_b ,
        // output [NB_LED-1:0]     o_led   ,
        // input  [NB_SW-1:0]      i_sw    ,
        // input  [NB_BUTTONS-1:0] i_btn   ,
        // input                   i_reset ,
        input                   clock   
    );

    wire [NB_LED-1:0]       o_led_r                     ;
    wire [NB_LED-1:0]       o_led_g                     ;
    wire [NB_LED-1:0]       o_led_b                     ;
    wire [NB_LED-1:0]       o_led                       ;
    wire [NB_SW-1:0]        i_sw                        ;
    wire [NB_BUTTONS-1:0]   i_btn                       ;
    wire                    i_reset                     ;

    wire                    connect_c2shiftref          ;
    wire [NB_LED-1:0]       connect_shiftref2led        ;
    wire [NB_LED-1:0]       connect_flash2led           ;
    wire [NB_LED-1:0]       connect_controller2led      ;
    wire [NB_LED-1:0]       connect_controller2led_r    ;
    wire [NB_LED-1:0]       connect_controller2led_g    ;
    wire [NB_LED-1:0]       connect_controller2led_b    ;


    count 
        #(
            .NB_SW  (NB_CNT - 1 ),
            .NB_CNT (NB_CNT     )
        )
        u_count
        (
            .o_valid    (connect_c2shiftref )  ,
            .i_sw       (i_sw[NB_SW-2:0]    )  ,
            .i_reset    (~i_reset           )  ,
            .clock      (clock              )
        );


    shiftreg 
        #(
            .NB_LED (NB_LED)
        )
        u_shiftreg
        (
            .o_led      (connect_shiftref2led   ) ,
            .i_valid    (connect_c2shiftref     ) ,
            .i_sw       (i_sw[NB_SW-1]          ) ,
            .i_reset    (~i_reset               ) ,
            .clock      (clock                  )
        );

    flash
        #(
            .NB_LED (NB_LED)
        )
        u_flash
        (
            .o_led      (connect_flash2led      ) ,
            .i_valid    (connect_c2shiftref     ) ,
            .i_reset    (~i_reset               ) ,
            .clock      (clock                  )
        );


    button_controller
        #(
            .NB_BUTTONS     (NB_BUTTONS )    ,
            .NB_LED         (NB_LED     )
        )
        u_button_controller
        (
            .o_led          (connect_controller2led     ),
            .o_led_r        (connect_controller2led_r   ),
            .o_led_g        (connect_controller2led_g   ),
            .o_led_b        (connect_controller2led_b   ),
            .i_led_flash    (connect_flash2led          ),   
            .i_led_shiftreg (connect_shiftref2led       ),   
            .i_btn          (i_btn                      ),
            .i_reset        (~i_reset                   ),
            .clock          (clock                      )
        );

    assign o_led_r  = connect_controller2led_r  ;
    assign o_led_g  = connect_controller2led_g  ;
    assign o_led_b  = connect_controller2led_b  ;
    assign o_led    = connect_controller2led    ;

    design_1
    u_vio
    (
        .clk_0       (clock     ),
        .probe_in0_0 (o_led_r   ),
        .probe_in1_0 (o_led_g   ),
        .probe_in2_0 (o_led_b   ),
        .probe_in3_0 (o_led     ),
        .probe_out0_0(i_btn     ),
        .probe_out1_0(i_sw      ),
        .probe_out2_0(i_reset   )

    );

    ila
    u_ila
    (
        .clk_0   (clock     ),
        .probe0_0(o_led_r   ),
        .probe1_0(o_led_g   ),
        .probe2_0(o_led_b   ),
        .probe3_0(o_led     )

    );

endmodule