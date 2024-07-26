import time
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# Start the timer
start_time = time.time()

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
    return (
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

# Create embeddings and retriever
embedding = OllamaEmbeddings(model="nomic-embed-text")
retriever = FAISS.from_documents(texts, embedding).as_retriever(search_kwargs={"k": 50})

# Read queries from the .txt file and execute each sequentially
with open("queries.txt", "r") as file:
    queries = file.readlines()

# Open the response file in append mode
with open("response.txt", "a") as response_file:
    for query in queries:
        query = query.strip()
        if query:
            # Perform the query
            docs = retriever.invoke(query)
            
            # Pretty print the retrieved documents
            pretty_docs = pretty_print_docs(docs)
            
            # Write the pretty printed documents to the response file
            response_file.write(f"\nQuery: {query}\n")
            response_file.write(pretty_docs)
            response_file.write("\n")
            
            # Set up the contextual compression retriever
            llm = Ollama(model="llama3.1")
            compressor = FlashrankRerank()
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=retriever
            )
            
            # Perform the compressed retrieval query
            compressed_docs = compression_retriever.invoke(query)
            compressed_doc_ids = [doc.metadata["id"] for doc in compressed_docs]
            response_file.write(f"Compressed Document IDs: {compressed_doc_ids}\n")
            
            # Create and execute the QA chain
            chain = RetrievalQA.from_chain_type(llm=llm, retriever=compression_retriever)
            response = chain({"query": query})
            
            # Write the response from the chain to the response file
            response_file.write(f"Response: {response}\n")
            response_file.write("\n" + "=" * 100 + "\n")

# Stop the timer and calculate the elapsed time in minutes
end_time = time.time()
elapsed_time = (end_time - start_time) / 60
print(f"The script took {elapsed_time:.2f} minutes to finish.")
