import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ============================================================
# Figure: Local site surrounded by 2D environment
# Slide 2.3: Environment encodes the rest of the infinite lattice
# ============================================================

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Center of figure
cx, cy = 7, 5

# ============================================================
# Draw the outer environment (large rounded rectangle)
# ============================================================
env_width = 10
env_height = 7
env_rect = patches.FancyBboxPatch(
    (cx - env_width/2, cy - env_height/2),
    env_width, env_height,
    boxstyle="round,pad=0.3",
    edgecolor='darkblue',
    facecolor='#E6F2FF',
    linewidth=4,
    zorder=1
)
ax.add_patch(env_rect)

# Environment label
ax.text(cx, cy + env_height/2 - 0.8, 'Environment',
       ha='center', va='center', fontsize=32, fontweight='bold',
       color='darkblue', zorder=2)

# ============================================================
# Draw the local site in the center (highlighted)
# ============================================================
local_size = 1.2
local_rect = patches.FancyBboxPatch(
    (cx - local_size/2, cy - local_size/2),
    local_size, local_size,
    boxstyle="round,pad=0.08",
    edgecolor='darkred',
    facecolor='#FFD700',
    linewidth=4,
    zorder=3
)
ax.add_patch(local_rect)

ax.text(cx, cy, r'$\sigma$', ha='center', va='center',
       fontsize=36, fontweight='bold', color='darkred', zorder=4)

# Label: "local"
ax.annotate('local site',
           xy=(cx + local_size/2 + 0.1, cy),
           xytext=(cx + 2.5, cy),
           ha='left', va='center', fontsize=24, color='darkred',
           fontweight='bold',
           arrowprops=dict(arrowstyle='->', color='darkred', lw=2.5),
           zorder=4)

# ============================================================
# Draw 4 bonds from local site to environment
# ============================================================
bond_length = 1.8
bond_width = 3

# Up
ax.plot([cx, cx], [cy + local_size/2, cy + bond_length],
       'k-', linewidth=bond_width, zorder=2)
# Down
ax.plot([cx, cx], [cy - local_size/2, cy - bond_length],
       'k-', linewidth=bond_width, zorder=2)
# Left
ax.plot([cx - local_size/2, cx - bond_length], [cy, cy],
       'k-', linewidth=bond_width, zorder=2)
# Right
ax.plot([cx + local_size/2, cx + bond_length], [cy, cy],
       'k-', linewidth=bond_width, zorder=2)

# Small dots at bond ends (representing connections to environment)
for dx, dy in [(0, bond_length), (0, -bond_length), 
               (-bond_length, 0), (bond_length, 0)]:
    dot = patches.Circle((cx + dx, cy + dy), 0.15,
                         edgecolor='black', facecolor='black',
                         linewidth=2, zorder=3)
    ax.add_patch(dot)

# ============================================================
# Add surrounding lattice structure (faded) to show context
# ============================================================
fade_alpha = 0.3
fade_radius = 0.1
fade_T_size = 0.5

# Draw a few faded sites and bonds around the environment border
# Top row
for i in range(-2, 3):
    x = cx + i * 1.5
    y = cy + 2.8
    if abs(i) <= 1:  # Skip center region
        continue
    circle = patches.Circle((x, y), fade_radius,
                           edgecolor='gray', facecolor='gray',
                           alpha=fade_alpha, zorder=1)
    ax.add_patch(circle)

# Bottom row
for i in range(-2, 3):
    x = cx + i * 1.5
    y = cy - 2.8
    if abs(i) <= 1:
        continue
    circle = patches.Circle((x, y), fade_radius,
                           edgecolor='gray', facecolor='gray',
                           alpha=fade_alpha, zorder=1)
    ax.add_patch(circle)

# ============================================================
# Key message
# ============================================================
ax.text(cx, cy - env_height/2 - 1.0,
       r'$\langle \sigma \rangle = \frac{\mathrm{Tr}(\text{Environment} \cdot \sigma)}{\mathrm{Tr}(\text{Environment})}$',
       ha='center', va='top', fontsize=28, fontweight='bold',
       color='black',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9',
                edgecolor='darkgreen', linewidth=2.5))

# Question at top
ax.text(cx, 9.3,
       r'Only need local $\langle\sigma\rangle$? $\Rightarrow$ Compress the environment!',
       ha='center', va='center', fontsize=26, fontweight='bold',
       color='#F57C00',
       bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF3E0',
                edgecolor='#F57C00', linewidth=2))

# ============================================================
# Save figure
# ============================================================
plt.tight_layout()
plt.savefig('figures/fig_2d_local_environment.pdf', format='pdf', bbox_inches='tight', dpi=300)
plt.savefig('figures/fig_2d_local_environment.png', format='png', bbox_inches='tight', dpi=150)
print("Saved: figures/fig_2d_local_environment.pdf")
print("Saved: figures/fig_2d_local_environment.png")
plt.close()
