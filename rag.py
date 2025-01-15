from cryptography.fernet import Fernet
from groq import Groq
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Generate an encryption key for PII masking
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_pii(data):
    """Encrypt PII data."""
    return cipher.encrypt(data.encode()).decode()

def mask_pii(text):
    """Mask PII data in text using regex."""
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "[EMAIL REDACTED]", text)
    text = re.sub(r'\+?\d[\d -]{8,}\d', "[PHONE REDACTED]", text)
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', "[SSN REDACTED]", text)
    return text

# Example Chat Data
chat_data = [
    {"user": "Hi, my name is John Smith. My email is john.smith@example.com and my phone is +1-555-123-4567.",
     "specialist": "Hi John, I’m Emily. I can help you resolve this issue."},
    {"user": "Hello, I’m Sarah Johnson. I’m facing an issue with my laptop. Email: sarah.johnson@example.com.",
     "specialist": "Hi Sarah, let me guide you through some troubleshooting steps."},
    {"user": "Hi, this is William. My phone number is +1-555-567-8901, and I forgot my password.",
     "specialist": "Hi William, I’ll help you reset your password now."},
]

# Encrypt and Mask PII in Data
for chat in chat_data:
    chat['user'] = encrypt_pii(chat['user'])
    chat['specialist'] = encrypt_pii(chat['specialist'])

# Vector DB Initialization
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.from_texts([chat['user'] + " " + chat['specialist'] for chat in chat_data], embeddings)

# Retrieval Function
def retrieve_best_chats(query, top_k=3):
    retriever = vector_store.as_retriever()
    docs = retriever.get_relevant_documents(query)
    return docs[:top_k]

# LLM Integration
def generate_response_with_context(query, context_docs):
    
    context = "\n".join([mask_pii(doc.page_content) for doc in context_docs])
    prompt = f"""
    Context:
    {context}
    
    Query:
    {query}
    
    Please provide a helpful response based on the above context while ensuring no PII is disclosed.
    """
    response = chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are an helpful assistant"},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content

# Example Query
query = "williams phone numer"
context_docs = retrieve_best_chats(query)

# Generate Response
response = generate_response_with_context(query, context_docs)
print(response)
