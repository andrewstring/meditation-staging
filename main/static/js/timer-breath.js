var timeObj = {
    second: 0,
    minute: cycle_time,
    numCycles: num_cycles,
    cycleTime: cycle_time,
    numBreathes: num_breathes,
    done: false
  };
document.getElementById("message").innerHTML = "Test";

breatheInner(timeObj);
setInterval(function() {
    breatheInner(timeObj);
}, 6000);

function breatheInner(time) {
    if(time.numBreathes > 0) {
        document.getElementById("message").innerHTML = "BREATHE IN";
        setTimeout(function() {
            document.getElementById("message").innerHTML = "BREATHE OUT";
        }, 3000);
        time.numBreathes--;
    } else {
        window.location.href = "runtime-hold";
    }
}