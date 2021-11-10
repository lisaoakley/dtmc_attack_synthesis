// Model taken from Daws04
// This is modified from a version by Ernst Moritz Hahn (emh@cs.uni-sb.de)
// Ref: https://depend.cs.uni-saarland.de/tools/param/casestudies/#zeroconf

dtmc

const int K = 65024;
const int m = 50000;
const double q = m/K;
const int n = 10;
const double p = .6;

module main
  s: [0..n+3];

  [] (s=n+2) -> (s'=n+3);
  [] (s=0) -> 1-q : (s'=n+2) + q : (s'=1);
  [] (s>0) & (s<n+1) -> 1-p : (s'=0) + p : (s'=s+1);

endmodule

init
  s = 0
endinit
