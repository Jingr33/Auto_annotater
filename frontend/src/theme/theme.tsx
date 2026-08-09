export const themeCSS = `
  :root {
    --text: #6b6375;
    --text-h: #08060d;
    --bg: #fff;
    --border: #e5e4e7;
    --code-bg: #f4f3ec;
    --accent: #aa3bff;
    --accent-bg: rgba(170, 59, 255, 0.1);
    --accent-border: rgba(170, 59, 255, 0.5);
    --social-bg: rgba(244, 243, 236, 0.5);
    --shadow:
      rgba(0, 0, 0, 0.1) 0 10px 15px -3px, rgba(0, 0, 0, 0.05) 0 4px 6px -2px;

    --sans: system-ui, 'Segoe UI', Roboto, sans-serif;
    --heading: system-ui, 'Segoe UI', Roboto, sans-serif;
    --mono: ui-monospace, Consolas, monospace;

    font: 18px/145% var(--sans);
    letter-spacing: 0.18px;
    color-scheme: light dark;
    color: var(--text);
    background: var(--bg);
    font-synthesis: none;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  @media (max-width: 1024px) {
    :root {
      font-size: 16px;
    }
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --text: #9ca3af;
      --text-h: #f3f4f6;
      --bg: #16171d;
      --border: #2e303a;
      --code-bg: #1f2028;
      --accent: #c084fc;
      --accent-bg: rgba(192, 132, 252, 0.15);
      --accent-border: rgba(192, 132, 252, 0.5);
      --social-bg: rgba(47, 48, 58, 0.5);
      --shadow:
        rgba(0, 0, 0, 0.4) 0 10px 15px -3px, rgba(0, 0, 0, 0.25) 0 4px 6px -2px;
    }

    #social .button-icon {
      filter: invert(1) brightness(2);
    }
  }

  #root {
    width: 1126px;
    max-width: 100%;
    margin: 0 auto;
    text-align: center;
    border-inline: 1px solid var(--border);
    min-height: 100svh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
  }

  body {
    margin: 0;
  }

  h1,
  h2 {
    font-family: var(--heading);
    font-weight: 500;
    color: var(--text-h);
  }

  h1 {
    font-size: 56px;
    letter-spacing: -1.68px;
    margin: 32px 0;
  }

  @media (max-width: 1024px) {
    h1 {
      font-size: 36px;
      margin: 20px 0;
    }
  }

  h2 {
    font-size: 24px;
    line-height: 118%;
    letter-spacing: -0.24px;
    margin: 0 0 8px;
  }

  @media (max-width: 1024px) {
    h2 {
      font-size: 20px;
    }
  }

  p {
    margin: 0;
  }

  code,
  .counter {
    font-family: var(--mono);
    display: inline-flex;
    border-radius: 4px;
    color: var(--text-h);
  }

  code {
    font-size: 15px;
    line-height: 135%;
    padding: 4px 8px;
    background: var(--code-bg);
  }

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
`

export const Theme = () => {
  return <style dangerouslySetInnerHTML={{ __html: themeCSS }} />
}
