class_name RTower extends Node2D

@onready var is_placed = false
@export var cost = 10
@export var damage = 2
@export var speed = 500
@onready var is_upgraded = false
@onready var targets_l = []
@onready var current_target = null

@onready var attack_delay = 0
@onready var attack_rate = 1
@onready var barrel = true

@onready var bullet_res = preload("res://Towers/bullet.tscn")

func _ready():
	pass # Replace with function body.

func _process(delta):
	if is_placed:
		if current_target:
			$Top.look_at(current_target.position)
			$Top.rotate(PI/2)
		attack_delay += delta
		if attack_delay > attack_rate:
			attack_delay = 0
			if current_target:
				_fire()

func _fire():
	var bullet = bullet_res.instantiate()
	$Bullets.add_child(bullet)
	bullet.damage = damage
	var offset = current_target.position + current_target.transform.x * 30.
	bullet._velocity = (offset - self.position).normalized() * speed
	
	if barrel:
		bullet.position = $Top/Barrell1.global_transform.origin - $Top.global_transform.origin
	else:
		bullet.position =$Top/Barrell2.global_transform.origin - $Top.global_transform.origin
	barrel = not barrel
	
	

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
	targets_l.append(target)
	if not current_target:
		current_target = targets_l[0]

func _on_range_area_exited(area):
	var target = area.get_parent()
	targets_l.erase(target)
	if current_target == target:
		if targets_l.size() > 0:
			current_target = targets_l[0]
		else:
			current_target = null
