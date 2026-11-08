
import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="MONSTER",
    page_icon="👹",
    layout="wide"
)

st.title("👹 MONSTER")
st.caption("THE JUNGLE FIGHT BEGINS!")

name = st.text_input("Enter your warrior name", "Warrior")

game = r"""
<!DOCTYPE html>
<html>
<head>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #06140c;
    color: white;
    font-family: Arial, sans-serif;
}
canvas {
    width: 100%;
    height: auto;
    display: block;
    border: 3px solid #20d878;
    border-radius: 12px;
    background: #102d20;
    outline: none;
}
.controls {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    padding: 12px 0;
}
button {
    background: #087a38;
    color: white;
    border: 2px solid #39ff88;
    border-radius: 12px;
    padding: 13px 22px;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
    touch-action: none;
}
button:active { background: #20d878; }
.help {
    text-align: center;
    color: #b5e9c7;
    font-size: 14px;
}
</style>
</head>
<body>

<canvas id="game" width="960" height="540" tabindex="0"></canvas>

<div class="controls">
    <button id="left">◀ LEFT</button>
    <button id="right">RIGHT ▶</button>
    <button id="jump">⬆ JUMP</button>
    <button id="attack">⚔️ ATTACK</button>
    <button id="restart">🔄 RESTART</button>
</div>

<div class="help">
    Keyboard: A/D or arrows = Move | W/Space = Jump | J = Attack
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;
const ground = 445;
const playerName = __PLAYER_NAME__;

let keys = {};
let particles = [];
let coins = [];
let time = 0;
let last = 0;
let state = "playing";
let message = "DEFEAT THE MONSTERS!";

let player;
let monster;
let level;
let totalCoins;

function resetGame() {
    player = {
        x: 150, y: ground - 75,
        w: 48, h: 75,
        vx: 0, vy: 0,
        hp: 100, maxHp: 150,
        face: 1, grounded: true,
        attack: 0, attackCooldown: 0,
        invincible: 0, walk: 0
    };

    level = 1;
    totalCoins = Math.floor(Math.random() * 4);
    particles = [];
    coins = [];
    state = "playing";
    message = "DEFEAT THE MONSTERS!";
    createMonster();
}

function createMonster() {
    monster = {
        x: 750, y: ground - 100,
        w: 75, h: 100,
        hp: 100, maxHp: 100,
        face: -1,
        attack: 0,
        cooldown: 0,
        flash: 0,
        walk: 0
    };
}

function rect(x, y, w, h, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
}

function text(t, x, y, size, color="#ffffff", align="left") {
    ctx.fillStyle = color;
    ctx.font = `bold ${size}px Arial`;
    ctx.textAlign = align;
    ctx.fillText(t, x, y);
}

function bar(x, y, w, h, value, max, color) {
    rect(x, y, w, h, "#241c1c");
    rect(x+3, y+3, (w-6)*Math.max(0,value/max), h-6, color);
    ctx.strokeStyle = "white";
    ctx.lineWidth = 2;
    ctx.strokeRect(x, y, w, h);
}

function background() {
    let sky = ctx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,"#071d2a");
    sky.addColorStop(1,"#174c30");
    rect(0,0,W,H,sky);

    // Moon
    ctx.fillStyle = "#d7f5bd";
    ctx.beginPath();
    ctx.arc(790,85,34,0,Math.PI*2);
    ctx.fill();

    // Jungle trees
    for(let i=0;i<12;i++) {
        let x = i*100 - 20;
        rect(x+25,160,20,285,"#422b1c");

        ctx.fillStyle = i%2 ? "#0a4826" : "#126333";
        ctx.beginPath();
        ctx.arc(x+35,160,65,0,Math.PI*2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(x,205,45,0,Math.PI*2);
        ctx.fill();
    }

    // Ground
    rect(0,ground,W,H-ground,"#49321c");
    rect(0,ground,W,12,"#23813d");

    for(let i=0;i<35;i++) {
        let x=(i*83)%W;
        rect(x,ground+25+(i%3)*20,30,4,"#73502b");
    }
}

function drawPlayer() {
    let p=player;
    let x=p.x, y=p.y;

    ctx.save();
    ctx.translate(x+p.w/2,y+p.h/2);
    ctx.scale(p.face,1);
    ctx.translate(-p.w/2,-p.h/2);

    if(p.invincible>0 && Math.floor(time/70)%2===0) {
        ctx.globalAlpha=0.4;
    }

    // Legs
    let leg=Math.sin(p.walk)*9;
    rect(8,51,13,23,"#203fbd");
    rect(28,51+leg,13,23,"#203fbd");

    // Body
    rect(8,23,33,32,"#188a45");

    // Head
    ctx.fillStyle="#d89b69";
    ctx.beginPath();
    ctx.arc(24,14,15,0,Math.PI*2);
    ctx.fill();

    // Hair
    rect(10,0,28,8,"#302018");

    // Eye
    rect(30,12,4,4,"#111111");

    // Sword arm
    rect(35,28,22,9,"#d89b69");

    // Sword animation
    ctx.save();
    ctx.translate(53,32);
    let swing=p.attack>0 ? -Math.sin(p.attack/12*Math.PI)*1.8 : 0;
    ctx.rotate(swing);
    rect(0,-3,43,6,"#d9e6ef");
    rect(36,-7,5,14,"#f6c344");
    ctx.restore();

    ctx.restore();
}

function drawMonster() {
    let m=monster;
    ctx.save();

    let shake=m.flash>0 ? (Math.random()-0.5)*12 : 0;
    ctx.translate(m.x+m.w/2+shake,m.y+m.h/2);
    ctx.scale(m.face,1);
    ctx.translate(-m.w/2,-m.h/2);

    if(m.flash>0) {
        ctx.globalAlpha=0.55;
    }

    let walk=Math.sin(m.walk)*5;

    // Legs
    rect(12,70,20,30,"#44203e");
    rect(47,70+walk,20,30,"#44203e");

    // Body
    ctx.fillStyle=level===1?"#8b2020":"#3d399e";
    ctx.beginPath();
    ctx.ellipse(38,48,38,38,0,0,Math.PI*2);
    ctx.fill();

    // Horns
    ctx.fillStyle="#e7dfbd";
    ctx.beginPath();
    ctx.moveTo(15,22);ctx.lineTo(4,-8);ctx.lineTo(29,12);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(56,22);ctx.lineTo(72,-8);ctx.lineTo(49,12);
    ctx.fill();

    // Eyes
    rect(15,30,15,12,"#ff2525");
    rect(47,30,15,12,"#ff2525");

    // Mouth
    rect(24,58,30,8,"#160b0b");
    for(let i=0;i<3;i++) {
        rect(27+i*9,58,5,8,"white");
    }

    // Fire attack
    if(m.attack>0) {
        ctx.fillStyle="#ff7b00";
        ctx.beginPath();
        ctx.moveTo(-8,40);
        ctx.lineTo(-48,20);
        ctx.lineTo(-35,45);
        ctx.lineTo(-58,60);
        ctx.lineTo(-8,55);
        ctx.fill();
    }

    ctx.restore();
}

function spawnParticles(x,y,color,count=12) {
    for(let i=0;i<count;i++) {
        let angle=Math.random()*Math.PI*2;
        let speed=2+Math.random()*5;
        particles.push({
            x,y,
            vx:Math.cos(angle)*speed,
            vy:Math.sin(angle)*speed,
            life:35,
            color
        });
    }
}

function updateParticles() {
    for(let i=particles.length-1;i>=0;i--) {
        let p=particles[i];
        p.x+=p.vx;
        p.y+=p.vy;
        p.vy+=0.12;
        p.life--;

        ctx.globalAlpha=Math.max(0,p.life/35);
        rect(p.x,p.y,7,7,p.color);
        ctx.globalAlpha=1;

        if(p.life<=0) particles.splice(i,1);
    }
}

function drawHUD() {
    text(playerName,25,35,20);
    bar(25,48,260,22,player.hp,player.maxHp,"#23e66b");
    text("❤️ "+Math.max(0,player.hp),25,93,17);

    text("MONSTER "+level,700,35,20);
    bar(700,48,230,22,monster.hp,monster.maxHp,"#ed2929");
    text("👹 "+Math.max(0,monster.hp),700,93,17);

    text("🪙 COINS: "+totalCoins,440,35,20,"#ffe477","center");
}

function playerAttack() {
    if(player.attackCooldown>0 || state!=="playing") return;

    player.attack=14;
    player.attackCooldown=30;

    let distance=monster.x-player.x;

    if(Math.abs(distance)<125 &&
       Math.sign(distance)===player.face) {

        monster.hp-=25;
        monster.flash=12;
        monster.x+=player.face*35;

        spawnParticles(monster.x+35,monster.y+40,"#ffcc33");
        message="💥 DIRECT HIT!";

        if(monster.hp<=0) {
            monster.hp=0;
            spawnParticles(monster.x+35,monster.y+45,"#ff9d20",35);

            if(level===1) {
                totalCoins+=5;
                player.hp=Math.min(150,player.hp+50);
                message="🏆 MONSTER 1 DEFEATED! +5 COINS +50 HEALTH!";
                level=2;
                setTimeout(()=>{
                    if(state==="playing") createMonster();
                },700);
            } else {
                totalCoins+=10;
                state="won";
                message="YOU ARE THE JUNGLE KING!";
            }
        }
    } else {
        message="⚔️ YOU MISSED! MOVE CLOSER!";
    }
}

function enemyAI(dt) {
    if(monster.hp<=0 || state!=="playing") return;

    let distance=player.x-monster.x;
    monster.face=distance<0?-1:1;

    if(Math.abs(distance)>105) {
        monster.x+=monster.face*1.15*dt;
        monster.walk+=0.15*dt;
    } else {
        monster.cooldown-=dt;

        if(monster.cooldown<=0) {
            monster.attack=18;
            monster.cooldown=95;

            if(player.invincible<=0) {
                player.hp-=12;
                player.invincible=45;
                spawnParticles(player.x+25,player.y+30,"#ff3030");
                message="💥 THE MONSTER HIT YOU!";
            }
        }
    }

    monster.x=Math.max(400,Math.min(850,monster.x));
}

function update(dt) {
    time+=dt*16;

    if(state!=="playing") return;

    let p=player;
    let speed=4.2;

    p.vx=0;

    if(keys.ArrowLeft||keys.a) {
        p.vx=-speed;
        p.face=-1;
    }
    if(keys.ArrowRight||keys.d) {
        p.vx=speed;
        p.face=1;
    }

    p.x+=p.vx*dt;
    p.x=Math.max(10,Math.min(860,p.x));

    if(p.vx!==0) p.walk+=0.2*dt;

    // Gravity
    p.vy+=0.65*dt;
    p.y+=p.vy*dt;

    if(p.y+p.h>=ground) {
        p.y=ground-p.h;
        p.vy=0;
        p.grounded=true;
    }

    if(p.attack>0) p.attack-=dt;
    if(p.attackCooldown>0) p.attackCooldown-=dt;
    if(p.invincible>0) p.invincible-=dt;
    if(monster.flash>0) monster.flash-=dt;
    if(monster.attack>0) monster.attack-=dt;

    enemyAI(dt);

    if(p.hp<=0) {
        p.hp=0;
        state="lost";
        message="GAME OVER! THE MONSTER WON!";
    }
}

function draw() {
    background();

    // Draw some jungle fireflies
    for(let i=0;i<12;i++) {
        let x=(i*91+time*0.3)%W;
        let y=120+(i*47)%240;
        ctx.fillStyle="#baff66";
        ctx.globalAlpha=0.5+Math.sin(time/15+i)*0.4;
        ctx.beginPath();
        ctx.arc(x,y,3,0,Math.PI*2);
        ctx.fill();
    }
    ctx.globalAlpha=1;

    drawPlayer();

    if(monster.hp>0) drawMonster();

    updateParticles();
    drawHUD();

    if(state==="won" || state==="lost") {
        ctx.fillStyle="rgba(0,0,0,0.78)";
        ctx.fillRect(0,0,W,H);

        text(state==="won"?"👑 VICTORY!":"💀 GAME OVER",
             W/2,220,48,state==="won"?"#ffe477":"#ff5555","center");
        text(message,W/2,275,23,"white","center");
        text("PRESS RESTART TO PLAY AGAIN",
             W/2,335,20,"#39ff88","center");
    } else {
        text(message,W/2,510,19,"#ffe477","center");
    }
}

function loop(timestamp) {
    let dt=last ? Math.min((timestamp-last)/16.67,2) : 1;
    last=timestamp;

    update(dt);
    draw();
    requestAnimationFrame(loop);
}

// Keyboard
document.addEventListener("keydown",e=>{
    if(["ArrowLeft","ArrowRight","ArrowUp"," "].includes(e.key))
        e.preventDefault();

    keys[e.key.toLowerCase()]=true;

    if((e.key===" "||e.key==="ArrowUp"||e.key.toLowerCase()==="w")
       && player.grounded && state==="playing") {
        player.vy=-13;
        player.grounded=false;
    }

    if(e.key.toLowerCase()==="j") playerAttack();
});

document.addEventListener("keyup",e=>{
    keys[e.key.toLowerCase()]=false;
});

// On-screen controls
function holdButton(id,key) {
    const b=document.getElementById(id);

    b.addEventListener("pointerdown",e=>{
        e.preventDefault();
        keys[key]=true;
        if(key==="jump" && player.grounded && state==="playing") {
            player.vy=-13;
            player.grounded=false;
        }
        if(key==="attack") playerAttack();
    });

    ["pointerup","pointerleave","pointercancel"].forEach(event=>{
        b.addEventListener(event,()=>keys[key]=false);
    });
}

holdButton("left","a");
holdButton("right","d");
holdButton("jump","jump");
holdButton("attack","attack");

document.getElementById("restart").onclick=resetGame;

resetGame();
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

game = game.replace("__PLAYER_NAME__", json.dumps(name or "Warrior"))

components.html(game, height=660, scrolling=False)
