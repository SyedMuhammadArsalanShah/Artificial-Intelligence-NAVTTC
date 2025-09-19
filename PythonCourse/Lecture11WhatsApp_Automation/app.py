import streamlit as st

import pandas as pd  
import pywhatkit as kit
import time
import pyautogui



st.set_page_config(page_title="Whatsapp Sender Automation",page_icon="📱📱")
st.title("Whatsapp Automation system ")
st.write("upload karen apni excel file ")


upload=st.file_uploader("Upload Excel File ", type=["xlsx"])


portfolio =st.text_input("Enter Your Portfolio Link ", "https://syedmuhammadarsalanshah.vercel.app/")
customMessage  =st.text_area("Enter Your Message Here ", "Follow me On github ")

if  upload is not None:
    df=pd.read_excel(upload)
    st.write("Contact Upload hogaye ")
    st.dataframe(df)
    if st.button("Send Message"):
        
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
