extends CharacterBody2D

var damage = 30
var end_point = Vector2(300, -150)
var lvl_m = null
var target = null

func _physics_process(delta):
	var children_l = lvl_m.get_node("Path2D").get_children()
	for children in children_l:
		if not target:
			target = children
			continue
		if ("Armor" in children):
			if not ("Armor" in target):
				target = children
			continue
		if children.progress > target.progress:
			target = children
	var direction = null
	if target:
		direction = (target.position - self.global_transform.origin).normalized()
	else:
		direction = (end_point - self.global_transform.origin).normalized()
	direction *= 2
	velocity = direction * 330
	rotation = atan2(velocity.y, velocity.x)
	move_and_slide()


func _on_visible_on_screen_notifier_2d_screen_exited():
	queue_free()
