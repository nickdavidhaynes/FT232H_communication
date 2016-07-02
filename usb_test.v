module usb_test(CLOCK_50,SW,GPIO,LEDR,LEDG,KEY);

input CLOCK_50;
input [7:0] SW;
input [0:0] KEY;

inout [35:0] GPIO;

output [8:0] LEDR;
output [7:0] LEDG;

wire [7:0] write_data;
wire [7:0] read_data;
wire byte_received;

wire write_request;

assign write_data[7:0] = SW[7:0];
assign LEDR[7:0] = write_data[7:0];
assign LEDG[7:0] = read_data[7:0];
assign LEDR[8] = byte_received;

slow_clk clk(CLOCK_50,write_request);
//assign write_request = ~KEY;

USB USB0(.CLOCK_50(CLOCK_50),
		   .GPIO(GPIO[35:0]),
			.reset(1'b0),
			.write_request(write_request),
			.byte_received(byte_received),
			.write_data(write_data[7:0]),
			.read_data(read_data[7:0]));

endmodule 