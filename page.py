import streamlit as st
import pickle
import speech_recognition as sr
from google import genai
import io

# Get API key from Streamlit secrets
API_KEY = st.secrets["API_KEY"]  # Retrieve API_KEY from Streamlit Secrets

st.title("🧑‍💻 Online DataMentor🚀")
st.write("This application analyzes the most frequently used words in data science job application texts using the DataMentor model and helps you map out your career path.")

# Get user input
user_input = st.text_area("📌 Describe your experience in data science :)")

# 🎤 Record Audio
st.write("🎙️ Click the button below to speak and input your voice.")
audio_input = st.audio_input("Click here to start recording")

# Process the audio input if available
if audio_input:
    st.write("✅ Your voice has been recorded.")
    
    # Convert audio input to bytes for processing
    audio_bytes = io.BytesIO(audio_input.getvalue())
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_bytes) as source:
            audio = recognizer.record(source)  # Listen to the recorded audio
        
        # Convert speech to text using Google API
        text_from_speech = recognizer.recognize_google(audio, language="en-US")
        st.success(f"🎤 Speech converted to text: {text_from_speech}")
        user_input += " " + text_from_speech  # Append speech text to input
    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio, please try again.")
    except sr.RequestError:
        st.error("⚠️ Could not connect to Google API, check your internet connection.")

# Ensure user input before running the model
if st.button("🔍 Generate My Career Plan"):
    if not user_input:
        st.warning("⚠️ Please enter information about yourself!")
    else:
        with open("data-mentor.pkl", "rb") as file:
            topic_model = pickle.load(file)

        topic_0_words = [word[0] for word in topic_model.get_topic(1)[:20]]

        prompt = f"""
        📊 Most common data science terms in job postings:
        {', '.join(topic_0_words)}

        🏆 My skills and experiences: {user_input}

        💡 Based on this information, can you generate a detailed **Data Scientist career path** for me? 
        """

        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )

        st.subheader("📌 Online DataMentor Recommendations:")
        st.write(response.text)
