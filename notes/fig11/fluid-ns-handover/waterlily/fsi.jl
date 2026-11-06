# Project 05 in a real fluid: cart + two rods, fully coupled with 3D incompressible Navier–Stokes (WaterLily.jl 1.8.0).
# Units: SI for the machine. WaterLily runs with lengths in cells (h metres each) and velocities in m/s, so
#   t_phys = h * t_wl,  nu_wl = nu / h,  F = rho h^2 F_wl,  M = rho h^3 M_wl,  omega_wl = h * omega_phys.
# Coordinates: x along the rail, y up, z out of the screen. The hinge sits on top of the cart at y = 0; angles from the vertical,
# positive leaning towards +x (the page's convention): rod k points along (sin θk, cos θk, 0).
using WaterLily, StaticArrays, LinearAlgebra, Printf

const G = 9.81

Base.@kwdef struct Machine
    m0::Float64 = 1.5; m1::Float64 = 0.5; m2::Float64 = 0.75; L1::Float64 = 0.5; L2::Float64 = 0.75
    r::Float64 = 0.01                     # rod radius, m
    cw::Float64 = 0.36; ch::Float64 = 0.12; cb::Float64 = 0.20   # cart: width (x), height (y), depth (z), m
    umax::Float64 = 60.0; Ts::Float64 = 0.01
    K::Vector{Float64} = [5.885587698152317, -297.35065624888904, 376.94950633324845, 16.857296568025124, -11.85241735175428, 89.41084011288147]   # page, glycerol
    rho::Float64 = 1261.0; mu::Float64 = 1.412                       # glycerol (page, section 13.1)
    mua::Float64 = 0.39615483361767295; mca::Float64 = 0.9581725206415027   # page's added mass per m of rod, and of the cart: used ONLY to stabilise the coupling
end
dvec(M::Machine) = [M.m0 + M.m1 + M.m2, (M.m1/2 + M.m2)*M.L1, M.m2*M.L2/2, (M.m1/3 + M.m2)*M.L1^2, M.m2*M.L1*M.L2/2, M.m2*M.L2^2/3]
function fvec(M::Machine)   # gravity minus buoyancy of the rods (the fluid in the solver has no hydrostatic pressure)
    bA = M.rho*π*M.r^2*G
    [(M.m1/2 + M.m2)*M.L1*G - bA*(M.L1^2/2 + M.L1*M.L2), M.m2*M.L2*G/2 - bA*M.L2^2/2]
end
function Dmat(M::Machine, a, b)
    d = dvec(M); c1, c2, c12 = cos(a), cos(b), cos(a - b)
    [d[1] d[2]*c1 d[3]*c2; d[2]*c1 d[4] d[5]*c12; d[3]*c2 d[5]*c12 d[6]]
end
function Mstab(M::Machine, a, b)   # page eq. (38): added-mass matrix of thin rods (C_a = 1) and the cart's m_c — the stabiliser
    μ, L1, L2 = M.mua, M.L1, M.L2; ca, cb, cab = cos(a), cos(b), cos(a - b)
    [μ*(L1*ca^2 + L2*cb^2)+M.mca   μ*(L1^2*ca/2 + L1*L2*cb*cab)   μ*L2^2*cb/2;
     μ*(L1^2*ca/2 + L1*L2*cb*cab)  μ*(L1^3/3 + L1^2*L2*cab^2)     μ*L1*L2^2*cab/2;
     μ*L2^2*cb/2                   μ*L1*L2^2*cab/2                μ*L2^3/3]
end
# state s = [x, θ1, θ2, ẋ, θ̇1, θ̇2]; Q = generalized fluid force; aprev = last accelerations (for the stabiliser)
function accel(M::Machine, s, u, Q, aprev)
    a, b, ad, bd = s[2], s[3], s[5], s[6]; d = dvec(M); f = fvec(M); sab = sin(a - b)
    Cq = [-d[2]*sin(a)*ad^2 - d[3]*sin(b)*bd^2, d[5]*sab*bd^2, -d[5]*sab*ad^2]
    Gv = [0.0, -f[1]*sin(a), -f[2]*sin(b)]
    Ms = Mstab(M, a, b)
    (Dmat(M, a, b) + Ms) \ ([u, 0.0, 0.0] .- Cq .- Gv .+ Q .+ Ms*aprev)
end
function rk4(M::Machine, s, u, Q, aprev, h)
    f(z) = vcat(z[4:6], accel(M, z, u, Q, aprev))
    k1 = f(s); k2 = f(s .+ h/2 .* k1); k3 = f(s .+ h/2 .* k2); k4 = f(s .+ h .* k3)
    s .+ h/6 .* (k1 .+ 2k2 .+ 2k3 .+ k4), k1[4:6]
end
control(M::Machine, s, sref) = clamp(-dot(M.K, s .- sref), -M.umax, M.umax)

# ---------- geometry: signed distances in each body's own frame, in cells ----------
sdf_box(hx, hy, hz) = (ξ, t) -> begin
    q = abs.(ξ) .- SA[hx, hy, hz]
    √sum(abs2, max.(q, 0)) + min(maximum(q), 0)
end
sdf_capsule(L, r) = (ξ, t) -> √(ξ[1]^2 + (ξ[2] - clamp(ξ[2], 0, L))^2 + ξ[3]^2) - r   # along +y from 0 to L
rot(θ) = SA[0f0, 0f0, Float32(-θ)]      # rod direction (sinθ, cosθ) maps to body +y with an angle -θ about z (RigidMap's rotation)

struct Rig
    M::Machine; h::Float64; X0::SVector{3,Float64}   # X0: cell coordinates of the physical origin (x = 0 on the rail, y = 0 at the hinge, z = 0 mid-plane)
    cart; rod1; rod2
end
cells(R::Rig, p) = R.X0 .+ p ./ R.h
function Rig(M::Machine, h, X0)
    T = Float32
    cart = AutoBody(sdf_box(T(M.cw/2/h), T(M.ch/2/h), T(M.cb/2/h)), RigidMap(SVector{3,T}(X0 .+ [0, -M.ch/2/h, 0]), SA{T}[0, 0, 0]))
    rod1 = AutoBody(sdf_capsule(T(M.L1/h), T(M.r/h)), RigidMap(SVector{3,T}(X0), SA{T}[0, 0, 0]))
    rod2 = AutoBody(sdf_capsule(T(M.L2/h), T(M.r/h)), RigidMap(SVector{3,T}(X0 .+ [0, M.L1/h, 0]), SA{T}[0, 0, 0]))
    Rig(M, h, SVector{3,Float64}(X0), cart, rod1, rod2)
end
function posed(R::Rig, s)   # bodies at state s: positions in cells, velocities in m/s, angular velocities in rad per wl-time
    M, h, T = R.M, R.h, Float32
    x, a, b, xd, ad, bd = s
    hinge = R.X0 .+ [x/h, 0, 0]; elbow = hinge .+ [M.L1*sin(a)/h, M.L1*cos(a)/h, 0]
    ve = [xd + M.L1*cos(a)*ad, -M.L1*sin(a)*ad, 0]
    c = setmap(R.cart; x₀ = SVector{3,T}(hinge .+ [0, -M.ch/2/h, 0]), V = SA{T}[xd, 0, 0])
    r1 = setmap(R.rod1; x₀ = SVector{3,T}(hinge), θ = rot(a), V = SA{T}[xd, 0, 0], ω = SA{T}[0, 0, -ad*h])
    r2 = setmap(R.rod2; x₀ = SVector{3,T}(elbow), θ = rot(b), V = SVector{3,T}(ve), ω = SA{T}[0, 0, -bd*h])
    c, r1, r2, hinge, elbow
end
# generalized forces from the solved flow (virtual work), SI
function genforce(R::Rig, flow, s)
    M, h = R.M, R.h; c, r1, r2, hinge, elbow = posed(R, s); a = s[2]
    # WaterLily's metrics return the force of the body ON the fluid (checked: a sphere in a +x stream gives C_D < 0), so negate
    F(body) = -(WaterLily.pressure_force(flow, body) .+ WaterLily.viscous_force(flow, body)) .* (M.rho*h^2)
    Mz(body, p) = -((WaterLily.pressure_moment(p, flow, body) .+ WaterLily.viscous_moment(p, flow, body)) .* (M.rho*h^3))[3]
    Fc, F1, F2 = F(c), F(r1), F(r2)
    M1, M2 = Mz(r1, hinge), Mz(r2, elbow)
    Qx = Fc[1] + F1[1] + F2[1]
    Q1 = -M1 + F2[1]*M.L1*cos(a) - F2[2]*M.L1*sin(a)     # rotation φ = -θ about z, so δW = -Mz δθ; rod 2 rides on the elbow
    Q2 = -M2
    [Qx, Q1, Q2], (cart = Fc, rod1 = F1, rod2 = F2, M1 = M1, M2 = M2)
end

# ---------- the coupled run ----------
Base.@kwdef struct Scenario
    name::String = "balance_breeze"
    U::Float64 = 0.5                         # breeze along +x, m/s
    s0::Vector{Float64} = [0.0, 0.05, -0.03, 0, 0, 0]
    sref::Vector{Float64} = zeros(6)
    T::Float64 = 6.0                         # physical seconds
    h::Float64 = 0.005                       # cell size, m
    box::NTuple{3,Float64} = (3.2, 2.0, 0.8) # domain size, m (x, y, z)
    origin::NTuple{3,Float64} = (1.2, 0.5, 0.4)   # where the hinge's start point sits inside the box, m
    out_dt::Float64 = 0.02
    slice_every::Int = 2                     # keep every n-th cell in the saved mid-plane slices
    kick::Float64 = 0.0                      # an impulse on the cart at t = spinup + 0.5 s, N s
    spinup::Float64 = 1.0                    # the machine is held at s0 while the flow develops round it, s (logged with t < 0)
end
function run(M::Machine, S::Scenario; mem = Array, outdir = "out_" * S.name, verbose = true)
    T = Float32; h = S.h
    dims = round.(Int, S.box ./ h); dims = map(n -> 16*cld(n, 16), dims)     # multiples of 16 for the multigrid
    X0 = S.origin ./ h
    R = Rig(M, h, X0)
    c, r1, r2, _, _ = posed(R, S.s0)
    U = max(S.U, 0.05)                                                          # velocity scale (also used for the time step limit)
    sim = Simulation(dims, (T(S.U), 0f0, 0f0), T(M.L1/h); U = T(U), ν = T(M.mu/M.rho/h), body = c ∪ r1 ∪ r2, T, mem, exitBC = S.U > 0)
    mkpath(outdir)
    s = copy(S.s0); aprev = zeros(3); u = 0.0; tnext_u = 0.0; t = -S.spinup; tout = -S.spinup; nstep = 0; kicked = false
    log = open(joinpath(outdir, "timeseries.csv"), "w")
    println(log, "t,x,th1,th2,xd,th1d,th2d,u,Qx,Q1,Q2,Fcx,Fcy,F1x,F1y,F2x,F2y,dt")
    nx, ny = dims[1], dims[2]; kz = round(Int, X0[3]) + 1
    t0 = time()
    while t < S.T
        if !kicked && S.kick != 0 && t >= 0.5; s[4] += S.kick/dvec(M)[1]; kicked = true; end
        held = t < 0                                                            # spin-up: bodies held at s0, the flow develops
        c, r1, r2, _, _ = posed(R, s); sim.body = c ∪ r1 ∪ r2
        sim_step!(sim; remeasure = true)
        dt = sim.flow.Δt[end]*h                                                 # physical fluid step just taken
        Q, parts = genforce(R, sim.flow, s)
        # the machine over the same interval, in substeps of at most 1 ms, the controller sampled every Ts (zero-order hold, as on the page)
        tend = t + dt
        if held; t = tend; nstep += 1; (t >= tout) && (verbose && @printf("spin-up t=%6.3f s  Q=(%+7.2f, %+7.3f, %+7.3f)  dt=%.2e s  wall=%.0f s\n", t, Q..., dt, time() - t0); tout += S.out_dt); continue; end
        while t < tend - 1e-12
            if t >= tnext_u - 1e-12; u = control(M, s, S.sref); tnext_u += M.Ts; end
            hs = min(1e-3, tend - t, tnext_u - t)
            s, aprev = rk4(M, s, u, Q, aprev, hs); t += hs
        end
        nstep += 1
        if t >= tout
            @printf(log, "%.5f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.4f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.5f,%.3e\n", t, s..., u, Q..., parts.cart[1], parts.cart[2], parts.rod1[1], parts.rod1[2], parts.rod2[1], parts.rod2[2], dt)
            flush(log)
            # mid-plane slice z = 0: u, v and ω_z, every slice_every cells, Float16, column-major (x fastest)
            ua = Array(sim.flow.u[:, :, kz, 1:2])            # only the mid-plane leaves the GPU
            uu = ua[2:end-1, 2:end-1, :]
            w = zeros(Float32, nx, ny)
            for j in 2:ny-1, i in 2:nx-1
                w[i, j] = ((ua[i+1, j+1, 2] - ua[i, j+1, 2]) - (ua[i+1, j+1, 1] - ua[i+1, j, 1]))/h   # ∂v/∂x - ∂u/∂y, 1/s
            end
            k = S.slice_every
            open(joinpath(outdir, @sprintf("slice_%06d.f16", round(Int, (t + S.spinup)/S.out_dt))), "w") do io
                write(io, Float16.(uu[1:k:end, 1:k:end, 1])); write(io, Float16.(uu[1:k:end, 1:k:end, 2])); write(io, Float16.(w[1:k:end, 1:k:end]))
            end
            verbose && @printf("t=%6.3f s  x=%+.3f  θ1=%+.3f  θ2=%+.3f  u=%+6.1f N  Q=(%+7.2f, %+7.3f, %+7.3f)  dt=%.2e s  steps=%d  wall=%.0f s\n", t, s[1], s[2], s[3], u, Q..., dt, nstep, time() - t0)
            tout += S.out_dt
            (abs(s[2]) > 1.2 || abs(s[3]) > 1.2) && (println("rods fell; stopping"); break)
            any(isnan, s) && (println("NaN; stopping"); break)
        end
    end
    close(log)
    open(joinpath(outdir, "meta.txt"), "w") do io
        println(io, "dims=$(dims) h=$(h) origin=$(S.origin) box=$(S.box) slice_every=$(S.slice_every) out_dt=$(S.out_dt) U=$(S.U) rho=$(M.rho) mu=$(M.mu) kz=$(kz)")
        println(io, "slice layout: Float16 arrays of size $(length(1:S.slice_every:nx-2)) x $(length(1:S.slice_every:ny-2)): u, v (m/s), omega_z (1/s); x fastest")
        println(io, "wall_seconds=$(time() - t0) steps=$(nstep)")
    end
    sim, s
end
