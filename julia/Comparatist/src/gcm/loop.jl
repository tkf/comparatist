using ..Helper: init


function simulate!(x, r, epsilon)
    dim, steps = size(x)
    for t = 2:steps

        # common = epsilon * mean(x[:, t-1])
        common = 0.0
        @simd for i = 1:dim
            common += x[i, t-1]
        end
        common *= epsilon / dim

        for i = 1:dim
            y = (1 - epsilon) * x[i, t-1] + common
            x[i, t] = r * y * (1 - y)
        end
    end
end


function prepare(name)
    res = init(name)
    function run()
        simulate!(res[:x], res[:r], res[:epsilon])
        res
    end
end
