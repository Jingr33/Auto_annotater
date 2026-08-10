import { ReactNode } from 'react'
import { translations } from '../../translations/translations'

export interface AppLayoutProps {
  children: ReactNode
  onLogout: () => void
}

export const AppLayout = ({ children, onLogout }: AppLayoutProps) => {
  return (
    <div className="app">
      <header className="app-header">
        <h1>{translations.app.title}</h1>
        <button className="logout-button" onClick={onLogout}>
          {translations.app.logout}
        </button>
      </header>
      <main className="app-main">
        {children}
      </main>
    </div>
  )
}
