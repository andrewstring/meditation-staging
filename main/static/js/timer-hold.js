var timeObj = {
    second: 0,
    minute: cycle_time,
    numCycles: num_cycles,
    cycleTime: cycle_time,
    numBreathes: num_breathes,
    done: false
  };


console.log(timeObj.second);
console.log(timeObj.minute);
document.getElementById('minutes').innerHTML = timeObj.minute;
document.getElementById('seconds').innerHTML = timeObj.second;


  setInterval(function() {
    countdown(timeObj);
  }, 1000);


function countdown(time) {
    if (time.second > 0) {
        time.second--;
    } else {
        if(time.minute == 0) {
            window.location.href = "runtime-breath";
        }
        time.second = 59;
        time.minute--;
    }
    document.getElementById('minutes').innerHTML = timeObj.minute;
    document.getElementById('seconds').innerHTML = timeObj.second;
}