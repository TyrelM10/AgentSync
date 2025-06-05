interface SidebarProps {
  activeTool: string | null;
  setActiveTool: (tool: string | null) => void;
}

const Sidebar = ({ activeTool, setActiveTool }: SidebarProps) => {
  const tools = [
    { id: 'email', label: 'Send Email', icon: '✉️' },
    { id: 'linear', label: 'Create Linear Issue', icon: '📋' },
    { id: 'notion', label: 'Create Notion Page', icon: '📝' },
    { id: 'notionSearch', label: 'Search Notion', icon: '🔍' },
    { id: 'slack', label: 'Post Slack Message', icon: '💬' },
  ];

  return (
    <div className="sidebar">
      <h1 className="text-xl font-orbitron text-blue-400 mb-4">AgentSync</h1>
      <nav>
        {tools.map((tool) => (
          <div
            key={tool.id}
            className={`sidebar-item p-2 mb-1 rounded-lg cursor-pointer transition-colors flex items-center gap-2 text-sm ${activeTool === tool.id ? 'active-tool' : ''}`}
            onClick={() => setActiveTool(activeTool === tool.id ? null : tool.id)}
          >
            <span>{tool.icon}</span>
            <span>{tool.label}</span>
          </div>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;