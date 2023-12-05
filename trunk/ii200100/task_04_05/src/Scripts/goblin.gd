extends PathFollow2D

@export var speed = 70
@export var HP = 10
@export var reward = 2

@onready var lvl_manager = get_parent().get_parent()

func _process(delta):
	if self.get_progress_ratio() == 1:
		lvl_manager._take_damage(2)
		queue_free()
	self.set_progress(self.get_progress() + speed*delta)


func _death():
	lvl_manager._get_reward(reward)
	lvl_manager._bonus(position)


func _on_area_2d_body_entered(body):
	HP -= body.damage
	if HP <= 0:
		_death()
		queue_free()
	body.queue_free()
