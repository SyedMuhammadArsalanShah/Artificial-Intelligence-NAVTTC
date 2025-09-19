import pandas as pd  
import pywhatkit as kit
import time
import pyautogui



df=pd.read_excel("PhoneBook.xlsx")


portfolio="https://syedmuhammadarsalanshah.vercel.app/"

customMessage="""

follow me on github and linkedin 


"""



for index,row in df.iterrows():
    phoneNumber=f"+{row["Phone"]}"
    message =f"{customMessage} {portfolio}"

    try:



        kit.sendwhatmsg_instantly(phoneNumber,message,wait_time=35)
        time.sleep(10)
        pyautogui.press("enter")
        print("sent ")
        time.sleep(5)
        pyautogui.press("enter")


    except Exception as e:
        print(" number not send ")
