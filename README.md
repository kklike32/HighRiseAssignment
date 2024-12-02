# Highrise FAQ Chatbot

This project is a prototype of an FAQ chatbot designed to assist users with questions about the Highrise app. The chatbot can answer user queries by providing relevant responses from the Highrise FAQ section found at [https://support.highrise.game/en/](https://support.highrise.game/en/).

**Author**: Keenan Kalra  
**Date**: December 2024  

## Table of Contents

- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How to Run the Chatbot](#how-to-run-the-chatbot)
  - [Running Locally](#running-locally)
   - [TF-IDF Chatbot](#tf-idf-chatbot)
   - [RAG Chatbot](#rag-chatbot)
   - [Running the Web App Locally](#running-the-web-app-locally)
  - [Using the Web App](#using-the-web-app)
- [Features Implemented](#features-implemented)
- [Logging and Reporting](#logging-and-reporting)
  - [AWS S3 Logging](#aws-s3-logging)
- [Next Steps](#next-steps)
- [Acknowledgments](#acknowledgments)
- [Sample Conversations](#sample-conversations)

## Project Structure

- **README.md**: This file.
- **data/**: Contains the scraped FAQ data and processed versions.
- **logs/**: Contains logs of user interactions and unanswered queries (used when running locally).
- **requirements.txt**: Lists all Python dependencies.
- **scraping.ipynb**: Jupyter notebook used for scraping the FAQ data.
- **src/**: Contains source code for both the TF-IDF and RAG chatbots.
  - **tfidf_chatbot/**: Contains the TF-IDF-based chatbot implementation.
  - **rag_chatbot/**: Contains the Retrieval-Augmented Generation (RAG) chatbot implementation.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- An OpenAI API key (for the RAG chatbot)
- AWS account with S3 bucket (for logging)
- Required Python packages (listed in `requirements.txt`)

### Installation Steps

1. **Clone the Repository**

   `git clone https://github.com/yourusername/HighriseAssignment.git`
   
   `cd HighriseAssignment`

2. **Install Dependencies**

   Install all required Python packages using pip:

   `pip install -r requirements.txt`

3. **Set Up Environment Variables**

   For the RAG chatbot, set your OpenAI API key as an environment variable:

   `export OPENAI_API_KEY='your-api-key-here'`

   Replace 'your-api-key-here' with your actual OpenAI API key.

   If you plan to use AWS S3 logging, set the following environment variables:

   ```
   export HR_AWS_ACCESS_KEY_ID='your-access-key-id'
   export HR_AWS_SECRET_ACCESS_KEY='your-aws-secret-access-key'
   export HR_AWS_DEFAULT_REGION='your-aws-region'
   export HR_AWS_BUCKET_NAME='your-aws-bucket-name'
   ```

   Replace placeholders with your actual AWS credentials and bucket name.

4. **Download NLTK Data**

   For text processing, some NLTK data packages are required. Run the following commands in a Python shell:

   ```
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

## How to Run the Chatbot

### Running Locally

#### TF-IDF Chatbot

The TF-IDF chatbot is a simple implementation that uses TF-IDF vectorization and cosine similarity to match user queries to the FAQ data.

**Steps to Run:**

1. **Preprocess the Data**

   `python src/tfidf_chatbot/preprocess.py`

   This script preprocesses the FAQ data for the TF-IDF model.

2. **Run the Chatbot**

   `python src/tfidf_chatbot/main.py`

#### RAG Chatbot

The RAG chatbot uses OpenAI's GPT models to generate responses, augmenting retrieval from the FAQ data.

**Steps to Run:**

1. **Preprocess the Data**

   `python src/rag_chatbot/preprocess.py`

   This script processes the FAQ data, splitting articles into individual question-answer pairs and cleaning the text.

2. **Compute Embeddings**

   `python src/rag_chatbot/compute_embeddings.py`

   This script computes embeddings for the processed data using OpenAI's embedding models.

3. **Build the Vector Store**

   `python src/rag_chatbot/vector_store.py`

   This script builds a FAISS index for efficient similarity search.

4. **Run the Chatbot**

   `python src/rag_chatbot/main.py`

### Running the Web App Locally

To run the web app locally, ensure you've completed the steps above for the RAG chatbot.

1. **Install Streamlit**

   If you haven't already, install Streamlit using pip:
   pip install Streamlit

2. **Run the Web App**

   `streamlit run web_app.py`

   This command will start the Streamlit server and open the web app in your default browser.

3. Access the Web App

   Open the URL displayed in the terminal to access the web app.

## Using the Web App
The chatbot is deployed and available at [https://highrisechatbot.streamlit.app](https://highrisechatbot.streamlit.app).

### How to Use

- **Ask a Question**: Enter your query in the text box labeled "Type your message here:".
- **Send**: Click the "Send" buton to submit your query.
- **View Response**: The chatbot will display the response to your query in the chat window.
- **Feddback**: Rate the response as "Helpful" or "Not Helpful" using the thumbs-up and thumbs-down buttons.
- **Conversation History**: View the chat history in the chat window. 

## Features Implemented

- **Basic NLP Techniques**: Implemented lemmatization and synonym expansion in the TF-IDF chatbot to improve text matching accuracy.
- **Retrieval-Augmented Generation (RAG)**: Integrated OpenAI's GPT models to enhance response generation in the RAG chatbot.
- **User Feedback**: Added ability for users to rate responses as helpful or unhelpful, storing this data for future improvements.
- **Logging**: Implemented logging of user interactions and feedback using AWS S3 for persistent storage.

## Logging and Reporting

### AWS S3 Logging

In the deployed app, interaction logs and user feedback are stored in an AWS S3 bucket. The logs are saved in the following formats:

- **Interaction Logs**: Each user query and chatbot response is saved as a JSON file in the S3 bucket under logs/interactions/all/.
- **Unanswered Queries**: User queries that the chatbot couldn't answer are stored in a separate JSON file under logs/interactions/unmatched/.
- **User Feedback**: User feedback (helpful or unhelpful) for each response is stored in a JSON file under logs/feedback/.

## Next Steps

- **Enhance User Interface**: Improve the web app's design for a better user experience.
- **Improved Error Handling**: Enhance exception handling for network errors, API rate limits, and other potential issues.
- **Data Analysis**: Develop tools or scripts to analyze the logs stored in AWS S3 for insights and improvements.
- **Learning Mode**: Enable the chatbot to learn from unanswered or misclassified questions by incorporating them into the dataset after review.

## Acknowledgments

- **Highrise**: For providing the FAQ data used in this project.
- **OpenAI**: For the GPT models used in the RAG chatbot.
- **NLTK**: For the natural language processing tools used in preprocessing.
- **Streamlit**: For the web app framework used in the deployment.
- **AWS**: For the cloud storage services used for logging.

## Sample Conversations

1. **User**: Where do I buy furniture?
   
   **Chatbot**: To buy furniture, stop by the Store in the Highrise app. Enter design mode in a room where you have design rights by clicking the pencil and ruler icon in the top right-hand corner of your screen. Then, select the "shop" option in the bottom right-hand corner. A storefront window will pop up, showcasing recent items and featured collections. You can browse through the furniture library organized by type. Most items can be purchased with bubbles, but some high-end pieces require gold. If you're looking for a specific item that may no longer be available, you can check the Marketplace for players selling it.

2. **User**: How much does the iPhone cost?
   
   **Chatbot**: I'm sorry, I couldn't find an answer to your question. I suggest checking the Highrise FAQ website for more information.

3. **User**: Can I change my room size?

   **Chatbot**: Yes, you can change your room size! To do this, go to 'Rooms' in the top left-hand corner of your screen, then navigate to the 'My rooms' tab and tap on 'Create a Room' to start fresh. If your current room size isn’t to your liking, you can delete the existing room by going to the room description page and selecting Edit > Basic Info > Delete Room. After that, you can create a new room with your desired size! Enjoy creating your perfect space!

4. **User**: How can I change my username?

   **Chatbot**: You can change your username by visiting your account's settings page and selecting the "Username" option under account management. Once you change your username, it will be updated everywhere in the application, and the username you use to log in will also change to your new one. Remember, all players receive one name change for free, but subsequent changes will cost 10,000 gold. Additionally, after changing your username, you have a 14-day period to revert to your original username for free.