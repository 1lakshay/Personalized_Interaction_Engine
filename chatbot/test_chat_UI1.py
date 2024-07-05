import os
import streamlit as st
import bs4
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv("keys.env")

# extracting URL
def get_site_url():
    query_params = st.query_params
    if 'site_url' in st.query_params:
        return query_params['site_url'][0]
    else:
        return None

# polishing the user input if incorrect
def polishing(result):
    prefix = "Corrected Query: "
    if result.startswith(prefix):
        return result[len(prefix):]
    else:
        return result

# intializing the model
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))

if get_site_url():
    url = get_site_url()
else:
    url = "http://localhost/wordpress/index.php/2024/06/24/neural-networks/"

# document_loader
loader = WebBaseLoader(
    web_paths=(url,),
    bs_kwargs={"parse_only": bs4_strainer}
)

# loading the documents
docs = loader.load()

# splitting docs into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
all_splits = text_splitter.split_documents(docs)

# storing chunks in vector database
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# to retrieve similar chunks
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

# template & chain to error free the user query
template_to_correct_spells = """
    You are an intelligent assistant designed to help users by correcting any errors in their queries. Your task is to read the user's query, identify any spelling or grammatical errors, and return the corrected version of the query. Do not provide an answer, only return the corrected query.
    Corrected Query:
    Original Query: {question}
"""
prompt_to_correct_spells = ChatPromptTemplate.from_template(template_to_correct_spells)
chain_to_correct_spells = prompt_to_correct_spells | llm | StrOutputParser()

# template & prompt to finding the context with previous queries
contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# Implementing Chain of thought strategy
qa_system_prompt = """You are a thoughtful assistant. \
        When asked a question, you generate a step-by-step chain of thought to arrive at the answer. \
        Please provide a detailed response with your reasoning.
    {context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)      # combining the chunks of docs which are relevant
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)  # chaining

# Title for the UI
st.title("Chatbot")

#initializing history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# to make all chats remain visible
for message in st.session_state['chat_history']:
    if message['role'] == 'user':
        st.chat_message("user").write(message['content'])        # user message
    else:
        st.chat_message("assistant").write(message['content'])   # assistant message

if query := st.chat_input("Say something"):                      # taking input
    corrected_query = polishing(chain_to_correct_spells.invoke({"question": query}))    # removing error from query
    st.session_state['chat_history'].append({'role': 'user', 'content': corrected_query})  # storing in chat_history
    st.chat_message("user").write(corrected_query)                                      # printing the user error free query
    with st.spinner("Fetching data..."):                                                # dynamic loading for better UX
        answer = rag_chain.invoke({"input": corrected_query, "chat_history": st.session_state['chat_history']})   # invoking the rag_chain to get output
        st.session_state['chat_history'].append({'role': 'assistant', 'content': answer["answer"]}) # storing response for context preservation
        st.chat_message("assistant").write(answer["answer"])                 # displaying the result
