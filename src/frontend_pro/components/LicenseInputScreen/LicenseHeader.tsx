export interface LicenseHeaderProps {
  title: string
  subtitle: string
}

export const LicenseHeader = ({ title, subtitle }: LicenseHeaderProps) => {
  return (
    <div className="license-header">
      <h1>{title}</h1>
      <p className="license-subtitle">{subtitle}</p>
    </div>
  )
}
