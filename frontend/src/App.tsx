import { useState } from 'react'
import { PipelineControls } from './components/PipelineControls'
import './App.css'

function App() {
  const [refreshKey, setRefreshKey] = useState(0)

  const handleRefresh = () => {
    setRefreshKey((k) => k + 1)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Auto Annotater</h1>
      </header>
      <main className="app-main">
        <PipelineControls key={refreshKey} onRefresh={handleRefresh} />
      </main>
    </div>
  )
}

export default App
