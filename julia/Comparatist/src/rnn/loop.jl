using ..Helper: init


function simulate!(x, m)
    dim, steps = size(x)
    for t = 2:steps, j = 1:dim
        y = 0.0
        @simd for i = 1:dim
            y += m[i, j] * x[i, t-1]
        end
        x[j, t] = tanh(y)
    end
end


function prepare(name; m=nothing)
    res = init(name)
    if m != nothing
        res[:m] = m
    end
    function run()
        simulate!(res[:x], res[:m])
        res
    end
end
