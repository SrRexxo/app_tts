import streamlit as st
import os
import time
import glob
import os
from gtts import gTTS
from PIL import Image
import base64

st.title("Conversión de Texto a Audio")
image = Image.open('pastor.jpg')
st.image(image, width=350)
with st.sidebar:
    st.subheader("Esrcibe y/o selecciona texto para ser escuchado.")


try:
    os.mkdir("temp")
except:
    pass

st.subheader("El pastorcito mentiroso")
st.write(' Un joven pastor, encargado de cuidar un rebaño de ovejas, disfrutaba jugando bromas a los aldeanos.  '  
         ' Varias veces gritó a voz en cuello "¡Lobo, lobo!", haciendo creer a los habitantes del pueblo que un feroz lobo amenazaba a sus ovejas. ' 
         ' Al ver que nadie acudía en su ayuda, los aldeanos, cansados de sus mentiras, dejaron de creerle. '  
         ' Sin embargo, un día, el lobo apareció de verdad y atacó al rebaño. ' 
         ' Pero esta vez nadie acudió al rescate del pastorcito, quien se quedó sin sus ovejas y aprendió una valiosa lección sobre la importancia de la honestidad. '        
        )
           
st.markdown("Puedes escuchar el anterior texto, o cualquiera que quieras, solo pega el texto en la parte de abajo")
text = st.text_area("Ingrese El texto a escuchar.")

tld='com'
option_lang = st.selectbox(
    "Selecciona el acento con el cual quieres escuchar tu audio",
    ("Español", "Ingles", "Frances", "Aleman"))
if option_lang=="Español" :
    lg='es'
if option_lang=="Ingles" :
    lg='en'
if option_lang=="Frances" :
    lg='fr'
if option_lang=="Aleman" :
    lg='de'

def text_to_speech(text, tld,lg):
    lang=lg
    tts = gTTS(text,lang=lg) # tts = gTTS(text,'en', tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


#display_output_text = st.checkbox("Verifica el texto")

if st.button("convertir a Audio"):
     result, output_text = text_to_speech(text, 'com',lg)#'tld
     audio_file = open(f"temp/{result}.mp3", "rb")
     audio_bytes = audio_file.read()
     st.markdown(f"## Tú audio:")
     st.audio(audio_bytes, format="audio/mp3", start_time=0)

     #if display_output_text:
     
     #st.write(f" {output_text}")
    
#if st.button("ElevenLAabs",key=2):
#     from elevenlabs import play
#     from elevenlabs.client import ElevenLabs
#     client = ElevenLabs(api_key="a71bb432d643bbf80986c0cf0970d91a", # Defaults to ELEVEN_API_KEY)
#     audio = client.generate(text=f" {output_text}",voice="Rachel",model="eleven_multilingual_v1")
#     audio_file = open(f"temp/{audio}.mp3", "rb")

     with open(f"temp/{result}.mp3", "rb") as f:
         data = f.read()

     def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href
     st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)
