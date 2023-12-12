import matplotlib.pyplot as plt
import json
from DelanuaTR import get_triangulate, DelanuaPoint

if __name__ == '__main__':
    json_file_path = r"S:\test.json"

    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    points = [DelanuaPoint(coord[0], coord[1]) for coord in json_data["vertices"]]

    triangles = get_triangulate(points)
    for triangle in triangles:
        triangle.plot_triangle()
    plt.show()
