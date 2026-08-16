import { Box, CircularProgress, Typography } from "@mui/material";
import { useTranslation } from "react-i18next";

export interface LoadingIndicatorProps {
  message?: string;
}

export const LoadingIndicator = ({ message }: LoadingIndicatorProps) => {
  const { t } = useTranslation();

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        gap: 1,
        p: 2,
      }}
    >
      <CircularProgress />
      <Typography variant="body2" color="text.secondary">
        {message ?? t("loading.default")}
      </Typography>
    </Box>
  );
};
