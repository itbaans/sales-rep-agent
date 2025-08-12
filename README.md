# Sales Agent RAG App

This repository contains a modular implementation of a sales-oriented AI agent powered by Retrieval-Augmented Generation (RAG) and optional speech capabilities. The project is organized into clear components for easy navigation and development.

## 📂 Project Structure

### **1. `agent/`**
Contains the core **agentic workflow** for the sales agent. This is where the logic for how the agent processes queries, retrieves information, and generates responses is implemented.

### **2. `audio/`**
Work-in-progress (**WIP**) implementation for **Text-to-Speech (TTS)** and **Speech-to-Text (STT)**.  
⚠️ Expect a lot of experimentation and unfinished code here.

### **3. `vectorstores/`**
Contains **RAG (Retrieval-Augmented Generation)** implementations.  
Two retrieval modes are supported:

- **JSON RAG** – Optimized for structured data like case studies, pricing, policies, etc.
  - Keys from the JSON files are stored as vectors.
  - Queries are matched to keys via vector similarity, and the corresponding values are returned.
  - Provides **fast retrieval** for common knowledge questions.

- **PDF/Document RAG** – Used for unstructured or semi-structured documents.
  - Implements a **chunking-based RAG** for content extraction and retrieval.
  - Useful for processing larger, less-structured files.

### **4. `UI/`**
A simple **chat interface** for interacting with the agent.  
Currently implemented using **Streamlit** for a quick web UI experience.

## 🚀 Running the Application

### **Command Line Interface (CLI)**
```bash
uv run main.py
```

### **Web UI (Streamlit)**
```bash
uv run main.py streamlit
```

### **Voice Integration (WIP)**
audio_wip.py contains a voice loop integration (agent listens and responds via speech).
Currently not functional due to local voice model dependencies that require manual modifications in certain libraries.
