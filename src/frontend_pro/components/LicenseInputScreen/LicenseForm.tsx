import { translations } from '../../translations/translations'

export interface LicenseFormProps {
  token: string
  onTokenChange: (token: string) => void
  onSubmit: () => void
  error: string | null
}

export const LicenseForm = ({ token, onTokenChange, onSubmit, error }: LicenseFormProps) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (token.trim()) {
      onSubmit()
    }
  }

  return (
    <form onSubmit={handleSubmit} className="license-form">
      <input
        type="text"
        value={token}
        onChange={(e) => onTokenChange(e.target.value)}
        placeholder={translations.license.inputPlaceholder}
        className="license-input"
        autoFocus
      />
      <button type="submit" className="license-button" disabled={!token.trim()}>
        {translations.license.activateButton}
      </button>
      {error && <p className="license-error">{error}</p>}
    </form>
  )
}
