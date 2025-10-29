import requests
import os
import json 
import pandas as pd
import joblib

def create_embedding(text_list):
    r=requests.post("http://localhost:11434/api/embed",json={
        "model":"bge-m3",
        "input":text_list

    })
    embed= r.json()["embeddings"]
    return embed



jsons=os.listdir("jsons")
my_dict=[]
chunks_id=0
# outer loop
for json_file in jsons:
    with open(f"jsons/{json_file}") as f:
        contents=json.load(f)
    print("for creating embeds")
    embeddings=create_embedding([c["text"] for c in contents["chunks"]])
    for i , chunk in enumerate(contents["chunks"]):
        chunk["chunks_id"]=chunks_id
        chunk["chunks_embeddings"]=embeddings[i]

        chunks_id+=1

        my_dict.append(chunk)
print(my_dict)


# a= create_embedding(["sat", "cat"])

# print(a)


df= pd.DataFrame.from_records(my_dict)
print(df)


joblib.dump(df, "embeddings.joblib")



