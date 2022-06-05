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
const rec = document.getElementsByClassName("recommend-outer");

const sentiscore = document.getElementsByClassName("sentiment-score-text-inner");
const posscore = document.getElementsByClassName("pos-span");
const neuscore = document.getElementsByClassName("neu-span");
const negscore = document.getElementsByClassName("neg-span");

var pricesArray = [];
var ratingsArray = [];
var ordersArray = [];
var sentimentsArray = [];

for ( i = 0; i < 4 ; i++ ){
    price = prices[i].innerHTML;
    price = price.replace(',','')
    pricesArray.push(parseInt(price));
}
for ( i = 0; i < 4 ; i++ ){
    ratings[i].innerHTML !== 'N/A' && ratingsArray.push(parseFloat(ratings[i].innerHTML));
}
for ( i = 0; i < 4 ; i++ ){
    order = orders[i].innerHTML;
    order = order.replace('(','')
    order = order.replace(')','')
    order = order.replace(',','')
    order !== 'N/A' && ordersArray.push(parseInt(order));

}
for ( i = 0; i < 4 ; i++ ){
    sentimentsArray.push(parseInt(sentiscore[i].innerHTML));
}




var pricesAvg = 0;
var ratingsAvg = 0;
var ordersAvg = 0;

for ( var i = 0; i < 4; i++){
    pricesAvg = pricesArray[i] + pricesAvg;
}
for ( var i = 0; i < ratingsArray.length ; i++){
    ratingsAvg = ((ratingsArray[i]/ratingsArray.length) + ratingsAvg );
}
for ( var i = 0; i < ordersArray.length ; i++){
    ordersAvg = ((ordersArray[i]/ordersArray.length) + ordersAvg );
}




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

var recommendationScores = [];

for ( i = 0; i < 4 ; i++ ){
    var priceCoefficient;
    if( pricesArray[i] && ratingsArray[i] && ordersArray[i] ){
        if(pricesArray[i] <= pricesAvg && ratingsArray[i] >= ratingsAvg && ordersArray[i] >= ordersAvg){
            priceCoefficient = 8;
        }
        else if(pricesArray[i] <= pricesAvg && ratingsArray[i] >= ratingsAvg && ordersArray[i] <= ordersAvg){
            priceCoefficient = 7;
        }
        else if(pricesArray[i] <= pricesAvg && ratingsArray[i] <= ratingsAvg && ordersArray[i] >= ordersAvg){
            priceCoefficient = 6;
        }
        else if(pricesArray[i] <= pricesAvg && ratingsArray[i] <= ratingsAvg && ordersArray[i] <= ordersAvg){
            priceCoefficient = 5;
        }
        else if(pricesArray[i] >= pricesAvg && ratingsArray[i] >= ratingsAvg && ordersArray[i] >= ordersAvg){
            priceCoefficient = 4;
        }
        else if(pricesArray[i] >= pricesAvg && ratingsArray[i] >= ratingsAvg && ordersArray[i] <= ordersAvg){
            priceCoefficient = 3;
        }
        else if(pricesArray[i] >= pricesAvg && ratingsArray[i] <= ratingsAvg && ordersArray[i] >= ordersAvg){
            priceCoefficient = 2;
        }
        else if(pricesArray[i] >= pricesAvg && ratingsArray[i] <= ratingsAvg && ordersArray[i] <= ordersAvg){
            priceCoefficient = 1;
        }
    }
    else{
        priceCoefficient = 0;
    }

    console.log(priceCoefficient);
    priceCoefficient !== 0 ? recommendationScores.push( priceCoefficient + ((ordersArray[i]*2)/ordersAvg) + (ratingsArray[i]*8.4) + (sentimentsArray[i]*0.4) ) : recommendationScores.push(0)
}

for ( i = 0; i < 4 ; i++ ){
    if (sentimentsArray[i] > 60){
        products[i].classList.add('positive-product')
    }
    else{
        products[i].classList.add('negative-product')
    }
}



const maxRecScore = Math.max(...recommendationScores);
const indexOfMax = recommendationScores.indexOf(maxRecScore);

products[indexOfMax].classList.contains("negative-product") && products[indexOfMax].classList.remove("negative-product");
products[indexOfMax].classList.remove("positive-product");
products[indexOfMax].classList.add('recommended')
rec[indexOfMax].classList.add('show')


