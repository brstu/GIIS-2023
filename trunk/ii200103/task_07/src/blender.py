import bpy
import json
import numpy as np

# Список для хранения вершин каждого объекта
all_vertices = []

# Получаем данные по всем объектам на сцене
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        # Извлекаем вершины для каждого объекта типа "Mesh"
        vertices = [v.co for v in obj.data.vertices]
        # Проверяем наличие вершин и добавляем их в список
        if vertices:
            all_vertices.append({
                "object_name": obj.name,
                "vertices": np.array(vertices).tolist()
            })

# Проверяем, были ли извлечены вершины
if all_vertices:
    output_filepath = '/Users/drsh/points/new_points.json'
    print('HI')
    with open(output_filepath, 'w') as file:
        json.dump(all_vertices, file)
else:
    print("Ошибка: Не удалось найти объекты типа 'Mesh' с вершинами на сцене.")
