import json
import numpy as np

def generate_four_organs():
    with open("data/ggplantmap_cells.json", "r") as f:
        cell_data = json.load(f)

    # 1. Leaf Cross-Section (Transverse Anatomy) - 138 cells
    leaf_cross_section_polys = cell_data.get("inflorescence", [])
    for i, p in enumerate(leaf_cross_section_polys):
        p["layer"] = "Leaf_Cross_Section"
        if i < 25:
            p["cellType"] = "Adaxial_Epidermis"
            p["name"] = f"Upper Adaxial Epidermis Cell {i+1}"
        elif i < 60:
            p["cellType"] = "Palisade_Mesophyll"
            p["name"] = f"Columnar Palisade Mesophyll Cell {i-24}"
        elif i < 95:
            p["cellType"] = "Spongy_Mesophyll"
            p["name"] = f"Spongy Mesophyll Parenchyma {i-59}"
        elif i < 115:
            p["cellType"] = "Vascular_Bundle"
            p["name"] = f"Vein Bundle Sheath & Xylem {i-94}"
        elif i < 130:
            p["cellType"] = "Abaxial_Epidermis"
            p["name"] = f"Lower Abaxial Epidermis Cell {i-114}"
        else:
            p["cellType"] = "Guard_Cells"
            p["name"] = f"Stomatal Guard Cell Complex {i-129}"

    # 2. Floral Diagram (Sepals, Petals, Stamens/Anthers, Pistil/Gynoecium, Ovules, Pedicel)
    floral_polys = []

    # A. Pedicel and Receptacle Base (Pedicel_Vascular)
    for i in range(5):
        y_top = 310 + i * 15
        y_bot = y_top + 15
        pts = f"188,{y_top} 212,{y_top} 212,{y_bot} 188,{y_bot}"
        floral_polys.append({
            "id": f"fl_ped_{i}",
            "points": pts,
            "cellType": "Pedicel_Vascular",
            "layer": "Flower",
            "name": f"Pedicel Vascular Cylinder {i+1}"
        })

    for i in range(6):
        x_left = 140 + i * 20
        x_right = x_left + 20
        pts = f"{x_left},292 {x_right},292 {x_right-3},310 {x_left+3},310"
        floral_polys.append({
            "id": f"fl_rec_{i}",
            "points": pts,
            "cellType": "Pedicel_Vascular",
            "layer": "Flower",
            "name": f"Floral Receptacle Cortex {i+1}"
        })

    # B. Sepals (Outer Calyx Whorl - 4 Sepals: Lateral Left, Outer Left, Outer Right, Lateral Right)
    for i in range(8):
        y_s = 200 + i * 12
        pts_l = f"95,{y_s} 125,{y_s-5} 120,{y_s+10} 90,{y_s+10}"
        pts_r = f"275,{y_s-5} 305,{y_s} 310,{y_s+10} 280,{y_s+10}"
        floral_polys.append({
            "id": f"fl_sep_l_{i}",
            "points": pts_l,
            "cellType": "Sepal",
            "layer": "Flower",
            "name": f"Protective Calyx Sepal Left {i+1}"
        })
        floral_polys.append({
            "id": f"fl_sep_r_{i}",
            "points": pts_r,
            "cellType": "Sepal",
            "layer": "Flower",
            "name": f"Protective Calyx Sepal Right {i+1}"
        })

    # C. Petals (Corolla Whorl - 4 Expanded Petals)
    for i in range(10):
        y_p = 95 + i * 18
        pts_l = f"105,{y_p} 145,{y_p-6} 150,{y_p+14} 100,{y_p+14}"
        pts_r = f"255,{y_p-6} 295,{y_p} 300,{y_p+14} 250,{y_p+14}"
        floral_polys.append({
            "id": f"fl_pet_l_{i}",
            "points": pts_l,
            "cellType": "Petal",
            "layer": "Flower",
            "name": f"Corolla Petal Blade Left {i+1}"
        })
        floral_polys.append({
            "id": f"fl_pet_r_{i}",
            "points": pts_r,
            "cellType": "Petal",
            "layer": "Flower",
            "name": f"Corolla Petal Blade Right {i+1}"
        })

    # D. Stamens & Anther Pollen Sacs (6 Stamens: Anther locules + filaments)
    # Stamen 1 (Long Inner Left)
    for i in range(4):
        dx = (i % 2) * 14
        dy = (i // 2) * 14
        floral_polys.append({
            "id": f"fl_anth_1_{i}",
            "points": f"{145+dx},{115+dy} {157+dx},{115+dy} {157+dx},{127+dy} {145+dx},{127+dy}",
            "cellType": "Anther", "layer": "Flower", "name": f"Inner Stamen Anther Locule L{i+1}"
        })
    floral_polys.append({"id": "fl_fil_1", "points": "150,143 156,143 166,285 160,285", "cellType": "Pedicel_Vascular", "layer": "Flower", "name": "Stamen Filament L1"})

    # Stamen 2 (Long Inner Right)
    for i in range(4):
        dx = (i % 2) * 14
        dy = (i // 2) * 14
        floral_polys.append({
            "id": f"fl_anth_2_{i}",
            "points": f"{230+dx},{115+dy} {242+dx},{115+dy} {242+dx},{127+dy} {230+dx},{127+dy}",
            "cellType": "Anther", "layer": "Flower", "name": f"Inner Stamen Anther Locule R{i+1}"
        })
    floral_polys.append({"id": "fl_fil_2", "points": "244,143 250,143 240,285 234,285", "cellType": "Pedicel_Vascular", "layer": "Flower", "name": "Stamen Filament R1"})

    # Stamen 3 (Lateral Short Left)
    for i in range(4):
        dx = (i % 2) * 14
        dy = (i // 2) * 14
        floral_polys.append({
            "id": f"fl_anth_3_{i}",
            "points": f"{132+dx},{165+dy} {144+dx},{165+dy} {144+dx},{177+dy} {132+dx},{177+dy}",
            "cellType": "Anther", "layer": "Flower", "name": f"Lateral Stamen Anther Locule L{i+1}"
        })
    floral_polys.append({"id": "fl_fil_3", "points": "136,193 142,193 154,285 148,285", "cellType": "Pedicel_Vascular", "layer": "Flower", "name": "Stamen Filament L2"})

    # Stamen 4 (Lateral Short Right)
    for i in range(4):
        dx = (i % 2) * 14
        dy = (i // 2) * 14
        floral_polys.append({
            "id": f"fl_anth_4_{i}",
            "points": f"{242+dx},{165+dy} {254+dx},{165+dy} {254+dx},{177+dy} {242+dx},{177+dy}",
            "cellType": "Anther", "layer": "Flower", "name": f"Lateral Stamen Anther Locule R{i+1}"
        })
    floral_polys.append({"id": "fl_fil_4", "points": "258,193 264,193 252,285 246,285", "cellType": "Pedicel_Vascular", "layer": "Flower", "name": "Stamen Filament R2"})

    # E. Central Gynoecium / Pistil (Stigma, Style, Ovary Carpel Walls, Replum Septum, Ovules)
    # Stigma & Style
    floral_polys.append({"id": "fl_stg_l", "points": "186,70 199,58 199,78 186,78", "cellType": "Gynoecium", "layer": "Flower", "name": "Stigma Papillae Left"})
    floral_polys.append({"id": "fl_stg_r", "points": "201,58 214,70 214,78 201,78", "cellType": "Gynoecium", "layer": "Flower", "name": "Stigma Papillae Right"})
    floral_polys.append({"id": "fl_sty", "points": "193,78 207,78 207,95 193,95", "cellType": "Gynoecium", "layer": "Flower", "name": "Style Transmission Neck"})

    # Ovary Carpel Valve Walls (Left & Right 6 segments each)
    for i in range(6):
        y_t = 95 + i * 32
        y_b = y_t + 32
        floral_polys.append({"id": f"fl_ov_w_l_{i}", "points": f"176,{y_t} 187,{y_t} 187,{y_b} 176,{y_b}", "cellType": "Gynoecium", "layer": "Flower", "name": f"Ovary Carpel Wall Left {i+1}"})
        floral_polys.append({"id": f"fl_ov_w_r_{i}", "points": f"213,{y_t} 224,{y_t} 224,{y_b} 213,{y_b}", "cellType": "Gynoecium", "layer": "Flower", "name": f"Ovary Carpel Wall Right {i+1}"})

    # Replum Central Septum (5 blocks)
    for i in range(5):
        y_s = 95 + i * 38
        floral_polys.append({"id": f"fl_rep_{i}", "points": f"197,{y_s} 203,{y_s} 203,{y_s+38} 197,{y_s+38}", "cellType": "Gynoecium", "layer": "Flower", "name": f"Ovary Central Replum Septum {i+1}"})

    # Developing Ovules (10 locular ovules attached to placenta)
    for i in range(10):
        y_ov = 102 + i * 18
        floral_polys.append({"id": f"fl_ovule_{i}", "points": f"189,{y_ov} 211,{y_ov} 211,{y_ov+14} 189,{y_ov+14}", "cellType": "Gynoecium", "layer": "Flower", "name": f"Developing Floral Ovule {i+1}"})

    four_organ_data = {
        "rosette": cell_data["rosette"],
        "root": cell_data["root"],
        "leaf_cross_section": leaf_cross_section_polys,
        "flower": floral_polys
    }

    with open("data/ggplantmap_four_organs.json", "w") as f:
        json.dump(four_organ_data, f, indent=2)

    print("Successfully built updated four organs JSON!")

if __name__ == "__main__":
    generate_four_organs()
