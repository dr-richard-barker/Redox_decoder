import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Set publication style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

fig = plt.figure(figsize=(16, 12))
plt.subplots_adjust(hspace=0.4, wspace=0.3, left=0.06, right=0.96, top=0.93, bottom=0.08)

# Grid layout: 4 studies as 4 major rows / quadrants
# Each study displays: [What Type (Bar)], [When (Timeline Gauge)], [Where (Spatial Map Schematic)]

studies = [
    {
        'id': 'OSD-678',
        'title': 'OSD-678 (Root Flight vs Ground)',
        'tissue': 'Primary Root & Stele',
        'what': {'H2O2': 42, 'Superoxide (O2•-)': 38, 'Ozone': 8, 'High Light': 5, 'Singlet Oxygen': 7},
        'when': {'category': 'Immediate / Early (<1h - 2h)', 'hours': 1.2, 'desc': 'Acute oxidative burst (RBOHD/F, ZAT12, APX1)'},
        'where': {'Root Stele': 0.85, 'Root Cap / QC': 0.65, 'Epidermis': 0.45, 'Shoot': 0.15},
        'color': '#ef4444'
    },
    {
        'id': 'OSD-223',
        'title': 'OSD-223 (Rosette Leaf Spaceflight)',
        'tissue': 'Rosette Leaf Lamina',
        'what': {'High Light / Photo-ox': 48, 'Singlet Oxygen (1O2)': 26, 'H2O2': 16, 'Superoxide': 8, 'Ozone': 2},
        'when': {'category': 'Late / Chronic (>12h)', 'hours': 16.5, 'desc': 'Chloroplast stress & photo-inhibition (CAT2 down, HSFA2 up)'},
        'where': {'Palisade Mesophyll': 0.90, 'Spongy Mesophyll': 0.75, 'Guard Cells': 0.50, 'Root': 0.10},
        'color': '#f59e0b'
    },
    {
        'id': 'OSD-624',
        'title': 'OSD-624 (Root Hypoxia-ROS Cross-talk)',
        'tissue': 'Root Vasculature & Meristem',
        'what': {'Superoxide (O2•-)': 45, 'H2O2': 32, 'Menadione': 12, 'Singlet Oxygen': 6, 'High Light': 5},
        'when': {'category': 'Mid Response (4-8h)', 'hours': 6.0, 'desc': 'Mitochondrial retrograde signaling (AOX1A, ANAC017, KIN10)'},
        'where': {'Root Vascular Stele': 0.88, 'Endodermis': 0.70, 'Meristem': 0.62, 'Leaves': 0.20},
        'color': '#8b5cf6'
    },
    {
        'id': 'OSD-38',
        'title': 'OSD-38 (Whole Seedling Flight)',
        'tissue': 'Intact Seedling (Shoot + Root)',
        'what': {'H2O2': 35, 'Superoxide': 28, 'High Light': 20, 'Singlet Oxygen': 10, 'Ozone': 7},
        'when': {'category': 'Early to Mid (2-6h)', 'hours': 3.8, 'desc': 'Systemic whole-plant oxidative signaling & antioxidant defense'},
        'where': {'Cotyledon Mesophyll': 0.65, 'Hypocotyl': 0.55, 'Root Stele': 0.72, 'Root Cap': 0.58},
        'color': '#10b981'
    }
]

# We will create a 4x3 grid: 4 studies, each having (1) What Type, (2) When Timeline, (3) Where Anatomical Profile
axes_grid = fig.subplots(4, 3)

for row, st in enumerate(studies):
    # Column 1: WHAT TYPE
    ax_what = axes_grid[row, 0]
    keys = list(st['what'].keys())
    vals = list(st['what'].values())
    bar_colors = ['#ef4444', '#f97316', '#eab308', '#10b981', '#06b6d4', '#8b5cf6'][:len(keys)]
    bars = ax_what.barh(keys, vals, color=bar_colors, edgecolor='black', linewidth=0.5, alpha=0.85)
    ax_what.invert_yaxis()
    ax_what.set_xlim(0, 60)
    for b in bars:
        ax_what.text(b.get_width() + 1.5, b.get_y() + b.get_height()/2.0, f"{b.get_width()}%", va='center', fontsize=9, fontweight='bold')
    ax_what.set_title(f"{st['id']}: Predicted ROS Type", fontsize=11, fontweight='bold', loc='left')
    ax_what.set_xlabel('Probability (%)', fontsize=9)
    ax_what.grid(axis='x', linestyle='--', alpha=0.3)

    # Column 2: WHEN (Timing)
    ax_when = axes_grid[row, 1]
    ax_when.set_xlim(0, 24)
    ax_when.set_ylim(-0.5, 1.5)
    # Draw timeline bar
    time_points = [1, 4, 12, 24]
    time_labels = ['Immediate\n(<1h)', 'Early\n(1-4h)', 'Mid\n(4-12h)', 'Late\n(>12h)']
    ax_when.barh([0.3], [1], left=[0], height=0.3, color='#fecaca', edgecolor='none')
    ax_when.barh([0.3], [3], left=[1], height=0.3, color='#fed7aa', edgecolor='none')
    ax_when.barh([0.3], [8], left=[4], height=0.3, color='#fef08a', edgecolor='none')
    ax_when.barh([0.3], [12], left=[12], height=0.3, color='#bbf7d0', edgecolor='none')
    
    # Mark study estimated time
    ax_when.scatter([st['when']['hours']], [0.3], color=st['color'], s=160, zorder=5, edgecolor='black', linewidth=1.5)
    ax_when.axvline(st['when']['hours'], color=st['color'], linestyle=':', linewidth=1.5)
    
    ax_when.set_xticks([0.5, 2.5, 8, 18])
    ax_when.set_xticklabels(time_labels, fontsize=8)
    ax_when.set_yticks([])
    ax_when.set_title(f"{st['id']}: Predicted Timing: ~{st['when']['hours']}h", fontsize=11, fontweight='bold', loc='left')
    ax_when.text(12, 0.95, st['when']['category'], ha='center', fontsize=10, fontweight='bold', color=st['color'])
    ax_when.text(12, -0.35, st['when']['desc'], ha='center', fontsize=8, color='#475569', style='italic')

    # Column 3: WHERE (Spatial Localization)
    ax_where = axes_grid[row, 2]
    loc_keys = list(st['where'].keys())
    loc_vals = list(st['where'].values())
    w_bars = ax_where.bar(loc_keys, loc_vals, color='#3b82f6', edgecolor='black', linewidth=0.5, alpha=0.8)
    ax_where.set_ylim(0, 1.1)
    ax_where.set_ylabel('Intensity Index', fontsize=9)
    ax_where.set_xticklabels(loc_keys, rotation=20, ha='right', fontsize=8.5, fontweight='500')
    ax_where.set_title(f"{st['id']}: Spatial Localization ({st['tissue']})", fontsize=11, fontweight='bold', loc='left')
    for wb in w_bars:
        ax_where.text(wb.get_x() + wb.get_width()/2.0, wb.get_height() + 0.03, f"{wb.get_height():.2f}", ha='center', fontsize=8.5, fontweight='bold')
    ax_where.grid(axis='y', linestyle='--', alpha=0.3)

fig.suptitle('Figure 11: OSDR Spaceflight Case Studies Decoded by CVAE & ggPlantMap (What, When, & Where)', fontsize=15, fontweight='bold', y=0.98)

# Save figures
plt.savefig('figures/fig11_osdr_spaceflight_case_studies.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig11_osdr_spaceflight_case_studies.svg', format='svg', bbox_inches='tight')
print("Successfully generated Figure 11 Spaceflight Case Studies (PNG + SVG)!")
