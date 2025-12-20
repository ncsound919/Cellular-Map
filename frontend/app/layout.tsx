import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'NetworkCellularMap - Networkologist Dashboard',
  description: 'Organ Agnostic Network Diagnosis Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
