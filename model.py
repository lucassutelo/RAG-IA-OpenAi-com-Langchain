import os
from dotenv import load_dotenv

load_dotenv()

from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationTokenBufferMemory
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Milvus
from milvus import default_server as milvus_server


class RAG:
    def __init__(self,
                 docs_dir: str,
                 n_retrievals: int = 4,
                 chat_max_tokens: int = 3097,
                 model_name: str = "gpt-4o-mini",
                 creativeness: float = 0.7):
        self.docs_dir = docs_dir
        self.__model = self.__set_llm_model(model_name, creativeness)
        self.__n_retrievals = n_retrievals
        self.__chat_history = self.__set_chat_history(max_token_limit=chat_max_tokens)
        self.__retriever = None  # Inicialize __retriever como None
        self.load_documents() 

    def load_documents(self):
        """Carrega os documentos do diretório e atualiza o índice do Milvus."""
        print("Carregando documentos...")
        self.__docs_list = self.__get_docs_list(self.docs_dir)
        self.__retriever = self.__set_retriever(k=self.__n_retrievals)

    def reset_db(self):
        """Recarrega os documentos e recria o índice do Milvus."""
        print("Resetando banco de dados...")

        # Correção: Use `utility` para acessar métodos de coleção
        if self.__retriever is not None and self.__retriever.vectorstore.collection_name in self.__retriever.vectorstore.utility.list_collections():
            self.__retriever.vectorstore.drop_collection()

        self.load_documents()
        print("Banco de dados resetado com sucesso.")

    def __set_llm_model(self, model_name: str = os.getenv("GPT_MODEL"), temperature: float = 0.7):
        return ChatOpenAI(model_name=model_name, temperature=temperature)

    def __get_docs_list(self, docs_dir: str) -> list:
        print("Carregando documentos...")
        loader = DirectoryLoader(docs_dir,
                                 recursive=True,
                                 show_progress=True,
                                 use_multithreading=True,
                                 max_concurrency=4)
        docs_list = loader.load_and_split()
        return docs_list

    def __set_retriever(self, k: int = 4):
        # Milvus Vector Store
        embeddings = OpenAIEmbeddings()
        milvus_server.start()
        vector_store = Milvus.from_documents(
            self.__docs_list,
            embedding=embeddings,
            connection_args={"host": os.getenv("MILVUS_HOST"), "port": os.getenv("MILVUS_PORT")},
            collection_name="personal_documents",
        )

        # Self-Querying Retriever
        metadata_field_info = [
            AttributeInfo(
                name="source",
                description="O caminho de diretórios onde se encontra o documento",
                type="string",
            ),
        ]

        document_content_description = "Documentos pessoais"

        _retriever = SelfQueryRetriever.from_llm(
            self.__model,
            vector_store,
            document_content_description,
            metadata_field_info,
            search_kwargs={"k": k}
        )

        return _retriever

    def __set_chat_history(self, max_token_limit: int = 15383):
        return ConversationTokenBufferMemory(llm=self.__model, max_token_limit=max_token_limit, return_messages=True)

    def ask(self, question: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Você é um assistente responsável por responder perguntas sobre documentos. Responda a pergunta do usuário com um nível de detalhes razoável e baseando-se no(s) seguinte(s) documento(s) de contexto:\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])

        output_parser = StrOutputParser()
        chain = prompt | self.__model | output_parser
        answer = chain.invoke({
            "input": question,
            "chat_history": self.__chat_history.load_memory_variables({})['history'],
            "context": self.__retriever.invoke(question)
        })

        # Atualização do histórico de conversa
        self.__chat_history.save_context({"input": question}, {"output": answer})

        return answer
