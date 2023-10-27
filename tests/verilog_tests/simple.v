module simple(a, b, c, d, o);
  input a, b, c, d;
  output o;
  wire a, b, c, d;
  wire o;
  wire n_0, n_1;
  NOR2X1 g43__2398(.A (n_1), .B (d), .Y (o));
  NOR2X1 g44__5107(.A (n_0), .B (c), .Y (n_1));
  AND2X1 g45__6260(.A (a), .B (b), .Y (n_0));
endmodule

