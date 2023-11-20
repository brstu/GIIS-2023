let BJgame = {
  'you': { 'scoreSpan': '#yourscore', 'div': '#your-box', 'score': 0 },
  'dealer': { 'scoreSpan': '#dealerscore', 'div': '#dealer-box', 'score': 0 },
  'cards': [],
  'cardsmap': {},
  'initializeCards': function () {
    const suits = ['C', 'D', 'H', 'S'];
    const cardValues = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'K', 'Q', 'J', 'A'];
    for (const suit of suits) {
        for (const value of cardValues) {
            const card = value + suit;
            let cardValue;

            if (value === 'A') {
                cardValue = [1, 11];
            } else if (value === 'K' || value === 'Q' || value === 'J') {
                cardValue = 10;
            } else {
                cardValue = parseInt(value, 10); // Provide the base (10) for decimal numbers
            }

            this.cards.push(card);
            this.cardsmap[card] = cardValue;
            }
        }
  },
  'wins': 0,
  'losses': 0,
  'draws': 0,
  'tokens': 20
};

// Initialize cards and cardsmap
BJgame.initializeCards();

const You = BJgame['you'];
const Dealer = BJgame['dealer'];

function isBlackJack() {
  if (You['score'] === 21) {
    BJgame['tokens'] += 100;
    alert('BLACK-JACK');
    findwinner();
    }
}

function drawCard(activeplayer) {
  let randomNumber;
  if (window.crypto?.getRandomValues) {
     const array = new Uint32Array(1);
     window.crypto.getRandomValues(array);
     randomNumber = array[0] % BJgame['cards'].length;
  } else {
      const crypto = require('crypto');
      const buf = crypto.randomBytes(1);
      randomNumber = buf.readUInt8() % BJgame['cards'].length;
    }
  const currentCard = BJgame['cards'].splice(randomNumber, 1);
  let card = document.createElement('img');
  card.src = `./static/${currentCard}.png`;
  document.querySelector(activeplayer['div']).appendChild(card);
  updateScore(currentCard, activeplayer);
  showScore(activeplayer);
}

function updateScore(currentcard, activeplayer) {
  if (currentcard == 'AC' || currentcard == 'AD' || currentcard == 'AH' || currentcard == 'AS') {
      if ((activeplayer['score'] + BJgame['cardsmap'][currentcard][1]) <= 21) {
          activeplayer['score'] += BJgame['cardsmap'][currentcard][1];
      } else {
          activeplayer['score'] += BJgame['cardsmap'][currentcard][0];
        }
    } else {  // For Other Cases
        activeplayer['score'] += BJgame['cardsmap'][currentcard];
    }
}

function showScore(activeplayer) {
  if (activeplayer['score'] > 21) {
      document.querySelector(activeplayer['scoreSpan']).textContent = 'Перебор!';
      document.querySelector(activeplayer['scoreSpan']).style.color = 'yellow';
  } else {
      document.querySelector(activeplayer['scoreSpan']).textContent = activeplayer['score'];
    }
}

function findwinner() {
  let winner;

  if (You['score'] <= 21) {
    if (Dealer['score'] < You['score'] || Dealer['score'] > 21) {
        BJgame['wins']++;
        BJgame['tokens'] += 5;
        winner = You;
      } else if (Dealer['score'] == You['score']) {
          BJgame['draws']++;
      } else {
          BJgame['losses']++;
          BJgame['tokens'] -= 3;
            winner = Dealer;
        }
    } else if (You['score'] > 21 && Dealer['score'] <= 21) {
        BJgame['losses']++;
        BJgame['tokens'] -= 3;
        winner = Dealer;
    } else if (You['score'] > 21 && Dealer['score'] > 21) {
        BJgame['draws']++;
    }
    return winner;
}

function showresults(winner) {
  if (winner == You) {
      document.querySelector('#command').textContent = 'Вы выиграли!';
      document.querySelector('#command').style.color = 'green';
  } else if (winner == Dealer) {
      document.querySelector('#command').textContent = "Вы проиграли!";
      document.querySelector('#command').style.color = 'red';
  } else {
      document.querySelector('#command').textContent = 'Ничья!';
      document.querySelector('#command').style.color = 'orange';
  }
}

function scoreboard() {
  document.querySelector('#wins').textContent = BJgame['wins'];
  document.querySelector('#losses').textContent = BJgame['losses'];
  document.querySelector('#draws').textContent = BJgame['draws'];
  document.querySelector('#tokens').textContent = BJgame['tokens'];
}

document.querySelector('#hit').addEventListener('click', BJhit);

function BJhit() {
    if (Dealer['score'] === 0 && You['score'] === 0) {
        drawCard(You);
        drawCard(You);
        isBlackJack();
        drawCard(Dealer);
    } else if (You['score'] < 21) {
        drawCard(You);
    }
}

document.querySelector('#deal').addEventListener('click', BJdeal);

function BJdeal() {
    if (You['score'] === 0) {
        alert('Сначала возьмите карту!');
    } else if (Dealer['score'] === 0) {
        alert('Нажмите Стоп, чтобы закончить набор...');
    } else {
        let yourimg = document.querySelector('#your-box').querySelectorAll('img');
        let dealerimg = document.querySelector('#dealer-box').querySelectorAll('img');

        for (const img of yourimg) {
            img.remove();
        }

        for (const img of dealerimg) {
            img.remove();
        }

        BJgame['cards'] = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'KC', 'QC', 'JC', 'AC', '2D', '3D',
            '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'KD', 'QD', 'JD', 'AD', '2H', '3H', '4H', '5H', '6H', '7H',
            '8H', '9H', '10H', 'KH', 'QH', 'JH', 'AH', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'KS',
            'QS', 'JS', 'AS'];

        You['score'] = 0;
        document.querySelector(You['scoreSpan']).textContent = You['score'];
        document.querySelector(You['scoreSpan']).style.color = 'whitesmoke';
        Dealer['score'] = 0;
        document.querySelector(Dealer['scoreSpan']).textContent = Dealer['score'];
        document.querySelector(Dealer['scoreSpan']).style.color = 'whitesmoke';
        document.querySelector('#command').textContent = "🤑🤑🤑🤑🤑🤑";
        document.querySelector('#command').style.color = 'black';
    }
}

document.querySelector('#stand').addEventListener('click', BJstand);

function BJstand() {
  if (You['score'] === 0) {
      alert('Сначала возьмите карту!');
  } else {
      while (Dealer['score'] < 16) {
          drawCard(Dealer);
      }
        setTimeout(function () {
            showresults(findwinner());
            scoreboard();
        }, 800);
    }
}
