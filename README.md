# docuchat
 
This repository is an example of how you can build a chatbot that runs on-device (uses a consumer CPU only, and doesnt need a high-end one) and lets you chat with your documents.
 
## Setting up the environment
python -m venv env_docu_chat
Activate the environment .\env_docu_chat\Scripts\activate
pip install -r requirements.txt


Install these in 
pip install torch --index-url https://download.pytorch.org/whl/cu117
pip install -q -U bitsandbytes
pip install -q -U git+https://github.com/huggingface/transformers.git
pip install -q -U git+https://github.com/huggingface/peft.git
pip install -q -U git+https://github.com/huggingface/accelerate.git