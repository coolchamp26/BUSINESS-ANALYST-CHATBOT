import React, { useState } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Legend, 
  ResponsiveContainer, 
  CartesianGrid,
  AreaChart,
  Area
} from 'recharts';
import { 
  Sparkles, 
  Clock, 
  CircleDollarSign, 
  Zap, 
  TrendingUp, 
  Building2, 
  Wrench, 
  ChevronRight, 
  TrendingDown,
  Info
} from 'lucide-react';

export default function DashboardPage({ analysis, onNavigate }) {
  const [activeRec, setActiveRec] = useState(0);

  // Extract analysis fields
  const summary = analysis.business_summary || {};
  const painPoints = analysis.pain_points || {};
  const readiness = analysis.readiness_scores || {};
  const recommendations = analysis.recommendations || [];
  const techStack = analysis.tech_stack || [];
  const roi = analysis.roi_prediction || {};

  // Formulate data for Recharts
  const leadData = [
    { name: 'Monthly Leads', Before: roi.current_leads || 0, After: roi.predicted_leads || 0 }
  ];

  const conversionData = [
    { name: 'Conversion Rate', Before: roi.current_conversion || 0, After: roi.predicted_conversion || 0 }
  ];

  const costData = [
    { name: 'Support Cost (INR)', Before: roi.current_support_cost || 0, After: roi.predicted_support_cost || 0 }
  ];

  // Helper for circular gauge color
  const getScoreColor = (score) => {
    if (score < 40) return 'text-red-500 stroke-red-500';
    if (score < 70) return 'text-amber-500 stroke-amber-500';
    return 'text-emerald-500 stroke-emerald-500';
  };

  return (
    <div className="space-y-8 pb-12">
      
      {/* HEADER SECTION */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <span className="text-[10px] text-indigo-400 font-extrabold uppercase tracking-widest flex items-center gap-1.5 mb-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            Audit Report Generated
          </span>
          <h2 className="text-2xl font-black text-white">{analysis.company_name} — Operational Cockpit</h2>
          <p className="text-xs text-slate-500">{analysis.industry}  |  {analysis.company_size}</p>
        </div>

        <button
          onClick={() => onNavigate('workflow')}
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition-all shadow-md shadow-indigo-600/15"
        >
          View Process Flowcharts
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* CORE ROI OVERVIEW CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glassmorphism p-5 rounded-2xl border border-slate-800 flex items-center justify-between relative overflow-hidden">
          <div className="space-y-1 z-10">
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Weekly Time Saved</span>
            <h3 className="text-2xl font-black text-white">{roi.hours_saved_weekly} Hours</h3>
            <span className="text-[9px] text-cyan-400 block font-semibold italic">Reclaimed staff hours</span>
          </div>
          <div className="bg-cyan-500/10 p-3 rounded-xl text-cyan-400 z-10 border border-cyan-500/20">
            <Clock className="w-6 h-6" />
          </div>
        </div>

        <div className="glassmorphism p-5 rounded-2xl border border-slate-800 flex items-center justify-between relative overflow-hidden">
          <div className="space-y-1 z-10">
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Support Overhead</span>
            <h3 className="text-2xl font-black text-red-400 flex items-center gap-1">
              -{Math.round(((roi.current_support_cost - roi.predicted_support_cost) / (roi.current_support_cost || 1)) * 100)}%
            </h3>
            <span className="text-[9px] text-slate-400 block">INR {roi.predicted_support_cost}/mo after automation</span>
          </div>
          <div className="bg-red-500/10 p-3 rounded-xl text-red-400 z-10 border border-red-500/20">
            <TrendingDown className="w-6 h-6" />
          </div>
        </div>

        <div className="glassmorphism p-5 rounded-2xl border border-slate-800 flex items-center justify-between relative overflow-hidden">
          <div className="space-y-1 z-10">
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Monthly Reclaimed Cash</span>
            <h3 className="text-2xl font-black text-emerald-400">INR {roi.monthly_cost_savings}</h3>
            <span className="text-[9px] text-emerald-400 block font-semibold italic">Direct operational savings</span>
          </div>
          <div className="bg-emerald-500/10 p-3 rounded-xl text-emerald-400 z-10 border border-emerald-500/20">
            <CircleDollarSign className="w-6 h-6" />
          </div>
        </div>

        <div className="glassmorphism p-5 rounded-2xl border border-slate-800 flex items-center justify-between relative overflow-hidden">
          <div className="space-y-1 z-10">
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Lead Conversion Lift</span>
            <h3 className="text-2xl font-black text-indigo-400">
              +{Math.round((roi.predicted_conversion - roi.current_conversion))} %
            </h3>
            <span className="text-[9px] text-indigo-400 block font-semibold italic">From {roi.current_conversion}% to {roi.predicted_conversion}%</span>
          </div>
          <div className="bg-indigo-500/10 p-3 rounded-xl text-indigo-400 z-10 border border-indigo-500/20">
            <TrendingUp className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* DEPARTMENT READINESS METERS */}
      <div className="glassmorphism p-6 rounded-2xl border border-slate-800 space-y-6">
        <div>
          <h3 className="font-extrabold text-sm text-white uppercase tracking-wider">Department Readiness Profile</h3>
          <p className="text-[10px] text-slate-500">Lower scores indicate manual dependency and higher priority to deploy AI solutions</p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-5 gap-6">
          {Object.entries(readiness).map(([dept, val]) => {
            const circleColor = getScoreColor(val);
            const radius = 30;
            const circumference = 2 * Math.PI * radius;
            const strokeDashoffset = circumference - (val / 100) * circumference;

            return (
              <div key={dept} className="flex flex-col items-center justify-center p-4 bg-slate-900/40 rounded-xl border border-slate-850 space-y-3">
                {/* SVG Circle Gauge */}
                <div className="relative w-16 h-16">
                  <svg className="w-full h-full transform -rotate-90">
                    <circle cx="32" cy="32" r={radius} className="stroke-slate-800 fill-none" strokeWidth="4" />
                    <circle 
                      cx="32" 
                      cy="32" 
                      r={radius} 
                      className={`fill-none transition-all duration-1000 ${circleColor.split(' ')[1]}`} 
                      strokeWidth="4" 
                      strokeDasharray={circumference}
                      strokeDashoffset={strokeDashoffset}
                      strokeLinecap="round"
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="font-extrabold text-xs text-white">{val}%</span>
                  </div>
                </div>

                <div className="text-center">
                  <span className="block font-bold text-[11px] text-slate-300 leading-tight">{dept}</span>
                  <span className={`text-[9px] font-semibold tracking-wider uppercase ${circleColor.split(' ')[0]}`}>
                    {val < 40 ? 'Critically Manual' : val < 70 ? 'Developing' : 'Optimized'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* CHART INSIGHTS (BEFORE VS AFTER) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Leads Chart */}
        <div className="glassmorphism p-5 rounded-2xl border border-slate-800 space-y-4">
          <h4 className="font-extrabold text-xs text-white uppercase tracking-wider flex items-center gap-1.5">
            <Zap className="w-3.5 h-3.5 text-cyan-400" />
            Monthly Lead Pipeline Growth
          </h4>
          <div className="h-48 w-full text-xs">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={leadData} barGap={10}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Legend />
                <Bar dataKey="Before" fill="#475569" radius={[4, 4, 0, 0]} />
                <Bar dataKey="After" fill="#22d3ee" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Conversion Chart */}
        <div className="glassmorphism p-5 rounded-2xl border border-slate-800 space-y-4">
          <h4 className="font-extrabold text-xs text-white uppercase tracking-wider flex items-center gap-1.5">
            <TrendingUp className="w-3.5 h-3.5 text-indigo-400" />
            Conversion Performance Lift
          </h4>
          <div className="h-48 w-full text-xs">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={conversionData} barGap={10}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" stroke="#64748b" />
                <YAxis stroke="#64748b" unit="%" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Legend />
                <Bar dataKey="Before" fill="#475569" radius={[4, 4, 0, 0]} />
                <Bar dataKey="After" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Cost Reduction Chart */}
        <div className="glassmorphism p-5 rounded-2xl border border-slate-800 space-y-4">
          <h4 className="font-extrabold text-xs text-white uppercase tracking-wider flex items-center gap-1.5">
            <TrendingDown className="w-3.5 h-3.5 text-rose-500" />
            Customer Support Cost Cut
          </h4>
          <div className="h-48 w-full text-xs">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={costData} barGap={10}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Legend />
                <Bar dataKey="Before" fill="#475569" radius={[4, 4, 0, 0]} />
                <Bar dataKey="After" fill="#f43f5e" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* RECOMMENDATIONS & TECHNOLOGY STACKS GRID */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* RECOMMENDATION SELECTOR */}
        <div className="glassmorphism p-6 rounded-2xl border border-slate-800 space-y-4">
          <div>
            <h3 className="font-extrabold text-sm text-white uppercase tracking-wider">AI Automation Opportunities</h3>
            <p className="text-[10px] text-slate-500">Tailored integrations selected for maximum operational leverage</p>
          </div>

          <div className="space-y-3">
            {recommendations.map((rec, idx) => (
              <button
                key={idx}
                onClick={() => setActiveRec(idx)}
                className={`w-full text-left p-4 rounded-xl border transition-all flex justify-between items-start gap-4 ${
                  activeRec === idx 
                    ? 'bg-slate-900 border-indigo-500 text-white' 
                    : 'bg-slate-950 border-slate-850 hover:border-slate-800 text-slate-400'
                }`}
              >
                <div className="space-y-1">
                  <span className="text-[8px] uppercase tracking-wider font-extrabold text-indigo-400">{rec.category}</span>
                  <h4 className="font-bold text-xs text-slate-200">{rec.title}</h4>
                  <p className="text-[10px] text-slate-500 line-clamp-1">{rec.problem}</p>
                </div>
                
                <div className="flex flex-col items-end gap-1.5 shrink-0">
                  <span className={`text-[8px] font-bold px-2 py-0.5 rounded-full ${
                    rec.priority === 'High' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                  }`}>
                    {rec.priority} Priority
                  </span>
                  <span className="text-[9px] text-slate-500 font-semibold">{rec.setup_time || 'N/A'}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* DETAILED BLUEPRINT PREVIEW */}
        <div className="glassmorphism p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
          {recommendations[activeRec] ? (
            <div className="space-y-5 flex-1">
              {/* Header */}
              <div className="border-b border-slate-800 pb-3 flex justify-between items-start">
                <div>
                  <span className="text-[8px] uppercase tracking-widest font-extrabold text-cyan-400">
                    Active Blueprint Detail
                  </span>
                  <h4 className="font-extrabold text-sm text-white mt-1">
                    {recommendations[activeRec].title}
                  </h4>
                </div>
                <div className="text-right text-[10px] text-slate-500 font-bold uppercase">
                  Setup Effort: <span className="text-cyan-400">{recommendations[activeRec].effort}</span>
                </div>
              </div>

              {/* Problem/Solution */}
              <div className="space-y-2">
                <div className="text-xs">
                  <span className="font-bold text-slate-400 block text-[9px] uppercase tracking-wider">Identified Friction:</span>
                  <p className="text-slate-300 italic text-[11px] leading-relaxed mt-0.5">"{recommendations[activeRec].problem}"</p>
                </div>
                <div className="text-xs">
                  <span className="font-bold text-slate-400 block text-[9px] uppercase tracking-wider">AI Solution:</span>
                  <p className="text-slate-300 text-[11px] leading-relaxed mt-0.5">{recommendations[activeRec].solution}</p>
                </div>
              </div>

              {/* Blueprint Steps */}
              {recommendations[activeRec].blueprint && (
                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-850 space-y-3">
                  <span className="text-[9px] font-bold text-slate-400 block uppercase tracking-wider">Technical Trigger-Action Sequence:</span>
                  <div className="text-xs space-y-2">
                    <div>
                      <span className="font-semibold text-cyan-400 text-[10px]">Trigger: </span>
                      <span className="text-slate-300 text-[10px]">{recommendations[activeRec].blueprint.trigger}</span>
                    </div>
                    <div className="space-y-1.5 pl-3 border-l border-slate-800 mt-2">
                      {recommendations[activeRec].blueprint.process?.map((stepText, idx) => (
                        <div key={idx} className="flex gap-2 text-[10px]">
                          <span className="text-indigo-400 font-bold">{idx + 1}.</span>
                          <span className="text-slate-400">{stepText}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center text-center p-8 h-full text-slate-600">
              <Info className="w-8 h-8 mb-2 text-slate-700" />
              Select an opportunity to view its implementation blueprint
            </div>
          )}

          <div className="pt-4 border-t border-slate-800 mt-6 flex justify-between items-center text-[10px]">
            <span className="text-slate-500 font-bold uppercase tracking-wider">Core Tools:</span>
            <span className="font-semibold text-slate-300">
              {recommendations[activeRec]?.blueprint?.tools?.join(', ') || 'N/A'}
            </span>
          </div>
        </div>
      </div>

      {/* RECOMMENDED TECHNOLOGY STACKS GRID */}
      <div className="glassmorphism p-6 rounded-2xl border border-slate-800 space-y-4">
        <div>
          <h3 className="font-extrabold text-sm text-white uppercase tracking-wider">Automation Software Architecture Stack</h3>
          <p className="text-[10px] text-slate-500">Selected technology tools and monthly licensing projections for your operations</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-900/40 text-slate-400 font-bold">
                <th className="p-4 rounded-l-xl">Category / Area</th>
                <th className="p-4">Recommended Tool</th>
                <th className="p-4">Monthly Cost</th>
                <th className="p-4">Complexity</th>
                <th className="p-4 rounded-r-xl">Setup Time</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {techStack.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-900/20 text-slate-300">
                  <td className="p-4 font-bold text-slate-400">{item.category}</td>
                  <td className="p-4 text-cyan-400 font-semibold">{item.tool}</td>
                  <td className="p-4">INR {item.cost}</td>
                  <td className="p-4">
                    <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
                      item.difficulty === 'High' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-slate-800 text-slate-400'
                    }`}>
                      {item.difficulty}
                    </span>
                  </td>
                  <td className="p-4 font-semibold text-slate-400">{item.setup_time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
    </div>
  );
}
