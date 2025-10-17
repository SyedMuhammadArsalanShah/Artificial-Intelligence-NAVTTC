import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense , Flatten , Input 
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

import numpy as np
import streamlit as st
from PIL import Image , ImageOps
# for canvas
from streamlit_drawable_canvas import st_canvas

st.set_page_config("MNIST DIGITS")
st.title("MNIST DIGITS DETECTOR")

@st.cache_resource
def train_Model():
    (x_train,y_train), (x_test , y_test)= mnist.load_data()
    x_train= x_train/255.0
    x_test= x_test/255.0
    y_train=to_categorical(y_train,10)
    y_test=to_categorical(y_test,10)
    model=Sequential([
     Input(shape=(28,28)),
    Flatten(),
    Dense(128,activation="relu"),
    Dense(10,activation="softmax")
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy",metrics=['accuracy'])
    model.fit(x_train,y_train, epochs=5,batch_size=32)
    test_loss, test_acc =model.evaluate(x_test, y_test)
    # print(f"Testing Accuracy{test_acc:.2f}")
    st.sidebar.success(f"Testing Accuracy{test_acc:.2f}")
    return model

model=train_Model()



# frontend



st.sidebar.header("Select An Option")

option=st.sidebar.radio("Select Input Mode", ["Draw a Number","Upload an Image"])


if option == "Draw a Number":
    st.write("Select a Number B/W 0-9")
    canvas_result= st_canvas(fill_color="#0000",stroke_width=15,stroke_color="#ffff", background_color="#00000",height=300, width=300,drawing_mode="freedraw",key="canvas")
    if canvas_result.image_data is not None:
        img=Image.fromarray((canvas_result.image_data[:,:,0]).astype(np.uint8))
        img=img.resize((28,28)).convert("L")
        img_array=np.array(img).reshape(1,28,28)/255
        if st.button("predicts"):
            prediction=model.predict(img_array)
            pred_class= np.argmax(prediction)
            st.success(f"Predicted Digit Is {pred_class}")
            st.bar_chart(prediction[0])
elif option == "Upload an Image":
    upload_file=st.file_uploader("Select image", type=["png", "jpg", "jpeg"])
    if upload_file is not None:
        image=Image.open(upload_file).convert("L")
        st.image(image, caption="img uploaded")
        img=ImageOps.invert(image.resize((28,28)))
        img_array=np.array(img).reshape(1,28,28)/255
        if st.button("predicts"):
            prediction=model.predict(img_array)
            pred_class= np.argmax(prediction)
            st.success(f"Predicted Digit Is {pred_class}")
            st.bar_chart(prediction[0])

st.markdown("# Developed BY DS Students")