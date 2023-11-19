class_name Rocket extends CharacterBody2D

var damage : int
var tower : Node2D

func _physics_process(delta):
	if not tower.current_target:
		queue_free()
		return
	var direction = (tower.current_target.position - self.global_transform.origin).normalized()
	velocity = direction * 150
	rotation = atan2(velocity.y, velocity.x)
	move_and_slide()


func _on_visible_on_screen_notifier_2d_screen_exited():
	queue_free()
