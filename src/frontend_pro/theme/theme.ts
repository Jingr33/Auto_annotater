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
    components: {
      MuiAppBar: {
        defaultProps: {
          position: 'static',
          color: 'transparent',
          elevation: 0,
        },
        styleOverrides: {
          root: ({ theme }) => ({
            borderBottom: '1px solid',
            borderColor: theme.palette.divider,
          }),
        },
      },
      MuiContainer: {
        styleOverrides: {
          root: ({ theme }) => ({
            paddingTop: theme.spacing(3),
            paddingBottom: theme.spacing(3),
          }),
        },
      },
      MuiPaper: {
        styleOverrides: {
          outlined: ({ theme }) => ({
            padding: theme.spacing(2),
          }),
        },
      },
      MuiChip: {
        styleOverrides: {
          root: {
            fontWeight: 500,
          },
        },
      },
    },
  })
