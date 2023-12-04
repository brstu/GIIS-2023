// import platform from './images/platform.png'

const platformImage = new Image();
platformImage.src = './images/platform.png'

const canvas = document.querySelector('canvas');
const c = canvas.getContext('2d');

canvas.width = innerWidth;
canvas.height = innerHeight;
// canvas.height = window.innerHeight;

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
            // this.velocity.y = 0;
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

class GenericObject{
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
        // c.fillStyle = 'blue';
        // c.fillRect(this.position.x, this.position.y, this.width, this.height);
        c.drawImage(this.image, this.position.x, this.position.y)
    }
}

const platformImg = createImage('./images/platform.png');
let player = new Player();
// const platform = new Platform();
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
    // const platform = new Platform();
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
    // platform.draw();
    if(keys.right.pressed && player.position.x < 400){
        player.velocity.x = player.speed;
    } else if((keys.left.pressed && player.position.x > 100) || keys.left.pressed && scrollOffset === 0 && player.position.x > 0){
        player.velocity.x = -player.speed;
    } else {
        player.velocity.x = 0;

        if(keys.right.pressed){
            platforms.forEach(platform => {
                scrollOffset += player.speed;
                platform.position.x -= player.speed
            });
            genericObjects.forEach(object => {
                object.position.x -= player.speed*.5;
            })
            // platform.position.x -= 5;
        } else if(keys.left.pressed && scrollOffset > 0){
            platforms.forEach(platform => {
                platform.position.x += player.speed
                scrollOffset -= player.speed;
            });
            genericObjects.forEach(object => {
                object.position.x += player.speed*.5;
            })
            // platform.position.x += 5;
        }
    }

    platforms.forEach(platform => {
        if(player.position.y + player.height <= platform.position.y && player.position.y + player.height + player.velocity.y >= platform.position.y && player.position.x + player.width >= platform.position.x && player.position.x <= platform.position.x + platform.width){
            player.velocity.y = 0;
        }
    })


    // win
    if(scrollOffset > 2000){
        console.log('you win ')
    }

    // lose 
    if(player.position.y > canvas.height){
        console.log('you lose');
        init();
    }

}

animate();

window.addEventListener('keydown', ({keyCode}) => {
    switch(keyCode){
        case 37:
            console.log('left');

            keys.left.pressed = true;
            // player.velocity.x = 5;
            break;
        case 38:
            console.log('up');
            player.velocity.y -= 10;
            break;
        case 39:
            console.log('right')
            keys.right.pressed = true;
            // player.velocity.x = 5;
            break;
        case 40:
            console.log('down');
            break;
    }
})

window.addEventListener('keyup', ({keyCode}) => {
    switch(keyCode){
        case 37:
            console.log('left');
            // player.velocity.x = 0;

            keys.left.pressed = false;
            break;
        case 38:
            console.log('up');
            player.velocity.y -= 0;
            break;
        case 39:
            console.log('right')
            keys.right.pressed = false;
            // player.velocity.x = 0;
            break;
        case 40:
            console.log('down');
            break;
    }
})