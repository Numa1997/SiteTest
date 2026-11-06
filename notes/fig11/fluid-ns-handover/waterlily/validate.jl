# Validation of WaterLily for this project, before any pendulum run.
#  V1  2D cylinder oscillating in fluid at rest vs the exact unsteady-Stokes force F = -ρπa²[1 + 4K₁(ka)/(ka K₀(ka))] dU/dt (derived in Wolfram)
#  V2  3D sphere at Re = 100 in a uniform stream: drag coefficient, grid-converged, vs the measured value (~1.09)
#  V3  speed: nanoseconds per cell per step, to size the production grid
using WaterLily, StaticArrays, SpecialFunctions, Printf

function V1(R; per = 3, mem = Array, T = Float32)
    a = R; ω = 2π/200; ka_abs = 4.0; ν = ω/(ka_abs/a)^2; X = 1.0     # |ka| = 4, amplitude 1 cell (KC = 2πX/2a small)
    n = 16R; c = SA{T}[n/2, n/2]
    body = AutoBody((ξ, t) -> √sum(abs2, ξ) - T(a), RigidMap(c, zero(T)))
    sim = Simulation((n, n), (0f0, 0f0), T(2a); U = T(X*ω), ν = T(ν), body, T, mem)
    ts = Float64[]; Fs = Float64[]
    while WaterLily.time(sim.flow) < per*2π/ω
        t = WaterLily.time(sim.flow)
        sim.body = setmap(sim.body; x₀ = c .+ SA{T}[X*sin(ω*t), 0], V = SA{T}[X*ω*cos(ω*t), 0])
        sim_step!(sim; remeasure = true)
        F = -(WaterLily.pressure_force(sim.flow, sim.body) .+ WaterLily.viscous_force(sim.flow, sim.body))   # force ON the body
        push!(ts, WaterLily.time(sim.flow)); push!(Fs, F[1])
    end
    # least-squares fit F = A cos ωt + B sin ωt over the last two periods
    sel = ts .> (per - 2)*2π/ω; C = cos.(ω .* ts[sel]); S = sin.(ω .* ts[sel])
    A = [C S] \ Fs[sel]
    k = √(-im*ω/ν); real(k) < 0 && (k = -k)
    Cm = 1 + 4besselk(1, k*a)/(k*a*besselk(0, k*a))
    Fh = im*ω^2*X*π*a^2*Cm                       # F(t) = Re[Fh e^{-iωt}] = Re(Fh) cos + Im(Fh) sin   (ρ = 1, per unit depth)
    @printf("V1  R=%3d  cos: %+.5e (exact %+.5e, %+.1f%%)   sin: %+.5e (exact %+.5e, %+.1f%%)   steps=%d\n",
            R, A[1], real(Fh), 100(A[1]/real(Fh) - 1), A[2], imag(Fh), 100(A[2]/imag(Fh) - 1), length(ts))
    (A, Fh)
end

function V2(D; Re = 100, mem = Array, T = Float32, tend = 30)
    n = (12D, 8D, 8D); c = SA{T}[3D, 4D, 4D]
    body = AutoBody((ξ, t) -> √sum(abs2, ξ .- c) - T(D/2))
    sim = Simulation(n, (1f0, 0f0, 0f0), T(D); ν = T(D/Re), body, T, mem, exitBC = true)
    sim_step!(sim)                                  # compile
    t0 = time(); n0 = length(sim.flow.Δt)
    hist = Float64[]
    while sim_time(sim) < tend
        sim_step!(sim; remeasure = false)
        sim_time(sim) > tend - 5 && push!(hist, -(WaterLily.pressure_force(sim)[1] + WaterLily.viscous_force(sim)[1])/(0.5*π*(D/2)^2))
    end
    wall = time() - t0; steps = length(sim.flow.Δt) - n0
    ns = 1e9*wall/(steps*prod(n))
    @printf("V2  D=%3d  cells=%.2e  C_D = %.4f (mean of last 5 D/U)   steps=%d  wall=%.0f s  %.2f ns per cell-step\n", D, prod(n), sum(hist)/length(hist), steps, wall, ns)
    sum(hist)/length(hist), ns
end
