import React, { useState } from 'react';
import { 
  FileDown, 
  Sparkles, 
  Printer, 
  Mail, 
  Share2, 
  Loader2, 
  CheckCircle,
  FileText
} from 'lucide-react';

export default function ReportCenter({ sessionId, analysis }) {
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownloadPDF = async () => {
    setIsDownloading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/reports/${sessionId}/pdf`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `flowarchitect_report_${analysis.company_name.replace(/\s+/g, '_')}.pdf`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } else {
        alert("Failed to download PDF report");
      }
    } catch (e) {
      console.error(e);
      alert("Error generating PDF");
    } finally {
      setIsDownloading(false);
    }
  };

  const summary = analysis.business_summary || {};
  const painPoints = analysis.pain_points || {};
  const readiness = analysis.readiness_scores || {};
  const recommendations = analysis.recommendations || [];
  const techStack = analysis.tech_stack || [];
  const roi = analysis.roi_prediction || {};
  const roadmap = analysis.roadmap_plan || { phase1: [], phase2: [], phase3: [] };

  return (
    <div className="space-y-8 pb-12">
      
      {/* HEADER SECTION */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <span className="text-[10px] text-indigo-400 font-extrabold uppercase tracking-widest flex items-center gap-1.5 mb-1.5">
            <FileDown className="w-3.5 h-3.5" />
            Executive Report Hub
          </span>
          <h2 className="text-2xl font-black text-white">Consulting Deliverables</h2>
          <p className="text-xs text-slate-500">
            Export high-fidelity assessments and roadmaps to share with stakeholders or implementation teams
          </p>
        </div>

        {/* Actions bar */}
        <div className="flex gap-2">
          <button
            disabled={isDownloading}
            onClick={handleDownloadPDF}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition-all shadow-md shadow-indigo-600/15 disabled:opacity-50"
          >
            {isDownloading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Compiling Report PDF...
              </>
            ) : (
              <>
                <FileDown className="w-4 h-4" />
                Download Brief PDF
              </>
            )}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        
        {/* DOWNLOAD ACTION INFO CARD */}
        <div className="lg:col-span-1 space-y-6">
          <div className="glassmorphism p-5 rounded-2xl border border-slate-800 space-y-4">
            <div className="bg-indigo-600/15 w-10 h-10 rounded-xl flex items-center justify-center text-indigo-400 border border-indigo-500/20">
              <FileText className="w-5 h-5" />
            </div>
            <div className="space-y-1">
              <h4 className="font-bold text-sm text-slate-200">Consulting Brief</h4>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Includes full department readiness profiles, visual flowchart structures, custom trigger processes, complete technology software costs, and ROI projection sheets.
              </p>
            </div>
            
            <div className="pt-2">
              <span className="text-[9px] font-bold text-slate-500 uppercase block mb-1">Target Format:</span>
              <span className="text-[10px] text-slate-300 font-semibold">Standard Letter / PDF</span>
            </div>
          </div>

          <div className="bg-slate-900/40 border border-slate-850 p-4 rounded-xl text-[10px] text-slate-500 space-y-2 leading-relaxed">
            <span className="font-bold text-slate-400 block uppercase">Sharing Note:</span>
            All generated reports comply with enterprise privacy policies. Data generated from Gemini API keys are processed in stateless sandbox environments.
          </div>
        </div>

        {/* PRINT PAPER LAYOUT PREVIEW SHEET */}
        <div className="lg:col-span-3 bg-white text-slate-800 p-8 sm:p-12 rounded-2xl shadow-2xl border border-slate-200 min-h-[800px] overflow-y-auto space-y-8 font-sans select-none max-w-4xl mx-auto">
          
          {/* Cover Header */}
          <div className="border-b-4 border-indigo-950 pb-6 flex justify-between items-start">
            <div className="space-y-1">
              <span className="text-xs font-black text-indigo-600 tracking-widest uppercase">FlowArchitect AI Report</span>
              <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight leading-tight">
                Business Process Assessment
              </h1>
              <p className="text-xs text-slate-500 font-medium">Digital Transformation & AI Rollout Blueprint</p>
            </div>
            
            <div className="text-right text-[10px] text-slate-500 leading-normal">
              <strong>Assessment Date:</strong> June 5, 2026<br />
              <strong>Company:</strong> {analysis.company_name}<br />
              <strong>Industry:</strong> {analysis.industry}
            </div>
          </div>

          {/* Section 1: Executive Summary */}
          <div className="space-y-3">
            <h3 className="text-sm font-extrabold text-indigo-950 uppercase tracking-wider border-b border-slate-200 pb-1">
              1. Executive Summary
            </h3>
            <p className="text-xs leading-relaxed text-slate-600">
              This deliverable provides an operational analysis of core pipelines at <strong>{analysis.company_name}</strong>. Our diagnostic agents mapped processes and isolated bottlenecks that waste weekly hours. We propose a phased automation layout with specialized tech stack layers to reclaim operational focus.
            </p>
            
            <div className="grid grid-cols-2 gap-4 mt-2 bg-slate-50 p-3 rounded-lg border border-slate-100">
              <div className="text-xs space-y-1">
                <span className="font-bold text-slate-500 text-[9px] uppercase tracking-wider block">Key Processes Analysed:</span>
                <ul className="list-disc pl-4 space-y-0.5 text-[10px] text-slate-600">
                  {summary.key_processes?.map((p, idx) => <li key={idx}>{p}</li>)}
                </ul>
              </div>
              <div className="text-xs space-y-1.5">
                <div>
                  <span className="font-bold text-slate-500 text-[9px] uppercase tracking-wider block">Current Tools:</span>
                  <span className="text-[10px] text-slate-600 font-semibold">{summary.existing_tools || 'None'}</span>
                </div>
                <div>
                  <span className="font-bold text-slate-500 text-[9px] uppercase tracking-wider block">Primary Bottlenecks:</span>
                  <span className="text-[10px] text-slate-600 block">{summary.operational_bottlenecks || 'None'}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Section 2: Pain Points */}
          <div className="space-y-3">
            <h3 className="text-sm font-extrabold text-indigo-950 uppercase tracking-wider border-b border-slate-200 pb-1">
              2. Operational Friction Points
            </h3>
            <div className="space-y-2 text-xs">
              <div className="grid grid-cols-4 gap-2 border-b border-slate-100 py-1.5">
                <strong className="text-slate-700 text-[10px]">Manual Work</strong>
                <span className="col-span-3 text-slate-600 text-[10px]">{painPoints.manual_work || 'N/A'}</span>
              </div>
              <div className="grid grid-cols-4 gap-2 border-b border-slate-100 py-1.5">
                <strong className="text-slate-700 text-[10px]">Communications</strong>
                <span className="col-span-3 text-slate-600 text-[10px]">{painPoints.customer_communication || 'N/A'}</span>
              </div>
              <div className="grid grid-cols-4 gap-2 py-1.5">
                <strong className="text-slate-700 text-[10px]">Sales/Support</strong>
                <span className="col-span-3 text-slate-600 text-[10px]">{painPoints.sales_inefficiencies || painPoints.support_inefficiencies || 'N/A'}</span>
              </div>
            </div>
          </div>

          {/* Section 3: Readiness Score Table */}
          <div className="space-y-3">
            <h3 className="text-sm font-extrabold text-indigo-950 uppercase tracking-wider border-b border-slate-200 pb-1">
              3. Department Readiness Scores
            </h3>
            <div className="grid grid-cols-5 gap-3 text-center">
              {Object.entries(readiness).map(([dept, val]) => (
                <div key={dept} className="p-2 border border-slate-100 bg-slate-50/50 rounded-lg text-xs">
                  <span className="block font-bold text-slate-500 text-[9px] uppercase tracking-wider">{dept}</span>
                  <span className="text-base font-extrabold text-slate-800 block mt-1">{val}%</span>
                </div>
              ))}
            </div>
          </div>

          {/* Section 4: Recommendations */}
          <div className="space-y-3">
            <h3 className="text-sm font-extrabold text-indigo-950 uppercase tracking-wider border-b border-slate-200 pb-1">
              4. Proposed AI Automation Blueprints
            </h3>
            <div className="space-y-4 text-xs">
              {recommendations.map((rec, idx) => (
                <div key={idx} className="p-4 border border-slate-100 bg-slate-50 rounded-xl space-y-2">
                  <div className="flex justify-between border-b border-slate-200 pb-1.5">
                    <strong className="text-slate-800 text-[11px]">#{idx+1} {rec.title}</strong>
                    <span className="text-[9px] font-bold text-indigo-600 uppercase">{rec.category} | {rec.priority} Priority</span>
                  </div>
                  <p className="text-slate-600 text-[10px] leading-relaxed">{rec.description}</p>
                  {rec.blueprint && (
                    <div className="pt-2 text-[9px] text-slate-500 space-y-1">
                      <div><strong>Trigger:</strong> {rec.blueprint.trigger}</div>
                      <div><strong>Actions:</strong> {rec.blueprint.process?.join(' -> ')}</div>
                      <div><strong>Tech Required:</strong> {rec.blueprint.tools?.join(', ')}</div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Section 5: Tech Stack & ROI */}
          <div className="grid grid-cols-2 gap-6 pt-4">
            <div className="space-y-3">
              <h4 className="text-xs font-bold text-indigo-950 uppercase tracking-wider border-b border-slate-200 pb-1">
                5. Tech Stack Stack
              </h4>
              <div className="space-y-2">
                {techStack.map((item, idx) => (
                  <div key={idx} className="flex justify-between text-[10px] border-b border-slate-100 pb-1">
                    <span className="font-semibold text-slate-600">{item.tool}</span>
                    <span className="text-slate-500">INR {item.cost}/mo</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="text-xs font-bold text-indigo-950 uppercase tracking-wider border-b border-slate-200 pb-1">
                6. ROI Projections
              </h4>
              <div className="space-y-2 text-[10px]">
                <div className="flex justify-between border-b border-slate-100 pb-1">
                  <span className="text-slate-600">Reclaimed Time:</span>
                  <strong className="text-indigo-600">{roi.hours_saved_weekly} Hours / week</strong>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-1">
                  <span className="text-slate-600">Net Monthly Savings:</span>
                  <strong className="text-emerald-600">INR {roi.monthly_cost_savings}</strong>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-1">
                  <span className="text-slate-600">Conversion Rate Shift:</span>
                  <strong className="text-indigo-600">{roi.current_conversion}% {"\u2192"} {roi.predicted_conversion}%</strong>
                </div>
              </div>
            </div>
          </div>

          {/* Section 6: Roadmap */}
          <div className="space-y-3">
            <h3 className="text-sm font-extrabold text-indigo-950 uppercase tracking-wider border-b border-slate-200 pb-1">
              7. Phased Implementation Roadmap
            </h3>
            
            <div className="space-y-3 text-[10px]">
              <div>
                <strong className="text-slate-700 block">Phase 1: Quick Wins (Weeks 1-2)</strong>
                {roadmap.phase1?.map((step, idx) => (
                  <div key={idx} className="pl-3 border-l-2 border-indigo-500 text-slate-600 mt-1">
                    • <strong>{step.title}:</strong> {step.action} (Deliverable: {step.deliverables})
                  </div>
                ))}
              </div>
              <div>
                <strong className="text-slate-700 block mt-2">Phase 2: CRM & Core Systems Integration (Weeks 3-5)</strong>
                {roadmap.phase2?.map((step, idx) => (
                  <div key={idx} className="pl-3 border-l-2 border-cyan-400 text-slate-600 mt-1">
                    • <strong>{step.title}:</strong> {step.action} (Deliverable: {step.deliverables})
                  </div>
                ))}
              </div>
              <div>
                <strong className="text-slate-700 block mt-2">Phase 3: Advanced AI & Agent Orchestration (Weeks 6-8)</strong>
                {roadmap.phase3?.map((step, idx) => (
                  <div key={idx} className="pl-3 border-l-2 border-emerald-400 text-slate-600 mt-1">
                    • <strong>{step.title}:</strong> {step.action} (Deliverable: {step.deliverables})
                  </div>
                ))}
              </div>
            </div>
          </div>
          
        </div>
      </div>
      
    </div>
  );
}
