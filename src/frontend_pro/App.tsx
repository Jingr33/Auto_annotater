import { useState } from 'react'
import { PipelineControls } from './components/PipelineControls'
import { LicenseInputScreen } from './components/LicenseInputScreen'
import { AppLayout } from './components/AppLayout/AppLayout'
import { LicenseProvider } from './contexts/LicenseContext'
import { Theme } from './theme/theme'
import { translations } from './translations/translations'
import { useLicenseValidation } from './hooks/useLicenseValidation'

function App() {
  const { licenseValid, licenseToken, licenseError, handleActivate, handleTokenChange, handleLogout } =
    useLicenseValidation()
  const [refreshKey, setRefreshKey] = useState(0)

  const handleRefresh = () => {
    setRefreshKey((k) => k + 1)
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
