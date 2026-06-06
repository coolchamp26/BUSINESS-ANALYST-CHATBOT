import React, { useState, useEffect } from 'react';
import { 
  Compass, 
  MessageSquare, 
  LayoutDashboard, 
  Network, 
  CalendarDays, 
  FileDown, 
  Settings, 
  Menu, 
  X, 
  Sparkles,
  ArrowRight,
  TrendingUp,
  Cpu
} from 'lucide-react';

// Page Imports
import LandingPage from './pages/LandingPage';
import ConsultationPage from './pages/ConsultationPage';
import DashboardPage from './pages/DashboardPage';
import WorkflowStudio from './pages/WorkflowStudio';
import RoadmapPage from './pages/RoadmapPage';
import ReportCenter from './pages/ReportCenter';

export default function App() {
  const [activeTab, setActiveTab] = useState('landing');
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [apiKey, setApiKey] = useState('');
  const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isLiveMode, setIsLiveMode] = useState(false);

  // Sync health check
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/health')
      .then(res => res.json())
      .then(data => {
        setIsLiveMode(data.live_mode);
      })
      .catch(() => {});
  }, []);

  const saveApiKey = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/settings/apikey', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gemini_api_key: apiKey }),
      });
      const data = await response.json();
      if (data.status === 'success') {
        setIsLiveMode(data.live_mode);
        setIsApiKeyModalOpen(false);
        alert('API Key configured successfully.');
      } else {
        alert('Verification failed: ' + data.message);
      }
    } catch (error) {
      alert('Error updating API key.');
    }
  };

  const loadSessionAnalysis = async (sessionId) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/consultation/${sessionId}/analysis`);
      if (response.ok) {
        const data = await response.json();
        setAnalysisData(data);
        setActiveSessionId(sessionId);
        setActiveTab('dashboard');
      } else {
        // Trigger calculation if not analyzed yet
        const analyzeRes = await fetch(`http://127.0.0.1:8000/api/consultation/${sessionId}/analyze`, {
          method: 'POST'
        });
        if (analyzeRes.ok) {
          const data = await analyzeRes.json();
          setAnalysisData(data);
          setActiveSessionId(sessionId);
          setActiveTab('dashboard');
        }
      }
    } catch (e) {
      console.error(e);
    }
  };

  const startConsultation = async (industry = '', companyName = '', companySize = '') => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/consultation/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ industry, company_name: companyName, company_size: companySize })
      });
      if (response.ok) {
        const data = await response.json();
        setActiveSessionId(data.id);
        setAnalysisData(null);
        setActiveTab('consultation');
      }
    } catch (e) {
      console.error(e);
    }
  };

  const loadTemplate = async (templateKey) => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/consultation/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ template_key: templateKey })
      });
      if (response.ok) {
        const sessionData = await response.json();
        setActiveSessionId(sessionData.id);
        await loadSessionAnalysis(sessionData.id);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const navItems = [
    { id: 'landing', label: 'Home Discovery', icon: Compass, disabled: false },
    { id: 'consultation', label: 'AI Consultation', icon: MessageSquare, disabled: !activeSessionId },
    { id: 'dashboard', label: 'Analysis Dashboard', icon: LayoutDashboard, disabled: !analysisData },
    { id: 'workflow', label: 'Workflow Studio', icon: Network, disabled: !analysisData },
    { id: 'roadmap', label: 'Implementation Roadmap', icon: CalendarDays, disabled: !analysisData },
    { id: 'report', label: 'Report Center', icon: FileDown, disabled: !analysisData }
  ];

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans">
      
      {/* SIDEBAR FOR DESKTOP */}
      <aside className="hidden md:flex flex-col w-64 bg-slate-900 border-r border-slate-800 z-30">
        {/* Brand */}
        <div className="p-6 flex items-center gap-3 border-b border-slate-800">
          <div className="bg-indigo-600 p-2 rounded-lg flex items-center justify-center glassmorphism-glow">
            <Sparkles className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <span className="font-extrabold text-lg bg-gradient-to-r from-white via-slate-200 to-indigo-400 bg-clip-text text-transparent">
              FlowArchitect AI
            </span>
            <span className="block text-[10px] text-slate-500 font-medium tracking-wider uppercase">
              Business Architect
            </span>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-4 py-6 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                disabled={item.disabled}
                onClick={() => {
                  setActiveTab(item.id);
                  setIsMobileMenuOpen(false);
                }}
                className={`flex items-center gap-3 w-full px-4 py-3 rounded-xl transition-all duration-200 ${
                  isActive 
                    ? 'bg-gradient-to-r from-indigo-900/60 to-indigo-950/40 text-cyan-400 border-l-2 border-cyan-400' 
                    : item.disabled 
                      ? 'text-slate-600 cursor-not-allowed opacity-40' 
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium text-sm">{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Settings / API Key Area */}
        <div className="p-4 border-t border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-xs text-slate-500 px-2">
            <span>Engine Mode:</span>
            <span className={`font-semibold uppercase tracking-wider flex items-center gap-1 ${isLiveMode ? 'text-emerald-400' : 'text-amber-500'}`}>
              <Cpu className="w-3 h-3" />
              {isLiveMode ? 'Live AI' : 'Simulation'}
            </span>
          </div>
          <button
            onClick={() => setIsApiKeyModalOpen(true)}
            className="flex items-center justify-center gap-2 w-full px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-all text-xs font-semibold border border-slate-700/50"
          >
            <Settings className="w-4 h-4" />
            Configure API Key
          </button>
        </div>
      </aside>

      {/* MOBILE HEADER */}
      <div className="flex flex-col flex-1 min-w-0">
        <header className="md:hidden flex items-center justify-between p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-40">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-cyan-400" />
            <span className="font-bold text-base bg-gradient-to-r from-white to-indigo-400 bg-clip-text text-transparent">
              FlowArchitect AI
            </span>
          </div>
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-1 hover:bg-slate-800 rounded-lg">
            {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </header>

        {/* MOBILE NAVIGATION DRAWER */}
        {isMobileMenuOpen && (
          <div className="md:hidden fixed inset-0 top-[57px] bg-slate-950 z-30 p-4 border-t border-slate-800 flex flex-col space-y-3">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  disabled={item.disabled}
                  onClick={() => {
                    setActiveTab(item.id);
                    setIsMobileMenuOpen(false);
                  }}
                  className={`flex items-center gap-3 w-full px-4 py-3.5 rounded-xl ${
                    isActive 
                      ? 'bg-indigo-900/40 text-cyan-400' 
                      : item.disabled 
                        ? 'text-slate-700 opacity-40 cursor-not-allowed' 
                        : 'text-slate-400'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-semibold text-sm">{item.label}</span>
                </button>
              );
            })}
            <div className="pt-4 border-t border-slate-800 mt-auto">
              <button
                onClick={() => {
                  setIsApiKeyModalOpen(true);
                  setIsMobileMenuOpen(false);
                }}
                className="flex items-center justify-center gap-2 w-full px-4 py-3 rounded-xl bg-slate-850 hover:bg-slate-800 text-slate-300 font-semibold text-sm border border-slate-700"
              >
                <Settings className="w-5 h-5" />
                Configure API Key
              </button>
            </div>
          </div>
        )}

        {/* MAIN PANEL CONTENT */}
        <main className="flex-1 p-4 md:p-8 overflow-y-auto">
          {activeTab === 'landing' && (
            <LandingPage 
              onStartConsultation={startConsultation} 
              onLoadTemplate={loadTemplate}
            />
          )}
          {activeTab === 'consultation' && (
            <ConsultationPage 
              sessionId={activeSessionId} 
              onAnalysisComplete={loadSessionAnalysis}
            />
          )}
          {activeTab === 'dashboard' && analysisData && (
            <DashboardPage 
              analysis={analysisData} 
              onNavigate={setActiveTab}
            />
          )}
          {activeTab === 'workflow' && analysisData && (
            <WorkflowStudio 
              analysis={analysisData}
            />
          )}
          {activeTab === 'roadmap' && analysisData && (
            <RoadmapPage 
              analysis={analysisData}
            />
          )}
          {activeTab === 'report' && analysisData && (
            <ReportCenter 
              sessionId={activeSessionId}
              analysis={analysisData}
            />
          )}
        </main>
      </div>

      {/* API KEY CONFIGURATION MODAL */}
      {isApiKeyModalOpen && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-800 w-full max-w-md p-6 rounded-2xl shadow-2xl space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-lg text-white flex items-center gap-2">
                <Settings className="w-5 h-5 text-indigo-400" />
                Configure Gemini Engine
              </h3>
              <button onClick={() => setIsApiKeyModalOpen(false)} className="text-slate-400 hover:text-slate-200">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <p className="text-xs text-slate-400 leading-relaxed">
              By default, FlowArchitect AI uses a simulation engine for demonstrating workflows. Provide a **Gemini API Key** to enable live business process parsing and dynamic follow-up conversations.
            </p>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Gemini API Key</label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="AIzaSy..."
                className="w-full px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:outline-none text-sm text-slate-200 placeholder-slate-600"
              />
            </div>

            <div className="flex gap-3 justify-end pt-2">
              <button
                onClick={() => setIsApiKeyModalOpen(false)}
                className="px-4 py-2 rounded-xl text-slate-400 hover:text-slate-200 text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                onClick={saveApiKey}
                className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition-all shadow-md shadow-indigo-600/10"
              >
                Save Configuration
              </button>
            </div>
          </div>
        </div>
      )}
      
    </div>
  );
}
