# Adaptive RAG - AI Chatbot

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.5.4-orange.svg)](https://python.langchain.com/langgraph/)
[![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-purple.svg)](https://qdrant.tech/)

## 📋 About the Project

**Adaptive RAG** is an AI-powered chatbot that can answer questions from your own uploaded documents. You can upload a PDF or text file, ask questions about it, and the system will find the most relevant answers.

It smartly decides whether to answer from your uploaded documents, use its general knowledge, or search the web in real time — all automatically.

---

## ✨ Features

- **Upload Documents**: Upload PDF or TXT files and chat with them
- **Smart Query Routing**: Automatically picks the best way to answer your question
- **Web Search**: Can search the web for real-time information when needed
- **Chat History**: Remembers your conversation using MongoDB
- **Simple Web UI**: Easy-to-use chat interface built with Streamlit
- **REST API**: FastAPI backend with clean endpoints

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.9+ |
| AI Framework | LangChain + LangGraph |
| Backend API | FastAPI |
| Frontend UI | Streamlit |
| Vector Database | Qdrant |
| Chat Database | MongoDB |
| LLM Provider | OpenAI (GPT-4o) |
| Web Search | Tavily |

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed and ready:
- Python 3.9 or higher
- MongoDB (local or cloud)
- Qdrant vector database
- OpenAI API key
- Tavily API key (for web search)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Adaptive-Rag.git
cd Adaptive-Rag

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root folder and add your keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_CODE_COLLECTION=code_documents
QDRANT_DOCS_COLLECTION=documents

MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=adaptive_rag
```

### Running the App

Open two terminals:

**Terminal 1 — Start the backend:**
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Start the frontend:**
```bash
streamlit run streamlit_app/home.py
```

Then open your browser:
- **Chat App**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

---

## 💬 How to Use

1. Go to http://localhost:8501
2. Create an account or log in
3. Upload a PDF or TXT file from the sidebar
4. Start asking questions in the chat!

---

## 📁 Project Structure

```
AdaptiveRag/
├── src/                        # Main backend code
│   ├── main.py                 # FastAPI app entry point
│   ├── api/routes.py           # API endpoints
│   ├── rag/                    # RAG pipeline logic
│   │   ├── graph_builder.py    # LangGraph workflow
│   │   ├── nodes.py            # Pipeline steps
│   │   └── document_upload.py  # Document processing
│   ├── memory/                 # Chat history
│   ├── models/                 # Data schemas
│   └── tools/                  # Utility functions
│
├── streamlit_app/              # Frontend UI
│   ├── home.py                 # Login page
│   └── pages/chat.py           # Chat interface
│
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔌 API Endpoints

### Ask a Question
```http
POST /rag/query
Content-Type: application/json

{
  "query": "What is the document about?",
  "session_id": "user_123"
}
```

### Upload a Document
```http
POST /rag/documents/upload
X-Description: Brief description of the document

Form Data:
- file: <your PDF or TXT file>
```

---

## 🙏 Acknowledgments

- Developed in collaboration with **Dhruv Singhal** ([@dhruvsinghal09](https://github.com/dhruvsinghal09))
- Built using [LangChain](https://www.langchain.com/) and [LangGraph](https://python.langchain.com/langgraph/)
- Vector search by [Qdrant](https://qdrant.tech/)
- LLM by [OpenAI](https://openai.com/)
- Web search by [Tavily](https://tavily.com/)

---

## 👤 Author

**Parth Dangaria**

---

## 📄 License

This project is licensed under the MIT License.
