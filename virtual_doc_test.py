import streamlit as st
from typing import Generator
from textblob import TextBlob
from groq import Groq

st.set_page_config(page_icon="🏥", layout="wide", page_title="Virtual Doc!")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

icon("🧑‍⚕️")
st.subheader("Your Personal Doctor")

client = Groq(
    api_key='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',
)

if "messages" not in st.session_state:
    st.session_state.messages = []

def analyze_mood(text):
    analysis = TextBlob(text)
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

st.header("Welcome to the AI-Powered Mental Health Companion!")
st.write("Track your mood, get personalized mindfulness exercises, and receive real-time emotional support.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Real-time chat input
if prompt := st.chat_input("Talk to the AI"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        chat_completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": "You are a virtual doctor named DocOuc. Your role is to diagnose and provide medical advice to patients while asking as few questions as possible. Your approach should be friendly, empathetic, and supportive, offering not only medical insights but also emotional and moral support. Engage with the patient in a kind and understanding manner, making them feel comfortable and cared for. Aim to build trust and provide reassurance throughout the conversation."
                },
                {
                    "role": "assistant",
                    "content": "Hello there! I'm DocOuc, your virtual doctor friend. It's wonderful to meet you! I'm here to listen, understand, and help you with any health concerns you may have. Please know that everything discussed in this chat is completely confidential and judgement-free. You're in a safe space now.\n\nWhat brings you to my virtual clinic today? Is there something specific that's been bothering you lately, or do you just need some general guidance on how to take care of yourself?"
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1028,
            stream=True
        )

        # Display AI response
        with st.chat_message("assistant"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = ''.join(list(chat_responses_generator))
            st.markdown(full_response)
            mood_analysis = analyze_mood(prompt)
            st.write("Mood Analysis:", mood_analysis)

        st.session_state.messages.append({"role": "doctor", "content": full_response})
    except Exception as e:
        st.error(e, icon="🚨")
