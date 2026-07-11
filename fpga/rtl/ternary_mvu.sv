// Synthesizable reference kernel: one output row, LANES weights per cycle.
// Encoding: 2'b00 skip, 2'b01 add, 2'b10 subtract, 2'b11 reserved/error.
module ternary_mvu #(
  parameter int LANES = 8,
  parameter int ACT_W = 8,
  parameter int ACC_W = 32
) (
  input  logic                         clk,
  input  logic                         rst_n,
  input  logic                         clear,
  input  logic                         valid_i,
  input  logic signed [ACT_W-1:0]      activation_i [LANES],
  input  logic        [1:0]            weight_i [LANES],
  output logic signed [ACC_W-1:0]      accumulator_o,
  output logic                         reserved_symbol_o
);
  integer lane;
  logic signed [ACC_W-1:0] cycle_sum;
  logic reserved_cycle;

  always_comb begin
    cycle_sum = '0;
    reserved_cycle = 1'b0;
    for (lane = 0; lane < LANES; lane = lane + 1) begin
      unique case (weight_i[lane])
        2'b00: cycle_sum = cycle_sum;
        2'b01: cycle_sum = cycle_sum + activation_i[lane];
        2'b10: cycle_sum = cycle_sum - activation_i[lane];
        default: reserved_cycle = 1'b1;
      endcase
    end
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      accumulator_o <= '0;
      reserved_symbol_o <= 1'b0;
    end else if (clear) begin
      accumulator_o <= '0;
      reserved_symbol_o <= 1'b0;
    end else if (valid_i) begin
      accumulator_o <= accumulator_o + cycle_sum;
      reserved_symbol_o <= reserved_symbol_o | reserved_cycle;
    end
  end
endmodule
