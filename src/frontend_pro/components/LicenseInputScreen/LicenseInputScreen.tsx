import { Container, Paper, Typography } from "@mui/material";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import { PageContainer } from "../common/PageContainer";
import { LicenseForm } from "./LicenseForm";
import { LicenseHeader } from "./LicenseHeader";

export interface LicenseInputScreenProps {
  onActivate: (token: string) => void;
  error: string | null;
}

export const LicenseInputScreen = ({ onActivate, error }: LicenseInputScreenProps) => {
  const { t } = useTranslation();
  const [token, setToken] = useState("");

  const handleSubmit = () => {
    onActivate(token.trim());
  };

  return (
    <PageContainer>
      <Container maxWidth="sm">
        <Paper elevation={3} sx={{ p: 5, textAlign: "center" }}>
          <LicenseHeader title={t("license.screenTitle")} subtitle={t("license.subtitle")} />
          <LicenseForm
            token={token}
            onTokenChange={setToken}
            onSubmit={handleSubmit}
            error={error}
          />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 3 }}>
            {t("license.helpText")}
          </Typography>
        </Paper>
      </Container>
    </PageContainer>
  );
};
