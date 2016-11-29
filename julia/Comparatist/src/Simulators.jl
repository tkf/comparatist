module Simulators

# FIXME: automate this:
module rnn
include("rnn/_helper.jl")
module loop
include("rnn/loop.jl")
end
module vec
include("rnn/vec.jl")
end
end


this_module = current_module()

function getnestedfield(value, path::AbstractString)
    getnestedfield(value, map(Symbol, split(path, "."))...)
end

function getnestedfield(value, name::Symbol, rest::Symbol...)
    getnestedfield(getfield(value, name), rest...)
end
getnestedfield(value) = value

function prepare(module_name, run_name)
    getnestedfield(this_module, module_name).prepare(Symbol(run_name))
end

end
