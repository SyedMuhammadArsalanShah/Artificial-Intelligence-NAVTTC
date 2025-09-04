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

    print("Program 01 Marksheet ")
    eng=float(input("Enter Your English Marks"))
    urdu=float(input("Enter Your Urdu Marks"))
    math=float(input("Enter Your Math Marks"))

    obtained=eng+urdu+math
    meriPercemtage=obtained/300*100
    print("Obatined Marks ", obtained)
    print("Percentage ", meriPercemtage)
    if meriPercemtage<=100 and meriPercemtage>=80:
        print("Grade A1 MashaAllah ")
    elif meriPercemtage<=79 and meriPercemtage>=70:
        print("Grade A ")
    elif meriPercemtage<=69 and meriPercemtage>=60:
        print("Grade B ")
    elif meriPercemtage<=59 and meriPercemtage>=50:
        print("Grade C ")
    elif meriPercemtage<=49 and meriPercemtage>=40:
        print("Grade D  ")
    elif meriPercemtage<=39 and meriPercemtage>=30:
        print("Grade F ")
    else:
        print("Try Again")

    
    print("Program No 02 EVEN / ODD")

    num=int(input("Enter Your Number "))
    if num%2==0:
        print("Even ",num)
    else:
        print("Odd", num)
    print("Program No 03 LEAP YEAR ")

    year=int(input("Enter Your Year "))
    if year%4==0:
        print("Leap Year ", year)
    else:
        print("Not a Leap Year",year)


    print("Program No 04 POS/ NEG")
    num1=int(input("Enter Your number "))
    if num1 <0:
        print("negative")
    else:
        print("positive",num1)

    print("Positive") if num1<0 else print("Negative")


else:
    print("Incorrect Email or Password ")
    