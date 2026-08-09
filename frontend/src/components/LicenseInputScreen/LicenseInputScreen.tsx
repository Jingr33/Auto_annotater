import { useState } from 'react'

export interface LicenseInputScreenProps {
  onActivate: (token: string) => void
  error: string | null
}

export const LicenseInputScreen = ({ onActivate, error }: LicenseInputScreenProps) => {
  const [token, setToken] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (token.trim()) {
      onActivate(token.trim())
    }
  }

  return (
    <div className="license-screen">
      <div className="license-container">
        <h1>Auto Annotater Pro</h1>
        <p className="license-subtitle">Enter your license token to activate Pro features</p>

        <form onSubmit={handleSubmit} className="license-form">
          <input
            type="text"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            placeholder="Paste your license token here"
            className="license-input"
            autoFocus
          />
          <button type="submit" className="license-button" disabled={!token.trim()}>
            Activate
          </button>
        </form>

        {error && <p className="license-error">{error}</p>}

        <p className="license-help">
          Don't have a license? Contact support to get one.
        </p>
      </div>
    </div>
  )
}
