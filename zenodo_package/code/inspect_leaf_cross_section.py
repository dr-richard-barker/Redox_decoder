import json
import numpy as np

def inspect_leaf():
    with open("data/ggplantmap_cells.json", "r") as f:
        data = json.load(f)

    inflo_cells = data.get("inflorescence", []) # 138 cells from fig9 panel C
    print(f"Total cells in leaf cross-section: {len(inflo_cells)}")

    # For each cell, calculate centroid (x_c, y_c), bounding box (min_x, max_x, min_y, max_y)
    cell_stats = []
    for i, c in enumerate(inflo_cells):
        pts = [tuple(map(float, p.split(","))) for p in c["points"].split()]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        cx = np.mean(xs)
        cy = np.mean(ys)
        cell_stats.append({
            "idx": i,
            "id": c["id"],
            "cx": cx,
            "cy": cy,
            "min_x": min(xs),
            "max_x": max(xs),
            "min_y": min(ys),
            "max_y": max(ys),
            "width": max(xs) - min(xs),
            "height": max(ys) - min(ys),
            "pts": c["points"]
        })

    # Overall bounds:
    min_y = min(cs["min_y"] for cs in cell_stats)
    max_y = max(cs["max_y"] for cs in cell_stats)
    min_x = min(cs["min_x"] for cs in cell_stats)
    max_x = max(cs["max_x"] for cs in cell_stats)
    print(f"Leaf Cross-Section Bounds: X=[{min_x:.1f}, {max_x:.1f}] (range={max_x-min_x:.1f}), Y=[{min_y:.1f}, {max_y:.1f}] (range={max_y-min_y:.1f})")

    # In Arabidopsis leaf transverse cross-section:
    # Let's inspect Y distribution:
    # Is Y=min the top (Adaxial upper surface) or bottom?
    # In SVG, Y=0 is at TOP!
    # So Y in [39, 120] is the UPPER surface (Adaxial Upper Epidermis & Palisade Mesophyll)!
    # Y in [120, 260] is the MIDDLE (Palisade Mesophyll, Central Vascular Bundle & Xylem/Phloem, Spongy Mesophyll)!
    # Y in [260, 406] is the LOWER surface (Abaxial Lower Epidermis, Spongy Mesophyll, Stomatal Guard Cells)!

    # Let's sort cells by Y centroid and inspect clusters
    cell_stats.sort(key=lambda s: s["cy"])
    print("\n--- Sorted by Y (Top to Bottom in SVG) ---")
    for s in cell_stats[:15]:
        print(f"Top cell {s['idx']:03d}: cy={s['cy']:.1f}, cx={s['cx']:.1f}, w={s['width']:.1f}, h={s['height']:.1f}")

    print("\n--- Middle cells around Y=200 ---")
    mid_cells = [s for s in cell_stats if 190 <= s["cy"] <= 230]
    for s in mid_cells[:15]:
        print(f"Mid cell {s['idx']:03d}: cy={s['cy']:.1f}, cx={s['cx']:.1f}, w={s['width']:.1f}, h={s['height']:.1f}")

    print("\n--- Bottom cells around Y=350 ---")
    for s in cell_stats[-15:]:
        print(f"Bottom cell {s['idx']:03d}: cy={s['cy']:.1f}, cx={s['cx']:.1f}, w={s['width']:.1f}, h={s['height']:.1f}")

if __name__ == "__main__":
    inspect_leaf()
