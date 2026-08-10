export const translations = {
  app: {
    title: 'Auto Annotater',
    logout: 'Logout',
  },
  license: {
    screenTitle: 'Auto Annotater Pro',
    subtitle: 'Enter your license token to activate Pro features',
    inputPlaceholder: 'Paste your license token here',
    activateButton: 'Activate',
    helpText: "Don't have a license? Contact support to get one.",
    invalidError: 'Invalid license token. Please try again.',
    validationError: 'Failed to validate license. Please try again.',
  },
  pipeline: {
    loadingStatus: 'Loading pipeline status...',
    finished: 'Pipeline finished',
    currentPrefix: 'Current:',
    totalSuffix: 'total',
    waiting: 'Waiting for items...',
    backButton: 'Back',
    skipButton: 'Skip',
    rejectButton: 'Reject',
    acceptButton: 'Accept',
  },
  loading: {
    default: 'Loading...',
  },
} as const

export type Translations = typeof translations
