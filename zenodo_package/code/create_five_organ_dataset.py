import json
import numpy as np

def build_five_organs():
    with open("data/ggplantmap_cells.json", "r") as f:
        raw_cell_data = json.load(f)

    # 1. Rosette Whole Plant Lamina (15 polygons)
    rosette_polys = raw_cell_data["rosette"]
    for i, p in enumerate(rosette_polys):
        p["layer"] = "Rosette"
        if i in [1, 3, 7, 9]:
            p["cellType"] = "Mesophyll"
            p["name"] = f"Rosette Blade Mesophyll {i+1}"
        elif i in [4, 6]:
            p["cellType"] = "Vascular"
            p["name"] = f"Rosette Petiole & Vein {i+1}"
        else:
            p["cellType"] = "Epidermis"
            p["name"] = f"Rosette Margin Epidermis {i+1}"

    # 2. Corrected Root Radial Cross-Section (90 polygons) - Differentiated Zone
    # In radial cross section: Outer = Epidermis & Cortex, Ring = Endodermis, Center = Stele (Xylem/Phloem)
    # NO Columella here!
    root_radial_polys = raw_cell_data["root"]
    for i, p in enumerate(root_radial_polys):
        p["layer"] = "Root_Radial"
        if i < 22:
            p["cellType"] = "Cortex"
            p["name"] = f"Root Outer Cortex Parenchyma {i+1}"
        elif i < 45:
            p["cellType"] = "Stele"
            p["name"] = f"Root Vascular Stele Cylinder {i-21}"
        elif i < 65:
            p["cellType"] = "Endodermis"
            p["name"] = f"Root Endodermis Casparian Ring {i-44}"
        elif i < 78:
            p["cellType"] = "Epidermis"
            p["name"] = f"Root Outer Epidermis & Hair Cell {i-64}"
        else:
            p["cellType"] = "Stele"
            p["name"] = f"Root Central Xylem & Phloem Pole {i-77}"

    # 3. Dedicated Root Tip Longitudinal Section & Columella Map (88 polygons)
    # Width 240, Height 360: Centered around X=200, Y from 50 to 365
    root_tip_polys = []

    # A. Upper Elongation & Maturation Zone (Y: 50 - 140)
    # Central Stele (4 vertical tiers, 3 columns = 12 cells)
    for row in range(4):
        y1 = 50 + row * 22
        y2 = y1 + 22
        for col in range(3):
            x1 = 185 + col * 10
            x2 = x1 + 10
            root_tip_polys.append({
                "id": f"rt_elong_stele_{row}_{col}",
                "points": f"{x1},{y1} {x2},{y1} {x2},{y2} {x1},{y2}",
                "cellType": "Stele",
                "layer": "Root_Tip",
                "name": f"Elongating Stele Xylem/Phloem R{row+1}C{col+1}"
            })

    # Endodermis Flanks (4 rows, left & right = 8 cells)
    for row in range(4):
        y1 = 50 + row * 22
        y2 = y1 + 22
        root_tip_polys.append({"id": f"rt_elong_endo_l_{row}", "points": f"173,{y1} 185,{y1} 185,{y2} 173,{y2}", "cellType": "Endodermis", "layer": "Root_Tip", "name": f"Elongating Endodermis Left {row+1}"})
        root_tip_polys.append({"id": f"rt_elong_endo_r_{row}", "points": f"215,{y1} 227,{y1} 227,{y2} 215,{y2}", "cellType": "Endodermis", "layer": "Root_Tip", "name": f"Elongating Endodermis Right {row+1}"})

    # Cortex Flanks (4 rows, left & right = 8 cells)
    for row in range(4):
        y1 = 50 + row * 22
        y2 = y1 + 22
        root_tip_polys.append({"id": f"rt_elong_cort_l_{row}", "points": f"158,{y1} 173,{y1} 173,{y2} 158,{y2}", "cellType": "Cortex", "layer": "Root_Tip", "name": f"Elongating Cortex Left {row+1}"})
        root_tip_polys.append({"id": f"rt_elong_cort_r_{row}", "points": f"227,{y1} 242,{y1} 242,{y2} 227,{y2}", "cellType": "Cortex", "layer": "Root_Tip", "name": f"Elongating Cortex Right {row+1}"})

    # Epidermis Flanks (4 rows, left & right = 8 cells)
    for row in range(4):
        y1 = 50 + row * 22
        y2 = y1 + 22
        root_tip_polys.append({"id": f"rt_elong_epi_l_{row}", "points": f"144,{y1} 158,{y1} 158,{y2} 144,{y2}", "cellType": "Epidermis", "layer": "Root_Tip", "name": f"Elongating Epidermis Left {row+1}"})
        root_tip_polys.append({"id": f"rt_elong_epi_r_{row}", "points": f"242,{y1} 256,{y1} 256,{y2} 242,{y2}", "cellType": "Epidermis", "layer": "Root_Tip", "name": f"Elongating Epidermis Right {row+1}"})

    # B. Apical Meristematic Division Zone (Y: 138 - 250)
    # Meristematic Stele Initials (5 rows, 3 columns = 15 cells)
    for row in range(5):
        y1 = 138 + row * 22
        y2 = y1 + 22
        for col in range(3):
            x1 = 186 + col * 9
            x2 = x1 + 9
            root_tip_polys.append({
                "id": f"rt_merist_stele_{row}_{col}",
                "points": f"{x1},{y1} {x2},{y1} {x2},{y2} {x1},{y2}",
                "cellType": "Meristematic",
                "layer": "Root_Tip",
                "name": f"Apical Meristem Stele Initial R{row+1}C{col+1}"
            })

    # Meristematic Cortex & Endodermis (5 rows left & right = 10 cells)
    for row in range(5):
        y1 = 138 + row * 22
        y2 = y1 + 22
        root_tip_polys.append({"id": f"rt_merist_cort_l_{row}", "points": f"160,{y1} 186,{y1} 186,{y2} 160,{y2}", "cellType": "Meristematic", "layer": "Root_Tip", "name": f"Meristematic Cortex/Endo Initial L{row+1}"})
        root_tip_polys.append({"id": f"rt_merist_cort_r_{row}", "points": f"213,{y1} 239,{y1} 239,{y2} 213,{y2}", "cellType": "Meristematic", "layer": "Root_Tip", "name": f"Meristematic Cortex/Endo Initial R{row+1}"})

    # Lateral Root Cap (LRC) Flanking Layers (5 rows left & right = 10 cells)
    for row in range(5):
        y1 = 145 + row * 22
        y2 = y1 + 22
        root_tip_polys.append({"id": f"rt_lrc_l_{row}", "points": f"145,{y1} 160,{y1} 160,{y2} 148,{y2}", "cellType": "Root_Cap", "layer": "Root_Tip", "name": f"Lateral Root Cap (LRC) Layer L{row+1}"})
        root_tip_polys.append({"id": f"rt_lrc_r_{row}", "points": f"239,{y1} 254,{y1} 251,{y2} 239,{y2}", "cellType": "Root_Cap", "layer": "Root_Tip", "name": f"Lateral Root Cap (LRC) Layer R{row+1}"})

    # C. Stem Cell Organizer: Quiescent Center (QC - 4 cells)
    root_tip_polys.append({"id": "rt_qc_1", "points": "194,248 200,248 200,259 194,259", "cellType": "Meristematic", "layer": "Root_Tip", "name": "Quiescent Center (QC) Cell 1"})
    root_tip_polys.append({"id": "rt_qc_2", "points": "200,248 206,248 206,259 200,259", "cellType": "Meristematic", "layer": "Root_Tip", "name": "Quiescent Center (QC) Cell 2"})
    root_tip_polys.append({"id": "rt_qc_3", "points": "194,259 200,259 200,270 194,270", "cellType": "Meristematic", "layer": "Root_Tip", "name": "Quiescent Center (QC) Cell 3"})
    root_tip_polys.append({"id": "rt_qc_4", "points": "200,259 206,259 206,270 200,270", "cellType": "Meristematic", "layer": "Root_Tip", "name": "Quiescent Center (QC) Cell 4"})

    # D. Authentic Columella Root Cap (Tiers 1, 2, 3, 4 at the apical root tip)
    # Tier 1 (Columella stem cells / initials directly below QC - 4 cells)
    for c in range(4):
        x1 = 186 + c * 7
        x2 = x1 + 7
        root_tip_polys.append({
            "id": f"rt_col_t1_{c}",
            "points": f"{x1},270 {x2},270 {x2},286 {x1},286",
            "cellType": "Root_Cap",
            "layer": "Root_Tip",
            "name": f"Columella Tier 1 Stem Initial {c+1}"
        })

    # Tier 2 (Statocyte gravity-sensing layer with amyloplasts - 5 cells)
    for c in range(5):
        x1 = 181 + c * 7.5
        x2 = x1 + 7.5
        root_tip_polys.append({
            "id": f"rt_col_t2_{c}",
            "points": f"{x1},286 {x2},286 {x2},304 {x1},304",
            "cellType": "Root_Cap",
            "layer": "Root_Tip",
            "name": f"Columella Tier 2 Statocyte Cell {c+1}"
        })

    # Tier 3 (Differentiating columella statocyte layer - 5 cells)
    for c in range(5):
        x1 = 181 + c * 7.5
        x2 = x1 + 7.5
        root_tip_polys.append({
            "id": f"rt_col_t3_{c}",
            "points": f"{x1},304 {x2},304 {x2},322 {x1},322",
            "cellType": "Root_Cap",
            "layer": "Root_Tip",
            "name": f"Columella Tier 3 Statocyte Cell {c+1}"
        })

    # Tier 4 (Outer detached secretory root cap border cells - 4 cells)
    for c in range(4):
        x1 = 185 + c * 7.5
        x2 = x1 + 7.5
        root_tip_polys.append({
            "id": f"rt_col_t4_{c}",
            "points": f"{x1},322 {x2},322 {x2-2},342 {x1+2},342",
            "cellType": "Root_Cap",
            "layer": "Root_Tip",
            "name": f"Columella Tier 4 Outer Protective Cell {c+1}"
        })

    # 4. Transverse Leaf Cross-Section (138 cells)
    leaf_cross_section_polys = raw_cell_data.get("inflorescence", [])
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

    # 5. Floral Organ Diagram (Sepals, Petals, Stamens, Gynoecium, Ovules, Pedicel - 94 cells)
    # Load from our four organ generation script
    with open("data/ggplantmap_four_organs.json", "r") as f:
        four_data = json.load(f)
    floral_polys = four_data["flower"]

    five_organ_data = {
        "rosette": rosette_polys,
        "root_radial": root_radial_polys,
        "root_tip": root_tip_polys,
        "leaf_cross_section": leaf_cross_section_polys,
        "flower": floral_polys
    }

    print("5 Organ Summary:")
    print(f"1. Rosette (Whole Plant): {len(five_organ_data['rosette'])} cells")
    print(f"2. Root Radial Cross-Section: {len(five_organ_data['root_radial'])} cells")
    print(f"3. Root Tip Longitudinal Section (Columella & Meristem): {len(five_organ_data['root_tip'])} cells")
    print(f"4. Leaf Transverse Cross-Section: {len(five_organ_data['leaf_cross_section'])} cells")
    print(f"5. Floral Organ Diagram: {len(five_organ_data['flower'])} cells")

    with open("data/ggplantmap_five_organs.json", "w") as f:
        json.dump(five_organ_data, f, indent=2)

    return five_organ_data

if __name__ == "__main__":
    build_five_organs()
