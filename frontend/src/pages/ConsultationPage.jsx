import React, { useState, useEffect, useRef } from 'react';
import { 
  Send, 
  Sparkles, 
  User, 
  Bot, 
  Loader2, 
  CheckCircle2, 
  TrendingUp,
  Cpu
} from 'lucide-react';

export default function ConsultationPage({ sessionId, onAnalysisComplete }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [isCompiling, setIsCompiling] = useState(false);
  const [compilingStep, setCompilingStep] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [sessionStatus, setSessionStatus] = useState('discovering');
  const chatEndRef = useRef(null);

  const stepsList = [
    { label: "Core Business Profile" },
    { label: "Team Size & Role" },
    { label: "Customer Contact Channels" },
    { label: "Sales & CRM Tooling" },
    { label: "Support Ticket Volumes" },
    { label: "Repetitive Daily Work" },
    { label: "Operations Software Stack" },
    { label: "Core Obstacles & Issues" }
  ];

  const compilingMessages = [
    "Discovery Agent packaging interview transcript...",
    "Analysis Agent running department audits & readiness metrics...",
    "Automation Agent creating custom WhatsApp/CRM integration blueprints...",
    "ROI Agent forecasting before/after conversion margins...",
    "Roadmap Agent compiling week-by-week transformation schedule...",
    "FlowArchitect AI compiling PDF reports and database records..."
  ];

  // Fetch session history
  const fetchSession = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/consultation/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ template_key: null }) // triggers loading if exists or starts a fresh one
      });
      // But we already have a sessionId passed in! So query message history directly
      if (sessionId) {
        const historyRes = await fetch(`http://127.0.0.1:8000/api/consultation/start`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ template_key: null })
        });
        // We will make a direct GET call on our main session endpoint to retrieve the messages
        // Wait, let's write a simple fetch session endpoint in App.jsx or fetch it here.
        // Actually, we can fetch directly from our start endpoint if we store it.
        // Let's call our session endpoint:
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Keep chat scrolled to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isCompiling]);

  // Initial load
  useEffect(() => {
    if (sessionId) {
      setMessages([]);
      setCurrentStep(0);
      setSessionStatus('discovering');
      loadSessionState();
    }
  }, [sessionId]);

  const loadSessionState = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/consultation/${sessionId}`);
      if (res.ok) {
        const data = await res.json();
        setMessages(data.messages);
        setCurrentStep(data.current_step);
        setSessionStatus(data.status);
        if (data.status === 'completed') {
          onAnalysisComplete(sessionId);
        } else if (data.status === 'analyzing') {
          triggerCompilation();
        }
      }
    } catch (e) {
      console.error(e);
    }
  };


  const handleSendMessage = async (contentStr) => {
    const text = contentStr || inputValue;
    if (!text.trim()) return;

    if (!contentStr) setInputValue('');
    
    // Add user message locally for speed
    const userMsg = { sender: 'user', content: text, timestamp: 'Just now' };
    setMessages(prev => [...prev, userMsg]);
    setIsSending(true);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/consultation/${sessionId}/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: text })
      });
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages);
        setCurrentStep(data.current_step);
        setSessionStatus(data.status);
        
        // If the consultation is complete, trigger compilation
        if (data.status === 'analyzing') {
          triggerCompilation();
        }
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsSending(false);
    }
  };

  const triggerCompilation = async () => {
    setIsCompiling(true);
    setCompilingStep(0);
    
    // Animate compile text
    const interval = setInterval(() => {
      setCompilingStep(prev => {
        if (prev < compilingMessages.length - 1) {
          return prev + 1;
        } else {
          clearInterval(interval);
          return prev;
        }
      });
    }, 1800);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/consultation/${sessionId}/analyze`, {
        method: 'POST'
      });
      if (response.ok) {
        // Wait at least 5 seconds for visual impact
        setTimeout(() => {
          clearInterval(interval);
          setIsCompiling(false);
          onAnalysisComplete(sessionId);
        }, 6000);
      }
    } catch (e) {
      console.error(e);
      clearInterval(interval);
      setIsCompiling(false);
    }
  };

  const quickReplies = [
    ["Dental Care", "E-commerce Retail", "Real Estate Office"],
    ["10 Employees", "25 Staff", "Under 5 Team members"],
    ["Phone & Emails", "WhatsApp Chat", "Instagram DMs"],
    ["HubSpot CRM", "Google Sheets", "Legacy custom software"]
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 h-[calc(100vh-8rem)] relative">
      
      {/* LEFT SIDEBAR: PROGRESS TRACKER */}
      <aside className="lg:col-span-1 glassmorphism p-6 rounded-2xl border border-slate-800 flex flex-col justify-between hidden lg:flex">
        <div className="space-y-6">
          <div className="space-y-1">
            <h3 className="font-bold text-sm text-white uppercase tracking-wider">Discovery Roadmap</h3>
            <p className="text-[10px] text-slate-500">Guided virtual consulting interview</p>
          </div>
          
          <div className="space-y-3.5">
            {stepsList.map((step, idx) => {
              const isCompleted = idx < currentStep;
              const isActive = idx === currentStep;
              return (
                <div key={idx} className="flex items-center gap-3.5 text-left text-xs">
                  <div className={`w-5 h-5 rounded-full flex items-center justify-center border transition-all ${
                    isCompleted 
                      ? 'bg-indigo-600/30 border-cyan-400 text-cyan-400' 
                      : isActive 
                        ? 'bg-slate-900 border-indigo-500 text-indigo-400 font-bold' 
                        : 'border-slate-800 text-slate-600'
                  }`}>
                    {isCompleted ? <CheckCircle2 className="w-3.5 h-3.5" /> : idx + 1}
                  </div>
                  <span className={`font-semibold ${isActive ? 'text-cyan-400' : isCompleted ? 'text-slate-300' : 'text-slate-500'}`}>
                    {step.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        <div className="pt-4 border-t border-slate-800 text-[10px] text-slate-500 leading-relaxed flex items-center gap-2">
          <Cpu className="w-3.5 h-3.5 text-indigo-400" />
          <span>Active Session ID:<br /><code className="text-slate-400">{sessionId}</code></span>
        </div>
      </aside>

      {/* RIGHT SIDE: CONVERSATION PANEL */}
      <div className="lg:col-span-3 flex flex-col glassmorphism border border-slate-800 rounded-2xl overflow-hidden h-full relative">
        {/* Chat Header */}
        <div className="p-4 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 w-8 bg-indigo-600/20 text-cyan-400 border border-indigo-500/30 p-1.5 rounded-lg flex items-center justify-center">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h4 className="font-bold text-xs text-white">Discovery Agent</h4>
              <span className="text-[10px] text-slate-500 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                Active consultation session
              </span>
            </div>
          </div>
          <div className="text-[10px] bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 px-2.5 py-1 rounded-full font-semibold">
            Stage {Math.min(currentStep + 1, 8)} / 8
          </div>
        </div>

        {/* Message Log */}
        <div className="flex-1 p-6 overflow-y-auto space-y-6 relative bg-slate-950/20">
          {messages.map((msg, idx) => {
            const isAgent = msg.sender === 'agent';
            return (
              <div key={idx} className={`flex gap-3 max-w-3xl ${isAgent ? '' : 'ml-auto flex-row-reverse'}`}>
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center border shrink-0 ${
                  isAgent 
                    ? 'bg-indigo-950 border-indigo-900 text-indigo-400' 
                    : 'bg-cyan-950 border-cyan-900 text-cyan-400'
                }`}>
                  {isAgent ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
                </div>

                {/* Bubble */}
                <div className="space-y-1">
                  <div className={`p-4 rounded-2xl text-xs leading-relaxed border ${
                    isAgent 
                      ? 'bg-slate-900/60 border-slate-800 text-slate-200 rounded-tl-none' 
                      : 'bg-indigo-600/10 border-indigo-500/20 text-indigo-200 rounded-tr-none'
                  }`}>
                    {msg.content}
                  </div>
                  {msg.agent_name && (
                    <span className="block text-[9px] text-slate-600 ml-1 font-medium italic">
                      Agent: {msg.agent_name}
                    </span>
                  )}
                </div>
              </div>
            );
          })}
          
          {isSending && (
            <div className="flex gap-3 max-w-lg">
              <div className="w-8 h-8 rounded-lg bg-indigo-950 border border-indigo-900 text-indigo-400 flex items-center justify-center animate-spin">
                <Loader2 className="w-4 h-4" />
              </div>
              <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-2xl rounded-tl-none text-xs text-slate-400 flex items-center gap-2 italic">
                Discovery Agent is thinking...
              </div>
            </div>
          )}

          {/* COMPILING OVERLAY SCREEN */}
          {isCompiling && (
            <div className="absolute inset-0 bg-slate-950/90 backdrop-blur-md flex flex-col items-center justify-center z-20 space-y-6 p-8">
              <div className="relative">
                <div className="w-16 h-16 rounded-full border-4 border-indigo-950 border-t-cyan-400 animate-spin" />
                <Sparkles className="w-6 h-6 text-cyan-400 absolute inset-0 m-auto animate-pulse" />
              </div>
              
              <div className="text-center space-y-2 max-w-sm">
                <h3 className="font-bold text-white text-base">Running Business Reasoning</h3>
                <p className="text-xs text-slate-400 h-10 flex items-center justify-center animate-pulse">
                  {compilingMessages[compilingStep]}
                </p>
              </div>

              <div className="w-64 h-1.5 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                <div 
                  className="h-full bg-gradient-to-r from-cyan-400 to-indigo-500 transition-all duration-1000" 
                  style={{ width: `${((compilingStep + 1) / compilingMessages.length) * 100}%` }}
                />
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Suggestion Chips */}
        {!isCompiling && currentStep < quickReplies.length && (
          <div className="px-6 py-2.5 bg-slate-900/40 border-t border-slate-800/60 flex flex-wrap gap-2">
            <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider py-1 pr-2">Quick responses:</span>
            {quickReplies[currentStep]?.map((replyText, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(replyText)}
                className="text-[10px] font-medium px-3 py-1 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-all border border-slate-700/50"
              >
                {replyText}
              </button>
            ))}
          </div>
        )}

        {/* Chat Input */}
        <div className="p-4 bg-slate-900 border-t border-slate-800">
          <form 
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex gap-3"
          >
            <input
              type="text"
              disabled={isSending || isCompiling || sessionStatus === 'completed'}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={sessionStatus === 'completed' ? "Consultation analysis completed." : "Enter your response..."}
              className="flex-1 px-4 py-3 bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:outline-none rounded-xl text-xs text-slate-200 placeholder-slate-600 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={isSending || isCompiling || sessionStatus === 'completed'}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white p-3 rounded-xl transition-all shadow-md shadow-indigo-600/10 flex items-center justify-center"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
      
    </div>
  );
}
