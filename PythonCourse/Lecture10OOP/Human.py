class Human :
    brain=True
    eyes=True

    
    def speak(self):
        print("Speak")



class Male(Human):

    beard=True

ali=Male()
print(ali.eyes)


