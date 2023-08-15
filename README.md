# Financial-ChatBot

The Financial Chatbot project is aimed at developing an innovative chatbot that functions as a reliable and efficient financial advisor. The primary objective of this project is to provide users with quick and accurate answers to their inquiries concerning public companies listed on NASDAQ. Leveraging cutting-edge technologies in both finance and AI, the chatbot will draw upon a vast database comprising approximately 10,000 public financial documents .

<p align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3.11%20-%23006400.svg?&style=for-the-badge&logo=Python&logoColor=green" /></a>
    <a href="https://openai.com/gpt-4">
        <img src="https://img.shields.io/badge/ChatGPT-3.5%20-%23FF8300.svg?&style=for-the-badge&logo=OpenAI&logoColor=white" /></a>
    <a href="https://www.pinecone.io/">
        <img src="https://img.shields.io/badge/Pinecone%20-%23003F8C.svg?&style=for-the-badge&logo=pinecone&logoColor=white" /></a>
    <a href="https://flask.palletsprojects.com/en/2.3.x/">
        <img src="https://img.shields.io/badge/flask%20-%64BCCA0.svg?&style=for-the-badge&logo=flask&logoColor=black" /></a>
    <a href="https://choosealicense.com/licenses/mit/">
        <img src="https://img.shields.io/badge/License-MIT%20-%23212121.svg?&style=for-the-badge&logoColor=green" /></a>
    <a href="https://www.linkedin.com/in/enzo-matias-gonzalez/">
        <img src="https://img.shields.io/badge/LinkedIn%20-%230270AD.svg?&style=for-the-badge&logo=Linkedin&logoColor=white" /></a>
    
</p>

## Key Features
- Comprehensive Database: With access to a rich repository of around 10,000 public financial documents, the chatbot will be able to provide well-informed answers based on historical data and trends.

- Advanced AI Capabilities: Powered by OpenAI GPT models, the chatbot will possess advanced natural language processing capabilities, enabling it to understand and respond to user queries in a human-like manner.

- Extensive Document Vector Storage: Pinecone is employed to efficiently store and retrieve document vectors, enhancing the speed and accuracy of information retrieval.

- User-friendly Interface: The chatbot will be deployed through a user-friendly interface making it easily accessible to users seeking financial advice.

## Technologies

- OpenAI GPT Models: State-of-the-art language models to enhance natural language understanding and generation
  
- Deepset Haystack: A robust open-source framework for document search and question answering.

- Pinecone: Efficient document vector storage and retrieval for optimized information processing.

## Installation Steps

Follow these steps to set up the Financial Chatbot project:

1. Clone the Repository: Start by cloning the project repository from GitHub:
    <br>`git clone https://github.com/Gonzalez-Matias/Financial-ChatBot.git`<br>
2. Install Python Dependencies: Install the required Python packages using pip:
   <br>`pip install -r requirements.txt`<br>
3. Configure Pinecone: Set up your Pinecone API keys and configurations. Refer to the [Pinecone documentation](https://www.pinecone.io/docs/) for guidance.
4. Load all your pdf documents into pdf_documents folder
5. Run load_docs script(from the project root):
   <br>`python3 scripts/load_docs.py`<br>
6. Run process_data script(from the project root), that will create a unique json file with all the text chunks:
   <br>`python3 scripts/process_data.py`<br>
7. Set env variables for Pinecone:
   <br>`export PINECONE_API_KEY="YOUR_PINECINE_KEY"`  
   `export PINECONE_ENV="YOUR_SERVER_LOCATION"`<br>
8. Encode the text chunks and Create pinecone vector database by running create_vector_db(from the project root):
   <br>`python3 scripts/create_vector_db.py`<br>
9. Set env variables for OpenAI API:
   <br>`export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`<br>
10. Run the app:
   <br>`python3 app.py`<br>
