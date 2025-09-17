class Student:
    centerName="NAVTTC"

    # def __init__(self,name,course,age):
    #     self.name=name
    #     self.course=course
    #     self.age=age
    #     print("Student Name Is ",self.name,"Course is ", self.course,"age is", self.age)
        
    @staticmethod
    def userEnroll():
        print("user Has been Erolled")

    def information(self,name,course):
        self.fullname=name
        self.courseName=course
        print("Student Name Is ",self.fullname,"Course is ", self.courseName)




# object1=Student()
# print(object1.centerName)
# object1.information("Ayesha","DS")



# object2=Student()
# print(object2.centerName)
# object2.information("Aisha","AI")


# object3=Student("Laiba","GD","45")
# object4=Student("Aisha","DS","46")
# object5=Student("Nawaira","DS","50")



object=Student()
object.userEnroll()
