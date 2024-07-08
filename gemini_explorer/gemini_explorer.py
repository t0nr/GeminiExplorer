import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.language_models import TextGenerationModel, Part, Content, ChatSession


project = "gemini-explorer"
vertexai.init(project=project, location="us-central1")

config = generative_models.GenerationConfig(
  temperature=0.4
)

model = generative_models.GenerativeModel(
  "Gemini-pro",
  generation_config=config
)

chat = model.start_chat()

def llm_function(chat: ChatSession, query):
  response = chat.send_message(query)
  output = response.condidates[0].content.parts[0].text

  with st.chat_message("model"):
    st.markdown(output)

  st.session_state.messages.append(
    {
      "role": "user",
      "content": query
    }
  )
  st.session_state.messages.append(
    {
      "role": "model",
      "content": output
    }
  )


st.title("gemini_explorer")

#Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = []

#Display and load to chat history
for index, message in enumerate(st.session_state.messages):
  content = Content(
    role = message["role"],
    parts = [Part.from_text(message["content"])]
  )

  if index != 0:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  chat.history.append(content)

user_name = st.text_input("Please enter your name")

if len(st.session_state.messages) == 0:
    if len(st.session_state.messages) == 0:
      if user_name:
        initial_prompt = f"Hey {user_name}! I'm ReX, an assistant powered by Google Gemini. Let's have some interactive conversations! 🤖✨"
      else:
        initial_prompt = "Hey there! I'm ReX, an assistant powered by Google Gemini. Let's have some interactive conversations! 🤖✨"
    llm_function(chat, initial_prompt)


query = st.chat_input("Gemini Explorer")

if query:
  with st.chat_message("user"):
    st.markdown(query)
  llm_function(chat, query)















