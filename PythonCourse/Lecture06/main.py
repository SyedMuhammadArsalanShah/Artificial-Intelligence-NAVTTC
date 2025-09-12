a=1

while(a<=10):
    print(a)
    # a=a+1
    a+=1




while True:
    username=input("Enter Your Name ")
    if username == "admin":
        print("Student Name ",username)
        break
    else:
        print("Student Name ",username)


total_bill=0

while True:
    p_name=input("Enter Your Product name")
    products=float(input("Enter Your Product Price "))
    if p_name == "counter_closed": 
        print("Allah Hafiz - Bhai kal ana ")
        break
    else:
        print(p_name,products)
        total_bill+=products

print("Final Bill ", total_bill)