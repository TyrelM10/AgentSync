'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

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
  const [inputMode, setInputMode] = useState<'email' | 'linear' | 'notion' | 'notionSearch' | 'slack' | 'custom'>('custom');

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResponse('');
    setError('');
    let finalQuery = query;

    if (inputMode === 'email') {
      if (!emailForm.to || !emailForm.subject || !emailForm.body) {
        setError('All email fields are required.');
        setLoading(false);
        return;
      }
      finalQuery = `Send an email to ${emailForm.to} with subject '${emailForm.subject}' and body '${emailForm.body}'`;
    } else if (inputMode === 'linear') {
      if (!linearForm.title || !linearForm.description || !linearForm.projectId || !linearForm.teamId) {
        setError('All Linear fields are required.');
        setLoading(false);
        return;
      }
      finalQuery = `Create a Linear issue with title "${linearForm.title}", description "${linearForm.description}", project ID "${linearForm.projectId}", and team ID "${linearForm.teamId}"`;
    } else if (inputMode === 'notion') {
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
    } else if (inputMode === 'notionSearch') {
      if (!notionSearchForm.query) {
        setError('Search query is required.');
        setLoading(false);
        return;
      }
      finalQuery = `Search Notion documents with query "${notionSearchForm.query}"`;
    } else if (inputMode === 'slack') {
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
    } else if (!query) {
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
        if (errorMessage.includes('401 Client Error: Unauthorized') && inputMode === 'notion') {
          errorMessage = 'Invalid Notion API token. Please check your NOTION_API_TOKEN in the backend configuration.';
        } else if (errorMessage.includes('parent_page_id') && inputMode === 'notion') {
          errorMessage = 'Invalid Parent Page ID or the Notion integration lacks access to the parent page.';
        } else if (errorMessage.includes('invalid_auth') && inputMode === 'slack') {
          errorMessage = 'Invalid Slack Bot Token. Please check your SLACK_BOT_TOKEN in the backend configuration.';
        }
        throw new Error(errorMessage);
      }
      setResponse(data.response);
    } catch (error: any) {
      setError(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">AgentSync Assistant</h1>
      <div className="flex flex-wrap space-x-4 mb-4">
        <label className="flex items-center space-x-2">
          <input
            type="radio"
            name="inputMode"
            checked={inputMode === 'email'}
            onChange={() => setInputMode('email')}
          />
          <span>Use Email Form</span>
        </label>
        <label className="flex items-center space-x-2">
          <input
            type="radio"
            name="inputMode"
            checked={inputMode === 'linear'}
            onChange={() => setInputMode('linear')}
          />
          <span>Use Linear Form</span>
        </label>
        <label className="flex items-center space-x-2">
          <input
            type="radio"
            name="inputMode"
            checked={inputMode === 'notion'}
            onChange={() => setInputMode('notion')}
          />
          <span>Use Notion Create Form</span>
        </label>
        <label className="flex items-center space-x-2">
          <input
            type="radio"
            name="inputMode"
            checked={inputMode === 'notionSearch'}
            onChange={() => setInputMode('notionSearch')}
          />
          <span>Use Notion Search Form</span>
        </label>
        <label className="flex items-center space-x-2">
          <input
            type="radio"
            name="inputMode"
            checked={inputMode === 'slack'}
            onChange={() => setInputMode('slack')}
          />
          <span>Use Slack Form</span>
        </label>
        <label className="flex items-center space-x-2">
          <input
            type="radio"
            name="inputMode"
            checked={inputMode === 'custom'}
            onChange={() => setInputMode('custom')}
          />
          <span>Use Custom Query</span>
        </label>
      </div>
      <form onSubmit={handleSubmit} className="space-y-4">
        {inputMode === 'email' && (
          <div className="space-y-4">
            <input
              type="email"
              value={emailForm.to}
              onChange={(e) => setEmailForm({ ...emailForm, to: e.target.value })}
              placeholder="Recipient (e.g., test@example.com)"
              className="w-full p-2 border rounded"
              required
            />
            <input
              type="text"
              value={emailForm.subject}
              onChange={(e) => setEmailForm({ ...emailForm, subject: e.target.value })}
              placeholder="Subject"
              className="w-full p-2 border rounded"
              required
            />
            <textarea
              value={emailForm.body}
              onChange={(e) => setEmailForm({ ...emailForm, body: e.target.value })}
              placeholder="Email body"
              className="w-full p-2 border rounded resize-y"
              rows={4}
              required
            />
          </div>
        )}
        {inputMode === 'linear' && (
          <div className="space-y-4">
            <input
              type="text"
              value={linearForm.title}
              onChange={(e) => setLinearForm({ ...linearForm, title: e.target.value })}
              placeholder="Issue Title (e.g., New Task)"
              className="w-full p-2 border rounded"
              required
            />
            <textarea
              value={linearForm.description}
              onChange={(e) => setLinearForm({ ...linearForm, description: e.target.value })}
              placeholder="Issue Description (e.g., Complete the integration test)"
              className="w-full p-2 border rounded resize-y"
              rows={4}
              required
            />
            <input
              type="text"
              value={linearForm.projectId}
              onChange={(e) => setLinearForm({ ...linearForm, projectId: e.target.value })}
              placeholder="Project ID (e.g., 9d542fc5-44d8-45cb-8a59-fda8f503ed79)"
              className="w-full p-2 border rounded"
              required
            />
            <input
              type="text"
              value={linearForm.teamId}
              onChange={(e) => setLinearForm({ ...linearForm, teamId: e.target.value })}
              placeholder="Team ID (e.g., team_12345)"
              className="w-full p-2 border rounded"
              required
            />
          </div>
        )}
        {inputMode === 'notion' && (
          <div className="space-y-4">
            <input
              type="text"
              value={notionForm.title}
              onChange={(e) => setNotionForm({ ...notionForm, title: e.target.value })}
              placeholder="Page Title (e.g., Sample Page)"
              className="w-full p-2 border rounded"
              required
            />
            <textarea
              value={notionForm.content}
              onChange={(e) => setNotionForm({ ...notionForm, content: e.target.value })}
              placeholder="Page Content (e.g., This is a test page)"
              className="w-full p-2 border rounded resize-y"
              rows={4}
              required
            />
            <input
              type="text"
              value={notionForm.parentPageId}
              onChange={(e) => setNotionForm({ ...notionForm, parentPageId: e.target.value })}
              placeholder="Parent Page ID (e.g., 12345678-1234-1234-1234-1234567890ab)"
              className="w-full p-2 border rounded"
              required
            />
          </div>
        )}
        {inputMode === 'notionSearch' && (
          <div className="space-y-4">
            <input
              type="text"
              value={notionSearchForm.query}
              onChange={(e) => setNotionSearchForm({ ...notionSearchForm, query: e.target.value })}
              placeholder="Search Query (e.g., project plan)"
              className="w-full p-2 border rounded"
              required
            />
          </div>
        )}
        {inputMode === 'slack' && (
          <div className="space-y-4">
            <input
              type="text"
              value={slackForm.channel}
              onChange={(e) => setSlackForm({ ...slackForm, channel: e.target.value })}
              placeholder="Channel (e.g., #general or C12345678)"
              className="w-full p-2 border rounded"
              required
            />
            <textarea
              value={slackForm.message}
              onChange={(e) => setSlackForm({ ...slackForm, message: e.target.value })}
              placeholder="Message (e.g., Hello team!)"
              className="w-full p-2 border rounded resize-y"
              rows={4}
              required
            />
          </div>
        )}
        {inputMode === 'custom' && (
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., Search Notion documents with query 'project plan' or Post a message to Slack channel '#general' with message 'Hello team!'"
            className="w-full p-2 border rounded resize-y"
            rows={4}
            required
          />
        )}
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-500 text-white p-2 rounded disabled:bg-gray-400 hover:bg-blue-600 transition flex items-center justify-center"
        >
          {loading ? (
            <svg
              className="animate-spin h-5 w-5 mr-2 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
          ) : null}
          {loading ? 'Processing...' : 'Submit'}
        </button>
      </form>
      {response && (
        <motion.div
          className="mt-4 p-4 border rounded bg-gray-50"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="font-semibold text-black">Response:</h2>
          <p className="text-black">{response}</p>
        </motion.div>
      )}
      {error && (
        <motion.div
          className="mt-4 p-4 border rounded bg-red-50 text-red-800"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="font-semibold">Error:</h2>
          <p>{error}</p>
        </motion.div>
      )}
    </div>
  );
}