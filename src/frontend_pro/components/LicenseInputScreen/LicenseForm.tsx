import type { FormEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { Alert, Button, Stack, TextField } from '@mui/material'

export interface LicenseFormProps {
  token: string
  onTokenChange: (token: string) => void
  onSubmit: () => void
  error: string | null
}

export const LicenseForm = ({ token, onTokenChange, onSubmit, error }: LicenseFormProps) => {
  const { t } = useTranslation()

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (token.trim()) {
      onSubmit()
    }
  }

  return (
    <Stack component="form" onSubmit={handleSubmit} spacing={2}>
      <TextField
        value={token}
        onChange={(e) => onTokenChange(e.target.value)}
        placeholder={t('license.inputPlaceholder')}
        autoFocus
        fullWidth
      />

      <Button type="submit" variant="contained" disabled={!token.trim()} fullWidth>
        {t('license.activateButton')}
      </Button>

      {error && <Alert severity="error">{error}</Alert>}
    </Stack>
  )
}
