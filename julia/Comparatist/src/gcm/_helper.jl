module Helper

params = Dict(
    :default =>
    Dict(:x0 => 0.1, :dim => 1000, :steps => 10000, :r => 4.0, :epsilon => 0.1),
)


function init(name)
    param = copy(params[name])
    x = zeros(Float64, (param[:dim], param[:steps]))
    x[:, 1] = param[:x0]
    param[:x] = x
    param
end

end
