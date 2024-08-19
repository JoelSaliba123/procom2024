module button_controller
    #(
        parameter NB_BUTTONS = 4,
        parameter NB_LED     = 4
    )
    (
        output [NB_LED-1:0]         o_led           ,
        output [NB_LED-1:0]         o_led_r         ,
        output [NB_LED-1:0]         o_led_g         ,
        output [NB_LED-1:0]         o_led_b         ,
        input  [NB_LED-1:0]         i_led_flash     ,   
        input  [NB_LED-1:0]         i_led_shiftreg  ,   
        input  [NB_BUTTONS-1:0]     i_btn           ,
        input                       i_reset         ,
        input                       clock
    );

    // LOCALPARAMS
    localparam  SEL_BUTTON      = 0;
    localparam  RED_BUTTON      = 1;
    localparam  GREEN_BUTTON    = 2;
    localparam  BLUE_BUTTON     = 3;

    //VARIABLES
    reg [NB_BUTTONS-1:0]    i_btn_last  ; 
    reg [NB_BUTTONS-1:0]    i_btn_det   ;
    reg [NB_BUTTONS-1:0]    i_btn_mem   ;

    always @(posedge clock) begin
        if (i_reset) begin
            i_btn_last <= {(NB_BUTTONS){1'b0}};
            i_btn_det  <= {(NB_BUTTONS){1'b0}};
            i_btn_mem  <= {(NB_BUTTONS){1'b0}};
        end
        else begin
            // Detectar flancos ascendentes
            i_btn_det <= (i_btn & ~i_btn_last);
    
            // Actualizar i_btn_mem basado en la detección de flancos ascendentes
            if (i_btn_det != {(NB_BUTTONS){1'b0}}) begin
                i_btn_mem[SEL_BUTTON] <= i_btn_mem[SEL_BUTTON] ^ i_btn_det[SEL_BUTTON];
                case (i_btn_det[BLUE_BUTTON:RED_BUTTON])
                    3'b001, 3'b010, 3'b100: begin
                        i_btn_mem[BLUE_BUTTON:RED_BUTTON] <= i_btn_det[BLUE_BUTTON:RED_BUTTON];
                    end
                    default: begin
                        i_btn_mem[BLUE_BUTTON:RED_BUTTON] <= i_btn_mem[BLUE_BUTTON:RED_BUTTON];
                    end
                endcase
            end
    
            // Actualizar i_btn_last
            i_btn_last <= i_btn;
        end
    end
    

    assign o_led   = i_btn_mem;
    assign o_led_r = i_btn_mem[RED_BUTTON     ]   ? (i_btn_mem[SEL_BUTTON] ? i_led_flash : i_led_shiftreg) : {(NB_LED){1'b0}};
    assign o_led_g = i_btn_mem[GREEN_BUTTON   ]   ? (i_btn_mem[SEL_BUTTON] ? i_led_flash : i_led_shiftreg) : {(NB_LED){1'b0}};
    assign o_led_b = i_btn_mem[BLUE_BUTTON    ]   ? (i_btn_mem[SEL_BUTTON] ? i_led_flash : i_led_shiftreg) : {(NB_LED){1'b0}};
    

endmodule    
    
