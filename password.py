def main():
    password()
def password():
    user_input="Enter password\n"
    p="helo"
    while user_input!=p:
        user_input=input("Enter password\n")
        print("Incorrect password")
    if user_input==p:
        print("Unlocked")
main()
