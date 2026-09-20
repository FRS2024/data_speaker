---
name: Ambient Intelligence Workspace
colors:
  surface: '#131314'
  surface-dim: '#131314'
  surface-bright: '#39393a'
  surface-container-lowest: '#0e0e0f'
  surface-container-low: '#1c1b1c'
  surface-container: '#201f20'
  surface-container-high: '#2a2a2b'
  surface-container-highest: '#353436'
  on-surface: '#e5e2e3'
  on-surface-variant: '#c3c6d3'
  inverse-surface: '#e5e2e3'
  inverse-on-surface: '#313031'
  outline: '#8d909d'
  outline-variant: '#434751'
  surface-tint: '#aec6ff'
  primary: '#aec6ff'
  on-primary: '#002e6a'
  primary-container: '#7ca7ff'
  on-primary-container: '#003a83'
  inverse-primary: '#2b5caf'
  secondary: '#d2bbff'
  on-secondary: '#3f018d'
  secondary-container: '#582ca7'
  on-secondary-container: '#c6aaff'
  tertiary: '#45dfa4'
  on-tertiary: '#003825'
  tertiary-container: '#01bf87'
  on-tertiary-container: '#00462f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#aec6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#eaddff'
  secondary-fixed-dim: '#d2bbff'
  on-secondary-fixed: '#25005a'
  on-secondary-fixed-variant: '#5629a4'
  tertiary-fixed: '#68fcbf'
  tertiary-fixed-dim: '#45dfa4'
  on-tertiary-fixed: '#002114'
  on-tertiary-fixed-variant: '#005137'
  background: '#131314'
  on-background: '#e5e2e3'
  surface-variant: '#353436'
typography:
  display-hero:
    fontFamily: Geist
    fontSize: 44px
    fontWeight: '500'
    lineHeight: 52px
    letterSpacing: -0.03em
  display-hero-mobile:
    fontFamily: Geist
    fontSize: 30px
    fontWeight: '500'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 28px
    fontWeight: '500'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Geist
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.06em
  code-tabular:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-lg: 1.5rem
  margin: 1rem
  margin-md: 1.5rem
  margin-lg: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system establishes an atmospheric, focused, dark-mode workspace tailored for advanced data analytics and natural conversational AI interaction. The aesthetic relies on an interplay of deep obsidian matte tones, layered tonal surfaces, micro-delicate translucency, and spectral ambient gradients reminiscent of state-of-the-art synthetic reasoning environments.

### Core Tenets
- **Cognitive Quiet:** High-density data dashboards and long-form AI reasoning demand an interface that recedes into the background. Visual noise, harsh high-contrast divides, and intrusive chrome are systematically eliminated.
- **Ambient Illumination:** Depth is derived not from heavy skeuomorphic drop shadows, but from luminous, ultra-soft spectral glows (indigo-to-cyan) emerging behind prompt capsules and primary analytical actions.
- **Precision Engineering:** High legibility, crisp tabular numerals, hairline ghost borders (5% to 10% white opacity), and pill-form inputs establish a precision laboratory feel.
- **Fluid Continuity:** The conversational thread and data canvas blend seamlessly across collapsing panels, streaming generative outputs, and contextual execution cards.

## Colors

The color palette is built for extreme low-light visual comfort, sustained analytical immersion, and luminous AI feedback cues.

### Surface Tiers & Neutral Scales
- **Canvas Base (`#131314` / `#0E1015`):** Ground-level environment for the application canvas and root shell.
- **Surface Level 1 (`#1E1F20`):** Secondary regions, collapsible sidebar panels, and bottom prompt containment shelves.
- **Surface Level 2 (`#23252A`):** Floating analytical cards, model configuration drawers, and contextual toolbars.
- **Surface Level 3 (`#282A2D`):** Active selections, hover overlays, modal headers, and elevated dropdown menus.

### Ambient AI Accents & Signals
- **Primary Electric Arc (`#7CA7FF`):** Represents interactive triggers, focused inputs, user prompts, and streaming indicators.
- **Secondary Aura (`#A87FFB`):** Paired with the primary hue to generate the characteristic ambient gradient (`rgba(26, 40, 68, 0.45)` transitioning into ethereal violet-blue).
- **Tertiary Telemetry Emerald (`#34D399`):** Reserved strictly for verified model status, valid database connections, positive delta metrics, and real-time execution success.
- **Hairline Ghost Borders:**
  - Standard edge: `rgba(255, 255, 255, 0.05)`
  - Active / hover edge: `rgba(255, 255, 255, 0.12)`
  - Elevated modal edge: `rgba(255, 255, 255, 0.18)`

### Text Contrast Tiers
- **High Emphasis Text (`#E3E3E3`):** Primary headings, prompt inputs, model responses, and active tabular values.
- **Medium Emphasis Text (`#9CA3AF`):** Labels, axis definitions, metadata stamps, and navigation items.
- **Subtle / Disabled Text (`#555960`):** Placeholder text, inactive controls, and trailing telemetry codes.

## Typography

The typographic hierarchy is clean, structural, and neutral. Geist handles standard user interface copy, conversation bubbles, and display greetings. JetBrains Mono is assigned to code snippets, telemetry statistics, query generation blocks, and metadata tags.

### Typographic Roles & Expressive Usage
- **Greeting & Conversational Display (`display-hero`):** Features negative letter-spacing and an optional subtle gradient mask (transitioning from `#FFFFFF` down to `#7CA7FF` / `#A87FFB`) for empty state conversational greetings (e.g., "Where shall we direct the analysis today?").
- **Generative Body Streams (`body-lg` / `body-md`):** Generous line heights (1.55–1.625) reduce cognitive fatigue during prolonged reading of multi-paragraph analytical conclusions.
- **Code & Metric Blocks (`code-tabular` / `label-caps`):** Ensures numeric data alignment within analytical matrix tables, token consumption tallies, execution timers, and SQL syntax viewers.

## Layout & Spacing

The workspace implements an adaptive shell layout governed by an asymmetrical dynamic split: an expandable/collapsible persistent vertical navigation rail (64px collapsed, 260px expanded) paired with an elastic, centered analytical chat stream (maximum content width: 840px for single-column dialogue; 1440px for dual-pane interactive analytics).

### Grid Models & Adaptive Behavior
- **Mobile (< 768px):** Single-column stack. Navigation collapses into an off-canvas drawer. The chat canvas runs edge-to-edge with `margin: 1rem`. Prompt entry docks directly above keyboard safe-insets.
- **Tablet (768px - 1024px):** Persistent 64px icon rail. Chat stream centers with `margin-md: 1.5rem`. Data inspector cards dock below execution outputs.
- **Desktop (1024px+):** Collapsible sidebar rail. Support for side-by-side generative split: Left pane displays conversation narrative and iterative prompts; right pane hosts reactive data visualizations, tables, and Vega/ECharts canvases with `gutter-lg: 1.5rem`.

### Spacing Density
A strict 4px base rhythm aligns micro-elements (`space-xs` = 4px, `space-sm` = 8px) across inline tags, prompt accessories, model switcher tags, and token pills.

## Elevation & Depth

Visual hierarchy uses tonal surface layering combined with low-intensity spectral lighting and hairline borders. Drop shadows are diffused and atmospheric rather than structural.

### The Depth Stack
- **Level 0 (Canvas Base - `#131314`):** Passive background. No shadow or edge treatment.
- **Level 1 (Docked Containers - `#1E1F20`):** Sidebar container, pinned action shelves, and contextual message feeds. Border: `1px solid rgba(255, 255, 255, 0.05)`. Shadow: None.
- **Level 2 (Interactive Floating Cards - `#23252A`):** Query cards, model parameter panels, and prompt pills.
  - Border: `1px solid rgba(255, 255, 255, 0.08)`.
  - Ambient Shadow: `0px 8px 32px -4px rgba(0, 0, 0, 0.5)`.
- **Level 3 (Modal Surfaces & Command Palettes - `#282A2D`):** Quick-switch menus, contextual tooltips, and data export dialogs.
  - Border: `1px solid rgba(255, 255, 255, 0.14)`.
  - Shadow: `0px 16px 48px -8px rgba(0, 0, 0, 0.75), 0px 0px 24px 0px rgba(124, 167, 255, 0.08)`.

### Ambient Radiant Glows
When the AI model is actively streaming, thinking, or parsing a complex dataset, active capsules gain an underlying atmospheric bloom:
- **Radial Glow:** `background: radial-gradient(circle at 50% 0%, rgba(124, 167, 255, 0.12) 0%, rgba(168, 127, 251, 0.05) 50%, transparent 100%)`.
- **Active Focus Ring:** `0px 0px 0px 1px rgba(124, 167, 255, 0.4), 0px 0px 16px 0px rgba(124, 167, 255, 0.2)`.

## Shapes

The interface embraces a modern pill-shaped aesthetic (`roundedness: 3`). Fully rounded capsules frame user interactions, prompt engines, and quick-filter switches, while large content containers utilize smooth, elevated curves to evoke an approachable, intelligent feel.

### Geometric Application
- **Pills (`rounded-full` / 9999px):** Primary input bars, prompt accessory chips, execution tags, model selectors, action buttons, and status badges.
- **Large Panels (`rounded-3xl` / 2rem):** Outer prompt docking containers and expansive greeting summary cards.
- **Medium Panels (`rounded-2xl` / 1.5rem):** Conversational AI responses, code sandboxes, and data grid cards.
- **Micro UI (`rounded-lg` / 0.5rem):** Inline table cells, dropdown menu items, code snippet blocks, and tooltip boxes.

## Components

### 1. Primary Prompt Input Bar
- **Structure:** Floating, large capsule-like container anchored to the bottom viewport.
- **Styling:** Base `#1E1F20`, hairline border `rgba(255, 255, 255, 0.08)`, radius `rounded-3xl`.
- **Focus State:** Transitions border to `rgba(124, 167, 255, 0.4)` with an ambient bottom-glow bloom of `rgba(26, 40, 68, 0.45)`.
- **Integrated Elements:** Multi-modal attach button (ghost pill), token usage indicator (`label-caps`), and a circular send action with a gradient fill (`#7CA7FF` to `#A87FFB`) when populated.

### 2. Buttons
- **Primary Pill:** Full pill radius. Gradient fill (`linear-gradient(135deg, #7CA7FF, #A87FFB)`), text `#0E1015` (bold weight for contrast). No border. On hover, luminance increases by 10% with a localized halo.
- **Secondary / Ghost Pill:** Background `#23252A`, border `1px solid rgba(255, 255, 255, 0.07)`, text `#E3E3E3`. On hover, background shifts to `#282A2D` and border to `rgba(255, 255, 255, 0.15)`.
- **Icon Button:** 36px circular pill. Transparent or `#1E1F20` base, text `#9CA3AF`, shifting to `#E3E3E3` on hover with a micro-scale transition (`scale: 1.05`).

### 3. Filter Chips & Model Switchers
- **Anatomy:** Compact pill (`rounded-full`, height 32px), inner padding `0.25rem 0.75rem`.
- **Inactive:** Background `rgba(255, 255, 255, 0.03)`, border `1px solid rgba(255, 255, 255, 0.06)`, text `#9CA3AF`.
- **Active:** Background `rgba(124, 167, 255, 0.12)`, border `1px solid rgba(124, 167, 255, 0.35)`, text `#7CA7FF`.

### 4. Conversational Cards & Response Bubbles
- **User Entry:** Right-aligned or clean indented pill layout, background `#23252A`, text `#E3E3E3`, subtle ghost border.
- **AI Response Stream:** Flat canvas placement with no heavy card boxing; reads cleanly directly over `#131314`. When returning generated SQL, python, or data charts, content is housed within a nested `#1E1F20` card (`rounded-2xl`, border `rgba(255, 255, 255, 0.06)`).

### 5. Checkboxes & Radio Controls
- **Checkbox:** 18px box with `rounded-md` corners, border `1px solid rgba(255, 255, 255, 0.2)`. When selected, fills with `#7CA7FF` and displays an obsidian `#0E1015` checkmark.
- **Radio Button:** Fully circular pill selector. Active state features a centered `#7CA7FF` pip inside an elevated ring.

### 6. Responsive Collapsible Sidebar
- **Expanded (260px):** Displays project workspaces, chat history groups (e.g., "Today", "Previous 7 Days"), and active data connection pills.
- **Collapsed (64px):** Compact vertical rail with centered icon buttons, live emerald status dot indicating cloud model readiness, and quick-access settings anchor.