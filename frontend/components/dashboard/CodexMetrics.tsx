'use client'

import React from 'react'

export default function CodexMetrics() {
  const metrics = [
    {
      name: 'Trueness',
      value: 0.85,
      description: 'Pan-cellular restoration score',
      color: '#4ecdc4'
    },
    {
      name: 'Flow',
      value: 0.90,
      description: 'Universal delivery efficiency',
      color: '#45b7d1'
    },
    {
      name: 'Gravity',
      value: 0.88,
      description: 'Universal hub impact score',
      color: '#667eea'
    }
  ]

  return (
    <div>
      {metrics.map((metric, index) => (
        <div key={index} style={{ marginBottom: '25px' }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '8px'
          }}>
            <div>
              <strong style={{ color: metric.color, fontSize: '1.1rem' }}>
                {metric.name}
              </strong>
              <div style={{ fontSize: '0.85rem', color: '#666' }}>
                {metric.description}
              </div>
            </div>
            <div style={{ 
              fontSize: '1.5rem', 
              fontWeight: 'bold',
              color: metric.color 
            }}>
              {(metric.value * 100).toFixed(0)}%
            </div>
          </div>
          <div style={{ 
            height: '10px', 
            background: '#e0e0e0', 
            borderRadius: '5px',
            overflow: 'hidden'
          }}>
            <div style={{ 
              height: '100%', 
              width: `${metric.value * 100}%`,
              background: metric.color,
              transition: 'width 0.5s ease'
            }} />
          </div>
        </div>
      ))}

      <div style={{ 
        marginTop: '30px', 
        padding: '15px', 
        background: '#f0f0f0', 
        borderRadius: '8px',
        borderLeft: '4px solid #667eea'
      }}>
        <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
          Overall Network Restoration
        </div>
        <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#667eea' }}>
          {((metrics.reduce((sum, m) => sum + m.value, 0) / metrics.length) * 100).toFixed(1)}%
        </div>
      </div>
    </div>
  )
}
