class_name Bullet extends CharacterBody2D

var damage : int
var _velocity : Vector2

func _physics_process(delta):
	rotation = atan2(velocity.y, velocity.x)
	velocity = _velocity
	move_and_slide()


func _on_visible_on_screen_notifier_2d_screen_exited():
	queue_free()
