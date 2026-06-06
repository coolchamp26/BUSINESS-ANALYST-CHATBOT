import React from 'react';
import { 
  Building2, 
  ShoppingCart, 
  Home, 
  Stethoscope, 
  GraduationCap, 
  Laptop, 
  UtensilsCrossed, 
  Megaphone,
  ArrowRight,
  Sparkles,
  Bot,
  Gauge,
  FileText
} from 'lucide-react';

export default function LandingPage({ onStartConsultation, onLoadTemplate }) {
  const templates = [
    { key: 'dental_clinic', label: 'Dental Clinic', desc: 'Appointment schedules, patient recalls & insurance processing workflows.', icon: Stethoscope, color: 'from-emerald-500/20 to-teal-500/10 border-emerald-500/30 text-emerald-400' },
    { key: 'ecommerce_store', label: 'E-commerce Store', desc: 'Inventory counts, cart drop-offs recovery drips & WISMO ticket reduction.', icon: ShoppingCart, color: 'from-blue-500/20 to-indigo-500/10 border-blue-500/30 text-blue-400' },
    { key: 'real_estate', label: 'Real Estate Agency', desc: 'Buyer qualifications, showing calendars & portal lead responders.', icon: Home, color: 'from-violet-500/20 to-purple-500/10 border-violet-500/30 text-violet-400' },
    { key: 'hospital', label: 'Hospital Center', desc: 'Patient check-ins, pre-op reminders, bed tracking & billing syncer.', icon: Building2, color: 'from-red-500/20 to-rose-500/10 border-red-500/30 text-rose-400' },
    { key: 'coaching_institute', label: 'Coaching Institute', desc: 'Automated subscription fee alerts & student RAG doubt responders.', icon: GraduationCap, color: 'from-amber-500/20 to-orange-500/10 border-amber-500/30 text-amber-400' },
    { key: 'saas_startup', label: 'SaaS Startup', desc: 'Segment onboarding triggers, API debugging bot & trial churn alerts.', icon: Laptop, color: 'from-cyan-500/20 to-sky-500/10 border-cyan-500/30 text-cyan-400' },
    { key: 'restaurant', label: 'Restaurant / F&B', desc: 'Reservation text agents, loyalty drops & automatic inventory reordering.', icon: UtensilsCrossed, color: 'from-pink-500/20 to-fuchsia-500/10 border-pink-500/30 text-pink-400' },
    { key: 'marketing_agency', label: 'Marketing Agency', desc: 'Client onboarding sheets,Looker dashboard syncer & PDF proposals.', icon: Megaphone, color: 'from-indigo-500/20 to-indigo-500/10 border-indigo-500/30 text-indigo-400' }
  ];

  return (
    <div className="space-y-16 py-4 relative">
      {/* Background radial glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none z-0" />
      
      {/* HERO SECTION */}
      <section className="text-center space-y-6 max-w-4xl mx-auto relative z-10 pt-8">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-xs font-semibold text-indigo-300">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          Virtual AI Operations Partner
        </div>
        
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight leading-[1.15] text-white">
          Architect Frictionless Operations <br />
          <span className="bg-gradient-to-r from-cyan-400 via-indigo-400 to-violet-500 bg-clip-text text-transparent">
            Powered by Multi-Agent AI
          </span>
        </h1>
        
        <p className="text-base md:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          FlowArchitect AI acts as an enterprise consultant. We analyze your workflows, find manual bottlenecks, design live blueprints, recommend tech stacks, and forecast ROI.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <button
            onClick={() => onStartConsultation()}
            className="flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm transition-all duration-200 shadow-lg shadow-indigo-600/20 hover:scale-[1.02]"
          >
            Start Interactive Audit
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </section>

      {/* CORE STATS HIGHLIGHT */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto relative z-10">
        <div className="glassmorphism p-6 rounded-2xl border border-slate-800 space-y-3">
          <div className="bg-cyan-500/15 w-10 h-10 rounded-lg flex items-center justify-center text-cyan-400">
            <Bot className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-white">Multi-Agent Diagnostics</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Collaborating agents analyze spreadsheets, support tickets, and scheduling logs to extract exact pain points.
          </p>
        </div>

        <div className="glassmorphism p-6 rounded-2xl border border-slate-800 space-y-3">
          <div className="bg-indigo-500/15 w-10 h-10 rounded-lg flex items-center justify-center text-indigo-400">
            <Gauge className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-white">ROI Prediction Engine</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Forecast conversion improvements, monthly savings, and employee hours saved with interactive charts.
          </p>
        </div>

        <div className="glassmorphism p-6 rounded-2xl border border-slate-800 space-y-3">
          <div className="bg-violet-500/15 w-10 h-10 rounded-lg flex items-center justify-center text-violet-400">
            <FileText className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-base text-white">Actionable Blueprints</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Generate detailed trigger-step execution maps and visual flowcharts ready to build in Zapier, n8n, or Python.
          </p>
        </div>
      </section>

      {/* QUICK START TEMPLATES SECTION */}
      <section className="space-y-6 relative z-10">
        <div className="text-center max-w-xl mx-auto space-y-2">
          <h2 className="text-2xl md:text-3xl font-bold text-white tracking-tight">
            Hackathon Demo Center
          </h2>
          <p className="text-xs md:text-sm text-slate-400">
            Load pre-populated operational details instantly to evaluate the entire suite of dashboards, flowcharts, roadmaps, and PDF exports.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {templates.map((tmpl) => {
            const Icon = tmpl.icon;
            return (
              <button
                key={tmpl.key}
                onClick={() => onLoadTemplate(tmpl.key)}
                className={`glassmorphism text-left p-5 rounded-2xl border transition-all duration-300 hover:scale-[1.03] group relative overflow-hidden flex flex-col justify-between h-48 hover:border-indigo-500/50 ${tmpl.color}`}
              >
                {/* Visual glow on card hover */}
                <div className="absolute -right-8 -bottom-8 w-24 h-24 bg-indigo-500/5 rounded-full blur-xl transition-all group-hover:scale-150" />
                
                <div className="space-y-3">
                  <div className="p-2 w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center">
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm text-white group-hover:text-cyan-400 transition-colors">
                      {tmpl.label}
                    </h4>
                    <p className="text-[11px] text-slate-400 leading-relaxed mt-1">
                      {tmpl.desc}
                    </p>
                  </div>
                </div>

                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 group-hover:text-indigo-400 transition-colors flex items-center gap-1.5 mt-4">
                  Run Diagnostics Demo
                  <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </button>
            );
          })}
        </div>
      </section>
      
    </div>
  );
}
