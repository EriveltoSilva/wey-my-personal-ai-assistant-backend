# AgentHub Backend - Python FastAPI

## Reference
Essential:
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

AgentHub is a SaaS platform that allows users to interact with specialized AI agents across different professional domains. This backend provides the API infrastructure for managing agents, chats, users, and AI interactions.


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

## 🌟 Features

### ✅ Implemented (MVP Core)

#### **1. Specialized AI Agents**
- **5 Pre-configured Agents**: Marketing Pro, Finance Advisor, Legal Consultant, Sales Expert, HR Specialist
- Each agent with unique personality, expertise, and conversation style
- Agent rating and usage tracking
- Example conversations for each agent

#### **2. Chat System**
- Real-time conversations with AI agents
- Complete message history and context preservation
- Multiple chat sessions per agent
- Automatic title generation
- Chat sharing capabilities
- Message feedback and rating system

#### **3. User Management**
- JWT-based authentication with refresh tokens
- User profiles with professional information
- Onboarding flow to match users with relevant agents
- User dashboard with statistics and recommendations

#### **4. Dashboard & Analytics**
- User overview with chat statistics
- Recent conversations
- Recommended agents based on user profile
- Featured agents showcase

#### **5. API & Integration**
- RESTful API with comprehensive documentation
- OpenAPI/Swagger integration
- WebSocket support for real-time features
- Proper error handling and validation

## 🏗️ Architecture

### **Technology Stack**
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Integration**: OpenAI GPT-4
- **Authentication**: JWT with refresh tokens
- **API Docs**: OpenAPI/Swagger
- **Async Support**: Full async/await implementation

### **Project Structure**
```
src/
├── agents/           # AI Agents management
│   ├── models.py     # Agent and AgentExample models
│   ├── schemas.py    # Pydantic schemas for validation
│   ├── services.py   # Business logic for agents
│   ├── routes.py     # API endpoints
│   └── enums.py      # Agent categories and configurations
├── chats/           # Chat and messaging system
│   ├── models.py     # Chat and Message models
│   ├── schemas.py    # Chat request/response schemas
│   ├── services.py   # Chat logic and AI integration
│   ├── routes.py     # Chat API endpoints
│   └── enums.py      # Chat and message enums
├── users/           # User management (existing)
├── auth/            # Authentication (existing)
├── dashboard/       # Dashboard and analytics
├── core/           # Core configuration and database
│   ├── database.py   # Database connection and models
│   ├── config.py     # Settings and configuration
│   ├── seed_data.py  # Initial data seeding
│   └── models_list.py # Model imports for migrations
├── exceptions/      # Custom exceptions (existing)
└── main.py         # FastAPI application entry point
```

### **Database Models**

#### **Agents**
- `Agent`: AI agent configuration and metadata
- `AgentExample`: Example conversations for each agent

#### **Chats**
- `Chat`: Chat sessions between users and agents
- `Message`: Individual messages with AI metadata

#### **Users** (Enhanced)
- Professional profile fields for agent matching
- Onboarding completion tracking
- Usage preferences and statistics

## 🚀 Quick Start

### **Prerequisites**
- Python 3.10+
- PostgreSQL 12+
- OpenAI API Key (for AI functionality)

### **Installation**

1. **Clone and Setup**
   ```bash
   cd agent-hub-backend-python
   ./setup.sh
   ```

2. **Manual Setup** (if script fails)
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Create database
   createdb agenthub_dev

   # Copy environment file
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Environment Configuration**
   Create `.env` file with:
   ```env
   # Database
   DATABASE_DEV_URL=postgresql+asyncpg://postgres:password@localhost:5432/agenthub_dev
   
   # OpenAI
   OPENAI_API_KEY=your-openai-api-key-here
   
   # Security
   SECRET_KEY=your-super-secret-key-change-this
   
   # Admin User
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=admin123
   ADMIN_EMAIL=admin@agenthub.com
   ```

4. **Run the Server**
   ```bash
   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

### **Initial Setup**
The server will automatically:
- Create database tables
- Create admin user
- Seed the 5 core AI agents with examples

## 📚 API Documentation

### **Access Points**
- **API Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### **Core Endpoints**

#### **Authentication**
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh access token

#### **Dashboard**
- `GET /api/v1/dashboard/` - User dashboard with stats and recommendations
- `POST /api/v1/dashboard/complete-onboarding` - Complete user onboarding

#### **Agents**
- `GET /api/v1/agents/` - List all agents with filtering
- `GET /api/v1/agents/featured` - Get featured agents
- `GET /api/v1/agents/recommended` - Get personalized recommendations
- `GET /api/v1/agents/{agent_id}` - Get agent details with examples
- `POST /api/v1/agents/{agent_id}/rate` - Rate an agent

#### **Chats**
- `GET /api/v1/chats/` - User's chat history
- `POST /api/v1/chats/` - Create new chat session
- `GET /api/v1/chats/{chat_id}` - Get chat with messages
- `POST /api/v1/chats/{chat_id}/messages` - Send message and get AI response
- `POST /api/v1/chats/{chat_id}/share` - Share chat publicly

### **Example Usage**

#### **Start a Conversation**
```bash
# 1. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password"}'

# 2. Get agents
curl -X GET "http://localhost:8000/api/v1/agents/featured" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. Create chat
curl -X POST "http://localhost:8000/api/v1/chats/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "AGENT_ID", "first_message": "Hello, I need help with marketing strategy"}'

# 4. Send message
curl -X POST "http://localhost:8000/api/v1/chats/CHAT_ID/messages" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "What are the best social media platforms for a small business?"}'
```

## � Agent Specializations

### **1. Marketing Pro** 📈
- **Expertise**: Digital marketing, brand strategy, social media
- **Use Cases**: Campaign planning, SEO guidance, content strategy
- **Tools**: Market research, presentation generator

### **2. Finance Advisor** 💰
- **Expertise**: Personal finance, investments, business finance
- **Use Cases**: Budget planning, investment advice, financial analysis
- **Tools**: Financial calculator, analysis tools

### **3. Legal Consultant** ⚖️
- **Expertise**: Business law, contracts, intellectual property
- **Use Cases**: Contract review, legal procedures, compliance
- **Tools**: Legal research, document analysis

### **4. Sales Expert** 🎯
- **Expertise**: Sales strategy, lead generation, CRM
- **Use Cases**: Sales process optimization, negotiation techniques
- **Tools**: Email drafting, presentation tools

### **5. HR Specialist** 👥
- **Expertise**: Talent management, policies, culture
- **Use Cases**: Recruitment, employee development, compliance
- **Tools**: Document analysis, policy templates

## 🔧 Development

### **Database Migrations**
```bash
# The app automatically creates tables on startup
# For manual database reset:
python -c "from src.core.database import create_db; import asyncio; asyncio.run(create_db())"
```

### **Seeding Data**
```bash
# Reseed agents and examples
python -c "from src.core.seed_data import seed_agents; import asyncio; asyncio.run(seed_agents())"
```

### **Running Tests**
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### **Code Quality**
```bash
# Install development tools
pip install black isort flake8

# Format code
black src/
isort src/

# Check code quality
flake8 src/
```

## 🚦 Roadmap

### **Completed ✅**
- [x] Core agent system with 5 specialized agents
- [x] Chat system with AI integration
- [x] User authentication and profiles
- [x] Dashboard with recommendations
- [x] API documentation and validation
- [x] Database models and relationships
- [x] OpenAI integration with fallback

### **Next Phase 🔄**
- [ ] WebSocket real-time chat
- [ ] File upload and analysis
- [ ] Agent customization
- [ ] Usage analytics and reporting
- [ ] Rate limiting and quotas
- [ ] Advanced AI tools integration

### **Future Enhancements 🔮**
- [ ] Multi-language support
- [ ] Voice chat capabilities
- [ ] Agent marketplace
- [ ] Enterprise features
- [ ] Mobile API optimizations

## 🐳 Docker Deployment

### **Development**
```bash
# Using existing docker-compose.yml
docker-compose up -d
```

### **Production**
```bash
# Build production image
docker build -t agenthub-backend .

# Run with production settings
docker run -e DEBUG=false -e DATABASE_PROD_URL=... agenthub-backend
```

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_DEV_URL` | Development database URL | `postgresql+asyncpg://...` |
| `DATABASE_PROD_URL` | Production database URL | - |
| `OPENAI_API_KEY` | OpenAI API key for AI responses | - |
| `SECRET_KEY` | JWT signing secret | - |
| `DEBUG` | Enable debug mode | `true` |
| `ADMIN_USERNAME` | Initial admin username | `admin` |
| `ADMIN_PASSWORD` | Initial admin password | `admin123` |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the agent examples for usage patterns

---

**AgentHub** - Democratizing access to specialized AI expertise 🚀
