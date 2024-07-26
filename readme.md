# Router Configuration Query Script

## Overview

This script is designed to read multiple queries from a `.txt` file and execute each query sequentially on a router configuration document. It leverages the LangChain framework to load, process, and retrieve relevant information from the document, using advanced language models to answer each query. The responses are appended to a `response.txt` file, and the script measures the total execution time.

## Features

- **Load and Split Documents**: The script loads a router configuration file and splits it into smaller, manageable chunks for efficient processing.
- **Read and Execute Queries**: Queries are read from an external `.txt` file and executed sequentially.
- **Contextual Compression and Retrieval**: The script uses contextual compression to enhance retrieval accuracy, ensuring relevant information is extracted from the document.
- **Question-Answering**: It uses advanced language models to answer each query based on the retrieved information.
- **Append Responses**: Only the query and result of each response are appended to a `response.txt` file.
- **Execution Timer**: The script measures and displays the total execution time in minutes.

## Requirements

- Python 3.6 or higher
- LangChain library
- Ollama library

## Script Workflow

1. **Start the Timer**: The script begins by recording the current time to measure the total execution duration.
2. **Load and Split Documents**:
   - Loads a router configuration file (`RR1_i9_startup-config.txt`) using `TextLoader`.
   - Splits the document into smaller chunks using `RecursiveCharacterTextSplitter` for efficient processing.
3. **Create Embeddings and Retriever**:
   - Creates embeddings for the document chunks using the `OllamaEmbeddings` model.
   - Sets up a retriever using `FAISS` to facilitate the search and retrieval of relevant document chunks.
4. **Read and Execute Queries**:
   - Reads queries from the `queries.txt` file.
   - For each query, retrieves relevant document chunks using the retriever.
   - Uses a contextual compression retriever to enhance retrieval accuracy.
5. **Question-Answering**:
   - Creates a question-answering chain using the `Ollama` model.
   - Executes the QA chain for each query and appends the responses (query and result) to `response.txt`.
6. **Stop the Timer**:
   - After processing all queries, stops the timer and calculates the total execution time.
   - Displays the total time taken in minutes.

## Usage

1. Ensure you have the necessary libraries installed.
2. Place your router configuration file in the same directory as the script and name it `RR1_i9_startup-config.txt`.
3. Create a `queries.txt` file in the same directory and add your queries, one per line.
4. Run the script.
5. The responses will be appended to a `response.txt` file, and the total execution time will be displayed in the console.

### Example `queries.txt`

```
What can you tell me about this router and what protocols are running on it?
How is the security configured on this router?
What are the interface IP addresses?
```

### Example Output in `response.txt`

```
Query: What can you tell me about this router and what protocols are running on it?
Result: The router is running OSPF and BGP protocols as indicated in the configuration details provided. OSPF is configured with area 0, and BGP has several neighbor relationships defined.

====================================================================================================

Query: How is the security configured on this router?
Result: The router has multiple ACLs applied to various interfaces, along with SSH configured for secure management access. Additionally, there are firewall rules set up to filter traffic.

====================================================================================================

Query: What are the interface IP addresses?
Result: The interfaces have the following IP addresses:
- GigabitEthernet0/0: 192.168.1.1
- GigabitEthernet0/1: 10.0.0.1

====================================================================================================
```

## Potential Use for Analyzing Cisco Devices

This script can be particularly useful for network administrators and engineers who need to analyze and manage Cisco router configurations. Here are some potential use cases:

- **Configuration Auditing**: Automate the auditing of router configurations by querying specific details such as protocol configurations, security settings, and interface details.
- **Troubleshooting**: Quickly retrieve relevant configuration information to diagnose and troubleshoot network issues.
- **Documentation**: Generate comprehensive reports on router configurations and operational details by querying and saving the results.
- **Security Analysis**: Assess security settings and access control configurations to ensure compliance with security policies.
- **Backup and Version Control**: Verify the existence and setup of backup and version control mechanisms for router configurations.
- **Change Management**: Track and document changes in router configurations over time by periodically running the script with updated queries.

By automating the extraction and analysis of configuration details, this script can significantly reduce the manual effort involved in managing and securing Cisco devices, leading to more efficient and reliable network operations.
