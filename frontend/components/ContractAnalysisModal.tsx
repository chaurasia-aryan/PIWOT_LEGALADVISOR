'use client';

import React, { useState } from 'react';
import { MLContractAnalysis } from '@/app/types';

interface AnalysisModalProps {
  isOpen: boolean;
  onClose: () => void;
  analysis: MLContractAnalysis | null;
  documentName: string;
}

export const ContractAnalysisModal: React.FC<AnalysisModalProps> = ({
  isOpen,
  onClose,
  analysis,
  documentName
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'clauses' | 'risks' | 'entities'>('overview');
  const [clauseFilter, setClauseFilter] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');

  if (!isOpen || !analysis) return null;

  const totalRiskFactors = analysis.risk?.reasons?.length || analysis.risk?.total_risk_factors || 0;
  const totalClauses = analysis.clauses?.length || 0;

  const getRiskBadge = (level: string, score: number) => {
    switch (level) {
      case 'High':
        return (
          <span className="px-3 py-1 font-mono text-xs uppercase tracking-wide rounded-sm bg-accent-coral/60 text-accent-deep border border-accent-clay/40 font-semibold">
            High Risk ({score}/100)
          </span>
        );
      case 'Medium':
        return (
          <span className="px-3 py-1 font-mono text-xs uppercase tracking-wide rounded-sm bg-surface-manilla/70 text-ink border border-surface-kraft/40 font-semibold">
            Medium Risk ({score}/100)
          </span>
        );
      default:
        return (
          <span className="px-3 py-1 font-mono text-xs uppercase tracking-wide rounded-sm bg-accent-cactus/40 text-[#3e5e54] border border-accent-cactus/70 font-semibold">
            Low Risk ({score}/100)
          </span>
        );
    }
  };

  const filteredClauses = (analysis.clauses || []).filter(c => {
    const matchesFilter = clauseFilter === 'all'
      ? true
      : clauseFilter === 'high_risk'
      ? c.risk_level === 'High'
      : c.category === clauseFilter;
    
    const matchesSearch = searchTerm.trim() === ''
      ? true
      : c.text.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.category.toLowerCase().includes(searchTerm.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  const categories = Array.from(new Set((analysis.clauses || []).map(c => c.category)));

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/50 backdrop-blur-sm p-2 sm:p-4 md:p-6 overflow-y-auto">
      <div className="bg-canvas border border-hairline rounded-md w-full max-w-5xl max-h-[94vh] flex flex-col text-ink shadow-2xl overflow-hidden">
        
        {/* Modal Header */}
        <div className="p-5 md:p-6 border-b border-hairline bg-surface-secondary shrink-0 flex justify-between items-start gap-4">
          <div className="space-y-1.5">
            <div className="eyebrow">
              CONTRACT INTELLIGENCE REPORT
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <h2 className="font-serif text-xl sm:text-2xl md:text-3xl font-normal text-ink break-all">
                {analysis.document.filename || documentName}
              </h2>
              {getRiskBadge(analysis.risk.level, analysis.risk.score)}
            </div>
            <p className="font-mono text-xs text-text-muted">
              DOC ID: {analysis.document.document_id} • {analysis.document.page_count} PAGES • {totalClauses} CLAUSES SEGMENTED • {analysis.document.char_count.toLocaleString()} CHARS
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-text-muted hover:text-ink p-2 rounded-sm bg-canvas border border-hairline hover:border-ink transition text-sm font-bold shrink-0"
            title="Close modal"
          >
            ✕
          </button>
        </div>

        {/* Robust, Clean Segmented Tab Bar (No Scrollbar Cutoff) */}
        <div className="bg-surface-secondary/90 border-b border-hairline px-4 sm:px-6 py-3 shrink-0 flex flex-wrap items-center gap-2">
          {[
            { id: 'overview' as const, label: 'Overview & Summary', icon: '📄', count: null },
            { id: 'risks' as const, label: 'Risk Factors', icon: '⚠️', count: `${totalRiskFactors} Factors` },
            { id: 'clauses' as const, label: 'Segmented Clauses', icon: '⚖️', count: `${totalClauses} Clauses` },
            { id: 'entities' as const, label: 'Parties & Metadata', icon: '🏢', count: `${analysis.entities?.parties?.length || 2} Parties` },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-3 sm:px-4 rounded-sm font-sans text-xs sm:text-sm font-medium transition-all flex items-center gap-2 cursor-pointer ${
                activeTab === tab.id
                  ? 'bg-ink text-canvas font-semibold shadow-sm'
                  : 'bg-canvas text-ink border border-hairline hover:border-ink hover:bg-surface-secondary'
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
              {tab.count && (
                <span className={`text-[11px] font-mono px-1.5 py-0.5 rounded ${
                  activeTab === tab.id ? 'bg-ink-soft text-canvas' : 'bg-surface-secondary text-text-muted'
                }`}>
                  {tab.count}
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Content Area */}
        <div className="p-4 sm:p-6 md:p-8 overflow-y-auto flex-1 space-y-6 bg-canvas">

          {/* TAB 1: OVERVIEW & SUMMARY */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              
              {/* Summary Card */}
              <div className="card-cream space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="font-serif text-xl font-normal text-ink">
                    Extractive Contract Summary
                  </h3>
                  <span className="eyebrow">
                    TextRank Centrality Engine
                  </span>
                </div>
                <div className="space-y-3 text-ink font-serif text-base md:text-lg leading-relaxed pt-1">
                  {analysis.summary.summary_sentences.map((sentence, idx) => (
                    <p key={idx} className="leading-relaxed">
                      • {sentence}
                    </p>
                  ))}
                </div>
                <div className="pt-2 font-mono text-xs text-text-muted border-t border-hairline/60 flex flex-wrap justify-between items-center gap-2">
                  <span>Source pages verified: {analysis.summary.source_pages.map(p => `P. ${p}`).join(', ')}</span>
                  <span>Extracted from {analysis.document.page_count} total pages</span>
                </div>
              </div>

              {/* Quick Metrics Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-surface-secondary p-5 rounded-sm border border-surface-warm space-y-1">
                  <div className="eyebrow">Effective Term</div>
                  <div className="font-mono text-sm text-ink pt-1">
                    {analysis.entities.effective_date || 'Not specified'} → {analysis.entities.expiry_date || 'Not specified'}
                  </div>
                </div>
                <div className="bg-surface-secondary p-5 rounded-sm border border-surface-warm space-y-1">
                  <div className="eyebrow">Governing Jurisdiction</div>
                  <div className="font-sans font-medium text-sm text-ink pt-1">
                    {analysis.entities.governing_jurisdiction || 'Jurisdiction not found'}
                  </div>
                </div>
                <div className="bg-surface-secondary p-5 rounded-sm border border-surface-warm space-y-1">
                  <div className="eyebrow">Financial Commitments</div>
                  <div className="font-sans font-medium text-sm text-ink pt-1">
                    {analysis.entities.monetary_amounts.slice(0, 3).join(', ') || 'No fixed amounts detected'}
                  </div>
                </div>
              </div>

              {/* Navigation Jump Callouts */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                <div
                  onClick={() => setActiveTab('risks')}
                  className="p-5 rounded-sm bg-surface-secondary border border-surface-warm hover:border-ink cursor-pointer transition space-y-2 group"
                >
                  <div className="flex justify-between items-center">
                    <span className="font-sans font-bold text-sm text-ink flex items-center gap-2">
                      ⚠️ Risk Evaluation Matrix
                    </span>
                    <span className="font-mono text-xs text-text-muted group-hover:text-ink transition">
                      Score: {analysis.risk.score}/100 →
                    </span>
                  </div>
                  <p className="font-serif text-xs text-text-muted">
                    {totalRiskFactors} risk factor(s) evaluated including liability bounds, default terms, and covenants.
                  </p>
                </div>

                <div
                  onClick={() => setActiveTab('clauses')}
                  className="p-5 rounded-sm bg-surface-secondary border border-surface-warm hover:border-ink cursor-pointer transition space-y-2 group"
                >
                  <div className="flex justify-between items-center">
                    <span className="font-sans font-bold text-sm text-ink flex items-center gap-2">
                      ⚖️ Segmented Clauses Inspector
                    </span>
                    <span className="font-mono text-xs text-text-muted group-hover:text-ink transition">
                      {totalClauses} Clauses →
                    </span>
                  </div>
                  <p className="font-serif text-xs text-text-muted">
                    Browse all {totalClauses} categorized legal clauses across {analysis.document.page_count} pages with benchmark references.
                  </p>
                </div>
              </div>

            </div>
          )}

          {/* TAB 2: RISKS & ANOMALIES */}
          {activeTab === 'risks' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center pb-2 border-b border-hairline flex-wrap gap-2">
                <h3 className="font-serif text-2xl text-ink font-normal">Risk Evaluation Matrix</h3>
                <span className="font-mono text-xs text-text-muted">Total Penalty Score: {analysis.risk.score}/100</span>
              </div>

              {analysis.risk.reasons.length === 0 ? (
                <div className="text-center py-12 text-text-muted font-serif text-base">
                  No significant legal risks or contractual anomalies detected.
                </div>
              ) : (
                <div className="space-y-3">
                  {analysis.risk.reasons.map((reason, idx) => (
                    <div
                      key={idx}
                      className={`p-5 rounded-sm border ${
                        reason.severity === 'High'
                          ? 'bg-accent-coral/20 border-accent-clay/40'
                          : reason.severity === 'Medium'
                          ? 'bg-surface-manilla/30 border-surface-kraft/40'
                          : 'bg-surface-secondary border-surface-warm'
                      }`}
                    >
                      <div className="flex justify-between items-start gap-4">
                        <div className="font-sans font-semibold text-sm text-ink flex items-center gap-2">
                          <span className={`w-2 h-2 rounded-full ${
                            reason.severity === 'High' ? 'bg-accent-clay' : reason.severity === 'Medium' ? 'bg-surface-kraft' : 'bg-accent-olive'
                          }`} />
                          {reason.title}
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs text-text-muted">Page {reason.page}</span>
                          <span className="font-mono text-xs px-2 py-0.5 rounded-sm bg-canvas border border-hairline text-ink font-medium">
                            +{reason.weight} pts
                          </span>
                        </div>
                      </div>
                      <p className="font-serif text-sm text-ink mt-2 leading-relaxed">{reason.description}</p>
                      {reason.evidence && (
                        <div className="mt-3 p-3 bg-canvas rounded-sm border border-hairline font-mono text-xs text-ink leading-relaxed">
                          &quot;{reason.evidence}&quot;
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 3: CLAUSES */}
          {activeTab === 'clauses' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center gap-4 flex-wrap pb-2 border-b border-hairline">
                <div>
                  <h3 className="font-serif text-2xl text-ink font-normal">Segmented Contract Clauses ({filteredClauses.length} of {totalClauses})</h3>
                  <p className="font-sans text-xs text-text-muted">Classified across 12 legal categories with confidence ratings and benchmark references</p>
                </div>
                <div className="flex items-center gap-3 flex-wrap">
                  <input
                    type="text"
                    placeholder="Search clause text..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="input-field py-1 text-xs w-48"
                  />
                  <select
                    value={clauseFilter}
                    onChange={(e) => setClauseFilter(e.target.value)}
                    className="input-field py-1.5 text-xs"
                  >
                    <option value="all">All Categories ({totalClauses})</option>
                    <option value="high_risk">⚠️ High Risk Clauses Only</option>
                    {categories.map(cat => (
                      <option key={cat} value={cat}>{cat.replace(/_/g, ' ').toUpperCase()}</option>
                    ))}
                  </select>
                </div>
              </div>

              {filteredClauses.length === 0 ? (
                <div className="text-center py-12 text-text-muted font-serif text-sm">
                  No clauses match the selected filter.
                </div>
              ) : (
                <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-2">
                  {filteredClauses.map((clause, idx) => (
                    <div key={clause.chunk_id || idx} className="p-5 rounded-sm bg-surface-secondary border border-surface-warm space-y-2">
                      <div className="flex justify-between items-center">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs uppercase tracking-wider text-ink font-bold">
                            {clause.category.replace(/_/g, ' ')}
                          </span>
                          <span className="font-mono text-xs text-text-muted">
                            ({Math.round(clause.confidence * 100)}% conf)
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={`font-mono text-xs uppercase px-2 py-0.5 rounded-sm ${
                            clause.risk_level === 'High'
                              ? 'bg-accent-coral/60 text-accent-deep border border-accent-clay/40'
                              : clause.risk_level === 'Medium'
                              ? 'bg-surface-manilla/70 text-ink border border-surface-kraft/40'
                              : 'bg-accent-cactus/40 text-[#3e5e54]'
                          }`}>
                            {clause.risk_level} Risk
                          </span>
                          <span className="font-mono text-xs text-text-muted">Page {clause.page_start}</span>
                        </div>
                      </div>
                      
                      <p className="font-serif text-sm text-ink leading-relaxed pt-1">{clause.text}</p>

                      {clause.similar_standard_clauses && clause.similar_standard_clauses.length > 0 && (
                        <div className="mt-3 p-3 bg-surface-warm/50 rounded-sm border border-surface-warm text-xs space-y-1">
                          <div className="font-sans font-semibold text-ink flex items-center gap-1.5">
                            <span>🔍</span> Benchmark Reference: {clause.similar_standard_clauses[0].title}
                            <span className="font-mono text-text-muted text-[11px]">({Math.round(clause.similar_standard_clauses[0].similarity_score * 100)}% match)</span>
                          </div>
                          <p className="font-serif text-text-muted italic">&quot;{clause.similar_standard_clauses[0].reference_text}&quot;</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 4: ENTITIES & METADATA */}
          {activeTab === 'entities' && (
            <div className="space-y-5">
              <h3 className="font-serif text-2xl text-ink font-normal pb-2 border-b border-hairline">Extracted Entities & Metadata</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                {/* Parties */}
                <div className="bg-surface-secondary p-5 rounded-sm border border-surface-warm space-y-2">
                  <div className="eyebrow">Contracting Parties</div>
                  {analysis.entities.parties.length > 0 ? (
                    <ul className="space-y-2 text-sm pt-1">
                      {analysis.entities.parties.map((p, idx) => (
                        <li key={idx} className="flex justify-between border-b border-hairline/60 pb-1.5 gap-2">
                          <span className="font-sans font-medium text-ink">{p.name}</span>
                          <span className="font-mono text-xs text-text-muted shrink-0">{p.role}</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="font-serif text-xs text-text-muted">No parties explicitly extracted.</p>
                  )}
                </div>

                {/* Dates & Notice */}
                <div className="bg-surface-secondary p-5 rounded-sm border border-surface-warm space-y-2">
                  <div className="eyebrow">Dates & Timelines</div>
                  <div className="space-y-1.5 text-sm pt-1 font-sans">
                    <div>Effective Date: <span className="font-mono text-ink">{analysis.entities.effective_date || 'N/A'}</span></div>
                    <div>Expiry Date: <span className="font-mono text-ink">{analysis.entities.expiry_date || 'N/A'}</span></div>
                    <div>Notice Period: <span className="font-mono text-ink">{analysis.entities.notice_period || 'Standard'}</span></div>
                  </div>
                </div>

                {/* Financials */}
                <div className="bg-surface-secondary p-5 rounded-sm border border-surface-warm space-y-2">
                  <div className="eyebrow">Financials & Amounts Extracted</div>
                  <div className="space-y-2 text-sm pt-1 font-sans">
                    <div>
                      <span className="text-xs text-text-muted block">Monetary Sums & Facilities:</span>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {analysis.entities.monetary_amounts.length > 0 ? (
                          analysis.entities.monetary_amounts.map((amt, idx) => (
                            <span key={idx} className="px-2 py-0.5 rounded bg-canvas border border-hairline font-mono text-xs text-ink font-semibold">
                              {amt}
                            </span>
                          ))
                        ) : (
                          <span className="text-text-muted text-xs">As specified in Schedule I</span>
                        )}
                      </div>
                    </div>
                    <div>
                      <span className="text-xs text-text-muted block">Interest Rates & Penalties:</span>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {analysis.entities.percentages.length > 0 ? (
                          analysis.entities.percentages.map((pct, idx) => (
                            <span key={idx} className="px-2 py-0.5 rounded bg-canvas border border-hairline font-mono text-xs text-ink font-semibold">
                              {pct}
                            </span>
                          ))
                        ) : (
                          <span className="text-text-muted text-xs">Standard commercial interest</span>
                        )}
                      </div>
                    </div>
                    <div>
                      <span className="text-xs text-text-muted block">Repayment / Terms:</span>
                      <div className="font-medium text-ink text-xs mt-0.5">
                        {analysis.entities.payment_terms.join(' • ')}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Legal & Jurisdiction */}
                <div className="bg-surface-secondary p-5 rounded-sm border border-surface-warm space-y-2">
                  <div className="eyebrow">Jurisdiction & Venues</div>
                  <div className="space-y-1.5 text-sm pt-1 font-sans">
                    <div>Governing Law: <span className="font-medium text-ink">{analysis.entities.governing_jurisdiction || 'N/A'}</span></div>
                    <div>Dispute Venues: <span className="font-medium text-ink">{analysis.entities.dispute_venues.join('; ') || 'Standard Arbitration'}</span></div>
                  </div>
                </div>
              </div>
            </div>
          )}

        </div>

        {/* Footer & Disclaimer */}
        <div className="p-4 border-t border-hairline bg-surface-secondary shrink-0 flex flex-col md:flex-row justify-between items-center gap-3 text-xs text-text-muted">
          <div className="font-serif italic text-xs">
            ⚖️ Prototype Disclaimer: {analysis.metadata.disclaimer}
          </div>
          <button
            onClick={onClose}
            className="px-5 py-2 bg-ink text-canvas hover:opacity-90 rounded-sm font-sans font-medium text-xs transition"
          >
            Close Analysis
          </button>
        </div>

      </div>
    </div>
  );
};
