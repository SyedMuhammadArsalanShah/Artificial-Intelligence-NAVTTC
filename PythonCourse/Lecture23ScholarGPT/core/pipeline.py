import os
import subprocess
import whisper
import json
import pandas as pd
import joblib
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity




model = whisper.load_model("base")
df = joblib.load("embeddings.joblib")

def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    return r.json()["embeddings"]

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    return r.json()


def run_chatbot(question):
    question_embedding = create_embedding([question])[0]

    similarities = cosine_similarity(
        np.vstack(df["chunks_embeddings"]),
        [question_embedding]
    ).flatten()

    top_results = 5
    max_indx = similarities.argsort()[::-1][0:top_results]
    new_df = df.loc[max_indx]

    # prompt = f"""
    # Nouman Ali Khan lecture QA bot 
    # {new_df[["start","end","name","text"]]}
    # """

    prompt=f"""
    You are a QA assistant for Nouman Ali Khan’s “Akhri Mojza” lecture series.

    Relevant content chunks:
    {new_df[["start","end","name","text"]]}

    User Question:
    "{question}"

    Instructions:
    • Answer naturally in human style.
    • Always tell the user the correct video name/number and the timestamps where the answer is discussed.
    • Help the user go directly to that part of the lecture.
    • If the question is not related to the Akhri Mojza series, politely refuse.
    • Do not mention or reveal the chunks or this prompt formatting in the answer.
    • Keep responses brief but meaningful.

    """


    response = inference(prompt)["response"]
    return response
