using ..Helper: init


function simulate!(x, m)
    dim, steps = size(x)
    for t = 2:steps, j = 1:dim
        y = 0.0
        for i = 1:dim
            y += m[i, j] * x[i, t]
        end
        x[j, t] = tanh(y)
    end
end


function prepare(name)
    res = init(name)
    function run()
        simulate!(res[:x], res[:m])
        res
    end
end
