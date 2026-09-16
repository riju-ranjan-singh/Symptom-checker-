# Niraksh Guardian - AI Services

This is the local AI service component of the Niraksh Guardian health platform. It provides intelligent health guidance powered by **medgemma1.5** running on **Ollama**.

## 🎯 What This Service Does

- **Health Guidance API**: Provides general, non-diagnostic health information
- **Symptom Discussion**: Helps users understand health concerns through conversational AI
- **Context-Aware Responses**: Considers the last 3 messages to provide coherent, progressive guidance
- **Safety First**: Explicitly avoids medical diagnosis and recommends professional consultation for serious issues
- **Multi-turn Conversations**: Maintains conversational continuity while building on previous information

### Key Features

✅ RESTful API with FastAPI  
✅ Real-time health guidance using local medgemma1.5 model  
✅ Conversation context awareness (tracks last 3 messages)  
✅ Greeting detection to provide appropriate responses  
✅ Health-only scope control (refuses non-medical queries)  
✅ Structured response format (Explanation → Causes → Action Plan)

---

## 📋 Prerequisites

Before running this service, you need:

1. **Python 3.10+** - Download from [python.org](https://www.python.org/downloads/)
2. **Ollama** - Download from [ollama.ai](https://ollama.ai)
3. **Git** (optional, for cloning the repository)

---

## 🚀 Installation & Setup

### Step 1: Install Ollama

**Windows:**

1. Download Ollama from https://ollama.ai
2. Run the installer and follow the installation wizard
3. Restart your computer after installation

**macOS:**

```bash
# Using Homebrew
brew install ollama

# Or download from https://ollama.ai
```

**Linux:**

```bash
curl https://ollama.ai/install.sh | sh
```

### Step 2: Download & Setup medgemma1.5 Model

Once Ollama is installed, pull the medgemma1.5 model:

```bash
ollama pull medgemma1.5
```

This will download the medgemma1.5 model. The download may take a few minutes depending on your internet speed.

### Step 3: Start Ollama Server

The Ollama server should auto-start after installation. If not, run:

```bash
ollama serve
```

You should see output indicating the server is running on `http://localhost:11434`

### Step 4: Setup Python Virtual Environment

Navigate to the ai-services directory:

```bash
cd ai-services
```

Create a virtual environment:

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Service

Make sure you're in the virtual environment and the ai-services directory.

### Start the API Server

```bash
uvicorn main:app --reload --port 8000
```

Expected output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

### Verify It's Working

Open your browser or use curl to test:

```bash
curl http://localhost:8000/
```

You should get:

```json
{ "message": "AI service is working" }
```

---

## 📡 API Endpoints

### 1. Health Check

**Endpoint:** `GET /`

**Response:**

```json
{ "message": "AI service is working" }
```

### 2. Generate Health Guidance

**Endpoint:** `POST /generate`

**Request Body:**

```json
{
	"prompt": "I have a fever and headache"
}
```

### 3. Stream Health Guidance

**Endpoint:** `POST /generate/stream`

**Request Body (JSON):**

```json
{
	"prompt": "I have persistent cough from 3 days",
	"language": "en",
	"image_data": {
		"base64": "<optional-base64-image>",
		"mime_type": "image/png"
	}
}
```

**SSE Events:**

```text
data: {"type":"chunk","delta":"..."}
data: {"type":"chunk","delta":"..."}
data: {"type":"done"}
```

**Response:**

```json
{
	"response": "Explanation:\nFever and headache are common symptoms that can indicate various conditions...\n\nPossible causes or factors:\n- Viral infections (flu, cold)\n- Bacterial infections\n...\n\nWhat to do:\n- Rest in a cool environment\n- Stay hydrated\n- Monitor temperature\n- Seek medical help if symptoms persist..."
}
```

---

## 🔧 Architecture Overview

```
Frontend Request (Chat)
       ↓
Backend Node.js/Express
       ↓
AI Services (Python/FastAPI)
       ↓
Ollama Server
       ↓
medgemma1.5 Model
       ↓
Response → Backend → Frontend
```

### Flow

1. User sends a health query through the web frontend
2. Niraksh Guardian backend (Node.js) forwards the request to this AI service
3. FastAPI processes the request with context handling
4. Ollama generates a response using the local Gemma 2B model
5. Response is returned to the backend and delivered to the user

---

## 🎯 System Instruction & Prompting

The local medgemma1.5 model is guided by a system instruction similar to the Gemini fallback provider:

**Core Role:** "Niraksh AI, an empathetic and highly knowledgeable Smart Healthcare Assistant"

**Key Behaviors:**

- ✅ Responds only to health-related queries
- ✅ Asks 1 targeted question at a time to understand issues
- ✅ Provides helpful, conversational guidance
- ✅ Never diagnoses or prescribes medications
- ✅ Always advises consulting healthcare professionals for serious symptoms

**Response Format:**
Unlike the previous rigid format, medgemma now responds naturally with:

- Flexible structure (paragraphs, bullet points, or sections as needed)
- Conversational tone while maintaining clinical accuracy
- Context-aware follow-ups based on conversation history

To customize the system instruction, edit `build_prompt()` in `main.py`.

---

## ⚙️ Configuration

### Model Configuration

The service uses:

- **Model**: `medgemma1.5`
- **Ollama Endpoint**: `http://localhost:11434/api/generate`
- **Stream**: Enabled via `POST /generate/stream`

To use a different model, edit `main.py` and change:

```python
"model": "medgemma1.5"  # Change to another model
```

Available Ollama models:

- `medgemma1.5` (recommended)
- `llama2` (~4GB)
- `mistral` (~4GB)

Pull other models with:

```bash
ollama pull mistral
# or
ollama pull llama2
```

### Generation Parameters

The service includes safeguards to prevent infinite loops and maintains response quality:

```python
MAX_TOKENS = 1000        # Maximum tokens per response (prevents runaway generation)
TEMPERATURE = 0.7        # Creativity level: 0.0 (deterministic) to 1.0+ (creative)
TOP_P = 0.9             # Nucleus sampling: controls diversity of token selection
```

**Why `TEMPERATURE = 0.7`?**

- Lower (0.0-0.3): Repetitive, deterministic responses
- **0.7 (current):** Good balance of consistency + variety, reduces loops
- Higher (0.9+): More creative but less reliable for health queries

**Adjust if:**

- Responses too repetitive: ↑ Increase `TEMPERATURE` to 0.8–0.9
- Responses too varied: ↓ Decrease `TEMPERATURE` to 0.5–0.6
- Model stuck in loops: ↓ Decrease `MAX_TOKENS` or `TEMPERATURE`

**Troubleshooting infinite loops:**

- ✓ Ensure `MAX_TOKENS` is set (default: 1000)
- ✓ Check Ollama is running: `curl http://localhost:11434/api/tags`
- ✓ Verify medgemma1.5 model exists: `ollama list`
- ✓ Restart Ollama if frozen: `killall ollama && ollama serve`

### Port Configuration

By default, the API runs on port `8000`. To use a different port:

```bash
uvicorn main:app --reload --port 8080
```

Then update the backend connection URL in `backend/src/services/ai/llm.ts`:

```typescript
const response = await axios.post("http://localhost:8080/generate", {
	prompt: payload,
});
```

---

## 🌍 Environment Requirements

- **Ollama Server**: Must be running on `http://localhost:11434`
- **Python Version**: 3.10 or higher
- **RAM**: Minimum 4GB (8GB recommended for smooth operation)
- **Disk Space**: ~2GB for Gemma 2B model
- **Internet**: Required for first-time model download only

---

## 📝 Health Response Format

All health queries return responses in a structured format:

```
Explanation:
[General overview of the condition/symptom]

Possible causes or factors:
- [Cause 1]
- [Cause 2]
- [Cause 3]

What to do:
- [Action 1]
- [Action 2]
- [Action 3]
```

---

## ⚠️ Important Safety Notes

This service is designed for **general health guidance only**:

- ✅ Does provide information about common symptoms
- ✅ Does suggest when to seek professional help
- ✅ Does maintain conversation context for coherent discussions
- ❌ Does NOT provide medical diagnosis
- ❌ Does NOT prescribe medications
- ❌ Does NOT replace professional medical consultation

For emergency situations or serious symptoms, users are always directed to consult qualified healthcare professionals or call emergency services.

---

## 🐛 Troubleshooting

### "Connection refused" Error

**Problem**: `Error: Failed to connect to http://localhost:11434`

**Solution**:

1. Make sure Ollama is installed and running: `ollama serve`
2. Check that port 11434 is not blocked by firewall
3. Verify Ollama is accessible: `curl http://localhost:11434`

### "Model not found" Error

**Problem**: `Error: model 'medgemma1.5' not found`

**Solution**:

```bash
ollama pull medgemma1.5
```

### Module Import Error

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:

1. Activate your virtual environment
2. Run: `pip install -r requirements.txt`

### Port Already in Use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solution**:

1. Kill the process on port 8000: `fuser -k 8000/tcp` (macOS/Linux) or find and close the app on Windows
2. Or use a different port: `uvicorn main:app --port 8001`

### Slow Responses

**Problem**: The AI service takes too long to respond

**Solutions**:

- Increase available RAM
- Close other applications
- Check system CPU usage
- If still slow, check system resources and Ollama health

---

## 📚 Dependencies

| Package  | Version | Purpose                                 |
| -------- | ------- | --------------------------------------- |
| fastapi  | 0.104.1 | Web framework for the API               |
| uvicorn  | 0.24.0  | ASGI server to run FastAPI              |
| requests | 2.31.0  | HTTP client for Ollama communication    |
| pydantic | 2.5.0   | Data validation and settings management |

---

## 🔗 Integration Points

### Connected to Backend

- **File**: `backend/src/services/ai/llm.ts`
- **Endpoint**: `POST http://localhost:8000/generate`
- **Usage**: Provides AI responses for user chat queries

### Dependency

- **Ollama API**: `POST http://localhost:11434/api/generate`
- **Used by**: FastAPI to generate health guidance

---

## 📞 Support

For issues or questions:

1. Check the Troubleshooting section above
2. Review Ollama documentation: https://ollama.ai
3. Check FastAPI docs: https://fastapi.tiangolo.com
4. Open an issue on the GitHub repository

---

## 📄 License

Part of the Niraksh Guardian project. See main repository for license details.

---

**Last Updated**: April 2026  
**Version**: 1.0  
**Status**: Production Ready ✅
