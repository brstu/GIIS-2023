import json
import matplotlib.pyplot as plt

# Функция для построения триангуляции Делоне по заданным точкам
def delaunay_triangulation(points):
    if len(points) == 3:
        return [points]
    elif len(points) == 4:
        return [[0, 1, 2], [0, 2, 3]]  # Триангуляция из двух треугольников для 4 точек
    elif len(points) < 8:
        return divide_3(points)
    elif len(points) < 12:
        return divide_4(points)
    else:
        return divide_5(points)

# Функция для разделения списка точек на группы по 3 точки
def divide_3(points):
    triangles = []
    for i in range(0, len(points), 3):
        triangle = points[i:i + 3]
        triangles.append(triangle)
    return triangles

# Функция для разделения списка точек на группы по 4 точки
def divide_4(points):
    triangles = []
    for i in range(0, len(points), 4):
        quad = points[i:i + 4]
        triangles.extend([[quad[0], quad[1], quad[2]], [quad[0], quad[2], quad[3]]])
    return triangles

# Функция для разделения списка точек на группы по 5 точек
def divide_5(points):
    mid = len(points) // 2
    left_half = points[:mid]
    right_half = points[mid:]

    left_triangles = delaunay_triangulation(left_half)
    right_triangles = delaunay_triangulation(right_half)

    return merge_triangles(left_triangles, right_triangles)

# Функция для объединения двух списков треугольников
def merge_triangles(left_triangles, right_triangles):
    return left_triangles + right_triangles


with open('new_points.json', 'r') as file:
    vertices = json.load(file)

# Создание общего списка точек из словарей
data = [vertex for obj_data in vertices for vertex in obj_data['vertices']]

# Получение триангуляции Делоне через разделяй и властвуй
triangles = delaunay_triangulation(data)

# Визуализация треугольников в 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Отображение треугольников
for triangle in triangles:
    x = [point[0] for point in triangle]  # Извлечение координат X каждой точки треугольника
    y = [point[1] for point in triangle]  # Извлечение координат Y каждой точки треугольника
    z = [point[2] for point in triangle]  # Извлечение координат Z каждой точки треугольника
    ax.plot(x + [x[0]], y + [y[0]], z + [z[0]], color='b')

# Установка меток осей
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Показать график
plt.show()