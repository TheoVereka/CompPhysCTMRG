from julia import Main as MainJulia
x = MainJulia.include("src_codes/core.jl")
print(x)