'use client';

import React, { useState, useEffect } from 'react';
import TapSpeakCard from './TapSpeakCard';

/**
 * TapSpeak Interfaces
 */
interface ConfidenceMetrics {
  esat: number;
  cep: number;
}

interface TapSpeakTranslation {
  id: number;
  tap_speak: string;
  professional: string;
  operational: string;
  translational: string;
  confidence: ConfidenceMetrics;
  hooks: string;
  tags: string[];
}

interface BBTechMapping {
  id: number;
  tap_speak: string;
  professional: string;
  operational: string;
  translational: string;
  confidence: ConfidenceMetrics;
  hooks: string;
  tags: string[];
}

interface TapSpeakDashboardData {
  core_concepts: TapSpeakTranslation[];
  workflow_steps: TapSpeakTranslation[];
  codex_metrics: TapSpeakTranslation[];
  bbtech_mappings: BBTechMapping[];
  total_translations: number;
  average_confidence: ConfidenceMetrics;
}

/**
 * TapSpeak Dashboard Component
 * 
 * Main dashboard for browsing and exploring TapSpeak translations
 * Features:
 * - Category filtering (core concepts, workflow, codex, bbtech)
 * - Tag filtering
 * - Common/Expert view toggle
 * - Search functionality
 */
export default function TapSpeakDashboard() {
  const [data, setData] = useState<TapSpeakDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeCategory, setActiveCategory] = useState<'all' | 'core' | 'workflow' | 'codex' | 'bbtech'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [defaultView, setDefaultView] = useState<'common' | 'expert'>('common');

  // Fetch dashboard data
  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/v1/tapspeak/dashboard');
      if (!response.ok) throw new Error('Failed to fetch TapSpeak data');
      const dashboardData = await response.json();
      setData(dashboardData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  // Get translations to display based on active category
  const getDisplayedTranslations = (): TapSpeakTranslation[] => {
    if (!data) return [];

    let translations: TapSpeakTranslation[] = [];
    
    switch (activeCategory) {
      case 'core':
        translations = data.core_concepts;
        break;
      case 'workflow':
        translations = data.workflow_steps;
        break;
      case 'codex':
        translations = data.codex_metrics;
        break;
      case 'bbtech':
        translations = data.bbtech_mappings;
        break;
      default:
        translations = [
          ...data.core_concepts,
          ...data.workflow_steps,
          ...data.codex_metrics
        ];
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      translations = translations.filter(t =>
        t.tap_speak.toLowerCase().includes(query) ||
        t.professional.toLowerCase().includes(query) ||
        t.hooks.toLowerCase().includes(query) ||
        t.tags.some(tag => tag.toLowerCase().includes(query))
      );
    }

    return translations;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading TapSpeak translations...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center bg-red-50 border border-red-200 rounded-lg p-8">
          <h2 className="text-xl font-bold text-red-600 mb-2">Error Loading TapSpeak</h2>
          <p className="text-red-800">{error}</p>
        </div>
      </div>
    );
  }

  const displayedTranslations = getDisplayedTranslations();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                TapSpeak Translation System
              </h1>
              <p className="text-gray-600 mt-2">
                Biotech → Basketball → Everybody Gets It
              </p>
            </div>
            
            {data && (
              <div className="text-right">
                <div className="text-3xl font-bold text-blue-600">{data.total_translations}</div>
                <div className="text-sm text-gray-600">Translations</div>
                <div className="mt-2 flex gap-4 text-xs">
                  <div>
                    <span className="font-semibold text-green-600">ESAT:</span>{' '}
                    <span className="text-gray-700">{data.average_confidence.esat.toFixed(1)}%</span>
                  </div>
                  <div>
                    <span className="font-semibold text-purple-600">CEP:</span>{' '}
                    <span className="text-gray-700">{data.average_confidence.cep.toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Controls */}
          <div className="mt-6 flex flex-wrap gap-4">
            {/* Search */}
            <div className="flex-1 min-w-[300px]">
              <input
                type="text"
                placeholder="Search translations, hooks, or tags..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* View toggle */}
            <div className="flex gap-2">
              <button
                onClick={() => setDefaultView('common')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  defaultView === 'common'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                🎯 Common View
              </button>
              <button
                onClick={() => setDefaultView('expert')}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  defaultView === 'expert'
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                🔬 Expert View
              </button>
            </div>
          </div>

          {/* Category tabs */}
          <div className="mt-4 flex gap-2 overflow-x-auto pb-2">
            {[
              { key: 'all', label: 'All Translations', count: data?.total_translations || 0 },
              { key: 'core', label: 'Core Concepts', count: data?.core_concepts.length || 0 },
              { key: 'workflow', label: 'Workflow', count: data?.workflow_steps.length || 0 },
              { key: 'codex', label: 'Codex Metrics', count: data?.codex_metrics.length || 0 },
              { key: 'bbtech', label: 'BBTech', count: data?.bbtech_mappings.length || 0 }
            ].map(({ key, label, count }) => (
              <button
                key={key}
                onClick={() => setActiveCategory(key as any)}
                className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-all ${
                  activeCategory === key
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
                }`}
              >
                {label} ({count})
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        {displayedTranslations.length === 0 ? (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No translations found</h3>
            <p className="text-gray-600">Try adjusting your search or filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {displayedTranslations.map((translation) => (
              <TapSpeakCard
                key={translation.id}
                translation={translation}
                defaultView={defaultView}
              />
            ))}
          </div>
        )}
      </div>

      {/* Footer info */}
      <div className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl mb-2">🏀</div>
              <h3 className="font-semibold text-gray-700">BBTech Bridge</h3>
              <p className="text-sm text-gray-600">Basketball stats → Biotech metrics</p>
            </div>
            <div>
              <div className="text-3xl mb-2">🧠</div>
              <h3 className="font-semibold text-gray-700">Memory Hooks</h3>
              <p className="text-sm text-gray-600">Instant recall with mnemonics</p>
            </div>
            <div>
              <div className="text-3xl mb-2">✅</div>
              <h3 className="font-semibold text-gray-700">Validated</h3>
              <p className="text-sm text-gray-600">ESAT ≥ 70% & CEP ≥ 80%</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
