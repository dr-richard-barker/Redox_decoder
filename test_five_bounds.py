import json

def test_five_bounds():
    with open("data/ggplantmap_five_organs.json", "r") as f:
        data = json.load(f)

    for organ, cells in data.items():
        all_x, all_y = [], []
        for c in cells:
            for pt in c["points"].split():
                x, y = pt.split(",")
                all_x.append(float(x))
                all_y.append(float(y))
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        print(f"Organ: {organ} ({len(cells)} cells)")
        print(f"  X: [{min_x:.1f}, {max_x:.1f}] (w={max_x-min_x:.1f})")
        print(f"  Y: [{min_y:.1f}, {max_y:.1f}] (h={max_y-min_y:.1f})")

if __name__ == "__main__":
    test_five_bounds()
