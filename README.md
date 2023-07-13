# docuchat

![demo_docuChat_0](https://github.com/rezabonyadi/docuchat/assets/25924343/4e97b567-bc87-42e2-af05-93467286162b)

 
This repository is an example of how you can build a chatbot that runs on-device and uses a consumer CPU only (not a high-end M1, but a normal i5 CPU), and lets you chat with your documents.

Quick example: See the Jupyter notebook.

# The chat system with graphics:
 
## Setting up the environment

First create your environment:

python -m venv env_docu_chat

Activate it:

Activate the environment .\env_docu_chat\Scripts\activate

And install the requirements:

pip install -r requirements.txt

## Setting up the chat model:

First, run the app by typing 

streamlit run main.py

You will see the following screen in your browser:
![image](https://github.com/rezabonyadi/docuchat/assets/25924343/840e12b0-63d8-4c19-8678-8fbf311c5946)

In the "Onedrive address" text box in the left, provide the address to a folder where you have some docx files you want to chat against.
Then click on "BUild dataset embedding" button. This will read your docx files from that folder, creates another folder (with the address "Docs address"), and saves those docx as text files in that folder. It then embeds them and creates a vector db for you in the "db" folder.

![image](https://github.com/rezabonyadi/docuchat/assets/25924343/e2ce35a8-028f-440c-b167-8066b62748bb)

Now click on "Question and answering" tab and start chatting!

![image](https://github.com/rezabonyadi/docuchat/assets/25924343/9522aa66-ba6f-408a-9462-6716cbba6c06)

The chat provides you with a response and with the context used (you can uncollapse the "See the context used".

![demo_docuChat_0](https://github.com/rezabonyadi/docuchat/assets/25924343/4e97b567-bc87-42e2-af05-93467286162b)

