
import random

userhealth = 100
monsterhealth = 100
monster2health = 100

name = input("Enter your name: ")
print(f"Hi {name}, welcome to your jungle!")

# Collect coins
coins = random.randint(0, 3)
print(f"You collected {coins} coins!")

# MONSTER 1 BATTLE
print("\n👹 MONSTER 1 APPEARED!")

while userhealth > 0 and monsterhealth > 0:

    user_attack = int(input("Enter your attack (0-30): "))

    if user_attack < 0 or user_attack > 30:
        print("Invalid attack! Choose between 0 and 30.")
        continue

    monsterhealth -= user_attack
    print("Monster 1 health:", monsterhealth)

    if monsterhealth <= 0:
        print("🎉 You defeated Monster 1!")
        break

    monster_attack = random.randint(0, 30)
    userhealth -= monster_attack

    print("Monster attacked you:", monster_attack)
    print("Your health:", userhealth)

if userhealth <= 0:
    print("☠ You lost! Monster 1 defeated you.")

else:
    # BONUS HEALTH
    userhealth += 50
    print("\n❤️ You received 50 bonus health!")
    print("Your health:", userhealth)

    # MONSTER 2 BATTLE
    print("\n🐉 MONSTER 2 APPEARED!")

    while userhealth > 0 and monster2health > 0:

        user_attack = int(input("Enter your attack (0-30): "))

        if user_attack < 0 or user_attack > 30:
            print("Invalid attack! Choose between 0 and 30.")
            continue

        monster2health -= user_attack
        print("Monster 2 health:", monster2health)

        if monster2health <= 0:
            print("🏆 CONGRATULATIONS! YOU WON THE GAME!")
            break

        monster_attack = random.randint(0, 30)
        userhealth -= monster_attack

        print("Monster 2 attacked you:", monster_attack)
        print("Your health:", userhealth)

    if userhealth <= 0:
        print("☠ Monster 2 defeated you!")
