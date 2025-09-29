import requests
import  streamlit as st 



st.set_page_config("Mushaf Web", page_icon="📖")

st.title("Mushaf Web APP")

st.sidebar.title("Controls")



surah_list=requests.get("http://api.alquran.cloud/v1/surah").json()["data"]
surah_names=[f"{s['number']}.{s['name']}.{s['englishName']}" for s in surah_list]


selected_surahs_name=st.sidebar.selectbox("choose a surah",surah_names)
surah_name_int= int(selected_surahs_name.split(".")[0])
st.write(surah_name_int)

search_keyword=st.sidebar.text_input("Search By Arabic Ayah")

showTr= st.sidebar.checkbox("Show Translation")
showRec= st.sidebar.checkbox("Show Audio")

selected_tr_choice=st.sidebar.selectbox("choose a surah",["ur.maududi","ur.junagarhi","ur.jalandhry"])



recitation_url=f"https://api.alquran.cloud/v1/surah/{surah_name_int}/ar.alafasy"

rec_Resp=requests.get(recitation_url).json()
arabic_ayah=rec_Resp["data"]["ayahs"]



if showTr:
    tr_recitation_url=f"https://api.alquran.cloud/v1/surah/{surah_name_int}/{selected_tr_choice}"

    tr_rec_Resp=requests.get(tr_recitation_url).json()
    tr_ayah=tr_rec_Resp["data"]["ayahs"]
else:
    tr_ayah=[None]*len(arabic_ayah)





if search_keyword.strip():
    filter_ar=[]
    filter_tr=[]
    for i , ayah in enumerate(arabic_ayah):
        if search_keyword in ayah["text"]:
            filter_ar.append(ayah)    
            filter_tr.append(tr_ayah[i])

    arabic_ayah=filter_ar    
    tr_ayah=filter_tr    


st.subheader(selected_surahs_name)


for i ,ayah in enumerate(arabic_ayah):
    st.markdown(f"**{ayah["numberInSurah"]}** | {ayah["text"]}")

    if showRec:
        if 'audio' in ayah and ayah["audio"]:
            st.audio(ayah["audio"])

    if showTr and tr_ayah[i]:
        st.info(tr_ayah[i]["text"])


st.markdown("##Developed By SMAS")