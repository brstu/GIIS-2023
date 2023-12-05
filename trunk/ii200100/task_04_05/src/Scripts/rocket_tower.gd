class_name Tower extends Node2D

@onready var is_placed = false
@export var cost = 50
@export var damage = 10
@export var speed = 300
@onready var is_upgraded = false
@onready var targets_l = []
@onready var a_targets_l = []
@onready var current_target = null

@onready var attack_delay = 0
@onready var attack_rate = 5

@onready var bullet_res = preload("res://Towers/rocket.tscn")

func _ready():
	pass # Replace with function body.

func _process(delta):
	check_target()
	if is_placed:
		if current_target:
			$Top.look_at(current_target.position)
			$Top.rotate(PI/2)
		attack_delay += delta
		if attack_delay > attack_rate:
			attack_delay = 0
			if current_target:
				_fire()

func check_target():
	if not current_target:
		if a_targets_l.size() > 0:
			current_target = a_targets_l[0]
		elif targets_l.size() > 0:
			current_target = targets_l[0]
		else:
			current_target = null

func _fire():
	var bullet = bullet_res.instantiate()
	bullet.tower = self
	$Bullets.add_child(bullet)
	bullet.damage = damage
	bullet.position = $Top.position

func set_valid(isValid):
	if isValid:
		$BottomRed.hide()
	else:
		$BottomRed.show()

func upgrade():
	if not is_upgraded:
		$Range.scale *= 1.5
	is_upgraded = true
	
func downgrade():
	if is_upgraded:
		$Range.scale /= 1.5
	is_upgraded = false

func _on_tower_mouse_entered():
	$Range.show()

func _on_tower_mouse_exited():
	$Range.hide()

func _on_range_area_entered(area):
	var target = area.get_parent()
	if ("Armor" in target):
		a_targets_l.push_back(target)
	else:
		targets_l.push_back(target)
	check_target()

func _on_range_area_exited(area):
	var target = area.get_parent()
	if ("Armor" in target):
		a_targets_l.erase(target)
	else:
		targets_l.erase(target)
	check_target()
