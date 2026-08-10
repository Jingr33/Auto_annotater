export const componentThemeCSS = `
  .app {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .app-header {
    text-align: center;
    padding: 20px 0;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 20px;
  }

  .app-header h1 {
    margin: 0;
    font-size: 1.5rem;
    color: #333;
  }

  .app-main {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .pipeline-controls {
    padding: 16px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background: #fafafa;
  }

  .status-info {
    margin-bottom: 12px;
  }

  .status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.875rem;
    font-weight: 500;
  }

  .status-badge.finished {
    background: #d4edda;
    color: #155724;
  }

  .status-badge.active {
    background: #cce5ff;
    color: #004085;
  }

  .status-badge.waiting {
    background: #fff3cd;
    color: #856404;
  }

  .controls {
    display: flex;
    gap: 8px;
  }

  .controls button {
    padding: 8px 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background: white;
    cursor: pointer;
    font-size: 0.875rem;
  }

  .controls button:hover:not(:disabled) {
    background: #f0f0f0;
  }

  .controls button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .license-screen {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: var(--bg);
  }

  .license-container {
    max-width: 400px;
    width: 100%;
    padding: 40px;
    text-align: center;
  }

  .license-container h1 {
    margin-bottom: 8px;
    font-size: 2rem;
  }

  .license-subtitle {
    color: var(--text);
    margin-bottom: 32px;
  }

  .license-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .license-input {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 1rem;
    background: var(--bg);
    color: var(--text);
    box-sizing: border-box;
  }

  .license-input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 2px var(--accent-bg);
  }

  .license-button {
    width: 100%;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    background: var(--accent);
    color: white;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: opacity 0.2s;
  }

  .license-button:hover:not(:disabled) {
    opacity: 0.9;
  }

  .license-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .license-error {
    color: #dc3545;
    margin-top: 16px;
    font-size: 0.875rem;
  }

  .license-help {
    color: var(--text);
    margin-top: 24px;
    font-size: 0.875rem;
  }

  .logout-button {
    position: absolute;
    right: 20px;
    top: 20px;
    padding: 8px 16px;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: transparent;
    color: var(--text);
    cursor: pointer;
    font-size: 0.875rem;
  }

  .logout-button:hover {
    background: var(--accent-bg);
    border-color: var(--accent-border);
  }

  .loading-indicator {
    padding: 16px;
    text-align: center;
    color: var(--text);
  }
`
