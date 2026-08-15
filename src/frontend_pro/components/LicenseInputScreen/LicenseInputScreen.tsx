import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { LicenseHeader } from './LicenseHeader'
import { LicenseForm } from './LicenseForm'

export interface LicenseInputScreenProps {
  onActivate: (token: string) => void
  error: string | null
}

export const LicenseInputScreen = ({ onActivate, error }: LicenseInputScreenProps) => {
  const { t } = useTranslation()
  const [token, setToken] = useState('')

  const handleSubmit = () => {
    onActivate(token.trim())
  }

  return (
    <div className="license-screen">
      <div className="license-container">
        <LicenseHeader
          title={t('license.screenTitle')}
          subtitle={t('license.subtitle')}
        />
        <LicenseForm
          token={token}
          onTokenChange={setToken}
          onSubmit={handleSubmit}
          error={error}
        />
        <p className="license-help">
          {t('license.helpText')}
        </p>
      </div>
    </div>
  )
}
