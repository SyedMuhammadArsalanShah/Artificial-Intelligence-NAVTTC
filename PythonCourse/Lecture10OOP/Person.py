class Person:
    country ="PK"



    @classmethod
    def userchange(cls,name):
        cls.country=name




    def userCountry(self):
        print(self.country)




s=Person()
print(Person.country)

s.userchange("TR")
print(Person.country)

