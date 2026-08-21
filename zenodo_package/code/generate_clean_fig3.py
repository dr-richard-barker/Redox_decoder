import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load tables
df_tissue = pd.read_csv('Table_S7_cell_type_proportions_by_tissue.csv')
df_sf = pd.read_csv('Table_S9_spaceflight_vs_ground_proportions.csv')

# Simplify tissue categories
def simplify_tissue(name):
    name = str(name).lower()
    if 'root' in name and 'seedling' not in name and 'rosette' not in name:
        return 'Root'
    elif 'rosette' in name:
        return 'Rosette Leaf'
    elif 'seedling' in name:
        return 'Seedling'
    elif 'flower' in name:
        return 'Flower'
    elif 'seed' in name:
        return 'Seed'
    elif 'stem' in name:
        return 'Stem'
    elif 'cell_culture' in name:
        return 'Cell Culture'
    else:
        return 'Mixed/Other'

df_tissue['primary_tissue'] = df_tissue['tissue'].apply(simplify_tissue)

# Aggregate proportions by primary tissue
numeric_cols = [c for c in df_tissue.columns if c not in ['tissue', 'primary_tissue']]
df_grouped = df_tissue.groupby('primary_tissue')[numeric_cols].mean()

# Select prominent cell types for clarity
prominent_cell_types = ['Epidermis', 'Anther', 'Gynoecium', 'Male_meiocyte', 'Meristematic', 'Phloem', 'Guard_cells', 'Vascular']
other_cols = [c for c in numeric_cols if c not in prominent_cell_types]
df_grouped['Other'] = df_grouped[other_cols].sum(axis=1)
df_tissue['Other'] = df_tissue[other_cols].sum(axis=1)

plot_cell_types = prominent_cell_types + ['Other']
colors = ['#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f', '#edc949', '#af7aa1', '#ff9da7', '#9c755f']

# Setup Figure
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
plt.subplots_adjust(hspace=0.45, wspace=0.32, bottom=0.12, top=0.92, left=0.08, right=0.95)

# --- Panel A: Cell type proportions by primary tissue ---
ax_a = axes[0, 0]
bottom = np.zeros(len(df_grouped))
tissues = df_grouped.index.tolist()
x_indices = np.arange(len(tissues))

for i, ct in enumerate(plot_cell_types):
    vals = df_grouped[ct].values
    ax_a.bar(x_indices, vals, bottom=bottom, label=ct.replace('_', ' '), color=colors[i % len(colors)], width=0.65, edgecolor='white', linewidth=0.8)
    bottom += vals

ax_a.set_xticks(x_indices)
ax_a.set_xticklabels(tissues, rotation=25, ha='right', fontsize=11, fontweight='500')
ax_a.set_ylabel('Proportion', fontsize=12, fontweight='bold')
ax_a.set_title('A. Cell Type Proportions by Tissue', fontsize=13, fontweight='bold', pad=12, loc='left')
ax_a.set_ylim(0, 1.05)
ax_a.grid(axis='y', linestyle='--', alpha=0.3)
ax_a.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fontsize=9, title='Cell Types')

# --- Panel B: Epidermis Proportion by Primary Tissue ---
ax_b = axes[0, 1]
epidermis_vals = df_grouped['Epidermis'].values
bar_colors = ['#3b82f6' if t != 'Root' else '#10b981' for t in tissues]
bars = ax_b.bar(x_indices, epidermis_vals, color=bar_colors, width=0.6, edgecolor='black', linewidth=0.5)

for bar in bars:
    yval = bar.get_height()
    ax_b.text(bar.get_x() + bar.get_width()/2.0, yval + 0.015, f"{yval:.2f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

ax_b.set_xticks(x_indices)
ax_b.set_xticklabels(tissues, rotation=25, ha='right', fontsize=11, fontweight='500')
ax_b.set_ylabel('Epidermis Fraction', fontsize=12, fontweight='bold')
ax_b.set_title('B. Epidermis Proportion Across Tissues', fontsize=13, fontweight='bold', pad=12, loc='left')
ax_b.set_ylim(0, max(epidermis_vals) * 1.2)
ax_b.grid(axis='y', linestyle='--', alpha=0.3)

# --- Panel C: Spaceflight vs Ground Cell Proportions ---
ax_c = axes[1, 0]
sf_conds = ['Ground', 'Spaceflight']
x_sf = np.arange(len(sf_conds))
bottom_sf = np.zeros(len(sf_conds))

df_sf_sub = df_sf.set_index('condition')[plot_cell_types[:-1]]
df_sf_sub['Other'] = df_sf.set_index('condition')[[c for c in numeric_cols if c not in plot_cell_types[:-1]]].sum(axis=1)

for i, ct in enumerate(plot_cell_types):
    vals = df_sf_sub.loc[sf_conds, ct].values
    ax_c.bar(x_sf, vals, bottom=bottom_sf, label=ct.replace('_', ' '), color=colors[i % len(colors)], width=0.5, edgecolor='white', linewidth=0.8)
    bottom_sf += vals

ax_c.set_xticks(x_sf)
ax_c.set_xticklabels(sf_conds, fontsize=12, fontweight='bold')
ax_c.set_ylabel('Proportion', fontsize=12, fontweight='bold')
ax_c.set_title('C. Deconvolution: Spaceflight vs. Ground', fontsize=13, fontweight='bold', pad=12, loc='left')
ax_c.set_ylim(0, 1.05)
ax_c.grid(axis='y', linestyle='--', alpha=0.3)

# --- Panel D: Cell Type Variance / Distribution Across Corpus ---
ax_d = axes[1, 1]
means = [df_tissue[ct].mean() for ct in plot_cell_types]
stds = [df_tissue[ct].std() for ct in plot_cell_types]
y_pos = np.arange(len(plot_cell_types))

ax_d.barh(y_pos, means, xerr=stds, align='center', alpha=0.85, color='#6366f1', ecolor='black', capsize=4, edgecolor='black', linewidth=0.5)
ax_d.set_yticks(y_pos)
ax_d.set_yticklabels([ct.replace('_', ' ') for ct in plot_cell_types], fontsize=10, fontweight='500')
ax_d.invert_yaxis()
ax_d.set_xlabel('Mean Proportion (± SD)', fontsize=12, fontweight='bold')
ax_d.set_title('D. Overall Cell Type Abundance in Corpus', fontsize=13, fontweight='bold', pad=12, loc='left')
ax_d.grid(axis='x', linestyle='--', alpha=0.3)

# Save high-res PNG and SVG
plt.savefig('figures/fig3_deconvolution_validation.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig3_deconvolution_validation.svg', format='svg', bbox_inches='tight')
print("Successfully generated clean Figure 3 (PNG + SVG) with clear x-axis text!")
