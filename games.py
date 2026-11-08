
import streamlit as st
import random

st.set_page_config(
    page_title="MONSTER",
    page_icon="👹",
    layout="wide"
)

# ---------------- CSS ANIMATIONS ----------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #061b12, #102d20, #020b08);
    color: white;
}

h1 {
    text-align: center;
    color: #39ff88;
    text-shadow: 0 0 15px #00ff66;
}

h2, h3, p, label {
    color: white !important;
}

.monster {
    font-size: 110px;
    text-align: center;
    animation: monsterIdle 2s infinite ease-in-out;
    filter: drop-shadow(0 0 15px red);
}

.monster.attack {
    animation: monsterAttack 0.7s ease-in-out;
}

.monster.hit {
    animation: monsterHit 0.5s ease-in-out;
}

@keyframes monsterIdle {
    0%, 100% { transform: translateY(0) rotate(-3deg); }
    50% { transform: translateY(-20px) rotate(3deg); }
}

@keyframes monsterAttack {
    0% { transform: translateX(0) scale(1); }
    40% { transform: translateX(-80px) scale(1.3); }
    100% { transform: translateX(0) scale(1); }
}

@keyframes monsterHit {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-15px) rotate(-10deg); }
    50% { transform: translateX(15px) rotate(10deg); }
    75% { transform: translateX(-10px); }
}

.jungle-card {
    background: rgba(0, 30, 15, 0.85);
    border: 2px solid #20d878;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 20px rgba(0,255,100,0.25);
}

.coin {
    display: inline-block;
    font-size: 45px;
    animation: coinSpin 1.5s infinite linear;
}

@keyframes coinSpin {
    0% { transform: rotateY(0deg); }
    100% { transform: rotateY(360deg); }
}

.fire {
    font-size: 45px;
    text-align: center;
    animation: fireEffect 0.5s infinite alternate;
}

@keyframes fireEffect {
    from { transform: scale(0.8); opacity: 0.6; }
    to { transform: scale(1.3); opacity: 1; }
}

.stButton > button {
    background: linear-gradient(90deg, #087a38, #19e66a);
    color: white;
    border: 2px solid #50ff9b;
    border-radius: 12px;
    font-weight: bold;
    width: 100%;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.04);
    box-shadow: 0 0 20px #00ff66;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GAME TITLE ----------------

st.title("👹 MONSTER")
st.markdown(
    "<p style='text-align:center;font-size:20px;'>"
    "⚔️ ENTER THE JUNGLE • DEFEAT THE MONSTERS ⚔️"
    "</p>",
    unsafe_allow_html=True
)

# ---------------- SESSION STATE ----------------

defaults = {
    "started": False,
    "userhealth": 100,
    "monsterhealth": 100,
    "monster2health": 100,
    "coins": 0,
    "level": 1,
    "game_over": False,
    "name": "",
    "effect": "idle",
    "message": "Your adventure begins!"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- START GAME ----------------

name = st.text_input("🧑 Enter your warrior name")

if st.button("🚀 START GAME"):
    st.session_state.started = True
    st.session_state.name = name if name else "Warrior"
    st.session_state.userhealth = 100
    st.session_state.monsterhealth = 100
    st.session_state.monster2health = 100
    st.session_state.coins = random.randint(0, 3)
    st.session_state.level = 1
    st.session_state.game_over = False
    st.session_state.effect = "idle"
    st.session_state.message = "The jungle adventure begins!"
    st.rerun()

# ---------------- MAIN GAME ----------------

if st.session_state.started:

    st.subheader(f"⚔️ Welcome, {st.session_state.name}!")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="jungle-card">
                <div class="coin">🪙</div>
                <h3>COINS</h3>
                <h2>{st.session_state.coins}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="jungle-card">
                <h3>❤️ YOUR HEALTH</h3>
                <h2>{st.session_state.userhealth}/150</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.progress(max(0, min(150, st.session_state.userhealth)) / 150)

    # -------- MONSTER DISPLAY --------

    if st.session_state.level == 1:
        monster_name = "MONSTER 1"
        monster_emoji = "👹"
        health = st.session_state.monsterhealth
    else:
        monster_name = "MONSTER 2"
        monster_emoji = "🐉"
        health = st.session_state.monster2health

    st.markdown(
        f"""
        <div class="jungle-card">
            <h2>🔥 {monster_name} 🔥</h2>
            <div class="monster {st.session_state.effect}">
                {monster_emoji}
            </div>
            <h3>MONSTER HEALTH: {health}/100</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(max(0, health) / 100)

    # -------- BATTLE --------

    if not st.session_state.game_over:

        st.subheader("⚔️ CHOOSE YOUR ATTACK")

        user = st.slider(
            "Select attack power",
            min_value=0,
            max_value=50,
            value=20
        )

        if st.button("🔥 ATTACK THE MONSTER"):

            st.session_state.effect = "hit"

            if st.session_state.level == 1:

                st.session_state.monsterhealth -= user

                if st.session_state.monsterhealth <= 0:

                    st.session_state.monsterhealth = 0
                    st.session_state.coins += 5
                    st.session_state.userhealth = min(
                        150, st.session_state.userhealth + 50
                    )
                    st.session_state.level = 2
                    st.session_state.message = (
                        "🏆 MONSTER 1 DEFEATED! +50 HEALTH +5 COINS!"
                    )
                    st.balloons()

                else:
                    monster_attack = random.randint(0, 100)
                    st.session_state.userhealth -= monster_attack
                    st.session_state.effect = "attack"
                    st.session_state.message = (
                        f"💥 You dealt {user} damage! "
                        f"Monster attacked for {monster_attack} damage!"
                    )

            elif st.session_state.level == 2:

                st.session_state.monster2health -= user

                if st.session_state.monster2health <= 0:

                    st.session_state.monster2health = 0
                    st.session_state.game_over = True
                    st.session_state.coins += 10
                    st.session_state.message = (
                        "👑 YOU DEFEATED BOTH MONSTERS! YOU ARE THE JUNGLE KING!"
                    )
                    st.balloons()

                else:
                    monster_attack = random.randint(0, 30)
                    st.session_state.userhealth -= monster_attack
                    st.session_state.effect = "attack"
                    st.session_state.message = (
                        f"💥 You dealt {user} damage! "
                        f"Monster attacked for {monster_attack} damage!"
                    )

            if st.session_state.userhealth <= 0:
                st.session_state.userhealth = 0
                st.session_state.game_over = True
                st.session_state.message = (
                    "💀 GAME OVER! THE MONSTER DEFEATED YOU!"
                )

            st.rerun()

    # -------- BATTLE MESSAGE --------

    st.info(st.session_state.message)

    # -------- GAME OVER --------

    if st.session_state.game_over:

        if st.session_state.userhealth > 0:
            st.balloons()
            st.markdown(
                """
                <div class="fire">🔥👑🔥</div>
                <h1>YOU ARE THE JUNGLE KING!</h1>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<h1 style='color:red;'>💀 GAME OVER 💀</h1>",
                unsafe_allow_html=True
            )

        st.subheader(f"🪙 FINAL COINS: {st.session_state.coins}")

# ---------------- RESTART ----------------

if st.button("🔄 RESTART GAME"):

    for key, value in defaults.items():
        st.session_state[key] = value

    st.rerun()
