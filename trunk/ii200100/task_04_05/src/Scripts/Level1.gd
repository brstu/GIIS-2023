extends Node2D

@onready var is_building = false
@onready var tile_size = 64

@onready var list_tower_res = [
	preload("res://Towers/tower.tscn"),
	preload("res://Towers/rocket_tower.tscn")
	]

@onready var HP = 100
@onready var money = 30

@onready var main_path = get_parent()
@onready var path2d = $Path2D
@export var goblin_res = preload("res://Enemies/goblin.tscn")
@onready var goblin_tick = 0
@export var tank_res = preload("res://Enemies/tank.tscn")
@onready var tank_tick = 0

@onready var plane_bonus_res = preload("res://plane_bonus.tscn")
@onready var plane_res = preload("res://plane.tscn")

var tower_to_place = null
var tower_placement_valid = false

# Called when the node enters the scene tree for the first time.
func _ready():
	main_path._updateUI(money ,HP)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_timer_timeout():
	if goblin_tick < 3:
		goblin_tick += 1
	else:
		goblin_tick = 0
		_spawn_enemy(goblin_res)
	if tank_tick < 70:
		tank_tick += 1
	else:
		tank_tick = 0
		_spawn_enemy(tank_res)


func _get_reward(reward):
	money += reward
	main_path._updateUI(money ,HP)


func _bonus(pos):
	if randi() % 100 < 4:
		var bonus = plane_bonus_res.instantiate()
		bonus.position = pos
		call_deferred("_addBonusChild", bonus)


func _addBonusChild(bonus):
	bonus.lvl_m = self
	$Bonus.add_child(bonus)


func _call_plane():
	var plane = plane_res.instantiate()
	plane.lvl_m = self
	$PlanePath.add_child(plane)


func _take_damage(damage):
	HP -= damage
	if HP <= 0:
		HP = 0
		main_path._game_over()
		var cildren_l = $Path2D.get_children()
		for child in cildren_l:
			child.queue_free()
		$Timer.stop()
	main_path._updateUI(money ,HP)


func _spawn_enemy(enemy_res):
	var enemy = enemy_res.instantiate()
	path2d.add_child(enemy)


func _input(event):
	if not is_building:
		return
	if event is InputEventMouseButton:
		if (event.button_index == MOUSE_BUTTON_LEFT and
		event.is_pressed()
		):
			if tower_placement_valid:
				if money >= tower_to_place.cost:
					money -= tower_to_place.cost
					main_path._updateUI(money ,HP)
					is_building = false
					tower_to_place.is_placed = true
					tower_to_place = null
	elif event is InputEventMouseMotion:
		var mouse_pos = get_global_mouse_position()
		var cell_pos = $Terrain/Hills.local_to_map(mouse_pos)
		mouse_pos = cell_pos * tile_size + \
			Vector2i(tile_size/2, tile_size/2)
		tower_to_place.position = mouse_pos
		
		var towers_l = $Towers.get_children()
		if towers_l:
			for tower in towers_l:
				if tower.position == tower_to_place.position and tower.is_placed:
					tower_placement_valid = false
					tower_to_place.set_valid(tower_placement_valid)
					return
		
		var is_on_hill = $Terrain/Hills.get_cell_source_id(0, cell_pos) != -1
		tower_placement_valid = (is_on_hill \
			or $Terrain/Plain.get_cell_source_id(0, cell_pos) != -1) \
			and not $Terrain/Road.get_cell_source_id(0, cell_pos) != -1 \
			and not $Terrain/Special.get_cell_source_id(0, cell_pos) != -1
		
		if is_on_hill:
			tower_to_place.upgrade()
		else:
			tower_to_place.downgrade()
		
		tower_to_place.set_valid(tower_placement_valid)
	
	elif event is InputEventKey:
		if event.get_keycode() == KEY_ESCAPE:
			is_building = false
			tower_to_place.queue_free()
			tower_to_place = null


func _start_build(i):
	if is_building:
		tower_to_place.queue_free()
		tower_to_place = null
	if not tower_to_place:
		tower_to_place = list_tower_res[i].instantiate()
		$Towers.add_child(tower_to_place)
	is_building = true

