import math
import matplotlib.pyplot as plt


class DelanuaPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rout(self, p):
        return math.sqrt((p.x - self.x) ** 2 + (p.y - self.y) ** 2)

    def plot_point(self):
        plt.plot([self.x], [self.y], 'ro')


class DelanuaTR:
    def __init__(self, p1, p2, p3):
        self.points = [p1, p2, p3]
        self.edges = [(p1, p2), (p1, p3), (p2, p3)]
        while self.pow_ccwe():
            self.points = [p1, p3, p2]

    def pow_ccwe(self):
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]
        return ((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)) > 0

    def in_circumcircle(self, p4):
        p1, p2, p3 = self.points
        d1x = p1.x - p4.x
        d1y = p1.y - p4.y
        d2x = p2.x - p4.x
        d2y = p2.y - p4.y
        d3x = p3.x - p4.x
        d3y = p3.y - p4.y
        det = ((d1x * d1x + d1y * d1y) * (d2x * d3y - d3x * d2y) -
               (d2x * d2x + d2y * d2y) * (d1x * d3y - d3x * d1y) +
               (d3x * d3x + d3y * d3y) * (d1x * d2y - d2x * d1y))
        return det < 0

    def plot_triangle(self):
        plt.plot([self.points[0].x, self.points[1].x, self.points[2].x, self.points[0].x],
                 [self.points[0].y, self.points[1].y, self.points[2].y, self.points[0].y], "ro-")

def for_edge(triangle, not_triangle):
    polygon = []
    for edge in triangle.edges:
        shared_count = 0
        for other_triangle in not_triangle:
            for other_edge in other_triangle.edges:
                if set(edge) == set(other_edge):
                    shared_count += 1
        if shared_count == 0:
            polygon.append(edge)
    return polygon


def delete_from(super_triangle, triangles, points):
    triangles_to_remove = []
    for i in range(len(triangles)):
        triangle = triangles[i]
        for point in triangle.points:
            if point in super_triangle.points:
                triangles_to_remove.append(i)

    for index in sorted(list(set(triangles_to_remove)), reverse=True):
        del triangles[index]

    for triangle in triangles:
        for point in points:
            if triangle.in_circumcircle(point):
                return "Ошибка"


def get_triangulate(points):
    points.sort(key=lambda p: p.x)

    x_minimal = min(point.x for point in points)
    y_minimal = min(point.y for point in points)
    x_max = max(point.x for point in points)
    y_max = max(point.y for point in points)

    range_x = x_max - x_minimal
    range_y = y_max - y_minimal

    max_range = max(range_x, range_y)

    x_cntr = (x_minimal + x_max) / 2
    y_cntr = (y_minimal + y_max) / 2

    p1 = DelanuaPoint(x_cntr - 20 * max_range, y_cntr - max_range)
    p2 = DelanuaPoint(x_cntr, y_cntr + 20 * max_range)
    p3 = DelanuaPoint(x_cntr + 20 * max_range, y_cntr - max_range)

    super_triangle = DelanuaTR(p1, p2, p3)

    triangles = [super_triangle]

    for point in points:
        bad_triangles = []
        for triangle in triangles:
            if triangle.in_circumcircle(point):
                bad_triangles.append(triangle)
        polygon = []
        for triangle in bad_triangles:
            not_triangle = [x for x in bad_triangles if x != triangle]
            polygon += for_edge(triangle, not_triangle)
        for triangle in bad_triangles:
            triangles.remove(triangle)
        for edge in polygon:
            triangle = DelanuaTR(edge[0], edge[1], point)
            triangles.append(triangle)

    delete_from(super_triangle, triangles, points)
    return triangles
