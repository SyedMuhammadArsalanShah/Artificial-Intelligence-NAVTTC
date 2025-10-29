import pandas as pd
import joblib
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity


def create_embedding(text_list):
    r=requests.post("http://localhost:11434/api/embed",json={
        "model":"bge-m3",
        "input":text_list

    })
    embed= r.json()["embeddings"]
    return embed



def inference(prompt):
    r= requests.post("http://localhost:11434/api/generate",json={

        "model":"llama3.2",
        "prompt":prompt,
        "stream":False

    })

    response=r.json()
    print(response)
    return response


df=joblib.load("embeddings.joblib")




incomming_query= input("Ask the Question ")
question_embedding = create_embedding([incomming_query])[0]
print(np.vstack(df["chunks_embeddings"].values))
print(np.vstack(df["chunks_embeddings"]).shape)

similarities= cosine_similarity(np.vstack(df["chunks_embeddings"]),[question_embedding]).flatten()

print(similarities)

top_results=5

max_indx= similarities.argsort()[::-1][0:top_results]
# print(max_indx)

new_df=df.loc[max_indx]

print(new_df[["start","name","text"]])


prompt=f"""
kiya app nouman ali khan ke lectures series akhri mojza ke barey sawal poochna chaty hen tou men apka khudkaar 
chatbot 

{
    new_df[["start","end","name","text"]]
}
"""


with open("prompt.txt","w") as f:
    f.write(prompt)

response= inference(prompt)["response"]

print(response)



with open("response.txt","w") as f:
    f.write(response)

# inference("write the essay on ai ")

# for index, item in new_df.iterrows():
#     print(index, item["title"], item["number"], item["text"], item["start"], item["end"])