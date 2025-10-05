# 🧠 Wey, a Jarvis-Like AI Assistant (Backend)

This is the **backend** of `Wey` — my personal **AI-powered, Jarvis-like assistant**.
It handles **AI orchestration**, **conversation management**, **database operations**, and **IoT communication** between the user and connected smart devices.

This project is a personal challenge that merges my knowledge in **Python**, **FastAPI**, **LangChain**, **AI**, and **IoT**, with the long-term goal of building an **intelligent, context-aware assistant** capable of interacting with both digital and physical systems.

---

## 🚀 Project Overview

The backend acts as the **brain** of the Wey assistant, responsible for:

* **User Authentication & Management** - JWT-based authentication system with user registration/login
* **Real-time Chat Communication** - WebSocket connections for instant messaging
* **AI-Powered Conversations** - LangChain integration with OpenAI and Google Gemini models
* **Streaming Responses** - Real-time AI response streaming to frontend
* **Database Operations** - Async PostgreSQL operations with SQLAlchemy 2.0
* **Background Task Processing** - Async task management for heavy operations
* **API Route Management** - RESTful endpoints for all frontend interactions
* **Agent System** - Modular agent architecture for different AI capabilities

The system features a complete user management system, chat persistence, real-time communication, and a scalable architecture designed for production deployment.

---

## 🧩 Tech Stack

| Layer                      | Technologies                     |
| -------------------------- | -------------------------------- |
| **Framework**              | FastAPI 0.116+                  |
| **AI / Orchestration**     | LangChain 0.3+, OpenAI API, Google Gemini |
| **Database**               | PostgreSQL + SQLAlchemy 2.0 (Async) |
| **Authentication**         | JWT (PyJWT), Password Hashing (argon2) |
| **Real-time Communication** | WebSockets, Background Tasks |
| **Async Processing**       | asyncio, asyncpg               |
| **Environment Management** | Python-dotenv, Pydantic Settings |
| **Development Tools**      | Uvicorn, Rich logging          |
| **Deployment**             | Docker, Uvicorn (production ready) |

---

## 🧠 Features

### ✅ Version 1.0 - Authentication & Core API

* **User Authentication System**
  - User registration and login endpoints
  - JWT token-based authentication
  - Password hashing with Argon2
  - Protected route middleware
* **User Management**
  - User profiles with interests and professional areas
  - User settings and preferences
* **Database Infrastructure**
  - PostgreSQL with SQLAlchemy 2.0 (async)
  - Database migrations and seeding
  - Connection pooling and optimization

### ✅ Version 1.5 - Real-time Chat System

* **WebSocket Communication**
  - Real-time bidirectional messaging
  - Connection management and authentication
  - Message broadcasting and routing
* **Chat Management**
  - Multiple chat rooms per user
  - Chat history persistence
  - Message threading and organization
* **AI Integration**
  - LangChain orchestration for conversations
  - OpenAI and Google Gemini model support
  - Streaming response generation
  - Background task processing for AI operations

### ⚡ Version 2.0 (in development)

* **Agent System**
  - Modular agent architecture
  - Agent registration and management
  - Specialized agents for different tasks
* **Advanced AI Features**
  - Tool-based reasoning and execution
  - Context-aware conversations
  - Multi-model support and switching

### 🔊 Future Versions

* **IoT Integration**
  - MQTT communication with smart devices
  - Device state management
  - Command execution and feedback
* **External Integrations**
  - Web search capabilities
  - Third-party API connections
  - Voice message handling (STT/TTS)
* **Enterprise Features**
  - Multi-tenant architecture
  - Advanced analytics and monitoring
  - Scalable deployment options

---

## 🧠 Architecture Overview

```mermaid
graph TD
    A[Frontend React App] -->|HTTP + WebSocket| B[FastAPI Backend]
    B -->|JWT Auth| C[Authentication Middleware]
    C -->|User Session| D[Protected Routes]
    
    D -->|Chat Messages| E[WebSocket Manager]
    E -->|Real-time| F[Chat Service]
    F -->|AI Processing| G[LangChain Integration]
    G -->|LLM Calls| H[OpenAI / Gemini APIs]
    
    F -->|Persist| I[PostgreSQL Database]
    I -->|SQLAlchemy 2.0| J[Async DB Operations]
    
    K[Background Tasks] -->|Process| F
    L[Agent System] -->|Modular AI| G
    
    B -->|User Management| M[User Service]
    M -->|Store Profiles| I
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone git@github.com:EriveltoSilva/wey-my-personal-ai-assistant-backend.git
cd wey-my-personal-ai-assistant-backend
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # on Linux/Mac
venv\Scripts\activate      # on Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup environment variables

Create a `.env` file in the backend root directory:

```env
# Project Settings
PROJECT_NAME=Wey AI Assistant
PROJECT_DESCRIPTION=Personal AI Assistant Backend
DEBUG=true
FRONTEND_URL=http://localhost:5173

# Database Configuration
DATABASE_DEV_URL=postgresql+asyncpg://user:password@localhost:5432/wey_db
DATABASE_PROD_URL=postgresql+asyncpg://user:password@prod-host:5432/wey_db
DATABASE_ECHO=true

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Models
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key

# API Configuration
API_VERSION=v1
API_V1_STR=/api/v1
```

### 5️⃣ Run the server
```bash
uvicorn  src.main:app  --host 0.0.0.0  --port 8000  --reload --> development
uvicorn  src.main:app  --host 0.0.0.0  --port 8000  --> production

```

By default, the backend runs on [http://localhost:8000](http://localhost:8000)

---

## 🏗️ Project Structure

```
backend/
│
├── src/                          # Source code directory
│   ├── main.py                   # FastAPI application entry point
│   │
│   ├── core/                     # Core application components
│   │   ├── config.py            # Application settings and environment variables
│   │   ├── security.py          # Authentication and security utilities
│   │   ├── logger.py            # Logging configuration
│   │   ├── models_list.py       # Available AI models configuration
│   │   ├── schemas.py           # Shared Pydantic schemas
│   │   └── database/            # Database configuration and utilities
│   │
│   ├── auth/                     # Authentication module
│   │   ├── routes.py            # Authentication endpoints (login, register)
│   │   └── schemas.py           # Auth-related Pydantic models
│   │
│   ├── users/                    # User management module
│   │   ├── routes.py            # User CRUD endpoints
│   │   ├── models.py            # User database models
│   │   ├── schemas.py           # User Pydantic models
│   │   ├── services.py          # User business logic
│   │   ├── enums.py             # User-related enumerations
│   │   ├── interest_routes.py   # User interests management
│   │   └── professional_area_routes.py # Professional areas management
│   │
│   ├── chats/                    # Chat system module
│   │   ├── routes.py            # Chat CRUD endpoints
│   │   ├── routes_streaming.py  # Real-time chat streaming endpoints
│   │   ├── models.py            # Chat and message database models
│   │   ├── schemas.py           # Chat Pydantic models
│   │   ├── schemas_streaming.py # Streaming-specific schemas
│   │   ├── services.py          # Chat business logic and AI integration
│   │   ├── enums.py             # Chat-related enumerations
│   │   ├── prompts.py           # AI system prompts and templates
│   │   └── background_tasks.py  # Async task processing
│   │
│   ├── agents/                   # AI Agent system
│   │   ├── routes.py            # Agent management endpoints
│   │   ├── models.py            # Agent database models
│   │   ├── schemas.py           # Agent Pydantic models
│   │   ├── services.py          # Agent business logic
│   │   └── enums.py             # Agent-related enumerations
│   │
│   ├── websocket/                # WebSocket communication
│   │   ├── routes.py            # WebSocket connection handling
│   │   ├── manager.py           # WebSocket connection manager
│   │   ├── chat_message_service.py # WebSocket message processing
│   │   └── schemas.py           # WebSocket message schemas
│   │
│   ├── exceptions/               # Error handling
│   │   ├── __init__.py          # Custom exception definitions
│   │   └── exception_handlers.py # Global exception handlers
│   │
│   ├── general/                  # General utilities
│   │   └── text.py              # Text processing utilities
│   │
│   ├── data/                     # Static data files
│   │   └── user_white_list.json # User whitelist configuration
│   │
│   └── tests/                    # Test modules
│       ├── test_chat.py         # Chat functionality tests
│       ├── test_hello.py        # Basic API tests
│       └── test_stream.py       # Streaming functionality tests
│
├── uploads/                      # File upload directory
├── docs/                         # Documentation
├── examples/                     # Example scripts and usage
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker containerization
└── README.md                     # This file
```

---

## � API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile
- `GET /api/v1/users/interests` - Get user interests
- `GET /api/v1/users/professional-areas` - Get professional areas

### Chats
- `POST /api/v1/chats` - Create new chat
- `GET /api/v1/chats` - List user's chats
- `GET /api/v1/chats/{chat_id}` - Get specific chat
- `GET /api/v1/chats/{chat_id}/messages` - Get chat messages
- `DELETE /api/v1/chats/{chat_id}` - Delete chat

### Real-time Communication
- `WS /ws?token={jwt_token}` - WebSocket connection for real-time chat
- `POST /api/v1/chat/stream` - Streaming chat responses

### Agents
- `GET /api/v1/agents` - List available agents
- `POST /api/v1/agents` - Create new agent
- `GET /api/v1/agents/{agent_id}` - Get agent details

### Health & Documentation
- `GET /` - API health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

---

## �💡 Roadmap

| Version  | Goal                                            | Status |
| -------- | ----------------------------------------------- | ------ |
| **v1.0** | ✅ User authentication & basic chat functionality | ✅ Complete |
| **v1.5** | ✅ WebSocket communication & AI streaming responses | ✅ Complete |
| **v2.0** | 🔄 Agent system & advanced AI capabilities     | 🔄 In Progress |
| **v2.5** | 📋 IoT integration via MQTT                   | 📋 Planned |
| **v3.0** | 🚀 Tool-based reasoning & external integrations | 🚀 Future |
| **v4.0** | 🌐 Enterprise features & scalable deployment  | 🌐 Future |

---

## 🤖 Author

**Erivelto Clénio da Costa e Silva**
Software Developer | AI & IoT Enthusiast | Partner of K.A Solutions
🌐 [Portfolio](https://eriveltosilva.com)

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

---

## ⚙️ Future Vision

> “The Wey Assistant is more than an AI chatbot — it’s a bridge between intelligence, automation, and the physical world.”




## Reference
Essential:
1. [LangGraph Quickstart](https://langchain-ai.github.io/langgraph/agents/agents/)
2. [LangGraph Graph API Concepts](https://langchain-ai.github.io/langgraph/concepts/low_level/)
3. [Basic Chatbot with LangGraph](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/)
4. [Add tools - LangGraph](https://langchain-ai.github.io/langgraph/tutorials/get-started/2-add-tools/)


[DataStreaming with LangChain & FastAPI](https://www.youtube.com/watch?v=Gn54EbU9mRg)
[LangChain Streaming - stream, astream, astream_events API & FastAPi Integration](https://www.youtube.com/watch?v=juzD9h9ewV8)
https://www.youtube.com/watch?v=xTTtqwGWemw
https://github.com/Coding-Crashkurse/FastAPI-LangChain-Streaming


Others:
[LangChain & FastAPI - Customized, secured ChatBot with JWT Authentication](https://www.youtube.com/watch?v=OqT3hKYoeTQ)
[Build an AI CHatbot with Live Web Search | Python Tutorial (LangGraph + React + FastAPI)](https://www.youtube.com/watch?v=bZObGhl7RAo)
[RAG in Production - LangChain & FastAPI](https://www.youtube.com/watch?v=Arf7UwWjGyc)
[Build a Modular RAG Chatbot with FastAPI, Streamlit & ChromaDB | PDF Chatbot using LLAMA + Groq](https://www.youtube.com/watch?v=TxtK6NUUklQ)

[Bases of Streaming with FastAPI and LangChain](https://github.com/Coding-Crashkurse/LangChain-FastAPI-Streaming)
https://github.com/snsupratim/RagBot-2.0/tree/main
https://python.langchain.com/docs/tutorials/qa_chat_history/
https://www.youtube.com/playlist?list=PL8hP5HjAnJ3-14JfI4iEVArq_kPG0HY-N
https://www.youtube.com/watch?v=8h6oWnNgkGA&t=1s

### Playlists
[Updated Langchain](https://www.youtube.com/playlist?list=PLZoTAELRMXVOQPRG7VAuHL--y97opD5GQ)
[FastAPI](https://www.youtube.com/playlist?list=PLgwf8yxWVbBj2FEaKP24NUz-8L5ANBlta)
[LangGraph Crash Course: From Basic to Building Powerful Agents | 2025](https://www.youtube.com/watch?v=WPgG_PlOsYs&list=PLNIQLFWpQMRXmns-7UarmPIR6DN7bgEzZ)


- https://www.youtube.com/watch?v=y2cRcOPHL_U
- https://www.youtube.com/watch?v=d9zbCsOpWCQ
- https://www.youtube.com/watch?v=8gx3wrGi7_U
- https://www.youtube.com/watch?v=1h6lfzJ0wZw
- https://www.youtube.com/watch?v=n0uPzvGTFI0
- https://www.youtube.com/watch?v=3o4mAJhT2HY
- https://www.youtube.com/watch?v=y2cRcOPHL_U
- https://www.youtube.com/watch?v=LzxSY7197ns
- https://www.youtube.com/watch?v=b3XsvoFWp4c&t=1026s
- https://www.youtube.com/watch?v=aeCPM0HXiuw
- https://www.youtube.com/watch?v=t2bSApmPzU4
- https://www.youtube.com/watch?v=n0uPzvGTFI0
- https://www.youtube.com/watch?v=juzD9h9ewV8
- https://www.youtube.com/watch?v=xTTtqwGWemw
- https://www.youtube.com/watch?v=JEBDfGqrAUA
- https://mirascope.com/blog/langchain-prompt-template
- https://medium.com/@mrcoffeeai/prompttemplate-and-chatprompttemplate-explained-87291576c6de
- https://dashboard.render.com/web/srv-d2aj2849c44c738u5me0/logs

