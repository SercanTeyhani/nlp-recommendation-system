import streamlit as st
import pickle
import speech_recognition as sr
from google import genai

# Google Gemini API anahtarını ekleyin
API_KEY = "AIzaSyBSwmxxUWnwoAvABHzaGNTX_jftZpWGIh0"  # Kendi API anahtarınızı buraya koyun

st.title("🧑‍💻 Data Scientist Kariyer Planlayıcı 🚀")
st.write("Bu uygulama, BERTopic modeli ile veri bilimi alanında iş başvuru metinlerinde en sık kullanılan kelimeleri analiz eder ve kariyer yolunuzu çizmeye yardımcı olur.")

# Kullanıcıdan bilgi alın
user_input = st.text_area("📌 Veri Bilimi ile alakalı kendinizden bahsedin.")

# 🎤 Ses Kaydı Al
st.write("🎙️ Ses ile giriş yapmak için aşağıdaki butona basıp konuşabilirsiniz.")

if st.button("🎤 Ses Kaydı Başlat"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🔴 Kayıt başladı, konuşabilirsiniz...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        st.write("✅ Kayıt tamamlandı, metne dönüştürülüyor...")

    try:
        text_from_speech = recognizer.recognize_google(audio, language="tr-TR")
        st.success(f"📝 Ses Metne Dönüştü: {text_from_speech}")
        user_input += " " + text_from_speech  # Kullanıcı metnine ekle
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

        topic_0_words = [word[0] for word in topic_model.get_topic(0)[:20]]

        prompt = f"""
        📊 İş ilanlarında en çok geçen veri bilimi terimleri:
        {', '.join(topic_0_words)}

        🏆 Benim becerilerim ve deneyimlerim: {user_input}

        💡 Bu bilgiler doğrultusunda benim için detaylı bir **Data Scientist kariyer yolu** çizebilir misin? 
        """

        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        st.subheader("📌 Modelin Tavsiyeleri:")
        st.write(response.text)







