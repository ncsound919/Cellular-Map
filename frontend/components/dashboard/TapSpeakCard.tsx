'use client';

import React, { useState } from 'react';

/**
 * TapSpeak Translation Interface
 * Matches backend schema
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

interface TapSpeakCardProps {
  translation: TapSpeakTranslation;
  defaultView?: 'common' | 'expert';
}

/**
 * TapSpeak Translation Card Component
 * 
 * Displays a single TapSpeak translation with toggle between:
 * - Common man view (TapSpeak + hooks)
 * - Expert view (Professional + operational details)
 */
export default function TapSpeakCard({ translation, defaultView = 'common' }: TapSpeakCardProps) {
  const [view, setView] = useState<'common' | 'expert'>(defaultView);
  
  const isCommonView = view === 'common';
  
  // Get confidence color
  const getConfidenceColor = (score: number): string => {
    if (score >= 90) return 'text-green-500';
    if (score >= 80) return 'text-blue-500';
    if (score >= 70) return 'text-yellow-500';
    return 'text-red-500';
  };
  
  // Get confidence badge color
  const getConfidenceBadgeColor = (score: number): string => {
    if (score >= 90) return 'bg-green-100 text-green-800 border-green-300';
    if (score >= 80) return 'bg-blue-100 text-blue-800 border-blue-300';
    if (score >= 70) return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    return 'bg-red-100 text-red-800 border-red-300';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden transition-all hover:shadow-xl">
      {/* Header with toggle */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 text-white">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <h3 className="text-xl font-bold mb-1">
              {isCommonView ? translation.tap_speak : translation.professional}
            </h3>
            <p className="text-sm opacity-90">
              {isCommonView ? '🎯 Plain English' : '🔬 Technical'}
            </p>
          </div>
          
          {/* Toggle switch */}
          <button
            onClick={() => setView(view === 'common' ? 'expert' : 'common')}
            className="ml-4 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full px-4 py-2 text-sm font-medium transition-all"
          >
            {isCommonView ? 'Expert View' : 'Common View'}
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {isCommonView ? (
          // Common Man View
          <div className="space-y-4">
            {/* Hook/Mnemonic */}
            <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg p-4 border-l-4 border-yellow-400">
              <div className="flex items-start">
                <span className="text-2xl mr-3">💡</span>
                <div>
                  <h4 className="font-semibold text-gray-700 mb-1">Memory Hook</h4>
                  <p className="text-lg font-medium text-gray-900">{translation.hooks}</p>
                </div>
              </div>
            </div>

            {/* Real-world impact */}
            <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-400">
              <div className="flex items-start">
                <span className="text-2xl mr-3">🌍</span>
                <div>
                  <h4 className="font-semibold text-gray-700 mb-1">Real-World Impact</h4>
                  <p className="text-gray-800">{translation.translational}</p>
                </div>
              </div>
            </div>

            {/* Simple explanation */}
            <div className="bg-green-50 rounded-lg p-4 border-l-4 border-green-400">
              <div className="flex items-start">
                <span className="text-2xl mr-3">⚙️</span>
                <div>
                  <h4 className="font-semibold text-gray-700 mb-1">How It Works</h4>
                  <p className="text-gray-800">{translation.operational}</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          // Expert View
          <div className="space-y-4">
            {/* Technical term */}
            <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-gray-400">
              <h4 className="font-semibold text-gray-700 mb-1">Technical Term</h4>
              <p className="text-lg font-medium text-gray-900">{translation.professional}</p>
            </div>

            {/* Operational details */}
            <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-400">
              <h4 className="font-semibold text-gray-700 mb-1">Operational Mechanism</h4>
              <p className="text-gray-800">{translation.operational}</p>
            </div>

            {/* Translational science */}
            <div className="bg-purple-50 rounded-lg p-4 border-l-4 border-purple-400">
              <h4 className="font-semibold text-gray-700 mb-1">Translational Impact</h4>
              <p className="text-gray-800">{translation.translational}</p>
            </div>

            {/* TapSpeak version */}
            <div className="bg-green-50 rounded-lg p-4 border-l-4 border-green-400">
              <h4 className="font-semibold text-gray-700 mb-1">TapSpeak Translation</h4>
              <p className="text-lg font-medium text-gray-900">{translation.tap_speak}</p>
              <p className="text-sm text-gray-600 mt-2">💡 {translation.hooks}</p>
            </div>
          </div>
        )}

        {/* Confidence metrics - always visible */}
        <div className="mt-6 pt-4 border-t border-gray-200">
          <h4 className="text-sm font-semibold text-gray-600 mb-3">Translation Confidence</h4>
          <div className="grid grid-cols-2 gap-4">
            {/* ESAT */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-medium text-gray-600">ESAT (Comprehension)</span>
                <span className={`text-sm font-bold ${getConfidenceColor(translation.confidence.esat)}`}>
                  {translation.confidence.esat}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all"
                  style={{ width: `${translation.confidence.esat}%` }}
                />
              </div>
            </div>

            {/* CEP */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-medium text-gray-600">CEP (Precision)</span>
                <span className={`text-sm font-bold ${getConfidenceColor(translation.confidence.cep)}`}>
                  {translation.confidence.cep}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all"
                  style={{ width: `${translation.confidence.cep}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Tags */}
        <div className="mt-4 flex flex-wrap gap-2">
          {translation.tags.map((tag, index) => (
            <span
              key={index}
              className="px-3 py-1 bg-gray-100 text-gray-700 text-xs font-medium rounded-full border border-gray-300 hover:bg-gray-200 transition-colors"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
