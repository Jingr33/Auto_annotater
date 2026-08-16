import { type ReactNode, createContext, useContext, useEffect, useState } from "react";

interface LicenseContextType {
  token: string | null;
  setToken: (token: string | null) => void;
}

const LicenseContext = createContext<LicenseContextType>({ token: null, setToken: () => {} });

export const useLicense = () => useContext(LicenseContext);

export interface LicenseProviderProps {
  children: ReactNode;
  initialToken: string | null;
  onTokenChange: (token: string | null) => void;
}

export const LicenseProvider = ({
  children,
  initialToken,
  onTokenChange,
}: LicenseProviderProps) => {
  const [token, setTokenState] = useState<string | null>(initialToken);

  const setToken = (newToken: string | null) => {
    setTokenState(newToken);
    onTokenChange(newToken);
  };

  useEffect(() => {
    setTokenState(initialToken);
  }, [initialToken]);

  return <LicenseContext.Provider value={{ token, setToken }}>{children}</LicenseContext.Provider>;
};
