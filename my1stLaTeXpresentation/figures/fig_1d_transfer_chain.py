"""
Generate figure: 1D chain with transfer matrices connecting sites
For CTMRG presentation - Part 1, Slide 1.1

Concept: σ₁ ──[T]── σ₂ ──[T]── σ₃ ──[T]── σ₄ ──[T]── ...
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(10, 3))
ax.set_aspect('equal')

# Define colors
spin_color = '#4A90E2'  # Blue for spins
transfer_color = '#E8F4F8'  # Light blue background for T boxes
transfer_edge_color = '#003366'  # Dark blue edge
text_color = '#333333'

# Positions
num_spins = 5  # Show 4 complete + indication of continuation
y_center = 0.5
x_start = 0.5
x_spacing = 1.8  # Space between consecutive spins

# Box size for transfer matrix T
box_width = 0.6
box_height = 0.5
spin_radius = 0.15

# Draw the chain
for i in range(num_spins):
    x_spin = x_start + i * x_spacing
    
    # Draw spin node (circle)
    if i < 4:  # Only draw first 4 spins clearly
        spin_circle = Circle((x_spin, y_center), spin_radius, 
                            color=spin_color, ec=transfer_edge_color, 
                            linewidth=2, zorder=3)
        ax.add_patch(spin_circle)
        
        # Label spin
        ax.text(x_spin, y_center, f'$\\sigma_{i+1}$', 
               ha='center', va='center', fontsize=14, 
               color='white', weight='bold', zorder=4)
    
    # Draw transfer matrix T between spins (except after last spin)
    if i < num_spins - 1:
        x_transfer = x_spin + x_spacing / 2
        
        if i < 3:  # Draw first 3 transfer matrices clearly
            # Connection line before T
            ax.plot([x_spin + spin_radius, x_transfer - box_width/2], 
                   [y_center, y_center], 
                   'k-', linewidth=2, zorder=1)
            
            # Transfer matrix box
            transfer_box = FancyBboxPatch(
                (x_transfer - box_width/2, y_center - box_height/2),
                box_width, box_height,
                boxstyle="round,pad=0.05", 
                facecolor=transfer_color,
                edgecolor=transfer_edge_color,
                linewidth=2.5,
                zorder=2
            )
            ax.add_patch(transfer_box)
            
            # Label T
            ax.text(x_transfer, y_center + 0.05, '$T$', 
                   ha='center', va='center', fontsize=16, 
                   weight='bold', color=transfer_edge_color, zorder=4)
            
            # Add "2×2" label below
            ax.text(x_transfer, y_center - 0.15, '$2\\times 2$', 
                   ha='center', va='center', fontsize=9, 
                   style='italic', color='#666666', zorder=4)
            
            # Connection line after T
            if i < num_spins - 2:
                ax.plot([x_transfer + box_width/2, x_spin + x_spacing - spin_radius], 
                       [y_center, y_center], 
                       'k-', linewidth=2, zorder=1)
        elif i == 3:
            # Draw dots for continuation
            x_dots = x_transfer
            for j, dx in enumerate([-0.2, 0, 0.2]):
                ax.plot(x_dots + dx, y_center, 'ko', markersize=8, zorder=3)

# Add annotation emphasizing 2×2
ax.annotate('Manageable!\nExact solution', 
            xy=(x_start + x_spacing/2, y_center), 
            xytext=(x_start + x_spacing/2, y_center - 0.9),
            ha='center', fontsize=11, color='#2E7D32',
            weight='bold',
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9', 
                     edgecolor='#2E7D32', linewidth=1.5))

# Add trace formula on top
ax.text(x_start + 1.5 * x_spacing, y_center + 0.85, 
       r'$Z = \mathrm{Tr}(T^N)$', 
       ha='center', va='center', fontsize=15, 
       bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF9E6', 
                edgecolor='#F57C00', linewidth=2))

# Set axis limits and remove axes
ax.set_xlim(-0.2, x_start + 4.5 * x_spacing)
ax.set_ylim(-0.5, 1.5)
ax.axis('off')

# Tight layout
plt.tight_layout()

# Save figure
output_path = 'figures/fig_1d_transfer_chain.pdf'
plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=300)
print(f"Figure saved to: {output_path}")

# Also save as PNG for preview
output_path_png = 'figures/fig_1d_transfer_chain.png'
plt.savefig(output_path_png, format='png', bbox_inches='tight', dpi=300)
print(f"Figure saved to: {output_path_png}")

plt.show()
