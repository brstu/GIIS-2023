import bpy
import json

# Выбираем объект меша
mesh_object = bpy.context.active_object

# Проверяем, является ли выбранный объект мешем
if mesh_object and mesh_object.type == 'MESH':
    # Получаем вершины меша
    vertices_xy = [(v.co.x, v.co.y) for v in mesh_object.data.vertices]

    # Создаем JSON-структуру
    mesh_data = {"vertices": vertices_xy}

    # Сохраняем в JSON-файл
    with open(r"S:\test.json", "w") as json_file:
        json.dump(mesh_data, json_file, indent=4)
    print("JSON-файл успешно создан.")
else:
    print("Выбранный объект не является мешем.")
