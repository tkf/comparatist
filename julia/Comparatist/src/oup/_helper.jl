module Helper

params = Dict(
    :default =>
    Dict(:x0 => 0.0, :steps => 1000000, :dt => 0.1, :sigma => 1.0, :seed => 1),
)


function init(name)
    param = copy(params[name])
    x = zeros(Float64, param[:steps])
    x[:, 1] = param[:x0]
    param[:x] = x
    param
end

end
