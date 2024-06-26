import streamlit as st 
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

import os
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

st.title("Chat with Groq!")
st.write("Hello! I am your friendly Groq chatbot. I can help answer your question, provide information or just chat. Lets start our conversation!!")

conversational_memory_lenght = 10
memory = ConversationBufferWindowMemory (k=conversational_memory_lenght)

#session state variable

if 'chat history' not in st.session_state:
	st.session_state.chat_history=[]

else:
	for message in st.session_state.chat_history:
	   memory.save_context({'input':message['human']}, {'output':message ['AI']})

#Initialize Groq Langchain chat object and conversation

groq_chat = ChatGroq(
		groq_api_key =os.environ.get("GROQ_API_KEY"),
		model_name ='llama3-8b-8192',
)
conversation=ConversationChain(
		llm=groq_chat,
		memory=memory
)

user_question= st.text_input("Ask A Queston : " )

# if the user has asked the question
if user_question:
		response = conversation (user_question)
		message = {'human': user_question, 'AI': response ['response']}
		st.session_state.chat_history.append(message)
		st.write("Chatbot:", response['response'])
