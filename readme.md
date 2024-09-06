# Criação do ambiente python

python3 -m venv venv
source venv/bin/activate

# Atualização do pip

pip install --upgrade pip

# Instalação das dependências

pip install python-dotenv langchain langchain-openai openai milvus pymilvus unstructured tiktoken lark
pip install -U langchain-community
pip install "unstructured[pdf]"

# Comando para rodar

python main.py
