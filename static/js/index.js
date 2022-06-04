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
    animateValue(negscore
    [i], start, end, 5000);
}

