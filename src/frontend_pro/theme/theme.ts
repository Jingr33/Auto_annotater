import { createTheme } from '@mui/material/styles'

export const createAppTheme = (mode: 'light' | 'dark') =>
  createTheme({
    palette: {
      mode,
      primary: {
        main: mode === 'dark' ? '#c084fc' : '#aa3bff',
      },
    },
    typography: {
      fontFamily: `system-ui, 'Segoe UI', Roboto, sans-serif`,
    },
  })
