using ..Helper: init


function simulate!(x, r, epsilon)
    dim, steps = size(x)
    for t = 2:steps
        y = (1 - epsilon) * x[:, t-1] + epsilon * mean(x[:, t-1])
        x[:, t] .= r .* y .* (1 .- y)
    end
end


function prepare(name)
    res = init(name)
    function run()
        simulate!(res[:x], res[:r], res[:epsilon])
        res
    end
end
