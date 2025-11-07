# Exact diagonalization — Step 1: enumerate zero-magnetization (half-filling) basis

# You can modify L here (realistically L ≤ 20 is fine for ED) and must be even.
L = 4

@assert iseven(L) "L must be even for the zero-magnetization (half-filling) sector"
@assert L ≤ 62 "Current bit encoding uses UInt64; please keep L ≤ 62 (recommended ≤ 20)"

"""
	enumerate_zero_magnetization_basis(L::Int) -> Vector{UInt64}

Enumerate all Fock basis states with exactly L/2 occupied sites (zero magnetization/half filling),
encoded as a bitmask in a UInt64 (least significant bit is site 1).

Returns a vector `states`, where `states[i]` is the binary encoding for the i-th basis state.
The number of states is D = binomial(L, L÷2).
"""
function enumerate_zero_magnetization_basis(L::Int)
	@assert iseven(L)
	k = L ÷ 2
	# Choose positions (1..L) of the k ones; build bitmasks.
	states = UInt64[]
	pos = Vector{Int}(undef, k)

	function gen(start::Int, depth::Int)
		if depth > k
			# Build mask from positions
			m::UInt64 = 0
			@inbounds for p in pos
				m |= UInt64(1) << (p - 1)  # site p maps to bit (p-1)
			end
			push!(states, m)
			return
		end
		# Ensure enough room left: p ∈ [start, L - (k - depth)]
		maxp = L - (k - depth)
		@inbounds for p in start:maxp
			pos[depth] = p
			gen(p + 1, depth + 1)
		end
	end

	gen(1, 1)
	return states
end

"""
	struct Basis
		L::Int
		states::Vector{UInt64}
	end

Holds the zero-magnetization basis for a given L. Access state by `state(b, i)`.
"""
struct Basis
	L::Int
	states::Vector{UInt64}
end

"""
	Basis(L::Int) -> Basis

Constructs the basis for the zero-magnetization sector at system size L.
"""
function Basis(L::Int)
	@assert iseven(L)
	@assert L ≤ 62
	Basis(L, enumerate_zero_magnetization_basis(L))
end


# Define the length function for Basis, which is just the length of states,
# and under half-filling this is D = (L, L/2)
Base.length(b::Basis) = length(b.states)


"""
	state(b::Basis, i::Integer) -> UInt64

Return the bit-encoded i-th basis vector (1-based index).
"""
state(b::Basis, i::Integer) = b.states[i]
# Yeah, julia has its very convenient way to define methods outside struct.
# e.g. this 'state' function is exactly a method of Basis struct.


"""
	decode_bits(m::UInt64, L::Int) -> Vector{Int} (but this vector of integer
    is not the vector in Hilber space, merely )

Decode a bitmask into a Vector{0,1} of length L (site 1 is index 1).
v[p] = 1 if site p is occupied, else 0. p-th site contribute 2^(p-1) to the bitmask.
"""
function decode_bits(m::UInt64, L::Int)
	v = Vector{Int}(undef, L)
	@inbounds for p in 1:L
		v[p] = Int((m >> (p - 1)) & 0x1)
	end
	return v
end

# Build basis and print a small summary for quick sanity check
b = Basis(L)
println("L = ", L, ", D = C(L, L/2) = ", length(b))

# Show the first few states in both integer and bitstring form
if false
    show_n = min(length(b), 6)
    for i in 1:show_n
        m = state(b, i)
        bits = decode_bits(m, L)
        # Display as a readable string, site L on the left (optional)
        print(rpad("i=$(i)", 6), "  mask=", m, "  ")
        println(join(reverse(bits), ""))
    end
end

# Example: retrieve the index-th state as requested by the instruction
# Usage: state(b, index)  where index = 1,...,D



# %%




using SparseArrays

"""
	build_hopping(b::Basis; periodic::Bool=true, t::Float64=0.5) -> SparseMatrixCSC{Float64}

Construct the hopping part of the many-body Hamiltonian in the zero-magnetization (half-filling)
sector spanned by `b`. Hard-core constraint is enforced by only allowing hops into empty sites.

Conventions:
- Sites are 1..L with periodic boundary connecting L ↔ 1 if `periodic=true`.
- Matrix is built so that column n corresponds to basis state `state(b, n)` and contains nonzero
  entries of value `t` for states reachable by a single nearest-neighbor hop.
"""
function build_hopping(b::Basis; periodic::Bool=true, t::Float64=0.5)
	L = b.L
	D = length(b)
	# Map state mask → basis index for O(1) lookup
	idx = Dict{UInt64,Int}()
	@inbounds for i in 1:D
		idx[b.states[i]] = i
	end

    # I and J are the row and column indices of nonzero entries,
    # V are the values of hopping
	I = Int[]; J = Int[]; V = Float64[]
	# Iterate columns (bra-ket convention: H[row, col])
	@inbounds for n in 1:D
		m = b.states[n]
		# Hops on bonds (i, i+1), i = 1..L-1, finished the job for open boundary
		for i in 1:(L-1)

			occ_i  = (m >> (i-1)) & 0x1
			occ_ip = (m >> i) & 0x1  # i+1
			if occ_i == 1 && occ_ip == 0
				# hop i → i+1
				m2 = (m & ~(UInt64(1) << (i-1))) | (UInt64(1) << i)
				push!(I, idx[m2]); push!(J, n); push!(V, t)
			elseif occ_i == 0 && occ_ip == 1
				# hop i+1 → i
				m2 = (m | (UInt64(1) << (i-1))) & ~(UInt64(1) << i)
				push!(I, idx[m2]); push!(J, n); push!(V, t)
			end

		end
		# Periodic bond (L, 1)
		if periodic && L > 1

			occ1 = (m >> 0) & 0x1
			occL = (m >> (L-1)) & 0x1
			if occL == 1 && occ1 == 0
				# hop L → 1
				m2 = (m & ~(UInt64(1) << (L-1))) | (UInt64(1) << 0)
				push!(I, idx[m2]); push!(J, n); push!(V, t)
			elseif occL == 0 && occ1 == 1
				# hop 1 → L
				m2 = (m | (UInt64(1) << (L-1))) & ~(UInt64(1) << 0)
				push!(I, idx[m2]); push!(J, n); push!(V, t)
			end

		end
	end

	return sparse(I, J, V, D, D)
end

# Build hopping matrix for current L (for later steps)
Hhop = build_hopping(b; periodic=true, t=0.5)
println("nnz(Hhop) = ", nnz(Hhop))

# Optional quick check for the example in the instruction with L=4 and state 0101
# (kept independent of current L so you don't need to modify the header)
if false
    let Ltest = 4
        b4 = Basis(Ltest)
        H4 = build_hopping(b4; periodic=true, t=0.5)
        println("nnz(H4) = ", nnz(H4))
        idx4 = Dict(s => i for (i, s) in enumerate(b4.states))
        mask0101 = UInt64(0b0101)
        if haskey(idx4, mask0101)
            n = idx4[mask0101]
            rows, vals = findnz(H4[:, n])
            println("Check (L=4): nonzeros in column for state 0101 → should be 1001,0011,0110,1100 with 1/2")
            for (r, v) in zip(rows, vals)
                m = b4.states[r]
                bits = decode_bits(m, Ltest)
                println(join(reverse(bits), ""), "  ->  ", v)
            end
        end
		println("H4 (dense) =")
		println(Matrix(H4))
    end
end


# %%



# Nearest-neighbor density interaction: sum_i Delta*(n_i - 1/2)*(n_{i+1} - 1/2)
"""
	build_nn_density_interaction(b::Basis; periodic::Bool=true, Delta::Float64=1.0)
		-> SparseMatrixCSC{Float64}

Return a diagonal sparse matrix representing Σ_i Delta*(n_i - 1/2)*(n_{i+1} - 1/2)
in the occupation basis spanned by `b`. `n_i ∈ {0,1}` for hard-core bosons. If
`periodic=true`, includes the bond (L,1).
"""
function build_nn_density_interaction(b::Basis; periodic::Bool=true, Delta::Float64=1.0)
	L = b.L
	D = length(b)
	diagvals = Vector{Float64}(undef, D)
	@inbounds for i in 1:D
		m = b.states[i]
		acc = 0.0 # to-be-summed interaction value
		# Open-chain bonds (p, p+1)
		@inbounds for p in 1:(L-1)
			ni = Float64((m >> (p-1)) & 0x1)
			nj = Float64((m >> p) & 0x1)
			acc += (ni - 0.5) * (nj - 0.5)
		end
		# Periodic bond (L,1)
		if periodic && L > 1
			ni = Float64((m >> (L-1)) & 0x1)
			nj = Float64((m >> 0) & 0x1)
			acc += (ni - 0.5) * (nj - 0.5)
		end
		diagvals[i] = Delta * acc
	end
	return spdiagm(0 => diagvals)
end

# Example composition of total Hamiltonian pieces (hopping + onsite + interaction)
Delta_val = 2.3
Honsite = build_nn_density_interaction(b; periodic=true, Delta=Delta_val)
Htot = Hhop + Honsite
println("nnz(Honsite) = ", nnz(Honsite), ", nnz(Htot) = ", nnz(Htot))
Matrix(Htot)

# %%


gaps = Float64[]
using Arpack                # load iterative eigensolver
using Plots


function occupation_centered(b::Basis)
	D = length(b); L = b.L
	M = Matrix{Float64}(undef, D, L)
	@inbounds for k in 1:D
		m = b.states[k]
		for p in 1:L
			M[k, p] = ((m >> (p-1)) & 0x1) == 1 ? 0.5 : -0.5
		end
	end
	return M
end


function dot_weighted_triplet(w::AbstractVector{<:Real}, x::AbstractVector{<:Real}, y::AbstractVector{<:Real})
	@assert length(w) == length(x) == length(y)
	s = 0.0
	@inbounds @simd for k in eachindex(w)
		s += w[k] * x[k] * y[k]
	end
	return s
end

# Plot correlations for multiple sizes on the same figure
sizes = 4:2:20
p_corr = plot(title="Ground State Density-Density Correlation",
			  xlabel="Distance",
			  ylabel="Correlation <(n_i-1/2)(n_{i+dist}-1/2)>", legend=:topright)

for Lsz in sizes
	b = Basis(Lsz)
	Hhop = build_hopping(b; periodic=true, t=0.5)
	Delta_val = 2.3
	Honsite = build_nn_density_interaction(b; periodic=true, Delta=Delta_val)
	Htot = Hhop + Honsite
	println("L = ", Lsz, ", D = ", length(b), ", nnz(Htot) = ", nnz(Htot))
	E0E1, psi0psi1 = eigs(Htot; nev=2, which=:SR)  # lowest two eigenpairs
	E1minusE0 = E0E1[2] - E0E1[1]
	push!(gaps, E1minusE0)
	psi0 = psi0psi1[:, 1]
	w = abs2.(psi0)                  # probabilities over basis states (length D)
	M = occupation_centered(b)       # D×Lsz matrix of centered occupations

	corrs = zeros(Float64, Lsz)
	@views for dist in 0:(Lsz-1)
		acc = 0.0
		@inbounds for i in 1:Lsz
			j = i + dist; if j > Lsz; j -= Lsz; end
			acc += dot_weighted_triplet(w, M[:, i], M[:, j])
		end
		corrs[dist + 1] = acc / Lsz
	end
	plot!(p_corr, 0:(Lsz-1), corrs; marker=:circle, label="L=$(Lsz)")
end
display(p_corr)

# Plot energy gap vs size correctly (x = sizes)
p_gap = plot(sizes, gaps; marker=:circle, xlabel="L", ylabel="Energy gap",
			 title="Energy Gap vs Size", legend=false)
display(p_gap)





# %%

# plot the energy gap as a function of Delta
Deltas = -4.0:0.1:4.0
gaps = Float64[]
for Delta_val in Deltas
    Honsite = build_nn_density_interaction(b; periodic=true, Delta=Delta_val)
    Htot = Hhop + Honsite
    E0E1, _ = eigs(Htot; nev=2, which=:SR)
    push!(gaps, E0E1[2] - E0E1[1])
end
plot(Deltas, gaps, marker=:circle, xlabel="Delta", ylabel="Energy Gap",
    title="Energy Gap vs Nearest-Neighbor Interaction Delta", legend=false)


# %%

sizes = 4:2:20
p_corr = plot(title="Ground State Density-Density Correlation",
			  xlabel="Distance",
			  ylabel="Correlation <(n_i-1/2)(n_{i+dist}-1/2)>", legend=:topright)

for Lsz in sizes
	b = Basis(Lsz)
	Hhop = build_hopping(b; periodic=true, t=0.5)
	Delta_val = 2.3
	Honsite = build_nn_density_interaction(b; periodic=true, Delta=Delta_val)
	Htot = Hhop + Honsite
	println("L = ", Lsz, ", D = ", length(b), ", nnz(Htot) = ", nnz(Htot))
	E0E1, psi0psi1 = eigs(Htot; nev=2, which=:SR)  # lowest two eigenpairs
	E1minusE0 = E0E1[2] - E0E1[1]
	push!(gaps, E1minusE0)
	psi0 = psi0psi1[:, 1]
	w = abs2.(psi0)                  # probabilities over basis states (length D)
	M = occupation_centered(b)       # D×Lsz matrix of centered occupations

	corrs = zeros(Float64, Lsz)
	@views for i in 1:(Lsz-1)
		corrs[i] = dot_weighted_triplet(w, M[:, i], M[:, i+1])
    corrs[Lsz] = dot_weighted_triplet(w, M[:, Lsz], M[:, 1])
	end
	plot!(p_corr, 0:(Lsz-1), corrs; marker=:circle, label="L=$(Lsz)")
end
display(p_corr)