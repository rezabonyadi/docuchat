from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from utils import settings

CHROMA_SETTINGS = settings.CHROMA_SETTINGS
db_persist_directory = settings.db_persist_directory

def get_context_retriver(embeddings_model_name, device='cpu'):
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name, 
                                    model_kwargs = {'device': device})
    db = Chroma(persist_directory=db_persist_directory, embedding_function=embeddings, 
                client_settings=CHROMA_SETTINGS)

    retriever = db.as_retriever()

    return retriever

from langchain import HuggingFacePipeline
from transformers import pipeline
from langchain.chains import RetrievalQA

def get_qa_engine(model_id, retriever, input_max_length=512, pipeline_model="text2text-generation", device=-1):
    # model_id = "MBZUAI/LaMini-T5-738M"
    # model_id = "lmsys/fastchat-t5-3b-v1.0"
    # input_max_length = 512

    pipe = pipeline(pipeline_model, model=model_id, truncation=True, 
                    max_length=input_max_length, device=device)

    llm = HuggingFacePipeline(pipeline=pipe)

    # llm = HuggingFacePipeline.from_model_id(model_id=model_id, 
    #                                         task="text2text-generation", 
    #                                         model_kwargs={"temperature":0, 
    #                                                       "max_length":64, 
    #                                                       'device': 0})
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", 
                                    retriever=retriever, return_source_documents=True)
    
    return qa