function animateValue(obj, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    obj.innerHTML = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

const products = document.getElementsByClassName("product-outer");
const prices = document.getElementsByClassName("price-right-price");
const ratings = document.getElementsByClassName("ratings-text");
const orders = document.getElementsByClassName("price-right-orders");


var pricesArray = [];
var ratingsArray = [];
var ordersArray = [];

for ( i = 0; i < 4 ; i++ ){
    price = prices[i].innerHTML;
    price = price.replace(',','')
    pricesArray.push(parseInt(price));
}
for ( i = 0; i < 4 ; i++ ){
    ratingsArray.push(parseFloat(ratings[i].innerHTML));
}
for ( i = 0; i < 4 ; i++ ){
    order = orders[i].innerHTML;
    order = order.replace('(','')
    order = order.replace(')','')
    order = order.replace(',','')
    ordersArray.push(parseInt(order));
}

console.log(ratingsArray)
console.log(ordersArray)
console.log(pricesArray)



var pricesAvg = 0;
var ratingsAvg = 0;
var ordersAvg = 0;

for ( var i = 0; i < 4; i++){
    price = prices[i].innerHTML;
    price = (parseInt(price.replace(',',''))/4);
    pricesAvg = price + pricesAvg;
}
for ( var i = 0; i < 4; i++){
    price = ratings[i].innerHTML;
    price = (parseFloat(price.replace(',',''))/4);
    ratingsAvg = price + ratingsAvg;
}
for ( var i = 0; i < 4; i++){
    price = orders[i].innerHTML;
    price = price.replace(',','');
    price = price.replace('(','');
    price = (parseInt(price.replace(')',''))/4);
    ordersAvg = price + ordersAvg;
}


const sentiscore = document.getElementsByClassName("sentiment-score-text-inner");
const posscore = document.getElementsByClassName("pos-span");
const neuscore = document.getElementsByClassName("neu-span");
const negscore = document.getElementsByClassName("neg-span");

for ( i = 0; i < 4 ; i++ ){
    var start = 0;
    var end = posscore[i].innerHTML;
    animateValue(posscore[i], start, end, 5000);
}
for ( i = 0; i < 4 ; i++ ){
    var start = 0;
    var end = sentiscore[i].innerHTML;
    animateValue(sentiscore[i], start, end, 5000);
}
for ( i = 0; i < 4 ; i++ ){
    var start = 0;
    var end = neuscore[i].innerHTML;
    animateValue(neuscore[i], start, end, 5000);
}
for ( i = 0; i < 4 ; i++ ){
    var start = 0;
    var end = negscore[i].innerHTML;
    animateValue(negscore[i], start, end, 5000);
}
for ( i = 0; i<4 ; i++ ){
    products[0].classList.add('positive-product')
}

