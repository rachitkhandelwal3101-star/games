
import streamlit as st
import random

st.title("🌴 Jungle Battle Game")
st.write("⚔️ Defeat both monsters to become the Jungle King!")

if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.userhealth = 100
    st.session_state.monsterhealth = 100
    st.session_state.monster2health = 100
    st.session_state.coins = 0
    st.session_state.level = 1
    st.session_state.game_over = False

name = st.text_input("Enter your name")

if st.button("🚀 Start Game"):
    st.session_state.started = True
    st.session_state.userhealth = 100
    st.session_state.monsterhealth = 100
    st.session_state.monster2health = 100
    st.session_state.coins = random.randint(0, 3)
    st.session_state.level = 1
    st.session_state.game_over = False
    st.rerun()

if st.session_state.started:

    st.subheader(f"Welcome {name}!")

    st.write(f"🪙 Coins: {st.session_state.coins}")
    st.write(f"❤️ Your health: {st.session_state.userhealth}")

    if st.session_state.level == 1:
        st.subheader("👹 Monster 1")
        st.write(f"Monster health: {st.session_state.monsterhealth}")
        st.progress(max(0, st.session_state.monsterhealth) / 100)

    elif st.session_state.level == 2:
        st.subheader("🐉 Monster 2")
        st.write(f"Monster health: {st.session_state.monster2health}")
        st.progress(max(0, st.session_state.monster2health) / 100)

    st.progress(max(0, st.session_state.userhealth) / 150)

    if not st.session_state.game_over:

        user = st.slider("Choose your attack power", 0, 50, 20)

        if st.button("⚔️ ATTACK"):

            if st.session_state.level == 1:

                st.session_state.monsterhealth -= user

                if st.session_state.monsterhealth <= 0:
                    st.session_state.monsterhealth = 0
                    st.session_state.coins += 5
                    st.session_state.userhealth += 50
                    st.session_state.level = 2
                    st.success("🏆 You defeated Monster 1! +50 health and 5 coins!")

                else:
                    monster_attack = random.randint(0, 100)
                    st.session_state.userhealth -= monster_attack
                    st.warning(f"Monster 1 attacked for {monster_attack} damage!")

            elif st.session_state.level == 2:

                st.session_state.monster2health -= user

                if st.session_state.monster2health <= 0:
                    st.session_state.monster2health = 0
                    st.session_state.game_over = True
                    st.session_state.coins += 10
                    st.balloons()
                    st.success("🎉 YOU DEFEATED MONSTER 2! YOU WON!")

                else:
                    monster_attack = random.randint(0, 30)
                    st.session_state.userhealth -= monster_attack
                    st.warning(f"Monster 2 attacked for {monster_attack} damage!")

            if st.session_state.userhealth <= 0:
                st.session_state.userhealth = 0
                st.session_state.game_over = True
                st.error("💀 GAME OVER! The monster defeated you!")

            st.rerun()

    if st.session_state.game_over:
        if st.session_state.userhealth > 0:
            st.success("👑 Jungle Champion!")
        else:
            st.error("Better luck next time!")

        st.write(f"Final coins: {st.session_state.coins}")

if st.button("🔄 Restart Game"):
    st.session_state.started = False
    st.session_state.userhealth = 100
    st.session_state.monsterhealth = 100
    st.session_state.monster2health = 100
    st.session_state.coins = 0
    st.session_state.level = 1
    st.session_state.game_over = False
    st.rerun()
