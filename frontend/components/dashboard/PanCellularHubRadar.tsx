'use client'

import React, { useEffect, useRef } from 'react'

export default function PanCellularHubRadar() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const width = canvas.width
    const height = canvas.height
    const centerX = width / 2
    const centerY = height / 2
    const radius = Math.min(width, height) / 2 - 40

    // Clear canvas
    ctx.clearRect(0, 0, width, height)

    // Data
    const axes = ['Heart Impact', 'Brain Impact', 'Liver Impact', 'Muscle Impact']
    const data = [0.85, 0.92, 0.78, 0.88]
    const angleStep = (Math.PI * 2) / axes.length

    // Draw radar background
    ctx.strokeStyle = '#e0e0e0'
    ctx.lineWidth = 1

    for (let i = 1; i <= 5; i++) {
      ctx.beginPath()
      const r = (radius / 5) * i
      for (let j = 0; j <= axes.length; j++) {
        const angle = angleStep * j - Math.PI / 2
        const x = centerX + r * Math.cos(angle)
        const y = centerY + r * Math.sin(angle)
        if (j === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      }
      ctx.closePath()
      ctx.stroke()
    }

    // Draw axes
    ctx.strokeStyle = '#ccc'
    ctx.lineWidth = 2
    axes.forEach((_, i) => {
      const angle = angleStep * i - Math.PI / 2
      ctx.beginPath()
      ctx.moveTo(centerX, centerY)
      ctx.lineTo(
        centerX + radius * Math.cos(angle),
        centerY + radius * Math.sin(angle)
      )
      ctx.stroke()
    })

    // Draw data
    ctx.fillStyle = 'rgba(102, 126, 234, 0.3)'
    ctx.strokeStyle = '#667eea'
    ctx.lineWidth = 3
    ctx.beginPath()
    data.forEach((value, i) => {
      const angle = angleStep * i - Math.PI / 2
      const r = radius * value
      const x = centerX + r * Math.cos(angle)
      const y = centerY + r * Math.sin(angle)
      if (i === 0) {
        ctx.moveTo(x, y)
      } else {
        ctx.lineTo(x, y)
      }
    })
    ctx.closePath()
    ctx.fill()
    ctx.stroke()

    // Draw labels
    ctx.fillStyle = '#333'
    ctx.font = 'bold 12px sans-serif'
    ctx.textAlign = 'center'
    axes.forEach((label, i) => {
      const angle = angleStep * i - Math.PI / 2
      const labelRadius = radius + 25
      const x = centerX + labelRadius * Math.cos(angle)
      const y = centerY + labelRadius * Math.sin(angle)
      ctx.fillText(label, x, y)
      
      // Draw value
      ctx.font = '10px sans-serif'
      ctx.fillStyle = '#667eea'
      ctx.fillText(`${(data[i] * 100).toFixed(0)}%`, x, y + 15)
      ctx.font = 'bold 12px sans-serif'
      ctx.fillStyle = '#333'
    })

  }, [])

  return (
    <div className="radar-chart">
      <canvas ref={canvasRef} width={500} height={400} style={{ width: '100%', height: 'auto' }} />
    </div>
  )
}
