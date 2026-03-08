import streamlit as st
import os
import shutil 
from PyPDF2 import PdfReader 
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import faiss
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from modules.htmlTemplates import css, bot_template, user_template
from modules.file_processor import process_file

#load_dotenv()
OPENAI_API_KEY = "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"


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(selected_pdfs):
    text = process_file(selected_pdfs)
    chunks = get_text_chunks(text)
    merged_chunks = []
    for pdf in selected_pdfs:
        stored_chunks_folder = os.path.join("stored_chunks", pdf)
        merged_chunks.extend(
            [open(os.path.join(stored_chunks_folder, file), encoding="utf-8").read() for file in sorted(os.listdir(stored_chunks_folder))]
        )

    embeddings = OpenAIEmbeddings()
    vectorstore = faiss.FAISS.from_texts(texts=merged_chunks, embedding=embeddings)
    return vectorstore
    

#The function get_conversation_chain builds an intelligent conversational system 
def get_conversation_chain(selected_pdfs):
    merged_chunks = []
    for pdf in selected_pdfs:
        stored_chunks_folder = os.path.join("stored_chunks", pdf)
        merged_chunks.extend(
            [open(os.path.join(stored_chunks_folder, file), encoding="utf-8").read() for file in sorted(os.listdir(stored_chunks_folder))]
        )

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    vectorstore = faiss.FAISS.from_texts(texts=merged_chunks, embedding=embeddings)

    llm = ChatOpenAI(api_key=OPENAI_API_KEY,model="gpt-3.5-turbo")
    retriever = vectorstore.as_retriever()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )

    return conversation_chain


def handle_userinput(user_question, conversation_chain):
    response = conversation_chain({'question': user_question})
    response_content = response['chat_history'][-1].content
    st.session_state.chat_history.append((user_question, response_content))

    # Display chat history
    for question, answer in st.session_state.chat_history:
        if question:
            st.write(user_template.replace("{{MSG}}", question), unsafe_allow_html=True)
        if answer:
            st.write(bot_template.replace("{{MSG}}", answer), unsafe_allow_html=True)

#
def main():
    #load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":Books")
    st.write(css, unsafe_allow_html=True)

    st.sidebar.markdown("---")     
    st.sidebar.subheader("About")
    st.sidebar.info("This app allows you to chat with multiple Files including PDFs, DOCX, PPTX, TXT, PNG AND JPEG/JPG.")
    st.sidebar.info("Select an option and start chatting!")

    st.header("Welcome to AI-Studybot")

    # Initialize conversation chain variable
    conversation_chain = None

    # Display options to the user
    user_choice = st.radio("Choose an option:", ["Chat with Files", "Store Files permanently", "Delete Files"])

    if user_choice == "Chat with Files":
        st.header("Chat with Files")
        st.warning("Select permanently stored files to start chatting.")

        # Display available files and allow the user to select multiple files for chatting
        available_files = [file for file in os.listdir("stored_chunks") if os.path.isdir(os.path.join("stored_chunks", file))]
        if available_files:
            st.subheader("Available Files")
            selected_files = st.multiselect("Select Files to chat with:", available_files)
            st.success("Selected Files: {}".format(', '.join(selected_files)))

            if selected_files:
                conversation_chain = get_conversation_chain(selected_files)  # Initialize conversation chain

                # Initialize chat history if not already done
                if 'chat_history' not in st.session_state:
                    st.session_state.chat_history = []

                user_question = st.text_input("Ask a question about the selected Files:")
                if user_question:
                    response = handle_userinput(user_question, conversation_chain)  # Get bot response
                    if response:
                        st.session_state.chat_history.append((user_question, response))  # Update chat history
                        for question, answer in st.session_state.chat_history[-4:]:  # Display last 3-4 interactions
                            st.write(f"Q: {question}")
                            st.write(f"A: {answer}")

    elif user_choice == "Store Files permanently":
        st.header("Store Files permanently")

        # Option to upload new PDFs, DOCX, or TXT for permanent storage
        uploaded_files = st.file_uploader("Upload new files (PDF, DOCX, TXT) for permanent storage:", 
                                          type=["pdf", "docx", "txt","pptx", "jpeg", "jpg", "png"], 
                                          accept_multiple_files=True)
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                with st.spinner(f"Storing {uploaded_file.name} permanently"):
                    raw_text = process_file(uploaded_file)  # Handles PDF, DOCX, and TXT
                    text_chunks = get_text_chunks(raw_text)

                    # Create a folder for each file
                    stored_chunks_folder = os.path.join("stored_chunks", os.path.splitext(uploaded_file.name)[0])
                    os.makedirs(stored_chunks_folder, exist_ok=True)

                    # Store chunks locally for permanent storage
                    for i, chunk in enumerate(text_chunks):
                        chunk_filename = os.path.join(stored_chunks_folder, f"chunk_{i + 1}.txt")
                        with open(chunk_filename, "w", encoding="utf-8") as file:
                            file.write(chunk)

                    st.success(f"{uploaded_file.name} stored permanently!")

    elif user_choice == "Delete Files":
        st.header("Delete Files")
        
        # Display available files for deletion
        stored_files = [file for file in os.listdir("stored_chunks") if os.path.isdir(os.path.join("stored_chunks", file))]
        if stored_files:
            st.subheader("Permanently Stored Files")
            files_to_delete = st.multiselect("Select Files to delete:", stored_files)
            if files_to_delete:
                for file in files_to_delete:
                    folder_to_delete = os.path.join("stored_chunks", file)
                    shutil.rmtree(folder_to_delete)  # Delete the folder and its contents
                st.success("Selected files deleted successfully!")

if __name__ == "__main__":
    main()
