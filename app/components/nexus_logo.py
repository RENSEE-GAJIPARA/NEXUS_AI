"""NEXUS AI Original Vector SVG Logo Mark."""

NEXUS_SVG_LOGO = """<svg width="44" height="44" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="nexusGrad" x1="8" y1="8" x2="40" y2="40" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#0EA5A4"/>
    </linearGradient>
  </defs>
  <line x1="12" y1="40" x2="12" y2="8" stroke="url(#nexusGrad)" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="12" y1="8" x2="36" y2="40" stroke="url(#nexusGrad)" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="36" y1="40" x2="36" y2="8" stroke="url(#nexusGrad)" stroke-width="3.5" stroke-linecap="round"/>
  <line x1="12" y1="24" x2="24" y2="24" stroke="#2563EB" stroke-width="1.5" stroke-dasharray="2 2" opacity="0.6"/>
  <line x1="24" y1="24" x2="36" y2="24" stroke="#0EA5A4" stroke-width="1.5" stroke-dasharray="2 2" opacity="0.6"/>
  <circle cx="12" cy="40" r="4" fill="#2563EB" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="12" cy="8" r="4" fill="#2563EB" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="24" cy="24" r="4.5" fill="url(#nexusGrad)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="36" cy="40" r="4" fill="#0EA5A4" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="36" cy="8" r="4" fill="#0EA5A4" stroke="#FFFFFF" stroke-width="2"/>
</svg>"""

def render_logo_html(size: int = 44) -> str:
    """Return HTML container string for NEXUS AI logo mark."""
    svg = NEXUS_SVG_LOGO.replace('width="44"', f'width="{size}"').replace('height="44"', f'height="{size}"')
    return f'<div style="display: inline-flex; align-items: center; justify-content: center;">{svg}</div>'
