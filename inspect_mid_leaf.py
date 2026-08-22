import json
import numpy as np

def inspect_mid_leaf():
    with open("data/ggplantmap_cells.json", "r") as f:
        data = json.load(f)

    inflo_cells = data.get("inflorescence", [])
    
    for i, c in enumerate(inflo_cells):
        pts = [tuple(map(float, p.split(","))) for p in c["points"].split()]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        cx, cy = np.mean(xs), np.mean(ys)
        w, h = max(xs)-min(xs), max(ys)-min(ys)
        
        if 190 <= cy <= 340:
            print(f"Cell {i:03d}: cy={cy:.1f}, cx={cx:.1f}, w={w:.1f}, h={h:.1f}")

if __name__ == "__main__":
    inspect_mid_leaf()
