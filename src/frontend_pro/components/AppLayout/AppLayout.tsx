import { ReactNode } from 'react'
import { useTranslation } from 'react-i18next'

export interface AppLayoutProps {
  children: ReactNode
  onLogout: () => void
}

export const AppLayout = ({ children, onLogout }: AppLayoutProps) => {
  const { t } = useTranslation()

  return (
    <div className="app">
      <header className="app-header">
        <h1>{t('app.title')}</h1>
        <button className="logout-button" onClick={onLogout}>
          {t('app.logout')}
        </button>
      </header>
      <main className="app-main">
        {children}
      </main>
    </div>
  )
}
