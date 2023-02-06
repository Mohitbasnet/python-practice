user_input=input("Enter your password:\n")
password="hello"
while user_input != password:
    print("Incorrect password")
    user_input=input("Enter your password:\n")

if password == "hello":
    print("Unlocked")