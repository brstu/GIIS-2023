extends Area2D

@onready var expire = 10
@onready var delt = 0
var lvl_m = null

func _process(delta):
	if delt < expire:
		delt += delta
	else:
		queue_free()


func _on_mouse_entered():
	if lvl_m:
		lvl_m._call_plane()
		queue_free()
