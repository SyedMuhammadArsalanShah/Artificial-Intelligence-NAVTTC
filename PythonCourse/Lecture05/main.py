




# for  a in range(90,100,2):
#     print("Index",a)


for a in range(100):
    if a % 2==0:
        print("Even ",a)
    else:
        print("Odd ",a)


num =int(input("Enter Your Number"))
merafactorial=1
for b in range(1,num+1):
    merafactorial*=b
print("Factorial is ",merafactorial)