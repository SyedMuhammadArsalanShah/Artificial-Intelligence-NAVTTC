print([])

students=["Ansaar","Usman", "KaleemUllah", "LAiba", "NAwaira"]
print(students)
print(students[3])

students[3]="Laiba Jawaid"
print(students)

students.sort()
print(students)
students.reverse()
print(students)

students.append("Ayesha")
print(students)
students.insert(1,"Fatimah")
print(students)
students.pop(1)
print(students)

students.remove("Ayesha")
print(students)
print(students.count("Usman"))
students.clear()
print(students)


a={}
print(type(a))

a=set()
print(type(a))

a={1,2,3,56,78,90,90}
print(a)

a.add(100)
a.add((100,78,90))

print(a)

a.pop()
print(a)
a.pop()
print(a)

a.remove(56)
print(a)


a=()

print(type(a))


a=("Usman", "Nawaira", "Laiba", "KaleemUllah", "Ansaar")

print(a)
print(a[1])
print(a.index("Usman"))
print(a.count("Laiba"))



a={
"name":"SMAS",
"age":00,
"FastFood":False,
"Hobbies":["a","b", "c"],
"education":{

    "DS":2025,
    "IT":2026,
    "BS":2027,
}
}

print(a)
print(a["name"])
print(a["Hobbies"])
print(a["education"]["DS"])
print(a.keys())
print(a.values())
print(a.items())
# print(a["Height"])
print(a.get("Height"))
print(a.get("name"))



oxfordDictionary={
"qalam":"pen",
"kitab":"book",
"smas":"kaam bht zayada dety bhai soch samjh kr join karen "


}

print("Check Your Words in world famous dictionary",
      list(oxfordDictionary.keys()))


search=input("Enter Your Word")
print(oxfordDictionary.get(search))
