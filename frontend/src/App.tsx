import { useState } from 'react';
import { Link, Route, Routes } from 'react-router-dom';

type ChatMessage = {
  id: string;
  role: 'assistant' | 'user';
  text: string;
};

function ChatbotWidget() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      text: 'Hi! I can help you review suspicious accounts, understand evidence confidence, and decide what to do next.',
    },
  ]);
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const sendMessage = async () => {
    const nextMessage = input.trim();
    if (!nextMessage || isSending) return;

    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
    const userMessage: ChatMessage = {
      id: `${Date.now()}-user`,
      role: 'user',
      text: nextMessage,
    };

    setMessages((current) => [...current, userMessage]);
    setInput('');
    setIsSending(true);

    try {
      const response = await fetch(`${apiBaseUrl}/api/chatbot/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: nextMessage }),
      });

      const data = await response.json();
      const reply = data?.reply || 'I am in demo mode right now. Connect the backend or add credentials to enable the live provider.';

      setMessages((current) => [
        ...current,
        { id: `${Date.now()}-assistant`, role: 'assistant', text: reply },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: `${Date.now()}-assistant`,
          role: 'assistant',
          text: 'The assistant is in local demo mode. Start the backend and use the configured provider to enable live answers.',
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="floating-widget">
      <a className="contact-bubble" href="tel:+15551234567" aria-label="Call support">
        <span className="contact-icon">☎</span>
        <span className="contact-text">+1 (555) 123-4567</span>
      </a>

      <button
        type="button"
        className="chat-toggle"
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
        aria-expanded={isOpen}
        onClick={() => setIsOpen((current) => !current)}
      >
        {isOpen ? '×' : 'Chat'}
      </button>

      {isOpen ? (
        <aside className="chatbot-panel">
          <div className="chatbot-header">
            <strong>AccountMap Assistant</strong>
            <span>{isSending ? 'Thinking…' : 'Online'}</span>
          </div>
          <div className="chatbot-body">
            {messages.map((message) => (
              <div key={message.id} className={`chat-message ${message.role}`}>
                {message.text}
              </div>
            ))}
          </div>
          <div className="chatbot-form">
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') {
                  event.preventDefault();
                  void sendMessage();
                }
              }}
              placeholder="Ask about account risk..."
              aria-label="Ask the assistant"
            />
            <button type="button" onClick={() => void sendMessage()} disabled={isSending}>
              {isSending ? '...' : 'Send'}
            </button>
          </div>
        </aside>
      ) : null}
    </div>
  );
}

function LandingPage() {
  return (
    <main className="page-shell">
      <header className="topbar">
        <div className="brand">AccountMap AI</div>
        <nav>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/inventory">Inventory</Link>
          <Link to="/security">Privacy</Link>
        </nav>
      </header>
      <section className="hero card">
        <div>
          <p className="eyebrow">Privacy-first account discovery</p>
          <h1>Review your digital footprint without guessing.</h1>
          <p>
            AccountMap AI helps you collect evidence from email activity, saved-password imports, and phone-associated records,
            then review what deserves action.
          </p>
          <div className="actions">
            <Link to="/dashboard" className="primary-button">Open dashboard</Link>
            <Link to="/signin" className="secondary-button">Sign in</Link>
          </div>
        </div>
        <div className="stats-box">
          <div className="mini-stat"><strong>12</strong><span>Possible accounts</span></div>
          <div className="mini-stat"><strong>3</strong><span>Pending review</span></div>
          <div className="mini-stat"><strong>2</strong><span>Email sources</span></div>
        </div>
      </section>
      <section className="card feature-grid">
        <div><h3>Email evidence</h3><p>Review welcome emails, password resets, receipts, and security notices.</p></div>
        <div><h3>Password imports</h3><p>Preview supported CSV exports without retaining raw passwords.</p></div>
        <div><h3>Cleanup guide</h3><p>Open official management and deletion pages only after review.</p></div>
      </section>
    </main>
  );
}

function SignInPage() {
  return (
    <main className="page-shell narrow">
      <section className="card auth-card">
        <h2>Sign in</h2>
        <form>
          <label><span>Email</span><input type="email" defaultValue="demo@accountmap.ai" /></label>
          <label><span>Password</span><input type="password" defaultValue="securepass123" /></label>
          <button type="button" className="primary-button">Continue</button>
        </form>
      </section>
    </main>
  );
}

function DashboardPage() {
  return (
    <main className="page-shell">
      <header className="section-header"><h2>Dashboard</h2><Link to="/inventory">Inventory</Link></header>
      <div className="stats-grid">
        <div className="card stat-card"><span>Total discovered</span><strong>24</strong></div>
        <div className="card stat-card"><span>Confirmed</span><strong>8</strong></div>
        <div className="card stat-card"><span>Awaiting review</span><strong>12</strong></div>
        <div className="card stat-card"><span>Saved-password imports</span><strong>4</strong></div>
      </div>
      <div className="card table-card">
        <h3>Recently discovered services</h3>
        <ul className="list">
          <li>GitHub · email evidence</li>
          <li>Dropbox · password import</li>
          <li>Netflix · phone-associated</li>
        </ul>
      </div>
    </main>
  );
}

function InventoryPage() {
  return (
    <main className="page-shell">
      <header className="section-header"><h2>Account inventory</h2><Link to="/import">Import</Link></header>
      <div className="card table-card">
        <table>
          <thead><tr><th>Service</th><th>Evidence</th><th>Confidence</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>GitHub</td><td>Welcome email</td><td>High</td><td>Review</td></tr>
            <tr><td>Dropbox</td><td>Saved password</td><td>Medium</td><td>Active</td></tr>
          </tbody>
        </table>
      </div>
    </main>
  );
}

function ImportPage() {
  return (
    <main className="page-shell narrow">
      <section className="card auth-card">
        <h2>Import saved passwords</h2>
        <p>Upload a supported CSV export. We only preview the website and identifiers and discard the password payload immediately.</p>
        <input type="file" accept=".csv" />
        <button type="button" className="primary-button">Preview import</button>
      </section>
    </main>
  );
}

function SecurityPage() {
  return (
    <main className="page-shell narrow">
      <section className="card auth-card">
        <h2>Privacy and security</h2>
        <ul className="list small-list">
          <li>OAuth token revocation workflow</li>
          <li>JSON/CSV data export</li>
          <li>Audit log of consent changes</li>
          <li>Local retention settings</li>
        </ul>
      </section>
    </main>
  );
}

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/inventory" element={<InventoryPage />} />
        <Route path="/import" element={<ImportPage />} />
        <Route path="/security" element={<SecurityPage />} />
      </Routes>
      <ChatbotWidget />
    </>
  );
}
