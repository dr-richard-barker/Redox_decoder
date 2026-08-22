import json

def test_all_four_maps():
    with open("data/ggplantmap_four_organs.json", "r") as f:
        four_organs = json.load(f)

    for organ, cells in four_organs.items():
        print(f"Testing {organ}: {len(cells)} cells")
        all_x = []
        all_y = []
        for c in cells:
            pts = c["points"].split()
            for pt in pts:
                x, y = pt.split(",")
                all_x.append(float(x))
                all_y.append(float(y))
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        print(f"  Bounds: X=[{min_x:.1f}, {max_x:.1f}] (width={max_x-min_x:.1f}), Y=[{min_y:.1f}, {max_y:.1f}] (height={max_y-min_y:.1f})")

if __name__ == "__main__":
    test_all_four_maps()
