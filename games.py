import random
userhealth=100
monsterhealth=100
monster2health=100
name=input("enter your name")
print(f"hi {name} welcome to your jungle")
import random
c=random.randint(0,3)
coins=c
import random
v=random.randint(0,100)
userhealth=userhealth-v
user=int(input("enter the attack"))
monsterhealth=monsterhealth-user
if userhealth<=0:
    print("you loose by monster1")
elif monsterhealth<=0:
    print(" you won congratulation from monster1")
    userhealth=userhealth+50
    user1=int(input("enter attack for second monnster"))
    monster2=random.randint(0,30)
    userhealth=userhealth-monster2
    monster2health=monster2health-user1
elif monster2health<=0:
    print("monster loose")
else:
    print("🎉you won")