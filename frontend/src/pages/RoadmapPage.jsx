import React, { useState } from 'react';
import { 
  CalendarDays, 
  Sparkles, 
  Zap, 
  Puzzle, 
  Cpu, 
  CheckCircle,
  HelpCircle,
  Clock
} from 'lucide-react';

export default function RoadmapPage({ analysis }) {
  const [activeStep, setActiveStep] = useState(null);
  const roadmap = analysis.roadmap_plan || { phase1: [], phase2: [], phase3: [] };

  const phases = [
    {
      id: 'phase1',
      title: 'Phase 1: Quick Wins',
      subtitle: 'Immediate impact, low-friction setup',
      timeline: 'Weeks 1–2',
      icon: Zap,
      color: 'text-amber-400 border-amber-500/20 bg-amber-500/5',
      bulletColor: 'bg-amber-400',
      steps: roadmap.phase1 || []
    },
    {
      id: 'phase2',
      title: 'Phase 2: CRM & Systems Integration',
      subtitle: 'Connecting core data pipelines',
      timeline: 'Weeks 3–5',
      icon: Puzzle,
      color: 'text-indigo-400 border-indigo-500/20 bg-indigo-500/5',
      bulletColor: 'bg-indigo-400',
      steps: roadmap.phase2 || []
    },
    {
      id: 'phase3',
      title: 'Phase 3: Advanced AI Operations',
      subtitle: 'Multi-agent automations & predictions',
      timeline: 'Weeks 6–8',
      icon: Cpu,
      color: 'text-cyan-400 border-cyan-500/20 bg-cyan-500/5',
      bulletColor: 'bg-cyan-400',
      steps: roadmap.phase3 || []
    }
  ];

  return (
    <div className="space-y-6 pb-12">
      
      {/* HEADER SECTION */}
      <div className="border-b border-slate-800 pb-5">
        <span className="text-[10px] text-indigo-400 font-extrabold uppercase tracking-widest flex items-center gap-1.5 mb-1.5">
          <CalendarDays className="w-3.5 h-3.5" />
          Phased Transformation Roadmap
        </span>
        <h2 className="text-2xl font-black text-white">8-Week Operational Rollout</h2>
        <p className="text-xs text-slate-500">
          A step-by-step technical implementation path designed to optimize cash flow and staff workload
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 relative">
        {/* Decorative connecting connector line for timeline */}
        <div className="absolute top-[28px] left-[26px] right-[26px] h-[3px] bg-slate-850 hidden lg:block z-0" />
        
        {phases.map((phase, pIdx) => {
          const PhaseIcon = phase.icon;
          return (
            <div key={phase.id} className="space-y-6 relative z-10">
              
              {/* Phase header card */}
              <div className={`p-4 rounded-xl border flex gap-3 items-center ${phase.color}`}>
                <div className="p-2 bg-slate-900 border border-slate-800 rounded-lg shrink-0">
                  <PhaseIcon className="w-5 h-5" />
                </div>
                <div>
                  <span className="text-[9px] font-extrabold tracking-widest uppercase opacity-75">{phase.timeline}</span>
                  <h4 className="font-bold text-xs text-white leading-tight mt-0.5">{phase.title}</h4>
                  <span className="text-[10px] text-slate-400 block mt-0.5">{phase.subtitle}</span>
                </div>
              </div>

              {/* Steps vertical path */}
              <div className="space-y-4 pl-2 border-l border-slate-850 lg:border-l-0 lg:pl-0">
                {phase.steps.map((step, sIdx) => {
                  const stepId = `${phase.id}-${sIdx}`;
                  const isActive = activeStep === stepId;
                  
                  return (
                    <div 
                      key={sIdx} 
                      className={`glassmorphism rounded-xl border transition-all duration-200 text-left p-4 hover:border-slate-700 cursor-pointer ${
                        isActive ? 'border-indigo-500' : 'border-slate-850'
                      }`}
                      onClick={() => setActiveStep(isActive ? null : stepId)}
                    >
                      <div className="flex gap-3.5 items-start">
                        {/* Timeline Bullet marker */}
                        <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 border ${
                          isActive ? 'border-cyan-400 text-cyan-400' : 'border-slate-800 text-slate-500'
                        }`}>
                          <CheckCircle className="w-3.5 h-3.5" />
                        </div>

                        <div className="space-y-1">
                          <span className="text-[8px] font-extrabold tracking-wider text-slate-500 uppercase flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {step.timeline || 'Schedule Pending'}
                          </span>
                          <h5 className="font-bold text-xs text-slate-200">{step.title}</h5>
                        </div>
                      </div>

                      {/* Expandable Action details */}
                      {isActive && (
                        <div className="mt-4 pt-3 border-t border-slate-850 text-xs space-y-3 animate-fadeIn">
                          <div className="space-y-1 bg-slate-900/40 p-3 rounded-lg border border-slate-850">
                            <span className="text-[9px] font-extrabold text-slate-500 uppercase tracking-widest block">Implementation Action:</span>
                            <p className="text-slate-300 leading-relaxed text-[11px] mt-0.5">{step.action}</p>
                          </div>
                          
                          <div className="space-y-1">
                            <span className="text-[9px] font-extrabold text-slate-500 uppercase tracking-widest block">Key Deliverable:</span>
                            <p className="text-cyan-400 text-[10px]">{step.deliverables}</p>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

            </div>
          );
        })}
      </div>

      {/* QUICK TROUBLESHOOTING NOTES */}
      <div className="glassmorphism p-5 rounded-2xl border border-slate-800 flex gap-4 items-start max-w-4xl">
        <div className="bg-indigo-500/10 p-2.5 rounded-xl text-indigo-400 shrink-0 border border-indigo-500/20">
          <HelpCircle className="w-5 h-5" />
        </div>
        <div className="space-y-1 text-xs">
          <h4 className="font-bold text-slate-200">Consultant Rollout Advice</h4>
          <p className="text-slate-400 leading-relaxed text-[11px]">
            We suggest completing Phase 1 FAQ configurations inside lookup sheets first. Doing this builds immediate employee confidence, clarifies messaging formats, and recaptures early hours to reinvest into complex database migrations in Phase 2.
          </p>
        </div>
      </div>
      
    </div>
  );
}
