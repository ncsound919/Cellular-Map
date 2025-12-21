/**
 * TapSpeak API Client
 * 
 * TypeScript client for accessing TapSpeak translation endpoints
 */

import type {
  ConfidenceMetrics,
  TapSpeakTranslation,
  BBTechMapping,
  TapSpeakDashboardData,
  TapSpeakSearchRequest,
  TapSpeakTranslateRequest,
  TapSpeakStats
} from './tapspeak-types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

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
