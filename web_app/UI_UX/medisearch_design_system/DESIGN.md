---
name: MediSearch Design System
colors:
  surface: '#f8f9ff'
  surface-dim: '#ccdbf4'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e6eeff'
  surface-container-high: '#dde9ff'
  surface-container-highest: '#d5e3fd'
  on-surface: '#0d1c2f'
  on-surface-variant: '#434654'
  inverse-surface: '#233144'
  inverse-on-surface: '#ebf1ff'
  outline: '#737685'
  outline-variant: '#c3c6d6'
  surface-tint: '#0c56d0'
  primary: '#003d9b'
  on-primary: '#ffffff'
  primary-container: '#0052cc'
  on-primary-container: '#c4d2ff'
  inverse-primary: '#b2c5ff'
  secondary: '#006b59'
  on-secondary: '#ffffff'
  secondary-container: '#7cf8da'
  on-secondary-container: '#00725f'
  tertiary: '#7b2600'
  on-tertiary: '#ffffff'
  tertiary-container: '#a33500'
  on-tertiary-container: '#ffc6b2'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2ff'
  primary-fixed-dim: '#b2c5ff'
  on-primary-fixed: '#001848'
  on-primary-fixed-variant: '#0040a2'
  secondary-fixed: '#7cf8da'
  secondary-fixed-dim: '#5ddbbe'
  on-secondary-fixed: '#00201a'
  on-secondary-fixed-variant: '#005143'
  tertiary-fixed: '#ffdbcf'
  tertiary-fixed-dim: '#ffb59b'
  on-tertiary-fixed: '#380d00'
  on-tertiary-fixed-variant: '#812800'
  background: '#f8f9ff'
  on-background: '#0d1c2f'
  surface-variant: '#d5e3fd'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  container-max: 1280px
  gutter: 24px
---

## Brand & Style
The design system is engineered for a high-trust, high-utility healthcare environment. It balances the rigor of clinical data with the approachable fluidity of a modern SaaS startup. The aesthetic is **Corporate Modern**, leaning into high-clarity interfaces that reduce cognitive load for both providers and patients.

The brand personality is authoritative yet empathetic. It achieves a "premium" feel through generous whitespace, precise alignment, and a restrained use of color that highlights critical health information over decorative elements. It draws inspiration from Material Design 3’s logic-based layout system but refines it with more sophisticated typography and softer, intentional depth.

## Colors
The palette is rooted in medical tradition but modernized for digital clarity. 
- **Primary (Medical Blue):** Used for primary actions, active states, and brand recognition. It signifies stability.
- **Secondary (Health Green):** Reserved for "healthy" status indicators, success states, and growth-related metrics.
- **Neutrals:** Soft Slate is used for body text to reduce the harsh contrast of pure black, improving long-form readability.
- **Surface Strategy:** In light mode, use light gray borders (#E2E8F0) to define containers. In dark mode, surfaces are tiered using subtle shifts in hex value rather than heavy shadows to maintain a clean look.

## Typography
This design system utilizes **Inter** for all roles to ensure maximum legibility and a systematic, utilitarian feel. 
- **Hierarchy:** Headlines use tighter letter-spacing and semi-bold weights to command attention. 
- **Readability:** Body text uses a generous 1.5x line-height ratio to facilitate ease of reading in data-heavy medical records.
- **Labels:** Small labels and captions should use medium or semi-bold weights to remain legible at reduced sizes, especially for metadata and chart annotations.

## Layout & Spacing
The layout follows a **Fixed-Fluid Hybrid** model. Content is contained within a 1280px max-width wrapper on desktop but utilizes a fluid 12-column grid within that container.

- **Desktop:** 12 columns, 24px gutters, 40px side margins.
- **Tablet:** 8 columns, 16px gutters, 24px side margins.
- **Mobile:** 4 columns, 16px gutters, 16px side margins.

A strict 4px/8px baseline grid is used to maintain vertical rhythm. Whitespace is used aggressively between sections to signify "cleanliness" and "order," two vital psychological triggers in healthcare software.

## Elevation & Depth
Depth in the design system is conveyed through **Tonal Layers** supplemented by **Ambient Shadows**. 

1. **Level 0 (Base):** The background (#FFFFFF).
2. **Level 1 (Cards/Sections):** Uses a 1px border (#E2E8F0) with no shadow or a very soft 2px blur.
3. **Level 2 (Dropdowns/Modals):** Uses a sophisticated shadow with two layers: 
   - Layer A: 0px 10px 15px -3px rgba(0, 0, 0, 0.1)
   - Layer B: 0px 4px 6px -4px rgba(0, 0, 0, 0.1)
4. **Interactive State:** Hover states on cards should result in a slight vertical lift (-2px) and a subtle increase in shadow density to provide tactile feedback.

## Shapes
The shape language is consistently **Rounded**. By using a base of 0.5rem (8px) for standard components and increasing to 1rem (16px) for larger containers and cards, the UI feels modern and accessible rather than sharp and institutional. 

- **Small elements (Inputs, Buttons):** 8px radius.
- **Large elements (Dashboard cards, Modals):** 16px radius.
- **Status Pills:** Fully rounded (pill-shaped) to distinguish them from interactive buttons.

## Components
- **Buttons:** Primary buttons use the Trustworthy Medical Blue with white text. Secondary buttons use a light blue ghost style or a border-only approach. Corner radius must be 8px.
- **Input Fields:** Use a 1px Slate-200 border that thickens and changes to Medical Blue on focus. Labels sit clearly above the field in `label-md`.
- **Cards:** White background, 16px corner radius, and a subtle light gray border. Avoid heavy shadows; prefer borders to define space.
- **Chips/Status:** Use the Health Green for positive results and Medical Blue for neutral categories. Text inside chips should be `label-sm`.
- **Data Visualization:** Use a curated palette of Secondary Green, Primary Blue, and a soft Orange for warnings. Lines should be 2px thick with rounded joints.
- **Checkboxes/Radios:** Use 4px rounded corners for checkboxes and fully circular for radios, utilizing Primary Blue for the active state to ensure visibility.