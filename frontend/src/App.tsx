import { useState, useEffect, useCallback } from 'react'
import { PipelineControls } from './components/PipelineControls'
import { LicenseInputScreen } from './components/LicenseInputScreen'
import { LicenseProvider } from './contexts/LicenseContext'
import { Theme } from './theme/theme'

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
        setLicenseError('Invalid license token. Please try again.')
      }
    } catch {
      setLicenseValid(false)
      setLicenseToken(null)
      setLicenseError('Failed to validate license. Please try again.')
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
            <p>Loading...</p>
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
      <div className="app">
        <header className="app-header">
          <h1>Auto Annotater</h1>
          <button className="logout-button" onClick={handleLogout}>
            Logout
          </button>
        </header>
        <main className="app-main">
          <PipelineControls key={refreshKey} onRefresh={handleRefresh} />
        </main>
      </div>
    </LicenseProvider>
  )
}

export default App
