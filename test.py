import streamlit as st
import pickle
import speech_recognition as sr
from google import genai
import io
import numpy as np

# Google Gemini API anahtarını ekleyin
API_KEY = "AIzaSyBSwmxxUWnwoAvABHzaGNTX_jftZpWGIh0"  # Kendi API anahtarınızı buraya koyun

st.title("🧑‍💻 Online DataMentor🚀")
st.write("Bu uygulama, DataMentor modeli ile veri bilimi alanında iş başvuru metinlerinde en sık kullanılan kelimeleri analiz eder ve kariyer yolunuzu çizmeye yardımcı olur.")

# Kullanıcıdan bilgi alın
user_input = st.text_area("📌 Veri Bilimi ile alakalı tecrübelerinizden bahsedin :)")

# 🎤 Ses Kaydı Al
st.write("🎙️ Ses ile giriş yapmak için aşağıdaki butona basıp konuşabilirsiniz.")
audio_input = st.audio_input("Ses kaydını başlatmak için buraya tıklayın")

# Eğer ses kaydı varsa, bunu işleyin
if audio_input:
    st.write("✅ Ses kaydınız alındı.")
    
    # Ses kaydını byte formatında almak ve işlemek
    audio_bytes = io.BytesIO(audio_input.getvalue())
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_bytes) as source:
            audio = recognizer.record(source)  # Ses kaydını dinle
        
        # Google API üzerinden metne dönüştürme
        text_from_speech = recognizer.recognize_google(audio, language="tr-TR")
        st.success(f"🎤 Ses metne dönüştürüldü: {text_from_speech}")
        user_input += " " + text_from_speech  # Ses kaydını metne ekle
    except sr.UnknownValueError:
        st.error("❌ Ses anlaşılamadı, lütfen tekrar deneyin.")
    except sr.RequestError:
        st.error("⚠️ Google API'ye bağlanılamadı, internet bağlantınızı kontrol edin.")

# Kullanıcı giriş yapmadan önce model çalışmaz
if st.button("🔍 Kariyer Planımı Oluştur"):
    if not user_input:
        st.warning("⚠️ Lütfen kendinizle ilgili bilgileri girin!")
    else:
        with open("bertopic_model.pkl", "rb") as file:
            topic_model = pickle.load(file)

        # Kullanıcı inputunun topic'lerini al
        topic_probs = topic_model.transform([user_input])[1]

        # En benzer topic'i bul
        most_similar_topic = np.argmax(topic_probs)
        
        # Terminalde hangi topic seçildiğini yazdır
        st.write(f"Seçilen Topic: {most_similar_topic}")
        print(f"Seçilen Topic: {most_similar_topic}")

        # Seçilen topic'in kelimelerini al
        topic_words = [word[0] for word in topic_model.get_topic(most_similar_topic)[:20]]

        prompt = f"""
        📊 İş ilanlarında en çok geçen veri bilimi terimleri:
        {', '.join(topic_words)}

        🏆 Benim becerilerim ve deneyimlerim: {user_input}

        💡 Bu bilgiler doğrultusunda benim için detaylı bir **Data Scientist kariyer yolu** çizebilir misin? 
        """

        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        st.subheader("📌 Online DataMentor Tavsiyeleri:")
        st.write(response.text)







