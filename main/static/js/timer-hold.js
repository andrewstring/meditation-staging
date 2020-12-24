var timeObj = {
    second: 0,
    minute: cycle_time,
    numCycles: num_cycles,
    cycleTime: cycle_time,
    numBreathes: num_breathes,
    done: false
  };

var runtime = {run: true};

console.log(timeObj.second);
console.log(timeObj.minute);
document.getElementById('minutes').innerHTML = timeObj.minute;
document.getElementById('seconds').innerHTML = timeObj.second;


  setInterval(function() {
    if (runtime.run) {
      countdown(timeObj);
    }
  }, 1000);


function countdown(time) {
    if (time.second > 0) {
      document.getElementById('minutes').innerHTML = timeObj.minute;
      document.getElementById('seconds').innerHTML = timeObj.second;
      time.second--;
    } else {
        if(time.minute == 0) {
          document.getElementById('minutes').innerHTML = '0';
          document.getElementById('seconds').innerHTML = '0';
          runtime = {run: false};
          window.location.href = "runtime-breath";
        }
        document.getElementById('minutes').innerHTML = timeObj.minute;
        document.getElementById('seconds').innerHTML = timeObj.second;
        time.second = 59;
        time.minute--;
    }
}