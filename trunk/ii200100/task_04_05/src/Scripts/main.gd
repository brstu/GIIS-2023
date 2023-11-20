extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _updateUI(money, hp):
	$CanvasLayer/UI/HBoxContainer/Dol/Label.text = "%s" % money
	$CanvasLayer/UI/HBoxContainer/HP/Label.text = "%s" % hp


func _game_over():
	$CanvasLayer/UI/Towers.hide()
	$CanvasLayer/UI/Label.show()


func _on_tower_pressed():
	$Level._start_build(0)


func _on_rockets_pressed():
	$Level._start_build(1)
