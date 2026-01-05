import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ============================================================
# Figure: 2D Tensor Network - rank-4 tensors on a lattice
# Slide 2.1: Each site has 4 neighbors, forming a network
# ============================================================

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(-0.5, 11)
ax.set_ylim(-0.5, 8)
ax.axis('off')

# Layout parameters
site_radius = 0.12  # Small dots
T_size = 0.8        # Transfer matrix size
x_spacing = 2.5
y_spacing = 2.5

# Colors
site_color = 'black'
T_color = '#FFD700'  # Gold
line_color = 'black'

# Grid dimensions: 4 columns x 3 rows of sites
n_cols = 4
n_rows = 3

# Starting positions
x_start = 1.5
y_start = 1.5

# ============================================================
# Draw the 2D network
# ============================================================

# First, draw all horizontal bonds (with T tensors between columns 1-2, 2-3)
for row in range(n_rows):
    y = y_start + row * y_spacing
    for col in range(n_cols - 1):
        x1 = x_start + col * x_spacing
        x2 = x_start + (col + 1) * x_spacing
        
        # Draw horizontal line
        ax.plot([x1 + site_radius, x2 - site_radius], [y, y], 
               'k-', linewidth=2.5, zorder=1)
        
        # Add T tensor in the middle (only for cols 0-1 and 1-2, i.e., 2 T's per row)
        if col < 2:
            T_x = (x1 + x2) / 2
            T_rect = patches.FancyBboxPatch(
                (T_x - T_size/2, y - T_size/2),
                T_size, T_size,
                boxstyle="round,pad=0.05",
                edgecolor='black',
                facecolor=T_color,
                linewidth=2.5,
                zorder=2
            )
            ax.add_patch(T_rect)
            ax.text(T_x, y, r'$T$', ha='center', va='center',
                   fontsize=28, fontweight='bold', color='black', zorder=3)

# Draw vertical bonds (with T tensors between rows 0-1, 1-2)
for col in range(n_cols):
    x = x_start + col * x_spacing
    for row in range(n_rows - 1):
        y1 = y_start + row * y_spacing
        y2 = y_start + (row + 1) * y_spacing
        
        # Draw vertical line
        ax.plot([x, x], [y1 + site_radius, y2 - site_radius],
               'k-', linewidth=2.5, zorder=1)
        
        # Add T tensor in the middle (only for first 3 columns, rows 0-1)
        if col < 3 and row == 0:
            T_y = (y1 + y2) / 2
            T_rect = patches.FancyBboxPatch(
                (x - T_size/2, T_y - T_size/2),
                T_size, T_size,
                boxstyle="round,pad=0.05",
                edgecolor='black',
                facecolor=T_color,
                linewidth=2.5,
                zorder=2
            )
            ax.add_patch(T_rect)
            ax.text(x, T_y, r'$T$', ha='center', va='center',
                   fontsize=28, fontweight='bold', color='black', zorder=3)

# Draw all sites (small dots) on top
for row in range(n_rows):
    y = y_start + row * y_spacing
    for col in range(n_cols):
        x = x_start + col * x_spacing
        circle = patches.Circle((x, y), site_radius,
                               edgecolor='black', facecolor=site_color,
                               linewidth=2, zorder=4)
        ax.add_patch(circle)

# ============================================================
# Add annotations
# ============================================================

# Highlight one T tensor to show it's rank-4
highlight_x = x_start + 0.5 * x_spacing
highlight_y = y_start + 0 * y_spacing

# Draw 4 legs annotation
ax.annotate('', xy=(highlight_x - T_size/2 - 0.3, highlight_y),
           xytext=(highlight_x - T_size/2 - 0.8, highlight_y),
           arrowprops=dict(arrowstyle='->', color='darkred', lw=2.5))
ax.annotate('', xy=(highlight_x + T_size/2 + 0.3, highlight_y),
           xytext=(highlight_x + T_size/2 + 0.8, highlight_y),
           arrowprops=dict(arrowstyle='->', color='darkred', lw=2.5))
ax.annotate('', xy=(highlight_x, highlight_y - T_size/2 - 0.3),
           xytext=(highlight_x, highlight_y - T_size/2 - 0.8),
           arrowprops=dict(arrowstyle='->', color='darkred', lw=2.5))
ax.annotate('', xy=(highlight_x, highlight_y + T_size/2 + 0.3),
           xytext=(highlight_x, highlight_y + T_size/2 + 0.8),
           arrowprops=dict(arrowstyle='->', color='darkred', lw=2.5))

# Label: rank-4 tensor
ax.text(highlight_x, highlight_y - 1.8, r'Rank-4 tensor',
       ha='center', va='top', fontsize=24, color='darkred', fontweight='bold')

# Main message at top
ax.text(5.5, 7.2, r'2D: Each $T$ has 4 legs $\Rightarrow$ No simple contraction order!',
       ha='center', va='center', fontsize=26, fontweight='bold',
       color='darkred',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFE4E1', 
                edgecolor='darkred', linewidth=2.5))

# Ellipsis to indicate continuation
ax.text(x_start + 3.5 * x_spacing + 0.5, y_start + 1 * y_spacing, '...',
       ha='left', va='center', fontsize=36, fontweight='bold', color='black')
ax.text(x_start + 1.5 * x_spacing, y_start + 2.5 * y_spacing + 0.3, '...',
       ha='center', va='bottom', fontsize=36, fontweight='bold', color='black')

# ============================================================
# Save figure
# ============================================================
plt.tight_layout()
plt.savefig('figures/fig_2d_tensor_network.pdf', format='pdf', bbox_inches='tight', dpi=300)
plt.savefig('figures/fig_2d_tensor_network.png', format='png', bbox_inches='tight', dpi=150)
print("Saved: figures/fig_2d_tensor_network.pdf")
print("Saved: figures/fig_2d_tensor_network.png")
plt.close()
