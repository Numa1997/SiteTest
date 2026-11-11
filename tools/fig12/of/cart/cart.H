// Fig. 12: the cart's equations of motion in C++, a line-by-line port of Cart in public/scripts/stout-cart.js (forces,
// sample, step, reset, resist), for the OpenFOAM coupling (tools/fig12/of/case/constant/fvModels, cartCoupling).
// The cart: x along the road, z_b the body (bottom), z_w the axle. A wheel of radius Rw on a radial tyre (kt, ct) rolls
// on the road, whose axle path z_a(x) (the height of the centre of an undeformed wheel rolling over the profile) is a table
// written by write_cart.cjs from the JavaScript Road; a spring and damper (k, c) hold the body on the axle; a DC gear motor
// in a current loop (lag tauI) drives the wheel through the tyre's grip (mu N); the controller, sampled every Ts, holds the
// current that balances the drag (off), adds a PI loop on the speed (speed), or also cancels the road's push one current
// lag ahead (preview). The liquid's reaction beyond rigid co-motion (Fx, Fz) comes from the fluid each step.
// Units SI. Parameters and the road come from two text files (write_cart.cjs): no defaults here.
#ifndef FIG12_CART_H
#define FIG12_CART_H
#include <cmath>
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include <stdexcept>

namespace fig12 {

struct Cart {
    // parameters
    double Mb, mw, Rw, Iw, k, c, kt, ct, cx, Crr, Tf, bf, CdA, rhoAir, vSmooth, v0, ml, Ls, g;
    double Ngear, Km, Ra, Jm, Vmax, Imax, tauI, Ts, Kp, Ki, csky, Umax, tauU, mu;
    int ctrl;      // 0 off, 1 speed, 2 preview
    int susp;      // 0 or 1
    // road: axle height table z_a(x) every h from xmin
    double xmin, h; std::vector<double> za;
    // state
    double x, vx, zb, vzb, zw, vzw, i, icmd, xi, us, uscmd, t, tSample;
    // derived each forces()
    double zaNow, dza, N, Fs, Froad, Fdrive, Fres, ax, azb, azw, ireach, emf, Vm, Flx, Flz, Fgrip; int slip;

    static std::map<std::string, double> readParams(const std::string& file) {
        std::ifstream in(file); if (!in) throw std::runtime_error("cart: cannot read " + file);
        std::map<std::string, double> p; std::string key; double v;
        while (in >> key >> v) p[key] = v;
        return p;
    }
    static double need(const std::map<std::string, double>& p, const char* key) {
        auto it = p.find(key); if (it == p.end()) throw std::runtime_error(std::string("cart: missing parameter ") + key);
        return it->second;
    }
    void load(const std::string& paramFile, const std::string& roadFile) {
        auto p = readParams(paramFile);
        Mb = need(p, "Mb"); mw = need(p, "mw"); Rw = need(p, "Rw"); Iw = need(p, "Iw"); k = need(p, "k"); c = need(p, "c");
        kt = need(p, "kt"); ct = need(p, "ct"); cx = need(p, "cx"); Crr = need(p, "Crr"); Tf = need(p, "Tf"); bf = need(p, "bf");
        CdA = need(p, "CdA"); rhoAir = need(p, "rhoAir"); vSmooth = need(p, "vSmooth"); v0 = need(p, "v0"); ml = need(p, "ml");
        Ls = need(p, "Ls"); g = need(p, "g"); Ngear = need(p, "Ngear"); Km = need(p, "Km"); Ra = need(p, "Ra"); Jm = need(p, "Jm");
        Vmax = need(p, "Vmax"); Imax = need(p, "Imax"); tauI = need(p, "tauI"); Ts = need(p, "Ts"); Kp = need(p, "Kp"); Ki = need(p, "Ki");
        csky = need(p, "csky"); Umax = need(p, "Umax"); tauU = need(p, "tauU"); mu = need(p, "mu");
        ctrl = int(need(p, "ctrl")); susp = int(need(p, "susp"));
        std::ifstream r(roadFile); if (!r) throw std::runtime_error("cart: cannot read " + roadFile);
        std::size_t n; r >> xmin >> h >> n; za.resize(n); for (std::size_t j = 0; j < n; j++) r >> za[j];
        if (!r) throw std::runtime_error("cart: road table short");
        reset(need(p, "x0"));
    }
    // Road.axle: [z_a, dz_a/dx], linear between table points, clamped to the table
    void axle(double xx, double& a, double& d) const {
        const double f = (xx - xmin) / h; long j = long(std::floor(f));
        if (j < 0) j = 0; if (j > long(za.size()) - 2) j = long(za.size()) - 2;
        const double tt = f - j, A = za[j], B = za[j + 1];
        a = A + tt * (B - A); d = (B - A) / h;
    }
    double bForce() const { return Ngear * Km / Rw; }
    double resist(double v, double NN) const {
        const double sg = v / std::sqrt(v * v + vSmooth * vSmooth);
        return cx * v + Crr * NN * sg + Tf / Rw * sg + bf * v / (Rw * Rw) + 0.5 * rhoAir * CdA * v * std::fabs(v);
    }
    double resistAtSetSpeed() const { return resist(v0, (Mb + ml + mw) * g); }
    double massX() const { return Mb + ml + mw + (Iw + Ngear * Ngear * Jm) / (Rw * Rw); }
    void reset(double x0) {
        const double Ms = Mb + ml; double a, d; axle(x0, a, d);
        x = x0; vx = v0;
        zw = a - (Ms + mw) * g / kt;
        zb = zw + Ls - Ms * g / k;
        vzb = 0; vzw = 0; t = 0; Flx = 0; Flz = 0;
        i = resistAtSetSpeed() / bForce();
        icmd = i; xi = 0; us = 0; uscmd = 0; tSample = 0;
        forces(0, 0);
    }
    void sample() {
        const double i0 = resistAtSetSpeed() / bForce(), e = v0 - vx;
        if (ctrl == 1 || ctrl == 2) {
            double ic = i0 + Kp * e + Ki * xi;
            if (ctrl == 2) { double a, d; axle(x + vx * tauI, a, d); ic += (Mb + ml + mw) * g * d / bForce(); }
            if (std::fabs(ic) < Imax) xi += e * Ts;
            icmd = ic;
        } else icmd = i0;
        uscmd = susp ? -csky * vzb : 0;
        if (uscmd > Umax) uscmd = Umax; else if (uscmd < -Umax) uscmd = -Umax;
    }
    void forces(double Fx, double Fz) {
        const double Ms = Mb + ml; double a, d; axle(x, a, d);
        const double vza = d * vx;
        double NN = kt * (a - zw) + ct * (vza - vzw); if (NN < 0) NN = 0;
        const double FS = -k * (zb - zw - Ls) - c * (vzb - vzw) + us;
        const double Mx = massX();
        const double Fm0 = bForce() * i, Fg = mu * NN, Fm = Fm0 > Fg ? Fg : Fm0 < -Fg ? -Fg : Fm0, Fr = -NN * d;
        slip = Fm != Fm0 ? 1 : 0; Fgrip = Fg;
        const double FR = resist(vx, NN); Fres = FR;
        const double AX = (Fr + Fm - FR + Fx) / Mx;
        const double AZB = (FS - Ms * g + Fz) / Ms;
        const double AZW = (-FS - mw * g + NN) / mw;
        const double E = Km * Ngear * vx / Rw;
        double il = icmd; if (il > Imax) il = Imax; else if (il < -Imax) il = -Imax;
        const double iHi = (Vmax - E) / Ra, iLo = (-Vmax - E) / Ra;
        if (il > iHi) il = iHi; else if (il < iLo) il = iLo;
        zaNow = a; dza = d; N = NN; Fs = FS; Froad = Fr; Fdrive = Fm;
        ax = AX; azb = AZB; azw = AZW; Flx = Fx; Flz = Fz; ireach = il; emf = E;
        Vm = Ra * i + E;
    }
    void step(double hh, double Fx, double Fz) {
        tSample += hh;
        if (tSample >= Ts - 1e-12) { tSample -= Ts; sample(); forces(Fx, Fz); }
        vx += hh * ax; vzb += hh * azb; vzw += hh * azw;
        x += hh * vx; zb += hh * vzb; zw += hh * vzw;
        const double ei = std::exp(-hh / tauI), eu = std::exp(-hh / tauU);
        i = ireach + (i - ireach) * ei;
        us = uscmd + (us - uscmd) * eu;
        t += hh;
        forces(Fx, Fz);
    }
};

} // namespace fig12
#endif
