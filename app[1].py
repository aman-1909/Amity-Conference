from flask import Flask, render_template_string import time

app = Flask(name)

Traffic light timing (seconds)

GREEN_TIME = 8 YELLOW_TIME = 2 RED_TIME = GREEN_TIME + YELLOW_TIME  # opposite side red duration

HTML = """

<!DOCTYPE html><html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Realistic Traffic Signal</title>
<style>
    body {
        background: #0f172a;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        font-family: Arial, sans-serif;
    }.junction {
    display: flex;
    gap: 60px;
}

.pole {
    width: 90px;
    background: #111827;
    padding: 18px 0;
    border-radius: 18px;
    box-shadow: inset 0 0 12px rgba(0,0,0,0.8), 0 0 25px rgba(0,0,0,0.6);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
}

.light {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: #1f2937;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.9);
    transition: all 0.4s ease;
}

.on.red {
    background: radial-gradient(circle at 30% 30%, #ff4d4d, #b30000);
    box-shadow: 0 0 18px #ff4d4d, inset 0 0 8px #fff2;
}

.on.yellow {
    background: radial-gradient(circle at 30% 30%, #ffd84d, #b38f00);
    box-shadow: 0 0 18px #ffd84d, inset 0 0 8px #fff2;
}

.on.green {
    background: radial-gradient(circle at 30% 30%, #4dff88, #009933);
    box-shadow: 0 0 18px #4dff88, inset 0 0 8px #fff2;
}

.label {
    color: #cbd5e1;
    font-size: 14px;
    margin-top: 6px;
    letter-spacing: 1px;
}

</style>
</head>
<body><div class="junction">
    <div class="pole" id="signalA">
        <div class="light red"></div>
        <div class="light yellow"></div>
        <div class="light green"></div>
        <div class="label">ROAD A</div>
    </div><div class="pole" id="signalB">
    <div class="light red"></div>
    <div class="light yellow"></div>
    <div class="light green"></div>
    <div class="label">ROAD B</div>
</div>

</div><script>
const GREEN = {{ green }};
const YELLOW = {{ yellow }};

let phase = 0; // 0:A green, 1:A yellow, 2:B green, 3:B yellow
let timer = 0;

function setLights(aRed,aYellow,aGreen,bRed,bYellow,bGreen){
    const a = document.querySelectorAll('#signalA .light');
    const b = document.querySelectorAll('#signalB .light');

    a[0].className = 'light red' + (aRed ? ' on red':'');
    a[1].className = 'light yellow' + (aYellow ? ' on yellow':'');
    a[2].className = 'light green' + (aGreen ? ' on green':'');

    b[0].className = 'light red' + (bRed ? ' on red':'');
    b[1].className = 'light yellow' + (bYellow ? ' on yellow':'');
    b[2].className = 'light green' + (bGreen ? ' on green':'');
}

function update(){
    timer++;

    if(phase===0){
        setLights(false,false,true, true,false,false);
        if(timer>=GREEN){ phase=1; timer=0; }
    }
    else if(phase===1){
        setLights(false,true,false, true,false,false);
        if(timer>=YELLOW){ phase=2; timer=0; }
    }
    else if(phase===2){
        setLights(true,false,false, false,false,true);
        if(timer>=GREEN){ phase=3; timer=0; }
    }
    else if(phase===3){
        setLights(true,false,false, false,true,false);
        if(timer>=YELLOW){ phase=0; timer=0; }
    }
}

setInterval(update,1000);
</script></body>
</html>
"""@app.route('/') def index(): return render_template_string(HTML, green=GREEN_TIME, yellow=YELLOW_TIME)

if name == 'main': app.run(debug=True)