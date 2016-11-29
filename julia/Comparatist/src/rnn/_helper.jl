module Helper

params = Dict(
    :default =>
    Dict(:x0 => 0.1, :dim => 1000, :steps => 100, :gain => 5.0, :seed => 1),
)


function init(name)
    param = params[name]
    rng = MersenneTwister(param[:seed])
    N = param[:dim]
    m = randn(rng, N, N) / sqrt(N) * param[:gain]
    x = zeros(Float64, (param[:dim], param[:steps]))
    x[:, 1] = param[:x0]
    y = zeros(x[:, 1])
    Dict(:x=>x, :y=>y, :m=>m)
end

end
