questions=[
["1. Which animal is known as the 'Ship of the Desert?","camel","dog","cat","reticulated pyhton",1],
["2. Which animal is known as the 'Ship of the Desert?","camel","dog","cat","reticulated pyhton",1],
["3. Which animal is known as the 'Ship of the Desert?","camel","dog","cat","reticulated pyhton",1],
["4. Which animal is known as the 'Ship of the Desert?","camel","dog","cat","reticulated pyhton",1],
["5. Which animal is known as the 'Ship of the Desert?","camel","dog","cat","reticulated pyhton",1],
["6. Which animal is known as the 'Ship of the Desert?","camel","dog","cat","reticulated pyhton",1],
["7. Which animal is known as the 'Ship of the Desert?","camel","dog","cat","reticulated pyhton",1],
]
levels=[1000,2000,3000,4000,5000,10000,25000]
money=0
for i in range(0,len(questions)):
    question=questions[i]
    print(f"Question for Rs.{levels[i]}")
    print(f"{question[0]}")
    print(f"a.{question[1]}     b.{question[2]}")
    print(f"c.{question[3]}       d.{question[4]}")
    reply=int(input("Enter your answer(1-4) or 0 to quit:\n"))
    if reply==question[5]:
        print(f"correct answer, You have won {levels[i]}\n\n")
        if i==0:
            money=1000
        elif i==1:
            money=2000
        elif i==2:
            money=3000
        elif i==3:
            money=4000
        elif i==4:
            money=5000
        elif i==5:
            money=10000
        elif i==6:
            money=25000        
    else:
        print("Wrong answer!")
        break
print(f"Your take home money is Rs. {money}")






