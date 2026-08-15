import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from '../locales/en/translation.json'
import de from '../locales/de/translation.json'

export const resources = {
  en: { translation: en },
  de: { translation: de },
} as const

export const defaultLanguage = 'en'

void i18n.use(initReactI18next).init({
  resources,
  lng: defaultLanguage,
  fallbackLng: defaultLanguage,
  interpolation: {
    escapeValue: false,
  },
})

export default i18n
