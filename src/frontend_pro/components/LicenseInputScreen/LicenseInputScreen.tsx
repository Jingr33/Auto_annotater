import { useState } from 'react'
import { LicenseHeader } from './LicenseHeader'
import { LicenseForm } from './LicenseForm'
import { translations } from '../../translations/translations'

export interface LicenseInputScreenProps {
  onActivate: (token: string) => void
  error: string | null
}

export const LicenseInputScreen = ({ onActivate, error }: LicenseInputScreenProps) => {
  const [token, setToken] = useState('')

  const handleSubmit = () => {
    onActivate(token.trim())
  }

  return (
    <div className="license-screen">
      <div className="license-container">
        <LicenseHeader
          title={translations.license.screenTitle}
          subtitle={translations.license.subtitle}
        />
        <LicenseForm
          token={token}
          onTokenChange={setToken}
          onSubmit={handleSubmit}
          error={error}
        />
        <p className="license-help">
          {translations.license.helpText}
        </p>
      </div>
    </div>
  )
}
