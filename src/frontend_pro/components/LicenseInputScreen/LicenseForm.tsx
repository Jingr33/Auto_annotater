import { useTranslation } from 'react-i18next'

export interface LicenseFormProps {
  token: string
  onTokenChange: (token: string) => void
  onSubmit: () => void
  error: string | null
}

export const LicenseForm = ({ token, onTokenChange, onSubmit, error }: LicenseFormProps) => {
  const { t } = useTranslation()

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
        placeholder={t('license.inputPlaceholder')}
        className="license-input"
        autoFocus
      />
      <button type="submit" className="license-button" disabled={!token.trim()}>
        {t('license.activateButton')}
      </button>
      {error && <p className="license-error">{error}</p>}
    </form>
  )
}
