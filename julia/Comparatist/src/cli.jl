module CLI

using JSON

using ..Simulators


function run_funcs(module_names, run_names, repeat)
    benchmark = []
    for i = 1:repeat, m = module_names, r = run_names
        run = Simulators.prepare(m, r)
        _, elapsed, bytes, gctime, gcdiff = @timed run()
        push!(benchmark, Dict(
            :try => i - 1,
            :module => m,
            :run => r,
            :elapsed => elapsed,
            :bytes => bytes,
            :gctime => gctime,
            :gcdiff => gcdiff,
        ))
    end
    benchmark
end


function cli_run(module_names, run_names, repeat)
    benchmark = run_funcs(module_names, run_names, repeat)
    JSON.print(Dict(:benchmark => benchmark, :lang => "julia"))
    println()
end


function main(args=ARGS)
    if args[1] == "run"
        repeat = 5
        cli_run(split(args[2], ','),
                split(args[3], ','),
                repeat)
    end
end


end
