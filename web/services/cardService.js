const cards = {}; // { uid: balance }

function updateCard(uid, balance) {
  cards[uid] = balance;
}

function getCards() {
  return cards;
}

function topupCard(uid, amount) {
  if (!cards[uid]) cards[uid] = 0;
  cards[uid] += amount;
  return cards[uid];
}

module.exports = { updateCard, getCards, topupCard };
