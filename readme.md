# RAG - Retriever-Augmented Generation

Este projeto é uma implementação de um **sistema de perguntas e respostas** que combina a abordagem de **Retriever-Augmented Generation (RAG)**, unindo o poder de **LLMs (Large Language Models)**, como o ChatGPT, com a habilidade de **buscar informações em documentos externos**. O sistema permite que você forneça seus próprios documentos para a IA buscar e fornecer respostas específicas ao contexto, enquanto também é capaz de responder com base no conhecimento geral de um modelo pré-treinado.

## 🛠️ Funcionalidades

- **Integração de LLM e Recuperação de Documentos**: Combina a busca por informações em documentos com a geração de respostas contextuais de um modelo de linguagem.
- **Flexibilidade**: Responde tanto com base em documentos específicos fornecidos pelo usuário quanto com base no conhecimento geral do LLM.
- **Alta precisão nas respostas**: Oferece respostas precisas ao extrair informações de fontes documentais enquanto aproveita a fluência e capacidade de compreensão do modelo de linguagem.
- **Fácil integração**: Projeto modular que pode ser adaptado para diversos tipos de documentos e interfaces.

## 🧑‍💻 Como funciona o RAG

1. **Recuperação de informações**: O sistema primeiro faz uma busca por documentos relevantes dentro da base de dados fornecida. Pode-se usar técnicas como BM25 ou outros algoritmos de similaridade para identificar os trechos mais relevantes.
2. **Geração de resposta**: Com base nos trechos recuperados e na pergunta feita, o sistema utiliza o LLM para gerar uma resposta mais fluida e completa, combinando o conhecimento do modelo com os documentos recuperados.
3. **Fallback para LLM**: Se não houver documentos relevantes, o sistema utiliza apenas o LLM para responder à pergunta, aproveitando seu conhecimento geral.

## 🖥️ Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/rag-system.git
   ```

2. Caso necessário, crie um ambiente python para rodar localmente (exemplo para linux):
   ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install python-dotenv langchain langchain-openai openai milvus pymilvus unstructured tiktoken lark
   pip install -U langchain-community
   pip install "unstructured[pdf]"
   ```

4. Configure a base de documentos em `/docs` ou o banco de dados que deseja utilizar para recuperação.

5. Inicie a aplicação:
   ```bash
   python main.py
   ```
