using ..Helper: init


function simulate!(x, dt, sigma, rng)
    sgm = sigma * sqrt(dt)
    steps, = size(x)
    for t = 2:steps
        x[t] = (1 - dt) * x[t-1] + sgm * randn(rng)
    end
end


function prepare(name)
    res = init(name)
    rng = MersenneTwister(res[:seed])
    function run()
        simulate!(res[:x], res[:dt], res[:sigma], rng)
        res
    end
end
