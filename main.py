import streamlit as st
from PIL import Image
from utils import build_datasets, prepare_chat_model, settings

def chatbot_response(user_input):
    # Put the inference and the LLM stuff here...
    if st.session_state.qa_engine is None:
        st.text('Load an engine')
        return
    
    query = user_input
    res = st.session_state.qa_engine(query)
    answer, docs = res['result'], res['source_documents']
    print(answer)
    # print('$$$$$$$ Used Context $$$$$$$')
    # print(docs)
    all_context = "\n\n".join(['Context: ' + i.dict()['page_content'] + '\n \n Taken from: ' + i.dict()['metadata']['source'] for i in docs])

    return answer, all_context

header_image = Image.open('assets/header.png')
user_logo = Image.open('assets/reza.png')
chatbot_logo = Image.open('assets/chatbot.png')

st.set_page_config(
    page_title="People Chat",
    page_icon="assets/chatbot.png",
    layout="centered"    
)
st.image(header_image, use_column_width=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'retriver' not in st.session_state:
    st.session_state.retriver = None

if 'qa_engine' not in st.session_state:
    st.session_state.qa_engine = None

# Create containers for user input and chat history

embedding_model = st.sidebar.selectbox('Embedding model for retriver', ('sentence-transformers/all-MiniLM-L6-v2', 'sentence-transformers/all-mpnet-base-v2'))
embedding_model_device = st.sidebar.selectbox('Embedding model device', ('cpu', 'cuda'))
chat_model = st.sidebar.selectbox('Chat model', ('MBZUAI/LaMini-T5-738M', 'lmsys/fastchat-t5-3b-v1.0'))

docs_folder = st.sidebar.text_input('Docs address', """source_documents/""")
tab_db, tab_qa = st.tabs(["Setup embedding database", "Question and answering"])

######################## Building db tab
button_build_ds = tab_db.button("Build dataset embeddings", use_container_width=True, key='start_build_db')
onedrive_folder = st.sidebar.text_input('Onedrive address', """C:/Users/rezabonyadi/OneDrive - Microsoft/Documents/projects/""")

if button_build_ds:    
    with st.spinner('Reading docs...'):
        build_datasets.get_docs(onedrive_folder, docs_folder)
        st.success('Done reading!')

    with st.spinner('Splitting and embedding documents...'):
        build_datasets.build_embedding_dataset(docs_folder, embedding_model, device = embedding_model_device)
        st.success('Done building db of your documents!')

    with st.spinner('Preparing the retriver...'):
        retriver = prepare_chat_model.get_context_retriver(embedding_model, device='cpu')
        st.session_state.retriver = retriver
        st.session_state.qa_engine = prepare_chat_model.get_qa_engine(chat_model, st.session_state.retriver, 
                                                                      input_max_length=512, pipeline_model="text2text-generation", device=-1)
        st.success('Retriver and Q&A engine ready!')

    # utils.utils. build_embedding_dataset(source_directory, embeddings_model_name, device = 'cpu')


######################## Builidng QA tab
# if st.session_state.retriver is None:
#     tab_qa.
with tab_qa:
    if st.session_state.retriver is None:
        with st.spinner('Loading the chat and context model...'):
            retriver = prepare_chat_model.get_context_retriver(embedding_model, device='cpu')
            st.session_state.retriver = retriver
            print('Loaded retriver')
            st.session_state.qa_engine = prepare_chat_model.get_qa_engine(chat_model, st.session_state.retriver, input_max_length=512, pipeline_model="text2text-generation", device=-1)
            print('Loaded engine')

    textbox_container = st.container()
    history_container = st.container()

# User input
with textbox_container:
    col1, col2 = st.columns([10, 1])
    user_input = col1.text_input("Type your message:", label_visibility='hidden')
    col2.text(' ')
    col2.text(' ')
    button_send = col2.button(":paperclip:", use_container_width=True)

# Handle user input
if user_input or button_send:
    st.session_state.chat_history.append(("user", user_input))
    chatbot_reply = chatbot_response(user_input)
    st.session_state.chat_history.append(("chatbot", chatbot_reply))    
    
    user_input = ""

# Redraw chat history with the new messages (in reverse order)
with history_container:
    for role, message in reversed(st.session_state.chat_history):
        if role == "user":
            col1, col2 = st.columns([1, 13])
            col1.image(user_logo, width=40, output_format='PNG')
            col2.markdown(f'<div style="background-color: #808080; border-radius: 10px; padding: 10px; margin-bottom: 1em;"><p style="color: white; margin-bottom: 0;">{message}</p></div>', unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([1, 13])
            col1.image(chatbot_logo, width=50, output_format='PNG')
            print(message[1])          
            col2.markdown(f'<div style="background-color: #0031C9; border-radius: 10px; padding: 10px; margin-bottom: 1em;"><p style="color: white; margin-bottom: 0;">{message[0]}</p></div>', unsafe_allow_html=True)
            with st.expander('See context used', expanded=False):
                st.write(message[1])

###################
# Alternative

# import streamlit as st
# from PIL import Image

# # Function to simulate chatbot response
# def chatbot_response(user_input):
#     return "This is a sample response to: " + user_input

# # Load your images and logos
# header_image = Image.open('assets/header.png')
# user_logo = Image.open('assets/th.jpeg')
# chatbot_logo = Image.open('assets/chatbot.png')

# # App layout
# st.set_page_config(
#     page_title="People Chat",
#     page_icon="assets/chatbot.png",
#     layout="centered"    
# )
# st.image(header_image, use_column_width=True)

# # Chat history
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# # Chat history container
# history_container = st.container()
# textbox_container = st.container()

# # User input
# with textbox_container:
#     col1, col2 = st.columns([10, 1])
#     user_input = col1.text_input("Type your message:", label_visibility='hidden')
#     col2.text(' ')
#     col2.text(' ')
#     button_send = col2.button(":high_heel:", use_container_width=True)

# # Handle user input
# if user_input or button_send:
#     st.session_state.chat_history.append(("user", user_input))
#     chatbot_reply = chatbot_response(user_input)
#     st.session_state.chat_history.append(("chatbot", chatbot_reply))
#     user_input = ""

# # Redraw chat history with the new messages
# with history_container:
#     # st.write('<style> .element-container { overflow-y: auto; max-height: 400px; } </style>', unsafe_allow_html=True)
#     for role, message in st.session_state.chat_history:
#         if role == "user":
#             col1, col2 = st.columns([1, 13])
#             # st.markdown(f'<p style="margin-bottom:0.25em;"><strong>{role.title()}:</strong> {message}</p>', unsafe_allow_html=True)
#             col1.image(user_logo, width=50, output_format='PNG')
#             col2.markdown(f'<div style="background-color: #808080; border-radius: 10px; padding: 10px; margin-bottom: 1em;"><p style="color: white; margin-bottom: 0;">{message}</p></div>', unsafe_allow_html=True)
#         else:
#             col1, col2 = st.columns([1, 13])
#             # st.markdown(f'<p style="margin-bottom:0.25em;"><strong>{role.title()}:</strong> {message}</p>', unsafe_allow_html=True)
#             col1.image(chatbot_logo, width=50, output_format='PNG')
#             col2.markdown(f'<div style="background-color: #0031C9; border-radius: 10px; padding: 10px; margin-bottom: 1em;"><p style="color: white; margin-bottom: 0;">{message}</p></div>', unsafe_allow_html=True)

###########################


