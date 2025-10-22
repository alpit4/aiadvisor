# AI Supervisor System

A human-in-the-loop AI system for managing customer relationships with intelligent escalation.

## 🎯 Overview

This system implements a complete human-in-the-loop AI supervisor for customer service. When the AI doesn't know an answer, it escalates to a human supervisor, learns from the response, and follows up with the customer.

## ✨ Features

- **Voice AI Agent**: Handles customer calls with salon business knowledge
- **Smart Escalation**: Automatically escalates unknown questions to supervisors
- **Real-time Notifications**: Supervisors get instant alerts for escalations
- **Knowledge Base**: Learns and stores answers from supervisor interactions
- **Supervisor Dashboard**: Web UI for managing help requests
- **Interactive Demo**: Type questions and see AI responses in real-time
- **Human-in-the-Loop**: Complete workflow from AI to human to learning
- **Request Lifecycle**: Pending → Resolved/Unresolved with proper tracking

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test the System

```bash
python simple_test.py
```

### 3. Start the Voice AI Demo

```bash
python interactive_voice_demo.py
```

### 4. Start the Supervisor Dashboard

```bash
python simple_main.py
```

### 5. Access the Dashboard

- Main server: http://localhost:8000
- Supervisor UI: http://localhost:8000/supervisor

## 🏗️ Architecture

### Core Components

1. **Main Application** (`simple_main.py`)

   - Phase 1 entry point without LiveKit dependencies
   - Starts FastAPI server for supervisor dashboard
   - Handles HTTP requests and responses

2. **Help Request System** (`src/database.py`)

   - Manages request lifecycle (Pending → Resolved/Unresolved)
   - Tracks customer information and questions
   - SQLAlchemy models for data persistence

3. **Knowledge Base** (`src/knowledge_base.py`)

   - Stores and retrieves learned answers
   - Simple keyword matching for question answering
   - Automatically learns from supervisor responses

4. **Supervisor UI** (`src/supervisor_ui_simple.py`)

   - Web dashboard for managing help requests
   - View pending, resolved, and unresolved requests
   - Manage knowledge base entries

5. **Voice AI System** (`interactive_voice_demo.py`, `voice_demo.py`)

   - Interactive voice demo for testing
   - Full LiveKit voice integration (Phase 2)
   - Real-time AI responses and escalation

6. **Testing & Setup** (`simple_test.py`, `add_test_data.py`)
   - System verification and testing
   - Database population with sample data

### Database Schema

- **HelpRequest**: Stores customer questions and supervisor responses
- **KnowledgeEntry**: Stores learned answers for the AI agent

## 🎨 Design Decisions

### Database Choice

- **SQLite**: Chosen for simplicity and portability
- **Rationale**: Easy setup, no external dependencies, sufficient for demo

### Request Lifecycle

- **Pending**: Initial state when AI doesn't know answer
- **Resolved**: Supervisor provided answer
- **Unresolved**: Request timed out or couldn't be resolved

### Knowledge Base

- **Simple keyword matching**: For demo purposes
- **Automatic learning**: From supervisor responses
- **Context tracking**: Links answers to original requests

### Scalability Considerations

- **Database indexing**: On status, created_at, timeout_at
- **Modular design**: Easy to replace components
- **Background processing**: Timeout manager runs independently
- **Stateless design**: Can scale horizontally

## 🎯 Demo Instructions

### Voice AI Demo

1. **Start the interactive demo**:

   ```bash
   python interactive_voice_demo.py
   ```

2. **Type questions** as if you're calling the salon:

   - "What are your hours?"
   - "Do you offer hair coloring?"
   - "How much does a massage cost?"

3. **Watch the AI respond** and escalate unknown questions

4. **See real-time notifications** when escalation happens

### Supervisor Dashboard

1. **Start the dashboard**:

   ```bash
   python simple_main.py
   ```

2. **Visit**: http://localhost:8000/supervisor

3. **See escalated requests** from the voice demo

4. **Respond to requests** and watch the AI learn

### Full LiveKit Integration (Phase 2)

For complete voice calls with LiveKit:

1. **Set up your .env file** with LiveKit credentials
2. **Run the full voice demo**:
   ```bash
   python voice_demo.py
   ```
3. **Make actual voice calls** using LiveKit

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=sqlite:///./ai_supervisor.db

# Server Configuration
HOST=0.0.0.0
PORT=8000

# LiveKit Configuration (Phase 2 - Optional)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# OpenAI Configuration (Required for voice AI)
OPENAI_API_KEY=your_openai_api_key
```

### Business Configuration

- Salon name, hours, services, and pricing
- Request timeout duration (default: 30 minutes)
- Knowledge base matching threshold

## 📊 Usage Examples

### 1. Customer Calls AI

```
Customer: "What are your hours?"
AI: "Our hours are Monday-Friday: 9AM-7PM, Saturday: 9AM-5PM, Sunday: Closed"
```

### 2. AI Escalates to Supervisor

```
Customer: "Do you offer pet grooming?"
AI: "Let me check with my supervisor and get back to you."
[Creates help request, notifies supervisor]
```

### 3. Supervisor Responds

```
Supervisor: "No, we don't offer pet grooming services."
[AI learns answer, notifies customer]
```

## 🚀 Deployment

### Local Development

```bash
python main.py
```

### Production Considerations

- Use PostgreSQL instead of SQLite
- Add proper logging and monitoring
- Implement authentication for supervisor UI
- Add rate limiting and security measures
- Use proper secret management

## 🧪 Testing

### Run System Tests

```bash
python test_system.py
```

### Manual Testing

1. Start the server
2. Visit supervisor dashboard
3. Create test help requests
4. Test supervisor responses
5. Verify knowledge base updates

## 📈 Monitoring

### Key Metrics

- Pending requests count
- Resolution time
- Knowledge base growth
- Timeout rate
- Customer satisfaction

### Logs

- Request creation and resolution
- Supervisor notifications
- Timeout events
- Knowledge base updates

## 🔮 Future Enhancements

### Phase 2 Features

- Live call transfer to supervisor
- Real-time supervisor availability
- Advanced NLP for question matching
- Customer sentiment analysis
- Integration with CRM systems

### Supervisor UI

- `GET /supervisor/` - Dashboard
- `GET /supervisor/requests` - All requests
- `GET /supervisor/knowledge` - Knowledge base
- `POST /supervisor/respond/{id}` - Respond to request
- `POST /supervisor/timeout/{id}` - Mark as unresolved
- `GET /supervisor/api/stats` - System statistics
