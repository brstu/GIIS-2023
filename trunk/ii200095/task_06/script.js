$(document).ready(function(){ 

	var square = $('.square');
	var documentWidth = $(document).width();
	var documentHeight = $(document).height();

	var squareWidth = square.width();
	var squareHeight = square.height();

	var squareInBottom = documentHeight- squareHeight;
	var squareInRight = documentWidth- squareWidth;
	var isCornerHit = false;
	var cornerRadius = 10;
	var speed = 2;

	function changeColor(){
		var r = Math.round(Math.random()*255);
		var g = Math.round(Math.random()*255);
		var b = Math.round(Math.random()*255);

		square.css({
			background:"rgb(" + r + "," + g + ","+ b + ")"
		})
	}

	function bottomLeft(){
		changeColor();
		console.log('bottomLeft');
		var topRightInterval = setInterval(function(){
			const top = parseInt($('.square').css('top'));
			const left = parseInt($('.square').css('left'));
	      	
	      	if(top >= (squareInBottom-cornerRadius) && left <= cornerRadius) {      
	      		console.log(isCornerHit,'bottomLeft corner_hits');
	      		if(!isCornerHit) { 
	      		
		      		
		      		isCornerHit = true; 
	      		}		
	      	}
	        if(top === squareInBottom) {
	        	topRight();
				clearInterval(topRightInterval);
				return;
			} else if(left === 0) {		
	        	rightBottom();
				clearInterval(topRightInterval);
				return;
			} else {
				$('.square').css({
					top:top+1+'px',
					left:left-1+'px'
				});
			}
		},speed);
	}

	function topRight(){
		changeColor();
		console.log('topRight');
		var topRightInterval = setInterval(function(){
			const top = parseInt($('.square').css('top'));
			const left = parseInt($('.square').css('left'));
	      	
	      	if(top <=cornerRadius && left <=cornerRadius) {    
	      		console.log(isCornerHit,'topRight corner_hits');
	      		if(!isCornerHit) {
	  			
		      		
		      		isCornerHit = true;       		
	      		}
	      	}

	        if(top === 0) {
	        	bottomLeft();
				clearInterval(topRightInterval);
				return;
			} else if(left === 0 ) {
				topLeft();
				clearInterval(topRightInterval);
				return;
			} else {
				$('.square').css({
					top:top-1+'px',
					left:left-1+'px'
				});
			}

			
			
		},speed);
	}

	function rightBottom(){
		changeColor();
		console.log('rightBottom');
		var rightBottomInterval = setInterval(function(){
			const top = parseInt($('.square').css('top'));
			const left = parseInt($('.square').css('left'));


			if(top >= squareInBottom-cornerRadius && left >= squareInRight-cornerRadius) {	
				console.log(isCornerHit,'rightBottom corner_hits');
      			if(!isCornerHit) {
		      	
		      		isCornerHit = true;      		
	   		   	}
	      	}

			if(top === squareInBottom ) {
				topLeft();
				clearInterval(rightBottomInterval);
				return;
			} else if(left === squareInRight ) {
				bottomLeft();
				clearInterval(rightBottomInterval);
				return;
			} else {
				$('.square').css({
					top:top+1+'px',
					left:left+1+'px'
				});				
			}
		},speed);	
	}


	function topLeft(){
		changeColor();
		console.log('topLeft');
		var topLeftInterval = setInterval(function(){
			const top = parseInt($('.square').css('top'));
			const left = parseInt($('.square').css('left'));

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
				return;
			}
			else if(top === 0) {
				rightBottom();
				clearInterval(topLeftInterval);
				return;
			} else {
				$('.square').css({
					top:top-1+'px',
					left:left+1+'px'
				});
		
			}			
		},speed);
		
	}

	var startLoop = setInterval(function(){

		const top = parseInt($('.square').css('top'));
		const left = parseInt($('.square').css('left'));
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