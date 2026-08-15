import { useCallback, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'

const LICENSE_STORAGE_KEY = 'licenseToken'

export const useLicenseValidation = () => {
  const { t } = useTranslation()
  const [licenseValid, setLicenseValid] = useState<boolean | null>(null)
  const [licenseToken, setLicenseToken] = useState<string | null>(null)
  const [licenseError, setLicenseError] = useState<string | null>(null)

  const validateToken = useCallback(async (token: string) => {
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
        setLicenseError(t('license.invalidError'))
      }
    } catch {
      setLicenseValid(false)
      setLicenseToken(null)
      setLicenseError(t('license.validationError'))
    }
  }, [t])

  useEffect(() => {
    const storedToken = localStorage.getItem(LICENSE_STORAGE_KEY)
    if (storedToken) {
      validateToken(storedToken)
    } else {
      setLicenseValid(false)
    }
  }, [validateToken])

  const handleActivate = useCallback(
    async (token: string) => {
      await validateToken(token)
    },
    [validateToken]
  )

  const handleTokenChange = useCallback((newToken: string | null) => {
    setLicenseToken(newToken)
    if (newToken) {
      localStorage.setItem(LICENSE_STORAGE_KEY, newToken)
    } else {
      localStorage.removeItem(LICENSE_STORAGE_KEY)
    }
  }, [])

  const handleLogout = useCallback(() => {
    setLicenseToken(null)
    setLicenseValid(false)
    localStorage.removeItem(LICENSE_STORAGE_KEY)
  }, [])

  return {
    licenseValid,
    licenseToken,
    licenseError,
    handleActivate,
    handleTokenChange,
    handleLogout,
  }
}
