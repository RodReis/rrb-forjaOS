---
name: Cybernetic Forge
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e18'
  surface-container-low: '#171b26'
  surface-container: '#1b1f2a'
  surface-container-high: '#262a35'
  surface-container-highest: '#313540'
  on-surface: '#dfe2f0'
  on-surface-variant: '#bac9cc'
  inverse-surface: '#dfe2f0'
  inverse-on-surface: '#2c303b'
  outline: '#849396'
  outline-variant: '#3b494c'
  surface-tint: '#00daf3'
  primary: '#c3f5ff'
  on-primary: '#00363d'
  primary-container: '#00e5ff'
  on-primary-container: '#00626e'
  inverse-primary: '#006875'
  secondary: '#d0bcff'
  on-secondary: '#3c0091'
  secondary-container: '#571bc1'
  on-secondary-container: '#c4abff'
  tertiary: '#ffe9df'
  on-tertiary: '#552100'
  tertiary-container: '#ffc4a6'
  on-tertiary-container: '#953f00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#9cf0ff'
  primary-fixed-dim: '#00daf3'
  on-primary-fixed: '#001f24'
  on-primary-fixed-variant: '#004f58'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#ffdbca'
  tertiary-fixed-dim: '#ffb690'
  on-tertiary-fixed: '#341100'
  on-tertiary-fixed-variant: '#783200'
  background: '#0f131d'
  on-background: '#dfe2f0'
  surface-variant: '#313540'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  display-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
    letterSpacing: -0.015em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  code-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 22px
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 16px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
  label-xs:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.06em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 0.75rem
  gutter-compact: 0.375rem
  margin: 1rem
  margin-dock: 0.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 2rem
---

## Brand & Style

This design system embodies the ethos of a high-performance developer workstation OS engineered specifically for software engineers, systems programmers, and game developers. The aesthetic blends tactical cyberpunk minimalism with ergonomic, high-density workstation utility. It evokes surgical precision, unyielding system speed, computational authority, and creative immersion.

The visual direction merges **Technical Minimalism** with **Subtle Cybernetic Glassmorphism**:
- Deep obsidian and graphite canvas tiers that reduce ocular fatigue during 14-hour compile and debugging sessions.
- Laser-focused neon accents that direct attention strictly to actionable state changes, execution flows, and critical telemetry.
- Ultra-refined 1px translucent borders mimicking precision-cut optic glass.
- Contrast-driven sensory hierarchy, allowing complex terminal multiplexers, pipeline graphs, and visual scene trees to sit comfortably beside system controls.

## Colors

The palette relies on absolute optical precision in low-light environments. Surfaces are layered to establish depth without heavy visual bulk.

### Surface System
- **Void Surface (Canvas Base):** `#0A0D14` – Primary desktop, root background, window frame backing.
- **Layer 1 (Panels & Workspaces):** `#10141E` – Sidebars, explorer trees, terminal docks.
- **Layer 2 (Elevated Surfaces & Cards):** `#161B26` – Tool palettes, inspectors, modal dialogues, floating tiles.
- **Layer 3 (Interactive Controls):** `#1E2433` – Inputs, inactive tabs, segmented control bars.
- **Border Ghost Substrates:** `rgba(255, 255, 255, 0.08)` resting, transitioning to `rgba(0, 229, 255, 0.35)` upon hover or focus.

### Accent & Telemetry Palette
- **Primary (Electric Cyan `#00E5FF` & Cyber Sky `#38BDF8`):** Active process states, current line indicators, focused borders, cursor pulse, and primary actions.
- **Secondary (Cyber Violet `#8B5CF6` & Deep Indigo `#6366F1`):** Neural execution states, local AI/Ollama engine activity, shader pipelines, branch tagging, and background daemon notifications.
- **Tertiary (Guará Forge Orange `#F97316` / `#FB923C`):** Mascot signature, compiler warnings, build execution checkpoints, breakpoint indicators, and human-in-the-loop overrides.
- **Telemetry Semantics:**
  - **Success / Docker Running:** `#10B981` (Emerald)
  - **Ollama / AI Stream:** `#8B5CF6` (Violet)
  - **GPU Peak / High Load:** `#F43F5E` (Crimson)
  - **Audit Passed:** `#00E5FF` (Cyan)

## Typography

The typography implements a strict bifurcation between system UI chrome and technical data streams:

1. **System Chromatics (Plus Jakarta Sans & Inter):** Geometric, uncluttered, and friendly without compromising industrial structure. Headings leverage tight letter spacing and high weight to establish fast landmark recognition. UI body text runs on Inter for unmatched micro-legibility in high-density inspector tables.
2. **Computational Chromatics (JetBrains Mono):** Monospaced forms are applied to all operational data, runtime readouts, memory addresses, file trees, status pills, and keyboard shortcuts. All numbers in telemetry dashboards must use tabular monospace alignment to prevent layout shifts during high-frequency metric streaming.

## Layout & Spacing

This design system uses a dockable, panel-based tiled layout model suited for multi-monitor workstations, ultrawide game-engine toolbars, and laptop screens:

- **Density Modes:** The grid adopts a base unit of `4px` with a standard component rhythm of `8px` (`0.5rem`) and `12px` (`0.75rem`).
- **Workspace Partitioning:** Tiled windows utilize split-screen gutter lines of `0.75rem` (`12px`) or compact `0.375rem` (`6px`) separators with interactive hover handles.
- **Micro-Paddings:** Dense operational panels (e.g., entity component trees, shader parameters) strictly employ `space-xs` and `space-sm` to maximize visible canvas area. High-level dashboard overviews scale out to `space-lg` and `space-xl`.

## Elevation & Depth

Visual hierarchy is constructed through luminosity tiers, selective backdrop filtering, and sub-pixel optical glow rather than standard volumetric drop shadows:

- **Backdrop Blur Matrix:** Modals, overlays, task switchers, and command palettes apply `backdrop-filter: blur(12px) saturate(180%)` over `rgba(16, 20, 30, 0.75)`.
- **Low-Contrast Ghost Outlines:** Every container, card, and docked module is delineated by a `1px` border set to `rgba(255, 255, 255, 0.08)`. In active states, this switches to `rgba(0, 229, 255, 0.4)` accompanied by a minimal cyan luminescent fringe: `0 0 12px rgba(0, 229, 255, 0.15)`.
- **Ambient Floor Shadows:** Floating palettes utilize an ultra-diffused shadow with a slight indigo tint: `0 8px 32px -4px rgba(6, 9, 15, 0.8), 0 2px 8px -2px rgba(139, 92, 246, 0.1)`.
- **No Direct Black Occlusions:** Never use pitch black `#000000` overlays; use graded opacity over `#0A0D14` to preserve surface glow integrity.

## Shapes

The design system maintains disciplined, industrial corner geometries calibrated between **8px** and **12px**:

- **Panels, Tiles & Windows:** Standard radius of `8px` (`rounded-lg` level under `roundedness: 1` equivalent to standard desktop shells) preserves screen real estate while mitigating brutalist harshness.
- **Controls & Chips:** Standard radius of `6px` to `8px`.
- **Micro-Indicators & Badges:** Distinct rectangular chips with `4px` corners, maintaining alignment with monospaced text geometry.
- **No Full Pill Contours:** Avoid full circular pill buttons (`rounded-full`) except for toggle switches and status pings to maintain an engineered, tactical hardware instrument aesthetic.

## Components

### Buttons & Action Triggers
- **Primary (Forge Cyan):** Background `linear-gradient(135deg, #00E5FF 0%, #00B4D8 100%)`, text `#0A0D14`, font `Plus Jakarta Sans` semi-bold 13px, border none, inner highlight `inset 0 1px 0 rgba(255,255,255,0.4)`. Hover state: subtle neon halo `0 0 16px rgba(0, 229, 255, 0.4)`.
- **Secondary (Cyber Shell):** Background `#161B26`, text `#F1F5F9`, border `1px solid rgba(255, 255, 255, 0.1)`. Hover state: background `#1E2433`, border `rgba(139, 92, 246, 0.5)`.
- **Ghost Tactical:** Transparent background, `JetBrains Mono` 12px, text `#94A3B8`. Hover state: text `#00E5FF`, background `rgba(0, 229, 255, 0.06)`.
- **Mascot / Guará Trigger:** Background `rgba(249, 115, 22, 0.12)`, text `#FB923C`, border `1px solid rgba(249, 115, 22, 0.3)`. Hover state: background `rgba(249, 115, 22, 0.22)`.

### System Telemetry & Micro-Indicators
- **Architecture:** Compact horizontal chips (`padding: 2px 6px`, radius `4px`, font `JetBrains Mono` 10px, uppercase).
- **Docker Indicator:** Green pulse dot `6px` (`#10B981`) with static label `#94A3B8`.
- **Ollama / AI Daemon:** Violet pulse dot `6px` (`#8B5CF6`) with active inference counter.
- **VRAM / GPU Load Meter:** Segmented 5-bar micro-gauge transitioning Cyan -> Violet -> Guará Orange under critical compute.
- **Audit Token:** Shield outline with cyan checkmark and micro-hash label.

### Cards & Workstation Modules
- Container background `#10141E` with `backdrop-filter: blur(8px)`.
- Header bar bordered bottom with `1px solid rgba(255, 255, 255, 0.06)`, height `36px`, housing title and quick-action icon rail.
- Content body cushioned with `0.75rem` (`space-md`) interior clearance.

### Form Inputs & Terminal Command Prompts
- Background `#0A0D14`, border `1px solid rgba(255, 255, 255, 0.12)`, corner radius `6px`.
- Input text rendered in `JetBrains Mono` 13px with syntax highlighting tokens.
- Focus state: border-color `#00E5FF`, box-shadow `0 0 0 1px #00E5FF, 0 0 12px rgba(0, 229, 255, 0.2)`.

### Selection & State Controls
- **Checkboxes & Radios:** Sharp `4px` corner squares for checkboxes, octagonal or minimal rounded forms for radios. Checked fill `#00E5FF` with dark `#0A0D14` iconography.
- **Tree View / Navigation Lists:** Left-edge `2px` dynamic marker in `#00E5FF` or `#F97316` for active document/scene-node with `#161B26` hover state background.