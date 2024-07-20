import streamlit as st
from typing import Generator
from textblob import TextBlob
from groq import Groq
import os

# port = int(os.environ.get('PORT',8501))

st.set_page_config(page_icon="🏥", layout="wide", page_title="Virtual Doc!")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(f'<span style="font-size: 78px; line-height: 1">{emoji}</span>', unsafe_allow_html=True)

icon("🧑‍⚕️")
st.subheader("Your Personal Doctor", divider="rainbow", anchor=False)

client = Groq(
    api_key='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',
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

def analyze_mood(text):
    analysis = TextBlob(text)
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if "real_time_support_input" not in st.session_state:
    st.session_state.real_time_support_input = ""

st.header("Welcome to the AI-Powered Mental Health Companion!")
st.write("Track your mood, get personalized mindfulness exercises, and receive real-time emotional support.")

chat_input = st.text_area("Talk to the AI", value=st.session_state.real_time_support_input, key="real_time_support_input")

if st.button("Get Response"):
    if chat_input:
        st.session_state.messages.append({"role": "user", "content": chat_input})
        with st.chat_message("user", avatar='🧑‍⚕️'):
            st.markdown(chat_input)

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
                    {"role": "user", "content": chat_input}
                ],
                max_tokens=1028,
                stream=True
            )

            with st.chat_message("assistant", avatar="🤖"):
                chat_responses_generator = generate_chat_responses(chat_completion)
                full_response = st.write_stream(chat_responses_generator)
                mood_analysis = analyze_mood(chat_input)
                st.write("Mood Analysis:", mood_analysis)
        except Exception as e:
            st.error(e, icon="🚨")

        if isinstance(full_response, str):
            st.session_state.messages.append({"role": "doctor", "content": full_response})
        else:
            combined_response = "\n".join(str(item) for item in full_response)
            st.session_state.messages.append({"role": "doctor", "content": combined_response})


# if __name__ == '__main__':
#     st.run(port=port)