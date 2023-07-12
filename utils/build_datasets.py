from chromadb.config import Settings
from utils import settings

CHROMA_SETTINGS = settings.CHROMA_SETTINGS
db_persist_directory = settings.db_persist_directory
# 
from tqdm import tqdm

from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

from langchain.docstore.document import Document

from typing import List
import glob
import os

LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (UnstructuredEmailLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PDFMinerLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "latin-1"}),
    # Add more mappings for other file extensions and loaders as needed
}

def load_single_document(file_path: str) -> Document:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()[0]

    raise ValueError(f"Unsupported file extension '{ext}'")

def load_documents(source_dir: str):
    # Loads all documents from source documents directory
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext}"), recursive=True)
        )
    return [load_single_document(file_path) for file_path in all_files]


from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_text_splits(source_directory, chunk_size = 500, chunk_overlap = 50):
    print(f"Loading documents from {source_directory}")
    documents = load_documents(source_directory)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # text_splitter = CharacterTextSplitter(        
    #     separator = "\n\n",
    #     chunk_size = chunk_size,
    #     chunk_overlap  = chunk_overlap,
    #     length_function = len,
    # )

    texts = text_splitter.split_documents(documents)
    print(f"Loaded {len(documents)} documents from {source_directory}")
    print(f"Split into {len(texts)} chunks of text (max. {chunk_size} characters each)")

    return texts

def build_embedding_dataset(source_directory, embeddings_model_name, device = 'cpu'):
    texts = get_text_splits(source_directory)
    
    # Create embeddings
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import Chroma

    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name, 
                                    model_kwargs = {'device': device})

    # Create and store locally vectorstore
    db = Chroma.from_documents(texts, embeddings, persist_directory=db_persist_directory, 
                            client_settings=CHROMA_SETTINGS)
    db.persist()
    db = None

def extract_text_from_docx(file_path: str) -> str:
    from docx import Document as docx_loader
    print('extracting content of ', file_path)
    # Document()
    document = docx_loader(file_path)

    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text)

def get_docs(folder_path, docs_folder):
    # This function is not working, I have provided the txt files separately in the folder source_documents/
    # loads the files from given folder and save them in the docs_folder as txt files
    latest_files_content = {'File name': [], 'Content': []}
    
    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder)    

    if folder_path != '':
        # files_and_texts = {'paths': [], 'names': [], 'text': []}
        for root, _, files in tqdm(os.walk(folder_path)):            
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(".docx"):
                    text = extract_text_from_docx(file_path)                    
                else:
                    continue
                txt_file_name = ''.join([docs_folder, file.split('.')[0], '.txt'])
                print('writing: ', txt_file_name)

                with open(txt_file_name, 'w', encoding="utf-8") as f:
                    f.write(text)

                latest_files_content['File name'].append(file)
                latest_files_content['Content'].append(text)
                # except:
                #     continue
    pass
