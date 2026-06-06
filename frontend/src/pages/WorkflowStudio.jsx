import React, { useState, useRef } from 'react';
import { 
  ZoomIn, 
  ZoomOut, 
  Maximize2, 
  Download, 
  Network, 
  FileJson, 
  Play, 
  HelpCircle,
  Code
} from 'lucide-react';

export default function WorkflowStudio({ analysis }) {
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [hoveredNode, setHoveredNode] = useState(null);
  const [activeTab, setActiveTab] = useState('diagram'); // diagram or json
  const svgRef = useRef(null);

  // Extract workflow data
  const workflow = analysis.workflow_diagram || { nodes: [], edges: [] };
  const nodes = workflow.nodes || [];
  const edges = workflow.edges || [];

  // Pan and Zoom Controls
  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.1, 2.0));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.1, 0.5));
  const handleReset = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  // Drag Canvas Handlers
  const handleMouseDown = (e) => {
    if (e.target.tagName === 'svg' || e.target.id === 'canvas-grid') {
      setIsDragging(true);
      setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      setPan({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y
      });
    }
  };

  const handleMouseUp = () => setIsDragging(false);

  // Export SVG as a file
  const handleExportSVG = () => {
    if (!svgRef.current) return;
    try {
      const serializer = new XMLSerializer();
      const source = serializer.serializeToString(svgRef.current);
      const svgBlob = new Blob([source], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(svgBlob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `flowarchitect_blueprint_${analysis.company_name.replace(/\s+/g, '_')}.svg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      alert("Error exporting SVG diagram");
    }
  };

  // Helper for nodes styles
  const getNodeColor = (type) => {
    switch (type) {
      case 'trigger': return 'fill-indigo-950 stroke-indigo-400 text-indigo-400';
      case 'process': return 'fill-slate-900 stroke-cyan-500 text-cyan-400';
      case 'action': return 'fill-slate-900 stroke-emerald-500 text-emerald-400';
      default: return 'fill-slate-900 stroke-slate-700 text-slate-400';
    }
  };

  return (
    <div className="space-y-6 pb-12">
      
      {/* HEADER BAR */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <span className="text-[10px] text-cyan-400 font-extrabold uppercase tracking-widest flex items-center gap-1.5 mb-1.5">
            <Network className="w-3.5 h-3.5" />
            Process Workflow Studio
          </span>
          <h2 className="text-2xl font-black text-white">Interactive Automation Blueprint</h2>
          <p className="text-xs text-slate-500">
            Visualizing the live trigger-action data flows generated for {analysis.company_name}
          </p>
        </div>

        {/* Tab Toggle */}
        <div className="flex bg-slate-900 border border-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('diagram')}
            className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-2 ${
              activeTab === 'diagram' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Network className="w-3.5 h-3.5" />
            Visual Canvas
          </button>
          <button
            onClick={() => setActiveTab('json')}
            className={`px-4 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-2 ${
              activeTab === 'json' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileJson className="w-3.5 h-3.5" />
            JSON Blueprint
          </button>
        </div>
      </div>

      {activeTab === 'diagram' ? (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* SVG CANVAS BOARD */}
          <div className="lg:col-span-3 flex flex-col glassmorphism border border-slate-800 rounded-2xl overflow-hidden h-[500px] relative select-none">
            {/* Board controls */}
            <div className="absolute top-4 right-4 flex gap-2 z-10">
              <button
                onClick={handleZoomIn}
                className="p-2 bg-slate-900 border border-slate-850 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-all shadow-md"
                title="Zoom In"
              >
                <ZoomIn className="w-4 h-4" />
              </button>
              <button
                onClick={handleZoomOut}
                className="p-2 bg-slate-900 border border-slate-850 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-all shadow-md"
                title="Zoom Out"
              >
                <ZoomOut className="w-4 h-4" />
              </button>
              <button
                onClick={handleReset}
                className="p-2 bg-slate-900 border border-slate-850 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-all shadow-md"
                title="Reset View"
              >
                <Maximize2 className="w-4 h-4" />
              </button>
              <button
                onClick={handleExportSVG}
                className="flex items-center gap-1.5 px-3 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-white text-xs font-bold transition-all shadow-md shadow-indigo-600/15"
                title="Export Image"
              >
                <Download className="w-4 h-4" />
                Export SVG
              </button>
            </div>

            {/* Instruction tooltip */}
            <div className="absolute bottom-4 left-4 bg-slate-900/80 border border-slate-800/85 px-3 py-1.5 rounded-lg text-[10px] text-slate-400 leading-normal pointer-events-none max-w-xs">
              <span className="font-semibold text-white block mb-0.5">Canvas Guide:</span>
              • Drag blank canvas space to PAN.<br />
              • Hover over process nodes to view details.
            </div>

            {/* SVG drawing board */}
            <svg
              ref={svgRef}
              className="w-full h-full cursor-grab active:cursor-grabbing"
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseUp}
              style={{ backgroundColor: '#020617' }}
            >
              {/* Background Dots Grid */}
              <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                  <circle cx="2" cy="2" r="1" fill="rgba(255,255,255,0.05)" />
                </pattern>
                
                {/* Arrow Marker Definitions */}
                <marker id="arrow-indigo" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#6366f1" />
                </marker>
                <marker id="arrow-cyan" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#22d3ee" />
                </marker>
              </defs>
              <rect id="canvas-grid" width="100%" height="100%" fill="url(#grid)" />

              {/* Viewport Transform Group (Handles Pan & Zoom) */}
              <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoom})`}>
                
                {/* Connector Arrow Lines */}
                {edges.map((edge, idx) => {
                  const srcNode = nodes.find(n => n.id === edge.source);
                  const tgtNode = nodes.find(n => n.id === edge.target);
                  
                  if (!srcNode || !tgtNode) return null;

                  // Connect from right boundary of source to left boundary of target
                  const x1 = srcNode.x + 150; // offset half width (assuming card width 160)
                  const y1 = srcNode.y + 35;  // offset half height (assuming card height 70)
                  const x2 = tgtNode.x;
                  const y2 = tgtNode.y + 35;

                  const midX = (x1 + x2) / 2;

                  // Smooth cubic bezier connection line
                  const pathD = `M ${x1} ${y1} C ${midX} ${y1}, ${midX} ${y2}, ${x2} ${y2}`;
                  
                  const markerColor = tgtNode.type === 'action' ? 'url(#arrow-cyan)' : 'url(#arrow-indigo)';
                  const strokeColor = tgtNode.type === 'action' ? '#06b6d4' : '#4f46e5';

                  return (
                    <g key={idx}>
                      {/* Outer backing path (shadow glow) */}
                      <path 
                        d={pathD} 
                        fill="none" 
                        stroke={strokeColor} 
                        strokeWidth="4" 
                        strokeOpacity="0.08" 
                      />
                      {/* Main connection line */}
                      <path 
                        d={pathD} 
                        fill="none" 
                        stroke={strokeColor} 
                        strokeWidth="1.5" 
                        strokeOpacity="0.5"
                        markerEnd={markerColor} 
                      />
                      {/* Pulse moving dot indicator */}
                      <path 
                        d={pathD} 
                        fill="none" 
                        stroke={tgtNode.type === 'action' ? '#22d3ee' : '#a5b4fc'} 
                        strokeWidth="1.5" 
                        className="flow-connector-pulse" 
                        pointerEvents="none"
                      />
                    </g>
                  );
                })}

                {/* Process Nodes */}
                {nodes.map((node) => {
                  const colorClass = getNodeColor(node.type);
                  const isHovered = hoveredNode?.id === node.id;
                  
                  return (
                    <g 
                      key={node.id} 
                      transform={`translate(${node.x}, ${node.y})`}
                      className="cursor-pointer"
                      onMouseEnter={() => setHoveredNode(node)}
                      onMouseLeave={() => setHoveredNode(null)}
                    >
                      {/* Glowing Card backing */}
                      <rect 
                        width="160" 
                        height="70" 
                        rx="12" 
                        className={`transition-all duration-300 ${
                          isHovered 
                            ? 'fill-slate-900 stroke-cyan-400 filter drop-shadow-[0_0_8px_rgba(34,211,238,0.2)]' 
                            : colorClass.split(' ')[0] + ' ' + colorClass.split(' ')[1]
                        }`} 
                        strokeWidth="1.5"
                      />

                      {/* Header block indicating type */}
                      <rect 
                        width="160" 
                        height="6" 
                        rx="2"
                        className={
                          node.type === 'trigger' ? 'fill-indigo-500' :
                          node.type === 'process' ? 'fill-cyan-500' : 'fill-emerald-500'
                        }
                      />

                      {/* Node Label Text */}
                      <foreignObject x="10" y="12" width="140" height="50">
                        <div className="h-full flex flex-col justify-center select-none pointer-events-none">
                          <span className={`text-[8px] font-extrabold uppercase tracking-wider block ${colorClass.split(' ')[2]}`}>
                            {node.type}
                          </span>
                          <span className="text-[10px] font-bold text-slate-100 line-clamp-2 leading-snug mt-0.5">
                            {node.label}
                          </span>
                        </div>
                      </foreignObject>
                    </g>
                  );
                })}
                
              </g>
            </svg>
          </div>

          {/* LEFT SIDEBAR: DETAILS INVENTORY */}
          <aside className="lg:col-span-1 glassmorphism p-5 rounded-2xl border border-slate-800 flex flex-col justify-between h-[500px]">
            <div className="space-y-5">
              <h3 className="font-extrabold text-sm text-white uppercase tracking-wider">Node Inspector</h3>
              
              {hoveredNode ? (
                <div className="space-y-4">
                  <div className="space-y-1">
                    <span className={`text-[8px] font-extrabold uppercase px-2 py-0.5 rounded-full inline-block ${
                      hoveredNode.type === 'trigger' ? 'bg-indigo-500/10 text-indigo-400' :
                      hoveredNode.type === 'process' ? 'bg-cyan-500/10 text-cyan-400' : 'bg-emerald-500/10 text-emerald-400'
                    }`}>
                      {hoveredNode.type} Node
                    </span>
                    <h4 className="font-bold text-sm text-white leading-snug">{hoveredNode.label}</h4>
                  </div>

                  <div className="space-y-1 bg-slate-900/60 p-3 rounded-xl border border-slate-850">
                    <span className="text-[9px] font-bold text-slate-500 uppercase tracking-wider block">Description / Action:</span>
                    <p className="text-xs text-slate-300 leading-relaxed">{hoveredNode.details}</p>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center text-center p-6 bg-slate-900/20 rounded-xl border border-slate-850 border-dashed h-48 text-slate-500 space-y-2">
                  <HelpCircle className="w-6 h-6 text-slate-600" />
                  <span className="text-[10px] leading-relaxed">
                    Hover over flowchart elements to view specific micro-service and webhook structures.
                  </span>
                </div>
              )}
            </div>

            <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-500">
              <span>Nodes: <strong className="text-slate-400">{nodes.length}</strong></span>
              <span>Connections: <strong className="text-slate-400">{edges.length}</strong></span>
            </div>
          </aside>
        </div>
      ) : (
        /* STRUCTURED JSON INSPECTOR */
        <div className="glassmorphism p-6 rounded-2xl border border-slate-800 space-y-4 relative">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-xs text-slate-400 font-semibold flex items-center gap-1.5">
              <Code className="w-4 h-4 text-indigo-400" />
              Compiled Integration Schema
            </span>
            <span className="text-[10px] text-slate-500 italic">Ready to deploy JSON structure</span>
          </div>

          <pre className="text-xs text-cyan-400 font-mono bg-slate-950 p-6 rounded-xl border border-slate-900 overflow-x-auto max-h-[500px]">
            <code>{JSON.stringify(analysis, null, 2)}</code>
          </pre>
        </div>
      )}
      
    </div>
  );
}
