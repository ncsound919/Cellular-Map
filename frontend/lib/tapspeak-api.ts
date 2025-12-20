/**
 * TapSpeak API Client
 * 
 * TypeScript client for accessing TapSpeak translation endpoints
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

/**
 * TapSpeak Types
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

/**
 * TapSpeak API Client Class
 */
export class TapSpeakAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Get all TapSpeak concepts
   */
  async getConcepts(category?: string): Promise<TapSpeakTranslation[]> {
    const url = category
      ? `${this.baseUrl}/tapspeak/concepts?category=${category}`
      : `${this.baseUrl}/tapspeak/concepts`;
    
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Failed to fetch concepts: ${response.statusText}`);
    return response.json();
  }

  /**
   * Get BBTech mappings
   */
  async getBBTechMappings(): Promise<BBTechMapping[]> {
    const response = await fetch(`${this.baseUrl}/tapspeak/bbtech`);
    if (!response.ok) throw new Error(`Failed to fetch BBTech mappings: ${response.statusText}`);
    return response.json();
  }

  /**
   * Search TapSpeak translations
   */
  async search(request: TapSpeakSearchRequest): Promise<TapSpeakTranslation[]> {
    const response = await fetch(`${this.baseUrl}/tapspeak/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    if (!response.ok) throw new Error(`Failed to search translations: ${response.statusText}`);
    return response.json();
  }

  /**
   * Translate a technical term
   */
  async translateTerm(request: TapSpeakTranslateRequest): Promise<TapSpeakTranslation> {
    const response = await fetch(`${this.baseUrl}/tapspeak/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(`No translation found for "${request.technical_term}"`);
      }
      throw new Error(`Failed to translate term: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get complete dashboard data
   */
  async getDashboardData(): Promise<TapSpeakDashboardData> {
    const response = await fetch(`${this.baseUrl}/tapspeak/dashboard`);
    if (!response.ok) throw new Error(`Failed to fetch dashboard data: ${response.statusText}`);
    return response.json();
  }

  /**
   * Get statistics
   */
  async getStats(): Promise<TapSpeakStats> {
    const response = await fetch(`${this.baseUrl}/tapspeak/stats`);
    if (!response.ok) throw new Error(`Failed to fetch stats: ${response.statusText}`);
    return response.json();
  }

  /**
   * Get concept by ID
   */
  async getConceptById(id: number): Promise<TapSpeakTranslation> {
    const response = await fetch(`${this.baseUrl}/tapspeak/concept/${id}`);
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(`Concept with ID ${id} not found`);
      }
      throw new Error(`Failed to fetch concept: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get all available tags
   */
  async getTags(): Promise<string[]> {
    const response = await fetch(`${this.baseUrl}/tapspeak/tags`);
    if (!response.ok) throw new Error(`Failed to fetch tags: ${response.statusText}`);
    return response.json();
  }
}

// Export singleton instance
export const tapspeakAPI = new TapSpeakAPI();

// Export default
export default tapspeakAPI;
