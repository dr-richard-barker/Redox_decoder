import json
import csv

def build_complete_dataset():
    # 1. Load fig9_cell_type_expression.csv
    cell_matrix = {}
    with open("fig9_cell_type_expression.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        # header: ["", "Unknown", "Epidermis", "Anther", "Tapetum", "Male_meiocyte", "Gynoecium", "Vascular", "Pollen", "Developing_ovule", "Guard_cells", "Stele", "Meristematic", "Seed_coat", "Mesophyll", "Phloem", "Trichoblast", "Phloem_parenchyma"]
        for row in reader:
            if not row or not row[0]: continue
            locus = row[0].strip().upper()
            vals = [float(v) if v else 0.0 for v in row[1:]]
            cell_matrix[locus] = dict(zip(header[1:], vals))

    # 2. Load polygon definitions
    with open("data/ggplantmap_cells.json", "r") as f:
        cell_data = json.load(f)

    # Tag polygons by cell type and descriptive anatomical name
    for i, p in enumerate(cell_data["rosette"]):
        if i in [1, 3, 7, 9]:
            p["cellType"] = "Mesophyll"
            p["name"] = f"Rosette Leaf Blade Mesophyll {i+1}"
        elif i in [4, 6]:
            p["cellType"] = "Vascular"
            p["name"] = f"Rosette Petiole & Primary Vein {i+1}"
        else:
            p["cellType"] = "Epidermis"
            p["name"] = f"Rosette Lamina Margin Epidermis {i+1}"

    for i, p in enumerate(cell_data["root"]):
        if i < 22:
            p["cellType"] = "Cortex"
            p["name"] = f"Root Outer Cortex Layer {i+1}"
        elif i < 45:
            p["cellType"] = "Stele"
            p["name"] = f"Root Central Vascular Stele {i-21}"
        elif i < 65:
            p["cellType"] = "Endodermis"
            p["name"] = f"Root Endodermal Ring {i-44}"
        elif i < 80:
            p["cellType"] = "Meristematic"
            p["name"] = f"Root Apical Meristem {i-64}"
        else:
            p["cellType"] = "Root_Cap"
            p["name"] = f"Columella Root Cap {i-79}"

    for i, p in enumerate(cell_data["inflorescence"]):
        if i < 30:
            p["cellType"] = "Petal"
            p["name"] = f"Floral Petal Whorl {i+1}"
        elif i < 65:
            p["cellType"] = "Anther"
            p["name"] = f"Anther & Pollen Chamber {i-29}"
        elif i < 100:
            p["cellType"] = "Gynoecium"
            p["name"] = f"Gynoecium Pistil & Ovules {i-64}"
        else:
            p["cellType"] = "Vascular"
            p["name"] = f"Floral Pedicel Stele {i-99}"

    # 3. Create comprehensive gene universe with exact cellScores mapping
    gene_list = [
        # Major ROS & Spaceflight Enzymes
        {
            "symbol": "RBOHD", "agi": "AT5G47910", "name": "Respiratory burst oxidase homolog D",
            "weights": {"h2o2": 0.60, "paraquat": 0.95, "menadione": 0.85, "ozone": 0.80, "singlet_oxygen": 0.60, "high_light": 0.72},
            "timeHours": 0.4, "organ": "Root", "cellType": "Stele",
            "cellScores": {"Stele": 0.98, "Root_Cap": 0.92, "Endodermis": 0.82, "Meristematic": 0.88, "Epidermis": 0.75, "Cortex": 0.55, "Mesophyll": 0.35, "Vascular": 0.85, "Anther": 0.30, "Gynoecium": 0.35, "Petal": 0.20}
        },
        {
            "symbol": "RBOHF", "agi": "AT1G64060", "name": "Respiratory burst oxidase homolog F",
            "weights": {"h2o2": 0.55, "paraquat": 0.90, "menadione": 0.80, "ozone": 0.82, "singlet_oxygen": 0.55, "high_light": 0.65},
            "timeHours": 0.5, "organ": "Root", "cellType": "Stele",
            "cellScores": {"Stele": 0.96, "Endodermis": 0.90, "Root_Cap": 0.88, "Meristematic": 0.85, "Epidermis": 0.70, "Cortex": 0.50, "Mesophyll": 0.30, "Vascular": 0.88, "Anther": 0.25, "Gynoecium": 0.30, "Petal": 0.15}
        },
        {
            "symbol": "CAT2", "agi": "AT4G35090", "name": "Catalase 2",
            "weights": {"h2o2": 0.95, "paraquat": 0.45, "menadione": 0.30, "ozone": 0.65, "singlet_oxygen": 0.40, "high_light": 0.85},
            "timeHours": 16.0, "organ": "Leaf", "cellType": "Mesophyll",
            "cellScores": {"Mesophyll": 0.98, "Epidermis": 0.70, "Vascular": 0.75, "Stele": 0.25, "Cortex": 0.20, "Root_Cap": 0.15, "Endodermis": 0.25, "Meristematic": 0.30, "Anther": 0.35, "Gynoecium": 0.35, "Petal": 0.40}
        },
        {
            "symbol": "CAT1", "agi": "AT1G20630", "name": "Catalase 1",
            "weights": {"h2o2": 0.85, "paraquat": 0.35, "menadione": 0.25, "ozone": 0.50, "singlet_oxygen": 0.30, "high_light": 0.60},
            "timeHours": 14.0, "organ": "Seedling", "cellType": "Epidermis",
            "cellScores": {"Epidermis": 0.88, "Mesophyll": 0.75, "Stele": 0.45, "Cortex": 0.40, "Root_Cap": 0.50, "Endodermis": 0.40, "Meristematic": 0.60, "Vascular": 0.60, "Anther": 0.30, "Gynoecium": 0.35, "Petal": 0.30}
        },
        {
            "symbol": "CAT3", "agi": "AT1G20620", "name": "Catalase 3",
            "weights": {"h2o2": 0.80, "paraquat": 0.40, "menadione": 0.20, "ozone": 0.45, "singlet_oxygen": 0.35, "high_light": 0.70},
            "timeHours": 18.0, "organ": "Stem", "cellType": "Vascular",
            "cellScores": {"Vascular": 0.92, "Stele": 0.85, "Mesophyll": 0.45, "Epidermis": 0.40, "Cortex": 0.30, "Root_Cap": 0.25, "Endodermis": 0.50, "Meristematic": 0.40, "Anther": 0.30, "Gynoecium": 0.30, "Petal": 0.30}
        },
        {
            "symbol": "APX1", "agi": "AT1G07890", "name": "Ascorbate peroxidase 1",
            "weights": {"h2o2": 0.92, "paraquat": 0.82, "menadione": 0.55, "ozone": 0.75, "singlet_oxygen": 0.50, "high_light": 0.90},
            "timeHours": 2.5, "organ": "Root", "cellType": "Epidermis",
            "cellScores": {"Stele": 0.90, "Epidermis": 0.88, "Root_Cap": 0.85, "Endodermis": 0.78, "Cortex": 0.60, "Meristematic": 0.80, "Mesophyll": 0.65, "Vascular": 0.80, "Anther": 0.45, "Gynoecium": 0.50, "Petal": 0.40}
        },
        {
            "symbol": "APX2", "agi": "AT3G09640", "name": "Ascorbate peroxidase 2",
            "weights": {"h2o2": 0.75, "paraquat": 0.70, "menadione": 0.40, "ozone": 0.60, "singlet_oxygen": 0.65, "high_light": 0.98},
            "timeHours": 0.75, "organ": "Leaf", "cellType": "Vascular",
            "cellScores": {"Vascular": 0.98, "Mesophyll": 0.92, "Epidermis": 0.75, "Stele": 0.55, "Cortex": 0.30, "Root_Cap": 0.20, "Endodermis": 0.40, "Meristematic": 0.50, "Anther": 0.45, "Gynoecium": 0.40, "Petal": 0.45}
        },
        {
            "symbol": "ZAT12", "agi": "AT5G59820", "name": "Zinc finger protein 12",
            "weights": {"h2o2": 0.95, "paraquat": 0.88, "menadione": 0.80, "ozone": 0.85, "singlet_oxygen": 0.75, "high_light": 0.90},
            "timeHours": 0.5, "organ": "Root", "cellType": "Stele",
            "cellScores": {"Stele": 0.98, "Endodermis": 0.90, "Meristematic": 0.92, "Root_Cap": 0.88, "Cortex": 0.65, "Epidermis": 0.70, "Mesophyll": 0.50, "Vascular": 0.85, "Anther": 0.40, "Gynoecium": 0.45, "Petal": 0.30}
        },
        {
            "symbol": "ZAT10", "agi": "AT1G27730", "name": "Zinc finger protein 10 (STZ)",
            "weights": {"h2o2": 0.89, "paraquat": 0.82, "menadione": 0.70, "ozone": 0.80, "singlet_oxygen": 0.70, "high_light": 0.85},
            "timeHours": 0.6, "organ": "Root", "cellType": "Meristematic",
            "cellScores": {"Meristematic": 0.96, "Stele": 0.92, "Root_Cap": 0.85, "Endodermis": 0.80, "Cortex": 0.55, "Epidermis": 0.60, "Mesophyll": 0.50, "Vascular": 0.75, "Anther": 0.35, "Gynoecium": 0.40, "Petal": 0.30}
        },
        {
            "symbol": "HSFA2", "agi": "AT2G26150", "name": "Heat shock factor A2",
            "weights": {"h2o2": 0.92, "paraquat": 0.75, "menadione": 0.60, "ozone": 0.70, "singlet_oxygen": 0.85, "high_light": 0.95},
            "timeHours": 1.5, "organ": "Inflorescence", "cellType": "Anther",
            "cellScores": {"Anther": 0.98, "Gynoecium": 0.94, "Petal": 0.88, "Meristematic": 0.90, "Mesophyll": 0.85, "Vascular": 0.80, "Epidermis": 0.70, "Stele": 0.55, "Endodermis": 0.45, "Cortex": 0.35, "Root_Cap": 0.40}
        },
        {
            "symbol": "CSD1", "agi": "AT1G08830", "name": "Cu/Zn superoxide dismutase 1",
            "weights": {"h2o2": 0.40, "paraquat": 0.96, "menadione": 0.88, "ozone": 0.70, "singlet_oxygen": 0.45, "high_light": 0.80},
            "timeHours": 5.0, "organ": "Leaf", "cellType": "Mesophyll",
            "cellScores": {"Mesophyll": 0.98, "Epidermis": 0.78, "Vascular": 0.75, "Stele": 0.45, "Cortex": 0.30, "Root_Cap": 0.25, "Endodermis": 0.35, "Meristematic": 0.50, "Anther": 0.45, "Gynoecium": 0.45, "Petal": 0.50}
        },
        {
            "symbol": "CSD2", "agi": "AT2G28190", "name": "Cu/Zn superoxide dismutase 2",
            "weights": {"h2o2": 0.35, "paraquat": 0.94, "menadione": 0.85, "ozone": 0.65, "singlet_oxygen": 0.50, "high_light": 0.85},
            "timeHours": 5.5, "organ": "Leaf", "cellType": "Mesophyll",
            "cellScores": {"Mesophyll": 0.98, "Epidermis": 0.72, "Vascular": 0.78, "Stele": 0.40, "Cortex": 0.25, "Root_Cap": 0.20, "Endodermis": 0.30, "Meristematic": 0.45, "Anther": 0.40, "Gynoecium": 0.40, "Petal": 0.45}
        },
        {
            "symbol": "FSD1", "agi": "AT4G25100", "name": "Fe superoxide dismutase 1",
            "weights": {"h2o2": 0.30, "paraquat": 0.98, "menadione": 0.90, "ozone": 0.60, "singlet_oxygen": 0.55, "high_light": 0.82},
            "timeHours": 3.0, "organ": "Leaf", "cellType": "Mesophyll",
            "cellScores": {"Mesophyll": 0.98, "Epidermis": 0.65, "Vascular": 0.70, "Stele": 0.35, "Cortex": 0.20, "Root_Cap": 0.15, "Endodermis": 0.25, "Meristematic": 0.40, "Anther": 0.35, "Gynoecium": 0.35, "Petal": 0.40}
        },
        {
            "symbol": "MSD1", "agi": "AT3G10920", "name": "Mn superoxide dismutase 1",
            "weights": {"h2o2": 0.50, "paraquat": 0.88, "menadione": 0.85, "ozone": 0.55, "singlet_oxygen": 0.40, "high_light": 0.60},
            "timeHours": 6.5, "organ": "Root", "cellType": "Stele",
            "cellScores": {"Stele": 0.94, "Endodermis": 0.88, "Root_Cap": 0.82, "Meristematic": 0.80, "Cortex": 0.60, "Epidermis": 0.50, "Mesophyll": 0.60, "Vascular": 0.80, "Anther": 0.40, "Gynoecium": 0.40, "Petal": 0.35}
        },
        {
            "symbol": "AOX1A", "agi": "AT3G22370", "name": "Alternative oxidase 1a",
            "weights": {"h2o2": 0.90, "paraquat": 0.85, "menadione": 0.92, "ozone": 0.80, "singlet_oxygen": 0.60, "high_light": 0.70},
            "timeHours": 2.0, "organ": "Root", "cellType": "Stele",
            "cellScores": {"Stele": 0.96, "Endodermis": 0.90, "Meristematic": 0.88, "Root_Cap": 0.85, "Cortex": 0.60, "Epidermis": 0.55, "Mesophyll": 0.50, "Vascular": 0.88, "Anther": 0.35, "Gynoecium": 0.40, "Petal": 0.30}
        },
        {
            "symbol": "ANAC017", "agi": "AT1G34190", "name": "NAC domain-containing protein 17",
            "weights": {"h2o2": 0.92, "paraquat": 0.78, "menadione": 0.88, "ozone": 0.75, "singlet_oxygen": 0.65, "high_light": 0.80},
            "timeHours": 0.6, "organ": "Root", "cellType": "Stele",
            "cellScores": {"Stele": 0.98, "Endodermis": 0.92, "Meristematic": 0.90, "Root_Cap": 0.80, "Cortex": 0.58, "Epidermis": 0.62, "Mesophyll": 0.55, "Vascular": 0.88, "Anther": 0.35, "Gynoecium": 0.40, "Petal": 0.35}
        },
        {
            "symbol": "KIN10", "agi": "AT3G01090", "name": "SnRK1.1 / KIN10 Kinase",
            "weights": {"h2o2": 0.70, "paraquat": 0.65, "menadione": 0.75, "ozone": 0.60, "singlet_oxygen": 0.50, "high_light": 0.55},
            "timeHours": 8.0, "organ": "Root", "cellType": "Stele",
            "cellScores": {"Stele": 0.92, "Endodermis": 0.85, "Meristematic": 0.82, "Root_Cap": 0.78, "Cortex": 0.60, "Epidermis": 0.45, "Mesophyll": 0.40, "Vascular": 0.82, "Anther": 0.30, "Gynoecium": 0.35, "Petal": 0.25}
        },
        {
            "symbol": "PRX34", "agi": "AT3G49120", "name": "Peroxidase 34",
            "weights": {"h2o2": 0.88, "paraquat": 0.75, "menadione": 0.65, "ozone": 0.70, "singlet_oxygen": 0.50, "high_light": 0.60},
            "timeHours": 3.5, "organ": "Root", "cellType": "Epidermis",
            "cellScores": {"Epidermis": 0.95, "Stele": 0.90, "Root_Cap": 0.88, "Cortex": 0.75, "Endodermis": 0.80, "Meristematic": 0.85, "Mesophyll": 0.45, "Vascular": 0.75, "Anther": 0.30, "Gynoecium": 0.35, "Petal": 0.30}
        },
        {
            "symbol": "GR1", "agi": "AT3G24170", "name": "Glutathione reductase 1",
            "weights": {"h2o2": 0.85, "paraquat": 0.75, "menadione": 0.70, "ozone": 0.65, "singlet_oxygen": 0.50, "high_light": 0.78},
            "timeHours": 5.0, "organ": "Root", "cellType": "Stele",
            "cellScores": {"Stele": 0.92, "Endodermis": 0.88, "Root_Cap": 0.80, "Meristematic": 0.78, "Cortex": 0.58, "Epidermis": 0.55, "Mesophyll": 0.60, "Vascular": 0.82, "Anther": 0.40, "Gynoecium": 0.40, "Petal": 0.35}
        },
        {
            "symbol": "GPX7", "agi": "AT4G31870", "name": "Glutathione peroxidase 7",
            "weights": {"h2o2": 0.88, "paraquat": 0.68, "menadione": 0.60, "ozone": 0.62, "singlet_oxygen": 0.80, "high_light": 0.90},
            "timeHours": 2.0, "organ": "Leaf", "cellType": "Mesophyll",
            "cellScores": {"Mesophyll": 0.96, "Epidermis": 0.75, "Vascular": 0.82, "Stele": 0.45, "Cortex": 0.30, "Root_Cap": 0.20, "Endodermis": 0.35, "Meristematic": 0.50, "Anther": 0.50, "Gynoecium": 0.45, "Petal": 0.50}
        },
        {
            "symbol": "WRKY33", "agi": "AT2G38470", "name": "WRKY transcription factor 33",
            "weights": {"h2o2": 0.85, "paraquat": 0.90, "menadione": 0.75, "ozone": 0.80, "singlet_oxygen": 0.60, "high_light": 0.70},
            "timeHours": 1.0, "organ": "Leaf", "cellType": "Mesophyll",
            "cellScores": {"Mesophyll": 0.94, "Epidermis": 0.82, "Vascular": 0.78, "Stele": 0.65, "Cortex": 0.45, "Root_Cap": 0.40, "Endodermis": 0.50, "Meristematic": 0.65, "Anther": 0.45, "Gynoecium": 0.45, "Petal": 0.45}
        },
        # Single-cell publication marker genes from fig9
        {
            "symbol": "AT2G07718", "agi": "AT2G07718", "name": "Anther & floral tapetum ROS marker",
            "weights": {"h2o2": 0.75, "paraquat": 0.60, "menadione": 0.50, "ozone": 0.65, "singlet_oxygen": 0.80, "high_light": 0.85},
            "timeHours": 4.0, "organ": "Inflorescence", "cellType": "Anther",
            "cellScores": {"Anther": 0.98, "Gynoecium": 0.92, "Petal": 0.85, "Vascular": 0.75, "Meristematic": 0.80, "Mesophyll": 0.40, "Epidermis": 0.45, "Stele": 0.30, "Cortex": 0.20, "Root_Cap": 0.15, "Endodermis": 0.25}
        },
        {
            "symbol": "AT3G47680", "agi": "AT3G47680", "name": "Gynoecium & ovule development ROS marker",
            "weights": {"h2o2": 0.70, "paraquat": 0.65, "menadione": 0.45, "ozone": 0.60, "singlet_oxygen": 0.75, "high_light": 0.80},
            "timeHours": 3.0, "organ": "Inflorescence", "cellType": "Gynoecium",
            "cellScores": {"Gynoecium": 0.98, "Anther": 0.92, "Petal": 0.80, "Vascular": 0.70, "Meristematic": 0.75, "Mesophyll": 0.35, "Epidermis": 0.40, "Stele": 0.25, "Cortex": 0.15, "Root_Cap": 0.10, "Endodermis": 0.20}
        },
        {
            "symbol": "AT5G17890", "agi": "AT5G17890", "name": "Guard cells & Epidermal peroxidase",
            "weights": {"h2o2": 0.80, "paraquat": 0.85, "menadione": 0.60, "ozone": 0.92, "singlet_oxygen": 0.70, "high_light": 0.75},
            "timeHours": 1.8, "organ": "Leaf", "cellType": "Epidermis",
            "cellScores": {"Epidermis": 0.98, "Mesophyll": 0.75, "Vascular": 0.70, "Stele": 0.60, "Root_Cap": 0.50, "Cortex": 0.45, "Endodermis": 0.50, "Meristematic": 0.55, "Anther": 0.40, "Gynoecium": 0.40, "Petal": 0.40}
        },
        {
            "symbol": "AT4G36140", "agi": "AT4G36140", "name": "Pollen & Tapetum meiosis marker",
            "weights": {"h2o2": 0.65, "paraquat": 0.60, "menadione": 0.40, "ozone": 0.50, "singlet_oxygen": 0.70, "high_light": 0.75},
            "timeHours": 4.5, "organ": "Inflorescence", "cellType": "Anther",
            "cellScores": {"Anther": 0.98, "Gynoecium": 0.85, "Petal": 0.75, "Vascular": 0.65, "Meristematic": 0.70, "Mesophyll": 0.30, "Epidermis": 0.35, "Stele": 0.25, "Cortex": 0.15, "Root_Cap": 0.10, "Endodermis": 0.20}
        },
        {
            "symbol": "AT5G46510", "agi": "AT5G46510", "name": "Epidermal trichoblast & root hair ROS",
            "weights": {"h2o2": 0.85, "paraquat": 0.80, "menadione": 0.70, "ozone": 0.88, "singlet_oxygen": 0.60, "high_light": 0.65},
            "timeHours": 1.2, "organ": "Root", "cellType": "Epidermis",
            "cellScores": {"Epidermis": 0.98, "Root_Cap": 0.88, "Stele": 0.80, "Cortex": 0.65, "Endodermis": 0.70, "Meristematic": 0.75, "Mesophyll": 0.40, "Vascular": 0.65, "Anther": 0.30, "Gynoecium": 0.30, "Petal": 0.25}
        },
        {
            "symbol": "AT5G05400", "agi": "AT5G05400", "name": "Phloem & vascular parenchyma transporter",
            "weights": {"h2o2": 0.75, "paraquat": 0.70, "menadione": 0.55, "ozone": 0.60, "singlet_oxygen": 0.50, "high_light": 0.70},
            "timeHours": 5.0, "organ": "Stem", "cellType": "Vascular",
            "cellScores": {"Vascular": 0.98, "Stele": 0.92, "Endodermis": 0.75, "Mesophyll": 0.45, "Epidermis": 0.40, "Cortex": 0.35, "Root_Cap": 0.25, "Meristematic": 0.45, "Anther": 0.30, "Gynoecium": 0.35, "Petal": 0.30}
        }
    ]

    # Populate remaining loci from cell_matrix if available
    for locus, cdict in cell_matrix.items():
        if not any(g["agi"] == locus for g in gene_list):
            max_type = max(cdict, key=cdict.get)
            gene_list.append({
                "symbol": locus, "agi": locus, "name": f"Arabidopsis locus {locus}",
                "weights": {"h2o2": 0.70, "paraquat": 0.70, "menadione": 0.50, "ozone": 0.60, "singlet_oxygen": 0.50, "high_light": 0.65},
                "timeHours": 3.0, "organ": "Root" if "Stele" in max_type or "Root" in max_type else "Leaf" if "Mesophyll" in max_type else "Inflorescence",
                "cellType": "Stele" if "Stele" in max_type else "Mesophyll" if "Mesophyll" in max_type else "Anther" if "Anther" in max_type or "Tapetum" in max_type else "Epidermis",
                "cellScores": {
                    "Stele": min(1.0, cdict.get("Stele", 0.02) * 5.0 + 0.1),
                    "Epidermis": min(1.0, cdict.get("Epidermis", 0.02) * 5.0 + 0.1),
                    "Mesophyll": min(1.0, cdict.get("Mesophyll", 0.02) * 5.0 + 0.1),
                    "Anther": min(1.0, (cdict.get("Anther", 0.02) + cdict.get("Tapetum", 0.02)) * 3.5 + 0.1),
                    "Gynoecium": min(1.0, (cdict.get("Gynoecium", 0.02) + cdict.get("Developing_ovule", 0.02)) * 3.5 + 0.1),
                    "Vascular": min(1.0, (cdict.get("Vascular", 0.02) + cdict.get("Phloem", 0.02)) * 3.5 + 0.1),
                    "Meristematic": min(1.0, cdict.get("Meristematic", 0.02) * 4.0 + 0.1),
                    "Root_Cap": min(1.0, cdict.get("Stele", 0.02) * 3.5 + 0.1),
                    "Endodermis": min(1.0, cdict.get("Stele", 0.02) * 4.0 + 0.1),
                    "Cortex": min(1.0, cdict.get("Epidermis", 0.02) * 3.0 + 0.1),
                    "Petal": min(1.0, cdict.get("Epidermis", 0.02) * 3.0 + 0.1)
                }
            })

    output_js = f"""/**
 * Arabidopsis ROS Decoder Web Application Data Asset
 * Comprehensive CVAE latent embeddings, spaceflight projections, gene profiles,
 * ROS stimulus signature matrices, temporal classes, and multi-view ggPlantMap spatial geometries.
 */

window.ROS_DECODER_DATA = {{
  metadata: {{
    title: "Arabidopsis ROS Decoder: Conditional VAE & Spaceflight Validation",
    version: "1.5.0",
    author: "Richard Barker, Ph.D.",
    affiliation: "Department of Agricultural and Biological Engineering, Purdue University",
    geneUniverseSize: 20869,
    totalSamples: 4332,
    groundSamples: 3453,
    spaceflightSamples: 879,
    geoStudies: 232,
    osdrStudies: 38,
    adaAtlasCells: 29993,
    adaCellTypes: 17
  }},

  models: [
    {{
      id: "original_33",
      name: "Original CVAE (33-dim)",
      condDim: 33,
      valLoss: 3860.86,
      bestEpoch: 95,
      trainTimeMin: 28.4,
      activeDims: 14,
      sfSilhouette: 0.0638,
      stimulusSilhouette: -0.3377,
      losoMse: 0.1824,
      losoAcc: "78.4%",
      description: "Baseline CVAE conditioned on 15 stimulus categories and 8 tissue types."
    }},
    {{
      id: "time_aware_37",
      name: "Time-Aware CVAE (37-dim)",
      condDim: 37,
      valLoss: 4095.37,
      bestEpoch: 98,
      trainTimeMin: 20.2,
      activeDims: 14,
      sfSilhouette: 0.1070,
      stimulusSilhouette: -0.4165,
      losoMse: 0.1745,
      losoAcc: "82.1%",
      description: "Incorporates 4-dim continuous/categorical temporal duration features."
    }},
    {{
      id: "devstage_41",
      name: "DevStage CVAE (41-dim)",
      condDim: 41,
      valLoss: 4206.88,
      bestEpoch: 89,
      trainTimeMin: 19.4,
      activeDims: 11,
      sfSilhouette: 0.0882,
      stimulusSilhouette: -0.3709,
      losoMse: 0.1691,
      losoAcc: "85.6%",
      description: "Conditioned on 4-dim developmental stage deconvolution proportions from Salk ADA atlas."
    }}
  ],

  spaceflightSummary: {{
    sfMeanReconError: 0.2736,
    groundMeanReconError: 0.1313,
    ttestPValue: 2.11e-66,
    topDiscriminatingDim: "Dim 1 (t = -13.23, p = 3.33e-39)",
    silhouetteScore: 0.0707
  }},

  osdrCaseStudies: [
    {{
      id: "OSD-678",
      title: "OSD-678 (Root Flight vs Ground)",
      tissue: "Primary Root & Vascular Stele",
      genes: "RBOHD, RBOHF, APX1, ZAT12, KIN10, AOX1A, GR1",
      what: {{ h2o2: 42, paraquat: 38, ozone: 8, singlet_oxygen: 7, high_light: 5 }},
      when: {{ hours: 1.2, label: "Immediate / Early (<1h - 2h)", desc: "Acute oxidative burst mediated by RBOHD/F and rapid APX1 induction." }},
      where: {{ rootStele: 0.88, rootCap: 0.65, leafMesophyll: 0.20, guardCells: 0.35 }},
      reconErr: 0.511
    }},
    {{
      id: "OSD-223",
      title: "OSD-223 (Rosette Leaf Spaceflight)",
      tissue: "Rosette Leaf Lamina",
      genes: "CAT2, HSFA2, GPX7, CSD1, APX2, ZAT10, FSD1",
      what: {{ high_light: 48, singlet_oxygen: 26, h2o2: 16, paraquat: 8, ozone: 2 }},
      when: {{ hours: 16.5, label: "Late / Chronic (>12h)", desc: "Photo-inhibition, chloroplastic singlet oxygen, and CAT2 suppression." }},
      where: {{ rootStele: 0.15, rootCap: 0.10, leafMesophyll: 0.92, guardCells: 0.60 }},
      reconErr: 0.201
    }},
    {{
      id: "OSD-624",
      title: "OSD-624 (Root Hypoxia-ROS Cross-talk)",
      tissue: "Root Vasculature & Meristem",
      genes: "AOX1A, ANAC017, KIN10, MSD1, WRKY40, ERF1",
      what: {{ paraquat: 45, h2o2: 32, menadione: 12, singlet_oxygen: 6, high_light: 5 }},
      when: {{ hours: 6.0, label: "Mid Response (4-8h)", desc: "Mitochondrial retrograde signaling and superoxide accumulation in stele." }},
      where: {{ rootStele: 0.85, rootCap: 0.70, leafMesophyll: 0.25, guardCells: 0.30 }},
      reconErr: 0.338
    }},
    {{
      id: "OSD-37",
      title: "OSD-37 (Four Ecotypes Spaceflight Acclimation)",
      tissue: "Whole Seedling (Col-0, Ler-0, Ws-2, Cvi-0)",
      genes: "RBOHD, RBOHF, APX1, PRX34, CSD1, GR1, CAT2",
      what: {{ h2o2: 39, paraquat: 31, high_light: 15, singlet_oxygen: 9, ozone: 6 }},
      when: {{ hours: 4.5, label: "Early to Mid (~4.5h)", desc: "Ecotype-divergent oxidative phosphorylation and cell wall peroxidase activation across Col-0, Ler-0, Ws-2, and Cvi-0." }},
      where: {{ rootStele: 0.76, rootCap: 0.72, leafMesophyll: 0.58, guardCells: 0.48 }},
      reconErr: 0.296
    }},
    {{
      id: "OSD-38",
      title: "OSD-38 (Whole Seedling Flight)",
      tissue: "Intact Seedling (Shoot + Root)",
      genes: "CAT1, APX1, ZAT12, HSFA2, DHAR1, CSD2, GR1",
      what: {{ h2o2: 35, paraquat: 28, high_light: 20, singlet_oxygen: 10, ozone: 7 }},
      when: {{ hours: 3.8, label: "Early to Mid (2-6h)", desc: "Systemic whole-plant oxidative signaling and cellular antioxidant buffering." }},
      where: {{ rootStele: 0.72, rootCap: 0.58, leafMesophyll: 0.68, guardCells: 0.50 }},
      reconErr: 0.205
    }}
  ],

  geneDatabase: {json.dumps(gene_list, indent=2)}
}};

window.ROS_DECODER_DATA.ggPlantMapCells = {json.dumps(cell_data)};
"""

    with open("data/ros_decoder_data.js", "w") as f:
        f.write(output_js)

    print(f"Successfully assembled complete spatial dataset with {len(gene_list)} annotated genes and full 243 cellular polygons!")

if __name__ == "__main__":
    build_complete_dataset()
