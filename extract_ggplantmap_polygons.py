import xml.etree.ElementTree as ET
import json
import re

def extract_polygons():
    svg_path = "figures/fig9_spatial_ros_patterns.svg"
    with open(svg_path, "r") as f:
        content = f.read()

    # Find all polygon tags
    poly_matches = re.findall(r"<polygon points='([^']+)'[^>]*fill:\s*([^;']+);?", content)
    print(f"Total polygons found in SVG: {len(poly_matches)}")

    # In fig9:
    # Panel A (Rosette): index 0 to 14
    # Panel B (Root): index 15 to 104 (90 polygons!)
    # Panel C (Inflorescence): index 105 to 180 (76 polygons!)

    rosette_polys = []
    root_polys = []
    inflo_polys = []

    for idx, (pts, fill) in enumerate(poly_matches):
        pts_clean = pts.strip()
        if idx < 15:
            rosette_polys.append({"id": f"ros_{idx}", "points": pts_clean, "defaultFill": fill, "layer": "Rosette"})
        elif idx < 105:
            # Root polygons
            root_polys.append({"id": f"root_{idx-15}", "points": pts_clean, "defaultFill": fill, "layer": "Root"})
        else:
            inflo_polys.append({"id": f"inflo_{idx-105}", "points": pts_clean, "defaultFill": fill, "layer": "Inflorescence"})

    print(f"Rosette: {len(rosette_polys)}, Root: {len(root_polys)}, Inflorescence: {len(inflo_polys)}")

    out_data = {
        "rosette": rosette_polys,
        "root": root_polys,
        "inflorescence": inflo_polys
    }

    with open("data/ggplantmap_cells.json", "w") as f:
        json.dump(out_data, f, indent=2)

    print("Saved to data/ggplantmap_cells.json!")

if __name__ == "__main__":
    extract_polygons()
