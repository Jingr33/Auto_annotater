import type { ReactNode } from 'react'
import { useTranslation } from 'react-i18next'
import { AppBar, Box, Button, Container, Toolbar, Typography } from '@mui/material'

export interface AppLayoutProps {
  children: ReactNode
  onLogout: () => void
}

export const AppLayout = ({ children, onLogout }: AppLayoutProps) => {
  const { t } = useTranslation()

  return (
    <Box sx={{ maxWidth: '1200px', mx: 'auto', px: 2, display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar
        position="static"
        color="transparent"
        elevation={0}
        sx={{ borderBottom: 1, borderColor: 'divider' }}
      >
        <Toolbar sx={{ position: 'relative' }}>
          <Typography variant="h6" sx={{ flexGrow: 1, textAlign: 'center' }}>
            {t('app.title')}
          </Typography>
          <Button onClick={onLogout} sx={{ position: 'absolute', right: 0 }}>
            {t('app.logout')}
          </Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ py: 3, flexGrow: 1 }}>
        {children}
      </Container>
    </Box>
  )
}
