'use client'

import React, { useEffect, useRef } from 'react'

export default function UniversalMutationMap() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (typeof window === 'undefined') return

    // Cytoscape will be initialized here
    // For now, showing a placeholder visualization
    const drawPlaceholder = () => {
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      if (!ctx || !containerRef.current) return

      canvas.width = containerRef.current.clientWidth
      canvas.height = 500
      canvas.style.width = '100%'
      canvas.style.borderRadius = '8px'

      // Draw background
      ctx.fillStyle = '#f0f0f0'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Draw network nodes
      const nodes = [
        { x: 200, y: 150, label: 'TP53', color: '#ff6b6b' },
        { x: 400, y: 200, label: 'MC4R', color: '#4ecdc4' },
        { x: 300, y: 300, label: 'BRCA1', color: '#45b7d1' },
        { x: 500, y: 250, label: 'EGFR', color: '#ffa07a' },
        { x: 350, y: 400, label: 'KRAS', color: '#98d8c8' },
      ]

      // Draw edges
      ctx.strokeStyle = '#999'
      ctx.lineWidth = 2
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          if (Math.random() > 0.5) {
            ctx.beginPath()
            ctx.moveTo(nodes[i].x, nodes[i].y)
            ctx.lineTo(nodes[j].x, nodes[j].y)
            ctx.stroke()
          }
        }
      }

      // Draw nodes
      nodes.forEach(node => {
        ctx.fillStyle = node.color
        ctx.beginPath()
        ctx.arc(node.x, node.y, 30, 0, Math.PI * 2)
        ctx.fill()
        ctx.strokeStyle = '#fff'
        ctx.lineWidth = 3
        ctx.stroke()

        // Label
        ctx.fillStyle = '#333'
        ctx.font = 'bold 12px sans-serif'
        ctx.textAlign = 'center'
        ctx.fillText(node.label, node.x, node.y - 45)
      })

      // Add title
      ctx.fillStyle = '#667eea'
      ctx.font = 'bold 14px sans-serif'
      ctx.textAlign = 'left'
      ctx.fillText('Universal Hub Network (Pan-Cellular)', 20, 30)

      containerRef.current.innerHTML = ''
      containerRef.current.appendChild(canvas)
    }

    drawPlaceholder()
  }, [])

  return (
    <div ref={containerRef} className="network-viz" />
  )
}
