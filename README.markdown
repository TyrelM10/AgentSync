# AgentSync

<div align="center">

<h1 align="center"><strong>🤖 AgentSync</strong><h6 align="center">An AI-Powered Productivity Hub</h6></h1>

![Python - 3.11+](https://img.shields.io/badge/PYTHON-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI - 0.115.12+](https://img.shields.io/badge/FastAPI-0.115.12+-teal?style=for-the-badge&logo=fastapi)
![React - 19.1.0+](https://img.shields.io/badge/React-19.1.0+-blue?style=for-the-badge&logo=react)
![Next.js - 15.3.1+](https://img.shields.io/badge/Next.js-15.3.1+-black?style=for-the-badge&logo=next.js&logoColor=white)
![TailwindCSS - 4.0.0+](https://img.shields.io/badge/TailwindCSS-4.0+-skyblue?style=for-the-badge&logo=tailwindcss)
![LangChain - 0.3.25+](https://img.shields.io/badge/LangChain-0.3.25+-orange?style=for-the-badge)
[![Generic badge](https://img.shields.io/badge/License-MIT-<COLOR>.svg?style=for-the-badge)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/YourUsername/agentsync.svg?style=for-the-badge)](https://github.com/YourUsername/agentsync/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg?style=for-the-badge)

</div>

---

> [!IMPORTANT]  
> 📋 Version Updates from v1.0:  
> 1. **Chatbot Integration**: Added a conversational AI chatbot powered by Ollama (Llama3.1:8b) for interactive tool usage guidance.  
> 2. **Speech Recognition**: Implemented Web Speech API for voice input with TypeScript type safety.  
> 3. **Tool Integration**: Enhanced backend with APIs for Email, Linear, Notion, and Slack using FastAPI.  
> 4. **UI Improvements**: Updated frontend with a futuristic glow effect using Tailwind CSS and Framer Motion animations.

---

## 📚 Table of Contents
- [Overview](#overview)
- [Achievements](#achievements)
- [Key Features](#key-features)
- [Tech Stack](#technology-stack)
- [Installation and Setup](#installation-setup)
  - [Manual Installation](#manual-setup)
- [Usage](#usage)
- [Upcoming Integrations and Features](#upcoming-integrations-and-features)
- [Contributions](#contributions)
- [License](#license)
- [Contact](#contact)

---

## 📌 Overview <a name="overview"></a>

**AgentSync** is an **AI-driven productivity hub** designed to streamline workflows for professionals by integrating with tools like Email, Linear, Notion, and Slack. Powered by a conversational AI chatbot using Ollama (Llama3.1:8b), it guides users through tool interactions, collects required inputs, and automates tasks. The platform features a sleek, futuristic UI with a metallic glow effect, built with Next.js, React, and Tailwind CSS, and a scalable backend with FastAPI.

🚀 **Powered by Conversational AI**, this system integrates:  
- **🤖 AI Chatbot**: Guides users through tool usage (e.g., sending emails, creating Notion pages) with natural language understanding via Ollama.  
- **🎙️ Speech Recognition**: Supports voice input using the Web Speech API, with TypeScript type safety.  
- **🌐 Real-Time UI**: Visualizes responses and errors with a futuristic design using Tailwind CSS and Framer Motion animations.  
- **⚡ Scalable Backend**: Built with FastAPI for efficient API handling and integration with external services.

### AgentSync Application Frontend - Screenshots

Below are the screenshots of the AgentSync POC Interface.

<div style="margin-bottom: 20px;">
  <img src="/screenshots/landing.png" alt="Home Page" width="600">
</div>
<div>
  <img src="/screenshots/gmail_server.png" alt="Mail Page" width="600">
</div>
<div>
  <img src="/screenshots/linear.png" alt="Linear Page" width="600">
</div>
<div>
  <img src="/screenshots/notion_create.png" alt="Notion Create Page" width="600">
</div>
<div>
  <img src="/screenshots/notion_search.png" alt="Notion Search Page" width="600">
</div>
<div>
  <img src="/screenshots/slack.png" alt="Slack Page" width="600">
</div>

### **What You’ll Learn from This Project** 📖  
🔹 **👨‍💻 Conversational AI**: Build an AI chatbot for workflow automation using Ollama and LangChain.  
🔹 **🎙️ Speech Recognition**: Implement voice input with the Web Speech API and TypeScript.  
🔹 **⚡ Modern Fullstack Development**: Develop scalable applications with FastAPI, Next.js, and React.  
🔹 **🎨 Futuristic UI Design**: Create a metallic-themed UI with glow effects using Tailwind CSS and Framer Motion.

📂 **For learners**: Refer to `src/app/page.tsx` for chatbot and speech recognition implementation, `src/components/ToolCard.tsx` for tool integration UI, and `backend/main.py` for API details! 🎯  

---

## 🏆 Achievements <a name="achievements"></a>

🚀 The AgentSync project was developed as a proof-of-concept (POC) for AI-driven productivity enhancement. It demonstrates a robust integration of conversational AI and web technologies, achieving:

- Seamless user guidance through a conversational chatbot, reducing manual input for tools like Email, Linear, Notion, and Slack with MCP support.
- A futuristic UI with a metallic glow effect, enhancing user engagement and experience.  
- Voice input support via the Web Speech API, with TypeScript type safety for better development experience.  
- Scalable backend architecture with FastAPI, handling API integrations with external services efficiently.

AgentSync showcases the potential of AI-driven productivity tools, providing a foundation for enterprise-grade solutions in industries like project management, communication, and documentation.

---

## ✨ Key Features <a name="key-features"></a>

- 🤖 **Conversational AI Chatbot**: Guides users through tool interactions (e.g., "Send an email") and collects inputs using Ollama (Llama3.1:8b).  
- 🎙️ **Speech Recognition**: Allows voice input for chatbot interactions, implemented with the Web Speech API and TypeScript types.  
- 📧 **Email Integration**: Sends emails via API with user-provided inputs (to, subject, body).  
- 📋 **Linear Integration**: Creates issues in Linear with title, description, project ID, and team ID.  
- 📝 **Notion Integration**: Creates Notion pages and searches documents with specified inputs.  
- 💬 **Slack Integration**: Posts messages to Slack channels with user-provided channel and message details.  
- 🌟 **Futuristic UI**: Features a metallic glow effect with gradient animations using Tailwind CSS and Framer Motion.  

---

## 🛠️ Technology Stack <a name="technology-stack"></a>

| Component | Technologies |
|-----------|-------------|
| 🔹 **Backend Framework** | FastAPI |
| 🔹 **AI Frameworks** | LangChain, Ollama (Llama3.1:8b) |
| 🔹 **Frontend** | Next.js, React, Tailwind CSS, Framer Motion |
| 🔹 **Environment Management** | python-dotenv |

**Backend Dependencies**:  
- `fastapi==0.115.12`, `langchain==0.3.25`, `langchain-ollama==0.3.2`  
- `python-dotenv==1.1.0`, `uvicorn==0.34.2`, `requests==2.25.1`  
- `gql==3.5.2`, `httpx==0.28.1`, `linear-py==0.0.6`  

**Frontend Dependencies**:  
- `next==15.3.1`, `react==19.1.0`, `react-dom==19.1.0`  
- `framer-motion==12.9.4`, `tailwindcss==4.0.0`  
- Dev: `typescript==5.0.0`, `eslint==9.0.0`, `eslint-config-next==15.3.1`  

---

## 🚀 Installation & Setup <a name="installation-setup"></a>

## 📌 Manual Installation <a name="manual-setup"></a>

### Prerequisites:
- Python 3.11+
- Node.js 18+, npm 9+
- Ollama (Llama3.1:8b) running locally or accessible via API

### 1️⃣ Clone the Repository
```
git clone https://github.com/TyrelM10/agentsync.git
cd agentsync
```

### 2️⃣ Backend Setup
#### Create & Activate Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```
cd backend
pip install -r requirements.txt
```

#### Environment Variables
Create `backend/.env`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
OLLAMA_URL=http://localhost:11434/api/generate
```

#### Run the Backend
```
uvicorn main:app --reload --port 8000
```
Backend available at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

### 3️⃣ Frontend Setup

#### Navigate to Frontend Directory
```
cd frontend
```

#### Install Dependencies
```
npm install
```

#### Run the Frontend
```
npm run dev
```
Frontend available at: [http://localhost:3000/](http://localhost:3000)

---

## 🧠 Usage <a name="usage"></a>

> [!NOTE]  
> 1. Ensure Ollama is running and accessible before starting the backend.  
> 2. Check browser console logs for frontend errors and backend terminal for logs.  

#### Steps:
1. Open [http://localhost:3000/](http://localhost:3000) in your browser to access the AgentSync interface.
2. Use the sidebar to select a tool (e.g., Email, Notion) or interact with the chatbot directly.
3. Type or speak a command (e.g., "Send an email") to the chatbot, which will prompt for required inputs.
4. Provide inputs as requested, and the chatbot will execute the task via the backend API.
5. View responses or errors in the UI, styled with a futuristic glow effect.

---

## 🌟 Upcoming Integrations & Features <a name="upcoming-integrations-and-features"></a>

- 🤖 **Google's A2A Protocol Integration**: Implement Google's Assistant-to-Assistant (A2A) protocol to enable seamless communication between multiple AI agents, enhancing task delegation and collaboration across tools.  
- 💬 **Enhanced Chatbot Services**: Integrate advanced chatbot services with sentiment analysis, multi-language support, and context-aware conversations using RAG or similar technologies.  
- 📈 **Analytics Dashboard**: Add visualizations for tool usage and performance metrics using Chart.js.  
- 🔒 **User Authentication**: Implement JWT-based authentication for secure access.  
- 🌐 **Real-Time Updates**: Use WebSockets for live updates on task execution status.  
- 🧠 **Advanced NLP**: Enhance chatbot capabilities with context retention and multi-turn conversations.  
- 📱 **Mobile Support**: Optimize the UI for mobile devices with responsive design improvements.  
- ☁️ **Cloud Deployment**: Scale with AWS, using S3 for file storage and Lambda for serverless tasks.

These features will position AgentSync as a leader in AI-driven productivity solutions.

---

## 🤝 Contributing <a name="contributions"></a>

Contributions are welcome! Check the [issues](https://github.com/TyrelM10/agentsync/issues) tab for feature requests and improvements.

To contribute:
1. Fork the repository.
2. Create a branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

---

## ⚖️ License <a name="license"></a>

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact <a name="contact"></a>

For inquiries or collaboration:

🔗 **GitHub**: [https://github.com/TyrelM10](https://github.com/TyrelM10)  
🔗 **Email**: tjmenezes08@gmail.com

<p align="right">
 <a href="#top"><b>🔝 Return</b></a>
</p>