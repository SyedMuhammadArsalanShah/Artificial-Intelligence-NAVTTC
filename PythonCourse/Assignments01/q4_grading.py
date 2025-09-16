# Q4: Grade calculation
print("Program Marksheet ")
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