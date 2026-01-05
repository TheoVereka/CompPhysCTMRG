import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ============================================================
# Figure: Plaquette tensor - 4 bonds around a face → W
# Slide 3.2: Bond-based T (rank-2) → Plaquette-based W (rank-4)
# ============================================================

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

# ============================================================
# LEFT SIDE: 4 bond tensors T around a plaquette (before)
# ============================================================
left_cx, left_cy = 3.5, 4

# 4 sites at corners of the plaquette (45° rotated = diamond shape)
site_radius = 0.12
diag = 1.8  # distance from center to site

site_positions = [
    (0, diag),    # top
    (diag, 0),    # right
    (0, -diag),   # bottom
    (-diag, 0)    # left
]

# Draw bonds between adjacent sites
bond_width = 3
for i in range(4):
    x1, y1 = site_positions[i]
    x2, y2 = site_positions[(i+1) % 4]
    ax.plot([left_cx + x1, left_cx + x2], [left_cy + y1, left_cy + y2],
           'k-', linewidth=bond_width, zorder=1)

# Draw T matrices on each bond (4 total)
T_size = 0.6
T_positions = [
    (diag/2, diag/2),    # top-right bond
    (diag/2, -diag/2),   # bottom-right bond
    (-diag/2, -diag/2),  # bottom-left bond
    (-diag/2, diag/2)    # top-left bond
]

for i, (tx, ty) in enumerate(T_positions):
    T_rect = patches.FancyBboxPatch(
        (left_cx + tx - T_size/2, left_cy + ty - T_size/2),
        T_size, T_size,
        boxstyle="round,pad=0.05",
        edgecolor='#B8860B',
        facecolor='#FFD700',
        linewidth=2.5,
        zorder=3
    )
    ax.add_patch(T_rect)
    ax.text(left_cx + tx, left_cy + ty, r'$T$',
           ha='center', va='center', fontsize=20, fontweight='bold',
           color='#8B4513', zorder=4)

# Draw sites
for dx, dy in site_positions:
    site = patches.Circle((left_cx + dx, left_cy + dy), site_radius,
                          edgecolor='black', facecolor='black',
                          linewidth=2, zorder=5)
    ax.add_patch(site)

# Central spin σ (the summed-over index)
ax.text(left_cx, left_cy, r'$\sigma$', ha='center', va='center',
       fontsize=28, fontweight='bold', color='darkred', zorder=4)

# Label: "Plaquette with 4 T's"
ax.text(left_cx, left_cy - 2.8, r'4 bond tensors $T$',
       ha='center', va='center', fontsize=22, fontweight='bold',
       color='#333333')
ax.text(left_cx, left_cy - 3.3, r'around central spin $\sigma$',
       ha='center', va='center', fontsize=18, color='#555555')

# External bond labels (u, d, l, r)
label_dist = 2.3
ax.text(left_cx, left_cy + label_dist, r'$u$', ha='center', va='center',
       fontsize=22, fontweight='bold', color='darkblue')
ax.text(left_cx + label_dist, left_cy, r'$r$', ha='center', va='center',
       fontsize=22, fontweight='bold', color='darkblue')
ax.text(left_cx, left_cy - label_dist, r'$d$', ha='center', va='center',
       fontsize=22, fontweight='bold', color='darkblue')
ax.text(left_cx - label_dist, left_cy, r'$l$', ha='center', va='center',
       fontsize=22, fontweight='bold', color='darkblue')

# ============================================================
# ARROW: Transformation
# ============================================================
arrow_x = 7
ax.annotate('', xy=(arrow_x + 1.2, 4), xytext=(arrow_x - 1.2, 4),
           arrowprops=dict(arrowstyle='->', color='darkgreen', lw=4))
ax.text(arrow_x, 4.6, r'$\sum_{\sigma}$', ha='center', va='center',
       fontsize=26, fontweight='bold', color='darkgreen')

# ============================================================
# RIGHT SIDE: Single plaquette tensor W (after)
# ============================================================
right_cx, right_cy = 10.5, 4

# Draw the W tensor as a larger square
W_size = 2.0
W_rect = patches.FancyBboxPatch(
    (right_cx - W_size/2, right_cy - W_size/2),
    W_size, W_size,
    boxstyle="round,pad=0.1",
    edgecolor='#B8860B',
    facecolor='#FFD700',
    linewidth=4,
    zorder=2
)
ax.add_patch(W_rect)

ax.text(right_cx, right_cy, r'$W$', ha='center', va='center',
       fontsize=36, fontweight='bold', color='#8B4513', zorder=3)

# 4 external legs of W
leg_length = 1.3
leg_width = 3.5

# Up
ax.plot([right_cx, right_cx], [right_cy + W_size/2, right_cy + W_size/2 + leg_length],
       'k-', linewidth=leg_width, zorder=1)
# Down
ax.plot([right_cx, right_cx], [right_cy - W_size/2, right_cy - W_size/2 - leg_length],
       'k-', linewidth=leg_width, zorder=1)
# Left
ax.plot([right_cx - W_size/2, right_cx - W_size/2 - leg_length], [right_cy, right_cy],
       'k-', linewidth=leg_width, zorder=1)
# Right
ax.plot([right_cx + W_size/2, right_cx + W_size/2 + leg_length], [right_cy, right_cy],
       'k-', linewidth=leg_width, zorder=1)

# External bond labels
label_dist = 2.5
ax.text(right_cx, right_cy + label_dist, r'$u$', ha='center', va='center',
       fontsize=22, fontweight='bold', color='darkblue')
ax.text(right_cx + label_dist, right_cy, r'$r$', ha='center', va='center',
       fontsize=22, fontweight='bold', color='darkblue')
ax.text(right_cx, right_cy - label_dist, r'$d$', ha='center', va='center',
       fontsize=22, fontweight='bold', color='darkblue')
ax.text(right_cx - label_dist, right_cy, r'$l$', ha='center', va='center',
       fontsize=22, fontweight='bold', color='darkblue')

# Label: "Plaquette tensor W"
ax.text(right_cx, right_cy - 2.8, r'Plaquette tensor $W$',
       ha='center', va='center', fontsize=22, fontweight='bold',
       color='#333333')
ax.text(right_cx, right_cy - 3.3, r'rank-4: $(u, d, l, r)$',
       ha='center', va='center', fontsize=18, color='#555555')

# ============================================================
# Top title
# ============================================================
ax.text(7, 7.5, r'$W_{u,d,l,r} = \sum_{\sigma} T_{\sigma,u} T_{\sigma,d} T_{\sigma,l} T_{\sigma,r}$',
       ha='center', va='center', fontsize=26, fontweight='bold',
       color='black',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9',
                edgecolor='darkgreen', linewidth=2.5))

# ============================================================
# Save figure
# ============================================================
plt.tight_layout()
plt.savefig('figures/fig_plaquette_tensor.pdf', format='pdf', bbox_inches='tight', dpi=300)
plt.savefig('figures/fig_plaquette_tensor.png', format='png', bbox_inches='tight', dpi=150)
print("Saved: figures/fig_plaquette_tensor.pdf")
print("Saved: figures/fig_plaquette_tensor.png")
plt.close()
