import { useState, useEffect, useCallback } from 'react'
import { PipelineControls } from './components/PipelineControls'
import { LicenseInputScreen } from './components/LicenseInputScreen'
import { AppLayout } from './components/AppLayout/AppLayout'
import { LicenseProvider } from './contexts/LicenseContext'
import { Theme } from './theme/theme'
import { translations } from './translations/translations'

const LICENSE_STORAGE_KEY = 'licenseToken'

function App() {
  const [licenseValid, setLicenseValid] = useState<boolean | null>(null)
  const [licenseToken, setLicenseToken] = useState<string | null>(null)
  const [licenseError, setLicenseError] = useState<string | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)

  useEffect(() => {
    const storedToken = localStorage.getItem(LICENSE_STORAGE_KEY)
    if (storedToken) {
      validateToken(storedToken)
    } else {
      setLicenseValid(false)
    }
  }, [])

  const validateToken = async (token: string) => {
    try {
      setLicenseError(null)
      const response = await fetch('/api/license/status', {
        headers: {
          'X-License-Token': token,
        },
      })
      const data = await response.json()

      if (data.valid && data.features.includes('react_ui')) {
        setLicenseValid(true)
        setLicenseToken(token)
        localStorage.setItem(LICENSE_STORAGE_KEY, token)
      } else {
        setLicenseValid(false)
        setLicenseToken(null)
        localStorage.removeItem(LICENSE_STORAGE_KEY)
        setLicenseError(translations.license.invalidError)
      }
    } catch {
      setLicenseValid(false)
      setLicenseToken(null)
      setLicenseError(translations.license.validationError)
    }
  }

  const handleActivate = async (token: string) => {
    await validateToken(token)
  }

  const handleTokenChange = useCallback((newToken: string | null) => {
    setLicenseToken(newToken)
    if (newToken) {
      localStorage.setItem(LICENSE_STORAGE_KEY, newToken)
    } else {
      localStorage.removeItem(LICENSE_STORAGE_KEY)
    }
  }, [])

  const handleRefresh = () => {
    setRefreshKey((k) => k + 1)
  }

  const handleLogout = () => {
    setLicenseToken(null)
    setLicenseValid(false)
    localStorage.removeItem(LICENSE_STORAGE_KEY)
  }

  if (licenseValid === null) {
    return (
      <>
        <Theme />
        <div className="license-screen">
          <div className="license-container">
            <p>{translations.loading.default}</p>
          </div>
        </div>
      </>
    )
  }

  if (!licenseValid) {
    return (
      <>
        <Theme />
        <LicenseInputScreen onActivate={handleActivate} error={licenseError} />
      </>
    )
  }

  return (
    <LicenseProvider initialToken={licenseToken} onTokenChange={handleTokenChange}>
      <Theme />
      <AppLayout onLogout={handleLogout}>
        <PipelineControls key={refreshKey} onRefresh={handleRefresh} />
      </AppLayout>
    </LicenseProvider>
  )
}

export default App
