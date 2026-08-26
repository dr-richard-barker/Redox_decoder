import xml.etree.ElementTree as ET
import numpy as np

def inspect_fig9_root():
    with open("figures/fig9_spatial_ros_patterns.svg", "r") as f:
        content = f.read()

    # Extract all polygons between line 134 and line 225
    lines = content.splitlines()[134:224]
    print(f"Total lines extracted: {len(lines)}")

    polys = []
    for idx, line in enumerate(lines):
        if "<polygon" not in line:
            continue
        # Extract points
        pts_str = line.split("points='")[1].split("'")[0].strip()
        pts = [tuple(map(float, p.split(","))) for p in pts_str.split()]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        cx = np.mean(xs)
        cy = np.mean(ys)
        
        # Extract fill style
        fill = "none"
        if "fill: #" in line:
            fill = "#" + line.split("fill: #")[1].split(";")[0].strip()
            
        polys.append({
            "idx": idx,
            "cx": cx,
            "cy": cy,
            "pts": pts_str,
            "fill": fill
        })

    print(f"Found {len(polys)} root radial polygons.")

    # Group by index ranges in SVG:
    for i, p in enumerate(polys):
        if i < 22:
            layer = "Epidermis"
            desc = "Root Hair Epidermis & Atrichoblasts"
        elif i < 39:
            layer = "Cortex"
            desc = "Cortical Parenchyma Outer Layer"
        elif i < 47:
            layer = "Endodermis"
            desc = "Endodermis Casparian Ring"
        elif i < 61:
            layer = "Pericycle_Outer_Stele"
            desc = "Pericycle & Stele Boundary"
        elif i < 66:
            layer = "Xylem_Phloem_Poles"
            desc = "Central Diarch Xylem & Phloem Conducting Vessels"
        else:
            layer = "Procambium_Stele"
            desc = "Procambium & Vascular Parenchyma Core"
            
        print(f"Cell {i:02d} ({p['fill']}): cx={p['cx']:.1f}, cy={p['cy']:.1f} -> {layer} ({desc})")

if __name__ == "__main__":
    inspect_fig9_root()
