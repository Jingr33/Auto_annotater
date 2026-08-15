import { baseThemeCSS } from './baseTheme.css'
import { componentThemeCSS } from './componentTheme.css'

export const themeCSS = `${baseThemeCSS}\n${componentThemeCSS}`

export const Theme = () => {
  return <style dangerouslySetInnerHTML={{ __html: themeCSS }} />
}
