import matplotlib.pyplot as plt
import numpy as np

def generate_figure_11():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
        'font.size': 10,
        'axes.linewidth': 1.2,
        'axes.edgecolor': '#1e293b'
    })

    fig, axes = plt.subplots(5, 3, figsize=(14, 16), gridspec_kw={'width_ratios': [1.2, 1.2, 1.4]})
    fig.patch.set_facecolor('#ffffff')

    case_studies = [
        {
            "id": "OSD-678",
            "title": "A. OSD-678 (Primary Root Flight)",
            "tissue": "Primary Root & Vascular Stele",
            "what": {"H2O2": 42, "Superoxide (O2•-)": 38, "Ozone": 8, "1O2": 7, "High Light": 5},
            "when_hours": 1.2,
            "when_label": "Immediate / Early (<1.2h)",
            "where": {"Stele": 0.88, "Root Cap": 0.65, "Epidermis": 0.55, "Mesophyll": 0.20},
            "color": "#ef4444"
        },
        {
            "id": "OSD-223",
            "title": "B. OSD-223 (Rosette Leaf Microgravity)",
            "tissue": "Rosette Leaf Lamina & Mesophyll",
            "what": {"High Light": 48, "1O2": 26, "H2O2": 16, "Superoxide": 8, "Ozone": 2},
            "when_hours": 16.5,
            "when_label": "Late / Chronic (>16h)",
            "where": {"Mesophyll": 0.92, "Guard Cells": 0.60, "Cuticle": 0.45, "Stele": 0.15},
            "color": "#10b981"
        },
        {
            "id": "OSD-624",
            "title": "C. OSD-624 (Root Hypoxia-ROS Cross-talk)",
            "tissue": "Root Vasculature & Endodermis",
            "what": {"Superoxide (O2•-)": 45, "H2O2": 32, "Menadione": 12, "1O2": 6, "High Light": 5},
            "when_hours": 6.0,
            "when_label": "Mid Response (~6.0h)",
            "where": {"Stele": 0.85, "Endodermis": 0.78, "Cortex": 0.70, "Mesophyll": 0.25},
            "color": "#f59e0b"
        },
        {
            "id": "OSD-37",
            "title": "D. OSD-37 (Four Ecotypes Spaceflight Acclimation)",
            "tissue": "Whole Seedling (Col-0, Ler-0, Ws-2, Cvi-0)",
            "what": {"H2O2": 39, "Superoxide (O2•-)": 31, "High Light": 15, "1O2": 9, "Ozone": 6},
            "when_hours": 4.5,
            "when_label": "Early-Mid (~4.5h)",
            "where": {"Stele": 0.76, "Root Meristem": 0.72, "Mesophyll": 0.58, "Epidermis": 0.48},
            "color": "#8b5cf6"
        },
        {
            "id": "OSD-38",
            "title": "E. OSD-38 (Intact Seedling Spaceflight)",
            "tissue": "Whole Intact Seedling (Shoot + Root)",
            "what": {"H2O2": 35, "Superoxide (O2•-)": 28, "High Light": 20, "1O2": 10, "Ozone": 7},
            "when_hours": 3.8,
            "when_label": "Early-Mid (~3.8h)",
            "where": {"Stele": 0.72, "Mesophyll": 0.68, "Root Cap": 0.58, "Epidermis": 0.50},
            "color": "#06b6d4"
        }
    ]

    for row_idx, cs in enumerate(case_studies):
        # Column 1: WHAT (ROS Stimulus Decoded Probabilities)
        ax_what = axes[row_idx, 0]
        categories = list(cs["what"].keys())
        values = list(cs["what"].values())
        y_pos = np.arange(len(categories))
        
        colors = ['#ef4444' if 'H2O2' in c else '#f97316' if 'Superoxide' in c else '#eab308' if 'High Light' in c else '#8b5cf6' if '1O2' in c else '#10b981' for c in categories]
        
        bars = ax_what.barh(y_pos, values, color=colors, edgecolor='#1e293b', height=0.65, alpha=0.88)
        ax_what.set_yticks(y_pos)
        ax_what.set_yticklabels(categories, fontsize=8.5, fontweight='bold')
        ax_what.invert_yaxis()
        ax_what.set_xlim(0, 60)
        ax_what.set_xlabel("Predicted Probability (%)", fontsize=8.5)
        ax_what.set_title(f"{cs['title']}\nWhat: Decoded ROS Stimulus", fontsize=9.5, fontweight='bold', loc='left', color='#1e293b')
        ax_what.grid(axis='x', linestyle='--', alpha=0.3)
        for bar in bars:
            w = bar.get_width()
            ax_what.text(w + 1.5, bar.get_y() + bar.get_height()/2, f"{int(w)}%", va='center', ha='left', fontsize=8, fontweight='bold', color='#334155')

        # Column 2: WHEN (Kinetics & Elapsed Duration Gauge)
        ax_when = axes[row_idx, 1]
        time_points = [0.5, 1.2, 4.0, 8.0, 16.0, 24.0]
        time_labels = ['0.5h', '1.2h', '4h', '8h', '16h', '24h']
        ax_when.plot(time_points, [0.2, 0.9, 0.7, 0.4, 0.2, 0.1] if row_idx == 0 else [0.1, 0.3, 0.5, 0.7, 0.95, 0.8] if row_idx == 1 else [0.2, 0.5, 0.85, 0.7, 0.3, 0.1] if row_idx == 2 else [0.3, 0.6, 0.88, 0.6, 0.3, 0.1] if row_idx == 3 else [0.3, 0.7, 0.82, 0.5, 0.2, 0.1], 
                     color=cs['color'], linewidth=2.5, marker='o', markersize=6)
        ax_when.axvline(cs["when_hours"], color='#ef4444', linestyle=':', linewidth=2)
        ax_when.text(cs["when_hours"] + 0.5, 0.85, f"Estimated: {cs['when_label']}", fontsize=8.5, fontweight='bold', color='#991b1b', bbox=dict(boxstyle="round,pad=0.25", fc="#fee2e2", ec="#f87171", lw=1))
        ax_when.set_xlim(0, 24)
        ax_when.set_ylim(0, 1.1)
        ax_when.set_xlabel("Elapsed Time Post-Induction (Hours)", fontsize=8.5)
        ax_when.set_ylabel("Kinetic ROS Index", fontsize=8.5)
        ax_when.set_title(f"When: Estimated ROS Timing", fontsize=9.5, fontweight='bold', loc='left', color='#1e293b')
        ax_when.grid(True, linestyle='--', alpha=0.3)

        # Column 3: WHERE (ggPlantMap Cellular Spatial Localization)
        ax_where = axes[row_idx, 2]
        tissues = list(cs["where"].keys())
        scores = list(cs["where"].values())
        x_pos = np.arange(len(tissues))
        
        bar_colors = [plt.cm.magma(0.2 + 0.75 * v) for v in scores]
        bars_w = ax_where.bar(x_pos, scores, color=bar_colors, edgecolor='#1e293b', width=0.55, alpha=0.9)
        ax_where.set_xticks(x_pos)
        ax_where.set_xticklabels(tissues, fontsize=8.5, fontweight='bold')
        ax_where.set_ylim(0, 1.15)
        ax_where.set_ylabel("ggPlantMap Spatial Intensity", fontsize=8.5)
        ax_where.set_title(f"Where: ggPlantMap Localization ({cs['tissue']})", fontsize=9.5, fontweight='bold', loc='left', color='#1e293b')
        ax_where.grid(axis='y', linestyle='--', alpha=0.3)
        for bar in bars_w:
            h = bar.get_height()
            ax_where.text(bar.get_x() + bar.get_width()/2, h + 0.03, f"{(h*100):.0f}%", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1e293b')

    plt.tight_layout(pad=2.5)
    plt.savefig("figures/fig11_osdr_spaceflight_case_studies.png", dpi=300, bbox_inches='tight')
    plt.savefig("figures/fig11_osdr_spaceflight_case_studies.svg", bbox_inches='tight')
    print("Regenerated Figure 11 with OSD-37 in PNG and SVG!")

if __name__ == "__main__":
    generate_figure_11()
