from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# Load and split the documents
documents = TextLoader(
    "RR1_i9_startup-config.txt",
).load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_documents(documents)
for idx, text in enumerate(texts):
    text.metadata["id"] = idx

# Define a function to pretty print documents
def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

# Create embeddings and retriever
embedding = OllamaEmbeddings(model="nomic-embed-text")
retriever = FAISS.from_documents(texts, embedding).as_retriever(search_kwargs={"k": 50})

# Perform the query
query = "What can you tell me about this router and what protocols are running on it?"
docs = retriever.invoke(query)

# Pretty print the retrieved documents
pretty_print_docs(docs)

# Set up the contextual compression retriever
llm = Ollama(model="llama3.1")
compressor = FlashrankRerank()
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

# Perform the compressed retrieval query
compressed_docs = compression_retriever.invoke(
    "What can you tell me about this router and what protocols are running on it?"
)
print([doc.metadata["id"] for doc in compressed_docs])

# Create and execute the QA chain
chain = RetrievalQA.from_chain_type(llm=llm, retriever=compression_retriever)
response = chain({"query": "What can you tell me about this router and what protocols are running on it?"})

# Print the response from the chain
print(response)
