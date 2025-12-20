'use client'

import React, { useEffect, useState } from 'react'
import UniversalMutationMap from './UniversalMutationMap'
import PanCellularHubRadar from './PanCellularHubRadar'
import CodexMetrics from './CodexMetrics'

export default function NetworkologistDashboard() {
  const [systemStatus, setSystemStatus] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Fetch system status
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    fetch(`${apiUrl}/`)
      .then(res => res.json())
      .then(data => setSystemStatus(data))
      .catch(err => {
        console.error('Failed to fetch system status:', err)
        setError('Unable to connect to backend API. Please check if the server is running.')
      })
  }, [])

  return (
    <div className="dashboard">
      <div className="header">
        <h1>NetworkCellularMap v2.0</h1>
        <p>Networkology Core Engine - Organ Agnostic Network Diagnosis</p>
        {error && (
          <div style={{ marginTop: '10px', color: '#d32f2f', fontSize: '0.9rem', padding: '10px', background: '#ffebee', borderRadius: '4px' }}>
            ⚠️ {error}
          </div>
        )}
        {systemStatus && !error && (
          <div style={{ marginTop: '10px', color: '#666', fontSize: '0.9rem' }}>
            Status: {systemStatus.status} | Paradigm: {systemStatus.paradigm}
          </div>
        )}
      </div>

      <div className="grid">
        <div className="card" style={{ gridColumn: '1 / -1' }}>
          <h2>Universal Mutation Map</h2>
          <p style={{ color: '#666', marginBottom: '15px' }}>
            3D force-directed graph highlighting same mutation across different tissues
          </p>
          <UniversalMutationMap />
        </div>

        <div className="card">
          <h2>Pan-Cellular Hub Radar</h2>
          <p style={{ color: '#666', marginBottom: '15px' }}>
            Multi-organ impact analysis for universal intervention points
          </p>
          <PanCellularHubRadar />
        </div>

        <div className="card">
          <h2>Codex Metrics</h2>
          <p style={{ color: '#666', marginBottom: '15px' }}>
            Trueness, Flow, and Gravity scores for network restoration
          </p>
          <CodexMetrics />
        </div>
      </div>

      <div className="grid" style={{ marginTop: '30px' }}>
        <div className="card">
          <h2>Disease Module Status</h2>
          <div className="metrics">
            <div className="metric">
              <div className="metric-value">92%</div>
              <div className="metric-label">Module Dissolution</div>
            </div>
            <div className="metric">
              <div className="metric-value">5</div>
              <div className="metric-label">Active Modules</div>
            </div>
            <div className="metric">
              <div className="metric-value">12</div>
              <div className="metric-label">Universal Hubs</div>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Network Health</h2>
          <div className="metrics">
            <div className="metric">
              <div className="metric-value">2.3</div>
              <div className="metric-label">Power Law α</div>
            </div>
            <div className="metric">
              <div className="metric-value">99%</div>
              <div className="metric-label">Random Robust</div>
            </div>
            <div className="metric">
              <div className="metric-value">20%</div>
              <div className="metric-label">Hub Vulnerable</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
