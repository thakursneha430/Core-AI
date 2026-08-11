<div align="center">

# 🧠 CORE AI

### Your Intelligent Document Assistant for Instant Answers

Upload documents, ask questions naturally, and receive accurate AI-generated answers with source references.

<p>

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-red?style=flat-square)
![Gemini](https://img.shields.io/badge/Google-Gemini-blue?style=flat-square)

</p>

</div>

---

## 📖 About

**CORE AI** is an AI-powered document intelligence system that allows users to upload documents and interact with them using natural language.

Instead of manually searching through pages, CORE AI understands document content, retrieves the most relevant information using semantic search, and generates accurate responses using Google's Gemini model.

Every answer is supported with relevant source chunks, making responses transparent and reliable.

---

## ✨ Features

- 📄 Upload PDF documents
- 💬 Ask questions in natural language
- 🧠 AI-powered document understanding
- 🔍 Semantic search with vector embeddings
- 📚 Retrieval-Augmented Generation (RAG)
- 🤖 Google Gemini integration
- 📌 Source-backed responses
- ⚡ FastAPI backend
- 🐳 Dockerized application
- 🎨 Interactive web interface

---

## 🏗️ Architecture

```text
                 Upload Document
                        │
                        ▼
             Document Processing
                        │
                        ▼
           Text Cleaning & Chunking
                        │
                        ▼
            Embedding Generation
                        │
                        ▼
             ChromaDB Vector Store
                        │
                        ▼
             Semantic Retrieval
                        │
                        ▼
                Google Gemini
                        │
                        ▼
        AI Response + Source References
```

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend Development |
| FastAPI | REST API |
| Google Gemini | Large Language Model |
| ChromaDB | Vector Database |
| BAAI/bge-small-en-v1.5 | Embedding Model |
| Docker | Containerization |
| HTML | Frontend |
| CSS | Styling |
| JavaScript | Frontend Logic |

---

## 📂 Project Structure

```text
CORE-AI
│
├── api/
├── frontend/
├── src/
│   ├── ingestion/
│   ├── processing/
│   ├── embeddings/
│   ├── vectorstore/
│   ├── rag/
│   └── pipeline/
│
├── data/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/yourusername/CORE-AI.git

cd CORE-AI
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Using Docker

```bash
docker build -t core-ai .

docker run --rm -p 8000:8000 --env-file .env core-ai
```

Open your browser:

```
http://localhost:8000
```

---

## 💡 Example Questions

- Summarize this document.
- What are the key insights?
- Explain the second section.
- List the important topics.
- Who is the author?
- What skills are mentioned?

---

## 📸 Demo

<p align="center">
Add screenshots or GIFs of your application here.
</p>

---

## 🎯 Future Improvements

- 📑 Multiple document support
- 💬 Conversation history
- ⚡ Streaming AI responses
- 🖼 OCR support for scanned documents
- 🧠 Multimodal image understanding
- 🔐 User authentication
- ☁ Cloud deployment

---

## 🤝 Contributing

Contributions, ideas, and suggestions are always welcome.

If you'd like to improve CORE AI, feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is developed for educational, learning, and portfolio purposes.

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a Star!

**Built with ❤️ by Sneha**

</div>

