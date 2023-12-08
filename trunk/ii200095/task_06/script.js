document.ready(function(){ 
const crypto = require("crypto");
let square =  (".square");
let documentWidth =  document.width();
let documentHeight =  document.height();

let squareInBottom = documentHeight;
let squareInRight = documentWidth;
let isCornerHit = false;
let cornerRadius = 10;
let speed = 2;

function secureRandom() {
	return crypto.randomInt(256);
}

function changeColor(){
	let r = secureRandom();
	let g = secureRandom();
	let b = secureRandom();

	square.css({
		background:"rgb(" + r + "," + g + ","+ b + ")"
	})
}

function bottomLeft(){
	changeColor();
	console.log("bottomLeft");
	let topRightInterval = setInterval(function(){
		const top = parseInt((".square").css("top"));
		const left = parseInt( (".square").css("left"));
				
				if(top >= (squareInBottom-cornerRadius) && left <= cornerRadius) {      
					console.log(isCornerHit,"bottomLeft corner_hits");
					if(!isCornerHit) { 
					
						
						isCornerHit = true; 
					}		
				}
				if(top === squareInBottom) {
					topRight();
			clearInterval(topRightInterval);
		} else if(left === 0) {		
					rightBottom();
			clearInterval(topRightInterval);
		} else{(".square").css({ top:top+1+"px", left:left-1+"px"});
		}
	},speed);
}

function topRight()
{
	changeColor();
	console.log("topRight");
	let topRightInterval = setInterval(function(){
		const top = parseInt( (".square").css("top"));
		const left = parseInt( (".square").css("left"));
				
				if(top <=cornerRadius && left <=cornerRadius) {    
					console.log(isCornerHit,"topRight corner_hits");
					if(!isCornerHit) {
						isCornerHit = true;       		
					}
				}
		if(top === 0) {
			bottomLeft();
			clearInterval(topRightInterval);
		} else if(left === 0 ) {
			topLeft();
			clearInterval(topRightInterval);
		} else {(".square").css({ top:top-1+"px", left:left-1+"px"});
		}
	},speed);
}

function rightBottom(){
	changeColor();
	console.log("rightBottom");
	let rightBottomInterval = setInterval(function(){
		const top = parseInt( (".square").css("top"));
		const left = parseInt( (".square").css("left"));
		if(top >= squareInBottom-cornerRadius && left >= squareInRight-cornerRadius) {	
			console.log(isCornerHit,"rightBottom corner_hits");
					if(!isCornerHit) {
					
						isCornerHit = true;      		
					}
				}

		if(top === squareInBottom ) {
			topLeft();
			clearInterval(rightBottomInterval);
		} else if(left === squareInRight ) {
			bottomLeft();
			clearInterval(rightBottomInterval);
		} else {
				(".square").css({
				top:top+1+"px",
				left:left+1+"px"
			});				
		}
	},speed);	
}

function topLeft(){
	changeColor();
	console.log("topLeft");
	let topLeftInterval = setInterval(function(){
		const top = parseInt( (".square").css("top"));
		const left = parseInt( (".square").css("left"));
		if(top > cornerRadius && left < squareInRight-cornerRadius ) { 
			isCornerHit = false;
		}
		if(top <= cornerRadius && left >= squareInRight-cornerRadius ) {
			if(!isCornerHit) {						
						isCornerHit = true; 
			}					
				}
				if(left === squareInRight) {	
					topRight();
			clearInterval(topLeftInterval);
		}
		else if(top === 0) {
			rightBottom();
			clearInterval(topLeftInterval);
		} else {
				(".square").css({
				top:top-1+"px",
				left:left+1+"px"
			});
	
		}			
	},speed);
}

let startLoop = setInterval(function(){
	const top = parseInt( (".square").css("top"));
	if(top === squareInBottom){
		topLeft();
		clearInterval(startLoop);
	}	
	else {
		rightBottom();	
		clearInterval(startLoop);
	}
},speed);
});