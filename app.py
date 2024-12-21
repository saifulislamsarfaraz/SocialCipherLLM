import streamlit as st
import speech_recognition as sr
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

# Title of the application with styling
st.markdown("""
    <style>
        .title {text-align: center; font-size: 36px; color: #00796b; font-family: 'Arial';}
        .instructions {text-align: center; font-size: 18px; color: #004d40;}
        .section {margin-bottom: 30px;}
        .button-style {background-color: #00796b; color: white; padding: 10px 20px; font-size: 16px; border-radius: 5px;}
        .response-box {background-color: #e0f2f1; padding: 10px; border-radius: 8px;}
        .error-box {background-color: #ffccbc; padding: 10px; border-radius: 8px;}
        .speech-icon {font-size: 24px; color: #00796b;}
        .custom-input {font-size: 18px; padding: 10px; border-radius: 8px; border: 1px solid #00796b;}
    </style>
    <h1 class="title">Cipher Expert Assistant</h1>
    <p class="instructions">Choose your input method (Text or Voice) to interact with the cipher transformation expert. Speak or type your message and get the transformed result.</p>
""", unsafe_allow_html=True)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         "You are a text cipher expert. You have the following cipher techniques at your disposal:\n"
         "1. Substitution Cipher\n"
         "2. Tweaked Language\n"
         "3. Gesture Ciphering\n"
         "4. Digital Encoding\n"
         "5. Code Words\n"
         "6. Professional Jargon\n"
         "7. Community-Specific Language\n"
         "8. Reverse Words\n"
         "9. Poetic Construction\n"
         "10. Language Switching\n\n"
         "For the given message (either plaintext or ciphertext) and cipher method, apply the following rule:\n"
         "- If the input is plaintext, generate the corresponding ciphertext using the specified cipher method.\n"
         "- If the input is ciphertext, decipher it back to the original message using the appropriate cipher logic.\n\n"
         "The input will consist of a plaintext or ciphertext followed by the specified cipher technique.\n"
         "Based on the cipher technique, perform the appropriate transformation.\n\n"
         "Provide the transformed text based on the input. For example:\n"
         "Substitution Cipher: 'Price: 430 BDT' → 'PCQ'\n"
         "Tweaked Language: 'Fish is expensive in the market.' → 'Fitatsh tisit expitasive itinat the titmarket.'\n"
         "Gesture Ciphering: 'This customer is lying.' → '[Eye wink + hand clap]'\n"
         "Digital Encoding: 'PIN: 1234' → 'Lbe Nipdrac'\n"
         "Code Words: 'Customer is just browsing.' → 'Hajano'\n"
         "Professional Jargon: 'The shoe's longevity is six months.' → 'Deg Mas'\n"
         "Community-Specific Language: 'This client is rude.' → 'Shidari namja dhaka korchish kya'\n"
         "Reverse Words: 'I love you' → 'Uoy evol I'\n"
         "Poetic Construction: 'Appointment at 5 PM' → 'A Bee Is Humming, 5 Birds Singing'\n"
         "Language Switching: 'Please pay attention.' → 'দয়া করে মনোযোগ দিন'\n"
         "\nNow, based on the user's input, perform the transformation accordingly."
        ),
        ("user", "Question: {question}")
    ]
)

# Initialize Ollama with the model
llm = Ollama(model="llama3.2")

# Function to capture speech and convert to text
def capture_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
        try:
            st.info("Recognizing...")
            speech_text = recognizer.recognize_google(audio)  # Use Google's speech recognition
            return speech_text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

# Interactive section for choosing input type
input_type = st.radio("Choose your input method:", ("Text", "Voice"), index=0, key="input_method")

if input_type == "Voice":
    # Voice Input Section
    st.markdown("<div class='section'></div>", unsafe_allow_html=True)  # Spacing between sections
    if st.button("🔊 Start Speaking", key="speak_button"):
        speech_input = capture_speech()
        
        if speech_input:
            st.subheader("Your Voice Input:")
            st.markdown(f"<div class='response-box'>{speech_input}</div>", unsafe_allow_html=True)

            # Process the speech input with the existing prompt chain
            try:
                # Chain the prompt and LLM
                chain = prompt | llm

                # Invoke the chain with the user's speech input
                response = chain.invoke({"question": speech_input})

                # Display the response
                st.subheader("Cipher Result:")
                st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"<div class='error-box'>Error: {str(e)}</div>", unsafe_allow_html=True)

elif input_type == "Text":
    # Text Input Section
    st.markdown("<div class='section'></div>", unsafe_allow_html=True)  # Spacing between sections
    question = st.text_input(
        "Enter your message:", 
        key="text_input", 
        help="Type the message and choose a cipher transformation."
    )

    if question:
        st.markdown("<div class='section'></div>", unsafe_allow_html=True)  
        with st.spinner("Processing... Please wait!"):

            try:
                chain = prompt | llm

                response = chain.invoke({"question": question})

                # Display the response
                st.subheader("Cipher Result:")
                st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"<div class='error-box'>Error: {str(e)}</div>", unsafe_allow_html=True)
