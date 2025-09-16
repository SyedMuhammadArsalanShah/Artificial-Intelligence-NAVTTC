print("*"*8)
print("Sign Up")

userName= input("Enter Your Name ")
userEmail= input("Enter Your Email ")
userPass= input("Enter Your  Password ")
userContact= input("Enter Your Contact ")
print("Account Successfully created")


userEmailLogin= input("Enter Your Email ")
userPassLogin= input("Enter Your  Password ")


if userEmail==userEmailLogin and userPass== userPassLogin:
    print("Welcome In MITI ",userName )
else:
    print("Incorrect Email or Password ")
    
