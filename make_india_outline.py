import json

# projectCoords function
def project_coords(lat, lng):
    min_lng, max_lng = 68.0, 95.0
    min_lat, max_lat = 7.5, 33.5
    svg_w, svg_h = 900, 950
    padding = 70
    x = padding + ((lng - min_lng) / (max_lng - min_lng)) * (svg_w - padding * 2)
    y = (svg_h - padding) - ((lat - min_lat) / (max_lat - min_lat)) * (svg_h - padding * 2)
    return round(x, 1), round(y, 1)

# Major outline coordinates of India (Lat, Lng)
india_pts = [
    (32.5, 74.8), (34.0, 74.5), (34.5, 76.5), (34.0, 78.0), (32.5, 78.8),
    (31.0, 79.0), (30.0, 80.5), (28.5, 82.0), (27.5, 84.5), (27.0, 88.0),
    (27.5, 88.8), (28.0, 91.5), (28.5, 94.5), (28.0, 96.0), (26.5, 96.5),
    (25.5, 95.0), (24.0, 93.5), (23.5, 92.5), (22.0, 92.0), (21.5, 89.0),
    (22.0, 88.0), (20.5, 86.5), (19.0, 85.0), (17.5, 83.5), (15.5, 80.5),
    (13.0, 80.3), (11.0, 79.8), (9.5, 79.0), (8.2, 77.5), (8.5, 76.8),
    (10.0, 76.0), (12.5, 75.0), (15.0, 73.8), (17.0, 73.2), (19.0, 72.8),
    (20.5, 72.7), (21.0, 72.0), (20.5, 70.0), (21.5, 69.5), (22.5, 69.0),
    (23.5, 68.5), (24.5, 68.8), (24.5, 71.0), (26.5, 70.5), (28.0, 71.0),
    (29.5, 72.5), (31.5, 74.5)
]

svg_pts = [project_coords(lat, lng) for lat, lng in india_pts]
path_d = "M " + " L ".join(f"{x} {y}" for x, y in svg_pts) + " Z"
print("Generated India Boundary SVG Path, length:", len(path_d))
print("Sample:", path_d[:120])

with open(r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\india_path.txt", "w") as f:
    f.write(path_d)
