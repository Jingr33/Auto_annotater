import { AppBar, Box, Button, Container, Toolbar, Typography } from "@mui/material";
import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";

export interface AppLayoutProps {
  children: ReactNode;
  onLogout: () => void;
}

export const AppLayout = ({ children, onLogout }: AppLayoutProps) => {
  const { t } = useTranslation();

  return (
    <Box
      sx={{
        maxWidth: "1200px",
        mx: "auto",
        px: 2,
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <AppBar>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, textAlign: "center" }}>
            {t("app.title")}
          </Typography>

          <Button onClick={onLogout}>{t("app.logout")}</Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ flexGrow: 1 }}>
        {children}
      </Container>
    </Box>
  );
};
