extends PathFollow2D

@export var speed = 20
@export var HP = 50
@export var reward = 12
@export var Armor = 2

@onready var lvl_manager = get_parent().get_parent()

func _process(delta):
	if self.get_progress_ratio() == 1:
		lvl_manager._take_damage(2)
		queue_free()
	self.set_progress(self.get_progress() + speed*delta)

func _death():
	lvl_manager._get_reward(reward)

func _on_area_2d_body_entered(body):
	HP -= body.damage/Armor
	if HP <= 0:
		_death()
		queue_free()
	body.queue_free()
