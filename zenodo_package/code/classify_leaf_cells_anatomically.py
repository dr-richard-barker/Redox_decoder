import json
import numpy as np

def classify_leaf_cells():
    with open("data/ggplantmap_cells.json", "r") as f:
        data = json.load(f)

    inflo_cells = data.get("inflorescence", [])
    
    classified_cells = []
    
    for i, c in enumerate(inflo_cells):
        pts = [tuple(map(float, p.split(","))) for p in c["points"].split()]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        cx = np.mean(xs)
        cy = np.mean(ys)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        w = max_x - min_x
        h = max_y - min_y
        
        # Determine exact anatomical layer based on biological leaf histology:
        # 1. Stomatal Guard Cells: narrow pairs on lower/upper epidermis (w < 8.5 and cy > 340 or cy < 100)
        if (w <= 8.5 and cy >= 340) or (w <= 8.0 and cy <= 105):
            cell_type = "Guard_Cells"
            cell_name = f"Stomatal Guard Cell Complex {i+1}"
            
        # 2. Upper Adaxial Epidermis (cy <= 98)
        elif cy <= 98:
            cell_type = "Adaxial_Epidermis"
            cell_name = f"Upper Adaxial Epidermis Cell {i+1}"
            
        # 3. Lower Abaxial Epidermis (cy >= 345)
        elif cy >= 345:
            cell_type = "Abaxial_Epidermis"
            cell_name = f"Lower Abaxial Epidermis Cell {i+1}"
            
        # 4. Central Vascular Bundle (vein bundle sheath, xylem, phloem)
        # Centered around X in [780, 845], Y in [190, 290]
        elif 780 <= cx <= 845 and 190 <= cy <= 290 and (w < 18 or h < 25 or (195 <= cy <= 265)):
            cell_type = "Vascular_Bundle"
            cell_name = f"Vein Bundle Sheath & Vascular Pole {i+1}"
            
        # 5. Palisade Mesophyll (columnar cells in sub-epidermal adaxial layer: 98 < cy <= 190)
        elif cy <= 190:
            cell_type = "Palisade_Mesophyll"
            cell_name = f"Columnar Palisade Mesophyll Cell {i+1}"
            
        # 6. Spongy Mesophyll (abaxial mesophyll with air spaces: 190 < cy < 345)
        else:
            cell_type = "Spongy_Mesophyll"
            cell_name = f"Spongy Mesophyll Parenchyma {i+1}"
            
        classified_cells.append({
            "id": c["id"],
            "points": c["points"],
            "cellType": cell_type,
            "layer": "Leaf_Cross_Section",
            "name": cell_name,
            "cx": round(cx, 1),
            "cy": round(cy, 1)
        })
        
    type_counts = {}
    for c in classified_cells:
        t = c["cellType"]
        type_counts[t] = type_counts.get(t, 0) + 1
        
    print("Anatomical Leaf Cross-Section Cell Classification:")
    for t, cnt in type_counts.items():
        print(f"  - {t}: {cnt} cells")
        
    return classified_cells

if __name__ == "__main__":
    classify_leaf_cells()
