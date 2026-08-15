import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { PipelineControls } from './components/PipelineControls'
import { LicenseInputScreen } from './components/LicenseInputScreen'
import { AppLayout } from './components/AppLayout/AppLayout'
import { LoadingIndicator } from './components/LoadingIndicator/LoadingIndicator'
import { PageContainer } from './components/common/PageContainer'
import { LicenseProvider } from './contexts/LicenseContext'
import { useLicenseValidation } from './hooks/useLicenseValidation'

function App() {
  const { t } = useTranslation()
  const { licenseValid, licenseToken, licenseError, handleActivate, handleTokenChange, handleLogout } =
    useLicenseValidation()
  const [refreshKey, setRefreshKey] = useState(0)

  const handleRefresh = () => {
    setRefreshKey((k) => k + 1)
  }

  if (licenseValid === null) {
    return (
      <PageContainer>
        <LoadingIndicator message={t('loading.default')} />
      </PageContainer>
    )
  }

  if (!licenseValid) {
    return <LicenseInputScreen onActivate={handleActivate} error={licenseError} />
  }

  return (
    <LicenseProvider initialToken={licenseToken} onTokenChange={handleTokenChange}>
      <AppLayout onLogout={handleLogout}>
        <PipelineControls key={refreshKey} onRefresh={handleRefresh} />
      </AppLayout>
    </LicenseProvider>
  )
}

export default App
