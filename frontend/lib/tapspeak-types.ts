/**
 * Shared TypeScript types for TapSpeak
 * Used across all frontend components
 */

export interface ConfidenceMetrics {
  esat: number;
  cep: number;
}

export interface TapSpeakTranslation {
  id: number;
  tap_speak: string;
  professional: string;
  operational: string;
  translational: string;
  confidence: ConfidenceMetrics;
  hooks: string;
  tags: string[];
}

export interface BBTechMapping {
  id: number;
  tap_speak: string;
  professional: string;
  operational: string;
  translational: string;
  confidence: ConfidenceMetrics;
  hooks: string;
  tags: string[];
}

export interface TapSpeakDashboardData {
  core_concepts: TapSpeakTranslation[];
  workflow_steps: TapSpeakTranslation[];
  codex_metrics: TapSpeakTranslation[];
  bbtech_mappings: BBTechMapping[];
  total_translations: number;
  average_confidence: ConfidenceMetrics;
}

export interface TapSpeakSearchRequest {
  query?: string;
  category?: 'core_concepts' | 'networkology_workflow' | 'codex_translations' | 'basketball_biotech_bridge';
  tags?: string[];
  min_esat?: number;
  min_cep?: number;
}

export interface TapSpeakTranslateRequest {
  technical_term: string;
  domain?: string;
  context?: string;
}

export interface TapSpeakStats {
  total_translations: number;
  average_confidence: ConfidenceMetrics;
  by_category: {
    core_concepts: number;
    networkology_workflow: number;
    codex_translations: number;
    bbtech_mappings: number;
  };
  total_tags: number;
  tags: string[];
}
