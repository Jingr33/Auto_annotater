import { useMediaQuery } from "@mui/material";
import { CssBaseline, ThemeProvider as MuiThemeProvider } from "@mui/material";
import type { ReactNode } from "react";
import { createAppTheme } from "./theme";

export interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider = ({ children }: ThemeProviderProps) => {
  const prefersDark = useMediaQuery("(prefers-color-scheme: dark)");
  const theme = createAppTheme(prefersDark ? "dark" : "light");

  return (
    <MuiThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </MuiThemeProvider>
  );
};
