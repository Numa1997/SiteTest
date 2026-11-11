// Fig. 12: the C++ cart against the JavaScript cart, the stout rigid (no fluid force), 0.1 ms steps.
// g++ -O2 -o test_cart test_cart.cpp && ./test_cart <dir from write_cart.cjs with TRACE> <T s>
#include "cart.H"
#include <cstdio>
#include <cstdlib>
int main(int argc, char** argv) {
    fig12::Cart c; const std::string d = argv[1]; c.load(d + "/cart.params", d + "/road.table");
    const double T = std::atof(argv[2]);
    std::FILE* f = std::fopen((d + "/trace.cpp.txt").c_str(), "w");
    for (long n = 1; n * 1e-4 <= T + 1e-12; n++) { c.step(1e-4, 0, 0); if (n % 100 == 0) std::fprintf(f, "%.17g %.17g %.17g %.17g %.17g %.17g %.17g\n", c.t, c.x, c.vx, c.zb, c.zw, c.i, c.xi); }
    std::fclose(f); return 0;
}
