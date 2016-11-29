using ..Helper: init


function simulate!(x, m, y)
    dim, steps = size(x)
    for t = 2:steps
        A_mul_B!(y, m, view(x, :, t-1))

        # x[:, t] .= tanh.(y)
        for i = 1:dim
            x[i, t] = tanh(y[i])
        end
    end
end


function prepare(name)
    res = init(name)
    function run()
        simulate!(res[:x], res[:m], res[:y])
        res
    end
end
