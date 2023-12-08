
const platformImage = new Image();
platformImage.src = './images/platform.png'

const canvas = document.querySelector('canvas');
const c = canvas.getContext('2d');

canvas.width = innerWidth;
canvas.height = innerHeight;

const gravity = .5;

class Player{
    constructor(){
        this.speed = 10;
        this.position = {
            x: 100,
            y: 100,
        }
        this.velocity = {
            x: 0,
            y: 0,
        }
        this.width = 30;
        this.height = 30;
    }

    draw(){
        c.fillStyle = 'red';
        c.fillRect(this.position.x, this.position.y, this.width, this.height);
    }

    update(){
        this.position.y += this.velocity.y;
        this.position.x += this.velocity.x;
        this.draw();
        if(this.position.y + this.height + this.velocity.y <= canvas.height){  
            this.velocity.y += gravity;
        } else {
        }
    }
}


const createImage = (src) => {
    const image = new Image();
    image.src = src;
    return image
}



class Platform{
    constructor({x, y, image}){
        this.position = {
            x,
            y,
        }
        this.width = image.width;
        this.height = image.height;
        this.image = image
    }

    draw(){
        c.fillStyle = 'blue';
        c.fillRect(this.position.x, this.position.y, this.width, this.height);
        c.drawImage(this.image, this.position.x, this.position.y)
    }
}


    draw(){
        
        c.drawImage(this.image, this.position.x, this.position.y)
    }
}

const platformImg = createImage('./images/platform.png');
let player = new Player();

let platforms = [
    new Platform({x: 0, y: canvas.height - 90, image: platformImg}), 
    new Platform({x: platformImg.width*1.5, y: canvas.height - 90, image: platformImg}),
    new Platform({x: platformImg.width*3, y: canvas.height - 90, image: platformImg}),
]
let genericObjects = [new GenericObject({x: 0, y: 0, image: createImage('./images/hills.png')})]
let keys = {
    right: {
        pressed: false
    },
    left: {
        pressed: false
    }
};
player.draw();

let scrollOffset = 0;

const init = () => {
     player = new Player();
    platforms = [
        new Platform({x: 0, y: canvas.height - 90, image: platformImg}), 
        new Platform({x: platformImg.width*1.5, y: canvas.height - 90, image: platformImg}),
        new Platform({x: platformImg.width*3, y: canvas.height - 90, image: platformImg}),
    ] 
    genericObjects = [new GenericObject({x: 0, y: 0, image: createImage('./images/hills.png')})]
     keys = {
        right: {
            pressed: false
        },
        left: {
            pressed: false
        }
    };
    player.draw();

     scrollOffset = 0;
}

const animate = () => {
    requestAnimationFrame(animate);
    c.clearRect(0, 0, canvas.width, canvas.height);

    genericObjects.forEach(object => {
        object.draw();
    })
    platforms.forEach(platform => {
        platform.draw()
    });
    player.update();
 
    platforms.forEach(platform => {
        if(player.position.y + player.height <= platform.position.y && player.position.y + player.height + player.velocity.y >= platform.position.y && player.position.x + player.width >= platform.position.x && player.position.x <= platform.position.x + platform.width){
            player.velocity.y = 0;
        }
    })


    if(scrollOffset > 2000){
        console.log('you win ')
    }

    if(player.position.y > canvas.height){
        console.log('you lose');
        init();
    }

}

animate();

window.addEventListener('keydown', ({k}) => {
    switch(k){
        case 37:
            console.log('left');
            keys.left.pressed = true;
            break;
        case 38:
            console.log('up');
            player.velocity.y -= 10;
            break;
        case 39:
            console.log('right')
            keys.right.pressed = true;
            break;
        case 40:
            console.log('down');
            break;
    }
})

window.addEventListener('keyup', ({k}) => {
    switch(k){
        case 37:
            console.log('left');

            keys.left.pressed = false;
            break;
        case 38:
            console.log('up');
            player.velocity.y -= 0;
            break;
        case 39:
            console.log('right')
            keys.right.pressed = false;
            break;
        case 40:
            console.log('down');
            break;
    }
})