import whisper
import json
import os 

model=whisper.load_model("base")
audios=os.listdir("audio")

print(audios)

for audio_file in audios:
    if("_" in audio_file):
        number=audio_file.split("_")[0]
        name=audio_file.split("_")[1]
        print(number, name)
        result=model.transcribe(audio=f"audio/{audio_file}",
                                language="ur",
                                task="translate",
                                word_timestamps=False)
        
        print(result)
        chunks=[]
        for segment in result["segments"]:
            chunks.append({"number":number,
                           "name":name,
                           "start":segment["start"],
                           "end":segment["end"],
                           "text":segment["text"]})
        chunks_with_all_meta_data={"chunks":chunks,"text":result["text"]}
        

        with open(f"jsons/{audio_file}.json","w") as f:
            json.dump(chunks_with_all_meta_data,f)