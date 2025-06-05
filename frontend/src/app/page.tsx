'use client';

import { useState, useEffect, useRef } from 'react';
import WelcomeBanner from '../app/components/WelcomeBanner';
import ToolCard from '../app/components/ToolCard';
import InputField from '../app/components/InputField';
import TextArea from '../app/components/TextArea';
import Sidebar from '../app/components/SideBar';

interface QueryResponse {
  response: string;
}

export default function AgentInterface() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [emailForm, setEmailForm] = useState({ to: '', subject: '', body: '' });
  const [linearForm, setLinearForm] = useState({ title: '', description: '', projectId: '', teamId: '' });
  const [notionForm, setNotionForm] = useState({ title: '', content: '', parentPageId: '' });
  const [notionSearchForm, setNotionSearchForm] = useState({ query: '' });
  const [slackForm, setSlackForm] = useState({ channel: '', message: '' });
  const [activeTool, setActiveTool] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [recognizedSpeech, setRecognizedSpeech] = useState('');
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const shouldListenRef = useRef(false);

  // Mouse glow effect
  useEffect(() => {
    const glowOverlay = document.getElementById('glow-overlay')!;
    const updateGlow = (e: MouseEvent) => {
      glowOverlay.style.background = `radial-gradient(circle 200px at ${e.clientX}px ${e.clientY}px, rgba(59, 130, 246, 0.15) 0%, transparent 100%)`;
    };
    window.addEventListener('mousemove', updateGlow);
    return () => window.removeEventListener('mousemove', updateGlow);
  }, []);

  // Speech recognition setup
  useEffect(() => {
    const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognitionAPI) {
      setError('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
      return;
    }

    recognitionRef.current = new SpeechRecognitionAPI();
    recognitionRef.current.continuous = true; // Keep listening until manually stopped
    recognitionRef.current.interimResults = true;
    recognitionRef.current.lang = 'en-US';

    recognitionRef.current.onresult = (event: SpeechRecognitionEvent) => {
      let transcript = '';
      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript + ' ';
      }
      setRecognizedSpeech(transcript.trim());
      setQuery(transcript.trim());
    };

    recognitionRef.current.onend = () => {
      if (shouldListenRef.current) {
        // Restart recognition if we should still be listening
        recognitionRef.current?.start();
      } else {
        setIsListening(false);
        if (recognizedSpeech.trim()) {
          handleSubmit(new Event('submit') as any, 'custom');
        }
      }
    };

    recognitionRef.current.onerror = (event: SpeechRecognitionErrorEvent) => {
      setError(`Speech recognition error: ${event.error}`);
      setIsListening(false);
      shouldListenRef.current = false;
    };

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, [recognizedSpeech]);

  const toggleListening = () => {
    if (isListening) {
      shouldListenRef.current = false;
      recognitionRef.current?.stop();
    } else {
      setRecognizedSpeech('');
      setQuery('');
      setError('');
      setResponse('');
      shouldListenRef.current = true;
      recognitionRef.current?.start();
      setIsListening(true);
    }
  };

  // UUID-like regex for parentPageId
  const isValidParentPageId = (id: string) => {
    const uuidRegex = /^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/i;
    return uuidRegex.test(id.replace(/[^0-9a-f-]/gi, ''));
  };

  // Basic validation for Slack channel (ID or #name)
  const isValidSlackChannel = (channel: string) => {
    const channelRegex = /^(#[\w-]+|[A-Z0-9]{9,11})$/i;
    return channelRegex.test(channel);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>, tool: string) => {
    e.preventDefault();
    setLoading(true);
    setResponse('');
    setError('');
    let finalQuery = query;

    if (tool === 'email') {
      if (!emailForm.to || !emailForm.subject || !emailForm.body) {
        setError('All email fields are required.');
        setLoading(false);
        return;
      }
      finalQuery = `Send an email to ${emailForm.to} with subject '${emailForm.subject}' and body '${emailForm.body}'`;
    } else if (tool === 'linear') {
      if (!linearForm.title || !linearForm.description || !linearForm.projectId || !linearForm.teamId) {
        setError('All Linear fields are required.');
        setLoading(false);
        return;
      }
      finalQuery = `Create a Linear issue with title "${linearForm.title}", description "${linearForm.description}", project ID "${linearForm.projectId}", and team ID "${linearForm.teamId}"`;
    } else if (tool === 'notion') {
      if (!notionForm.title || !notionForm.content || !notionForm.parentPageId) {
        setError('All Notion fields are required.');
        setLoading(false);
        return;
      }
      if (!isValidParentPageId(notionForm.parentPageId)) {
        setError('Parent Page ID must be a valid UUID (e.g., 12345678-1234-1234-1234-1234567890ab or 123456781234123412341234567890ab)');
        setLoading(false);
        return;
      }
      finalQuery = `Create a Notion page with title "${notionForm.title}", content "${notionForm.content}", and parent page ID "${notionForm.parentPageId}"`;
    } else if (tool === 'notionSearch') {
      if (!notionSearchForm.query) {
        setError('Search query is required.');
        setLoading(false);
        return;
      }
      finalQuery = `Search Notion documents with query "${notionSearchForm.query}"`;
    } else if (tool === 'slack') {
      if (!slackForm.channel || !slackForm.message) {
        setError('All Slack fields are required.');
        setLoading(false);
        return;
      }
      if (!isValidSlackChannel(slackForm.channel)) {
        setError('Slack channel must be a valid channel name (e.g., #general) or ID (e.g., C12345678).');
        setLoading(false);
        return;
      }
      finalQuery = `Post a message to Slack channel "${slackForm.channel}" with message "${slackForm.message}"`;
    } else if (tool === 'custom' && !query) {
      setError('Custom query cannot be empty.');
      setLoading(false);
      return;
    }

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      if (!apiUrl) {
        throw new Error('NEXT_PUBLIC_API_URL is not defined');
      }
      const res = await fetch(`${apiUrl}/agent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: finalQuery }),
      });
      const data: QueryResponse = await res.json();
      if (!res.ok) {
        let errorMessage = data.response || `HTTP error! status: ${res.status}`;
        if (errorMessage.includes('401 Client Error: Unauthorized') && tool === 'notion') {
          errorMessage = 'Invalid Notion API token. Please check your NOTION_API_TOKEN in the backend configuration.';
        } else if (errorMessage.includes('parent_page_id') && tool === 'notion') {
          errorMessage = 'Invalid Parent Page ID or the Notion integration lacks access to the parent page.';
        } else if (errorMessage.includes('invalid_auth') && tool === 'slack') {
          errorMessage = 'Invalid Slack Bot Token. Please check your SLACK_BOT_TOKEN in the backend configuration.';
        }
        throw new Error(errorMessage);
      }
      setResponse(data.response);
    } catch (error: any) {
      setError(`Error: ${error.message}`);
    } finally {
      setLoading(false);
      setRecognizedSpeech(''); // Clear speech display after submission
    }
  };

  return (
    <>
      <div id="glow-overlay"></div>
      <div className="layout-container">
        <Sidebar activeTool={activeTool} setActiveTool={setActiveTool} />
        <div className="main-content">
          <header className="header">
            <h1 className="text-xl font-orbitron text-blue-400">AgentSync Assistant</h1>
            <p className="text-sm text-gray-400">Your AI-powered productivity hub</p>
          </header>
          <div className="flex-1 overflow-hidden">
            <WelcomeBanner />
            {activeTool === 'email' && (
              <ToolCard
                title="Send Email"
                description="Send an email to any recipient with a subject and body."
                onSubmit={(e) => handleSubmit(e, 'email')}
                isLoading={loading}
              >
                <InputField
                  type="email"
                  value={emailForm.to}
                  onChange={(e) => setEmailForm({ ...emailForm, to: e.target.value })}
                  placeholder="Recipient (e.g., test@example.com)"
                  required
                />
                <InputField
                  type="text"
                  value={emailForm.subject}
                  onChange={(e) => setEmailForm({ ...emailForm, subject: e.target.value })}
                  placeholder="Subject"
                  required
                />
                <TextArea
                  value={emailForm.body}
                  onChange={(e) => setEmailForm({ ...emailForm, body: e.target.value })}
                  placeholder="Email body"
                  required
                  rows={2}
                />
              </ToolCard>
            )}
            {activeTool === 'linear' && (
              <ToolCard
                title="Create Linear Issue"
                description="Create a new issue in Linear with title, description, project, and team."
                onSubmit={(e) => handleSubmit(e, 'linear')}
                isLoading={loading}
              >
                <InputField
                  type="text"
                  value={linearForm.title}
                  onChange={(e) => setLinearForm({ ...linearForm, title: e.target.value })}
                  placeholder="Issue Title (e.g., New Task)"
                  required
                />
                <TextArea
                  value={linearForm.description}
                  onChange={(e) => setLinearForm({ ...linearForm, description: e.target.value })}
                  placeholder="Issue Description (e.g., Complete the integration test)"
                  required
                  rows={2}
                />
                <InputField
                  type="text"
                  value={linearForm.projectId}
                  onChange={(e) => setLinearForm({ ...linearForm, projectId: e.target.value })}
                  placeholder="Project ID (e.g., 9d542fc5-44d8-45cb-8a59-fda8f503ed79)"
                  required
                />
                <InputField
                  type="text"
                  value={linearForm.teamId}
                  onChange={(e) => setLinearForm({ ...linearForm, teamId: e.target.value })}
                  placeholder="Team ID (e.g., team_12345)"
                  required
                />
              </ToolCard>
            )}
            {activeTool === 'notion' && (
              <ToolCard
                title="Create Notion Page"
                description="Create a new page in Notion with a title, content, and parent page."
                onSubmit={(e) => handleSubmit(e, 'notion')}
                isLoading={loading}
              >
                <InputField
                  type="text"
                  value={notionForm.title}
                  onChange={(e) => setNotionForm({ ...notionForm, title: e.target.value })}
                  placeholder="Page Title (e.g., Sample Page)"
                  required
                />
                <TextArea
                  value={notionForm.content}
                  onChange={(e) => setNotionForm({ ...notionForm, content: e.target.value })}
                  placeholder="Page Content (e.g., This is a test page)"
                  required
                  rows={2}
                />
                <InputField
                  type="text"
                  value={notionForm.parentPageId}
                  onChange={(e) => setNotionForm({ ...notionForm, parentPageId: e.target.value })}
                  placeholder="Parent Page ID (e.g., 12345678-1234-1234-1234-1234567890ab)"
                  required
                />
              </ToolCard>
            )}
            {activeTool === 'notionSearch' && (
              <ToolCard
                title="Search Notion Documents"
                description="Search for documents in Notion by keyword."
                onSubmit={(e) => handleSubmit(e, 'notionSearch')}
                isLoading={loading}
              >
                <InputField
                  type="text"
                  value={notionSearchForm.query}
                  onChange={(e) => setNotionSearchForm({ ...notionSearchForm, query: e.target.value })}
                  placeholder="Search Query (e.g., project plan)"
                  required
                />
              </ToolCard>
            )}
            {activeTool === 'slack' && (
              <ToolCard
                title="Post Slack Message"
                description="Send a message to a Slack channel."
                onSubmit={(e) => handleSubmit(e, 'slack')}
                isLoading={loading}
              >
                <InputField
                  type="text"
                  value={slackForm.channel}
                  onChange={(e) => setSlackForm({ ...slackForm, channel: e.target.value })}
                  placeholder="Channel (e.g., #general or C12345678)"
                  required
                />
                <TextArea
                  value={slackForm.message}
                  onChange={(e) => setSlackForm({ ...slackForm, message: e.target.value })}
                  placeholder="Message (e.g., Hello team!)"
                  required
                  rows={2}
                />
              </ToolCard>
            )}
            {response && (
              <div className="p-4 bg-gray-900/50 rounded-lg border border-blue-700/30 mt-2 text-sm text-gray-200">
                <strong>Response:</strong> {response}
              </div>
            )}
            {error && (
              <div className="p-4 bg-red-900/50 rounded-lg border border-red-700/30 mt-2 text-sm text-red-300">
                <strong>Error:</strong> {error}
              </div>
            )}
          </div>
          <div className="mic-section">
            {recognizedSpeech && (
              <div className="speech-display">
                {recognizedSpeech}
              </div>
            )}
            <button
              onClick={toggleListening}
              className={`mic-button ${isListening ? 'listening' : ''}`}
              disabled={loading}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="w-6 h-6 text-blue-400"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-7a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </>
  );
}