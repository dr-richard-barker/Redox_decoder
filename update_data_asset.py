import json

def update_ros_decoder_data():
    with open("data/ggplantmap_cells.json", "r") as f:
        cell_data = json.load(f)

    # Read existing ros_decoder_data.js
    with open("data/ros_decoder_data.js", "r") as f:
        js_content = f.read()

    # Tag polygons by cell type / sub-organ for expression mapping
    for i, p in enumerate(cell_data["root"]):
        # Categorize root cells by index based on anatomy
        if i < 20:
            p["cellType"] = "Cortex"
            p["name"] = f"Root Cortex Cell {i+1}"
        elif i < 45:
            p["cellType"] = "Stele"
            p["name"] = f"Root Vascular Stele {i-19}"
        elif i < 65:
            p["cellType"] = "Endodermis"
            p["name"] = f"Root Endodermis {i-44}"
        elif i < 80:
            p["cellType"] = "Meristematic"
            p["name"] = f"Root Apical Meristem {i-64}"
        else:
            p["cellType"] = "Root_Cap"
            p["name"] = f"Columella Root Cap {i-79}"

    for i, p in enumerate(cell_data["inflorescence"]):
        if i < 30:
            p["cellType"] = "Petal"
            p["name"] = f"Floral Petal Layer {i+1}"
        elif i < 65:
            p["cellType"] = "Anther"
            p["name"] = f"Anther & Pollen Sac {i-29}"
        elif i < 100:
            p["cellType"] = "Gynoecium"
            p["name"] = f"Pistil / Gynoecium {i-64}"
        else:
            p["cellType"] = "Vascular"
            p["name"] = f"Pedicel Vascular Stele {i-99}"

    for i, p in enumerate(cell_data["rosette"]):
        if i in [1, 3, 7]:
            p["cellType"] = "Mesophyll"
            p["name"] = f"Rosette Leaf Blade {i+1}"
        elif i in [4, 6]:
            p["cellType"] = "Vascular"
            p["name"] = f"Petiole / Vein {i+1}"
        else:
            p["cellType"] = "Epidermis"
            p["name"] = f"Rosette Lamina Margin {i+1}"

    # Build updated JS file
    cells_json_str = json.dumps(cell_data)
    
    # Inject into ros_decoder_data.js
    injection = f"\n\nwindow.ROS_DECODER_DATA.ggPlantMapCells = {cells_json_str};\n"
    
    if "window.ROS_DECODER_DATA.ggPlantMapCells" in js_content:
        # replace
        js_content = js_content.split("window.ROS_DECODER_DATA.ggPlantMapCells")[0] + f"window.ROS_DECODER_DATA.ggPlantMapCells = {cells_json_str};\n"
    else:
        js_content += injection

    with open("data/ros_decoder_data.js", "w") as f:
        f.write(js_content)

    print("Updated data/ros_decoder_data.js with complete ggPlantMap cell geometries!")

if __name__ == "__main__":
    update_ros_decoder_data()
