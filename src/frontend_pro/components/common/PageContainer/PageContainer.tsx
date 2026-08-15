import type { ReactNode } from 'react'
import { Box } from '@mui/material'

export interface PageContainerProps {
  children: ReactNode
}

export const PageContainer = ({ children }: PageContainerProps) => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {children}
    </Box>
  )
}
