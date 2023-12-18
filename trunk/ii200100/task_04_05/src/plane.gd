extends PathFollow2D

@onready var speed = 100
@export var rocket_res = preload("res://rocket_bonus.tscn")
@onready var spawn_rate = 3
@onready var delay = 0

var lvl_m = null

func _process(delta):
	if delay > spawn_rate:
		delay = 0
		var rocket = rocket_res.instantiate()
		rocket.lvl_m = lvl_m
		rocket.position = position
		lvl_m.get_node("Bonus").add_child(rocket)
	delay += delta
	if self.get_progress_ratio() == 1:
		queue_free()
	self.set_progress(self.get_progress() + speed*delta)
