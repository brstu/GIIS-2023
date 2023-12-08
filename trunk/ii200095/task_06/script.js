(function($) {
    const crypto = require('crypto');
    const square = $('.square');
    const documentWidth = $(document).width();
    const documentHeight = $(document).height();

    const squareWidth = square.width();
    const squareHeight = square.height();

    const squareInBottom = documentHeight - squareHeight;
    const squareInRight = documentWidth - squareWidth;
    let isCornerHit = false;
    const cornerRadius = 10;
    const speed = 2;

    function secureRandom() {
        return crypto.randomInt(256);
    }

    function changeColor() {
        const r = secureRandom();
        const g = secureRandom();
        const b = secureRandom();

        square.css({
            background: "rgb(" + r + "," + g + "," + b + ")"
        });
    }

    function moveSquare(topIncrement, leftIncrement, nextFunction) {
        changeColor();
        const moveInterval = setInterval(function() {
            const top = parseInt(square.css('top'));
            const left = parseInt(square.css('left'));

            if (topIncrement > 0 && top >= (squareInBottom - cornerRadius) && left <= cornerRadius) {
                if (!isCornerHit) {
                    isCornerHit = true;
                }
            } else if (topIncrement < 0 && top <= cornerRadius && left <= cornerRadius) {
                if (!isCornerHit) {
                    isCornerHit = true;
                }
            } else if (leftIncrement > 0 && top >= (squareInBottom - cornerRadius) && left >= (squareInRight - cornerRadius)) {
                if (!isCornerHit) {
                    isCornerHit = true;
                }
            } else if (leftIncrement < 0 && top <= cornerRadius && left >= (squareInRight - cornerRadius)) {
                if (!isCornerHit) {
                    isCornerHit = true;
                }
            } else {
                isCornerHit = false;
            }

            if (topIncrement > 0 && top === squareInBottom) {
                clearInterval(moveInterval);
                nextFunction();
            } else if (topIncrement < 0 && top === 0) {
                clearInterval(moveInterval);
                nextFunction();
            } else if (leftIncrement > 0 && left === squareInRight) {
                clearInterval(moveInterval);
                nextFunction();
            } else if (leftIncrement < 0 && left === 0) {
                clearInterval(moveInterval);
                nextFunction();
            } else {
                square.css({
                    top: top + topIncrement + 'px',
                    left: left + leftIncrement + 'px'
                });
            }
        }, speed);
    }

    function bottomLeft() {
        moveSquare(1, -1, topRight);
    }

    function topRight() {
        moveSquare(-1, -1, topLeft);
    }

    function rightBottom() {
        moveSquare(1, 1, topLeft);
    }

    function topLeft() {
        moveSquare(-1, 1, rightBottom);
    }

    moveSquare(1, 1, topLeft);

})(jQuery);