---
name: Alabaster Forge
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#3f4850'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#707881'
  outline-variant: '#bfc7d2'
  surface-tint: '#006398'
  primary: '#006194'
  on-primary: '#ffffff'
  primary-container: '#007bb9'
  on-primary-container: '#fdfcff'
  inverse-primary: '#93ccff'
  secondary: '#4b41e1'
  on-secondary: '#ffffff'
  secondary-container: '#645efb'
  on-secondary-container: '#fffbff'
  tertiary: '#a33900'
  on-tertiary: '#ffffff'
  tertiary-container: '#cc4900'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#cce5ff'
  primary-fixed-dim: '#93ccff'
  on-primary-fixed: '#001d31'
  on-primary-fixed-variant: '#004b73'
  secondary-fixed: '#e2dfff'
  secondary-fixed-dim: '#c3c0ff'
  on-secondary-fixed: '#0f0069'
  on-secondary-fixed-variant: '#3323cc'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb599'
  on-tertiary-fixed: '#370e00'
  on-tertiary-fixed-variant: '#7f2b00'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.03em
  display-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: 0em
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
  code-inline:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

The design system establishes a daylight desktop operating environment tailored for engineering, architecture, and high-focus systems workflows. It balances computational precision with ceramic tactility, departing from conventional stark dark terminals in favor of an airy, high-contrast, structural workspace.

### Core Character
- **Target Audience:** Systems engineers, full-stack builders, command-line artisans, and desktop OS power users who require absolute legibility during long sessions.
- **Emotional Response:** Sharp clarity, architectural stability, surgical precision, and ergonomic calm.
- **Design Movement:** Clean Modernist Desktop meets Precision Glassmorphism. The visual surface language relies on matte alabaster planes, frosted window chrome, hairline borders, and vivid technical accents evoking phosphor status lights and compiler diagnostics.

## Colors

The palette reproduces the feel of industrial instrumentation and polished ceramic workstations. The environment uses high-luminance, low-saturation substrates paired with saturated signal emitters for runtime states, active processes, and focused panes.

### Surface System
- **Base Canvas (Alabaster):** `#f8fafc` — Primary desktop backdrop and root OS canvas.
- **Window Surfaces & Panels:** `#ffffff` — Foremost content planes, active code buffers, and inspector viewports.
- **Sunken Dock & Inset Panels:** `#f1f5f9` — Terminal trays, tab wells, and auxiliary utility docks.
- **Subtle Structural Hairlines:** `#e2e8f0` (default) and `#cbd5e1` (active window perimeter / focus splits).

### Pigment Roles
- **Primary (`#0284c7` Electric Cyan/Teal):** Used for active tab strokes, system cursor states, focused process meters, and primary execution triggers.
- **Secondary (`#4f46e5` Cyber Indigo-Violet):** Applied to package management tags, symbolic tokens, branch references, and persistent OS dock anchors.
- **Tertiary (`#ea580c` Guará Orange):** Dedicated signal color for build notifications, breakpoint markers, pending migrations, and destructive or critical triggers.
- **Neutral Core (`#0f172a` Slate Graphite):** Maximum-contrast ink for headlines, executable metrics, and system labels. Secondary copy rests at `#334155` and muted chrome metadata at `#64748b`.

## Typography

Plus Jakarta Sans brings a geometric yet ergonomic posture to desktop application frames, code panels, and workspace management. Tight negative letter-spacing in headline scales gives multi-window titlebars an assertive, dense, software-suite identity.

### Structural Rules
- **Legibility Guardrails:** Running body copy must not drop below 12px. Technical status labels and memory counters are set at 11px with uppercase tracking (`+0.04em`) to ensure instant glanceability under dense desktop load.
- **Hierarchy Handling:** Active application window headers use `headline-sm`, tooltips and badge metadata rely on `label-sm`, and modal dialogs lead with `headline-md`.
- **Numeric Clarity:** Ensure tabular figures are enabled where supported to prevent jitter across CPU monitors, process IDs, and clock tickers.

## Layout & Spacing

The OS utilizes a floating-window container grid superimposed on an immutable root desktop plane. Spacing operates strictly on an 8pt architectural rhythm to mirror fixed hardware display coordinates.

### Canvas & Window Model
- **Tiling & Floating Grid:** Workspaces arrange windows across dynamic multi-split panes using a 16px (`gutter`) gap. Windows must maintain a minimum 24px (`margin`) offset from the screen perimeter when floating.
- **App Chrome Density:** Toolbar heights are standardized to 40px (compact) or 48px (standard), with internal controls spaced using `space-xs` (4px) and `space-sm` (8px).
- **Responsive Modes:**
  - **Desktop (>= 1280px):** Multi-pane tiling, simultaneous floating windows, persistent system utility bar, docked side-rail inspectors.
  - **Compact Display (< 1280px):** Single active window with automatic sheet overlays; panels collapse into flyout drawers; gutters scale down to `space-sm`.

## Elevation & Depth

Visual separation relies on physical layering: frosted translucent planes, hairline structural borders, and razor-sharp ambient shadows.

### Atmospheric Glassmorphism
- **Frosted Window Chrome:** Top-level window headers, popover context menus, and the bottom launcher dock implement a translucent backdrop (`rgba(255, 255, 255, 0.82)`) coupled with a 12px blur filter and a 1px inner inset border (`rgba(255, 255, 255, 0.6)`).
- **Hairline Framing:** Every pane, detached inspector, and card boundary must be defined by a 1px border (`#e2e8f0`). Active/focused windows step up to `#cbd5e1` with a cyan-tinted accent rim.

### Shadow Architecture
- **Level 1 (Dock, Toolbars, Embedded Panels):** Flat, border-only containment or zero-blur micro offsets (`0 1px 2px rgba(15, 23, 42, 0.05)`).
- **Level 2 (Inactive Windows, Tiles, Flyout Cards):** `0 4px 12px -2px rgba(15, 23, 42, 0.06), 0 2px 4px -1px rgba(15, 23, 42, 0.03)`.
- **Level 3 (Focused Window, Modal Prompts, Context Overlays):** `0 16px 32px -6px rgba(15, 23, 42, 0.10), 0 6px 12px -3px rgba(15, 23, 42, 0.04)`.

## Shapes

The OS adheres strictly to an 8px radius geometry (`ROUND_FOUR` / Level 2), balancing tactile softness with clean desktop density.

### Radius Assignments
- **Windows & Main Modals:** Unified 8px perimeter radius. Floating window corners clip contents cleanly without cutting into window controls.
- **Buttons, Text Inputs, and Code Chips:** 8px radius for full internal component cohesion.
- **Sub-segment Pills & Group Toggles:** Nested inner elements use 4–6px to maintain concentric geometric balance inside 8px-bounded parents.
- **System Dock:** 12px floating chassis radius with 8px internal app launcher icons.

## Components

### Buttons
- **Primary (`Action/Execute`):** Electric Cyan (`#0284c7`) solid fill with white label (`#ffffff`), 8px border radius, 36px height for toolbars, 40px for dialogs. Subtle hover elevation with cyan glow halo (`rgba(2, 132, 199, 0.25)`).
- **Secondary (`Workspace/Nav`):** Pure white ceramic fill (`#ffffff`), 1px border in `#e2e8f0`, deep slate text (`#0f172a`). Hover shifts background to `#f8fafc` and border to `#cbd5e1`.
- **Accent/Destructive (`Kill/Deploy`):** Guará Orange (`#ea580c`) fill or muted tint (`rgba(234, 88, 12, 0.1)`) with `#ea580c` border and text.

### Chips & Badges
- **Status Pills:** 22px height, 6px radius, uppercase `label-sm` font.
  - Active/Running: Soft cyan substrate (`rgba(2, 132, 199, 0.1)`) with `#0284c7` typography and 4px pulsing indicator dot.
  - Build Warning/Pending: Soft orange substrate (`rgba(234, 88, 12, 0.1)`) with `#ea580c` text.
  - Runtime/Kernel: Cyber Indigo substrate (`rgba(79, 70, 229, 0.1)`) with `#4f46e5` text.

### Window Cards & Process Panels
- Solid off-white ceramic surface (`#ffffff`) surrounded by 1px `#e2e8f0` border.
- Header bars utilize frosted glass (`rgba(255, 255, 255, 0.85)` + backdrop blur), housing traffic light status or window management glyphs on the left, and workspace breadcrumbs in deep slate graphite (`#0f172a`) in the center.

### Input Fields & Command Omnibars
- **Text Inputs:** Ceramic white base, 1px border in `#cbd5e1`, 8px corner radius. Focused state applies `#0284c7` border and an ambient `0 0 0 3px rgba(2, 132, 199, 0.15)` focus ring.
- **Omnibar / Quick Switcher (Cmd+K):** Floating center overlay, Level 3 elevation, frosted glassmorphism background, large input (`headline-sm`), with secondary cyber indigo shortcut indicators.

### Checkboxes & Radio Controls
- High-contrast 16px geometric boxes with 4px (checkbox) or 8px (radio) curvature.
- Inactive state: `#ffffff` canvas with `#cbd5e1` perimeter.
- Active state: `#0284c7` fill containing a crisp white tick mark or centered indicator disc.

### Lists & Tree Views
- Dense file and process trees set with 28px row heights.
- Hovered row receives `#f1f5f9` fill; selected active row adopts `#e0f2fe` (soft cyan) background with `#0284c7` left border indicator (2px wide) and bold text weight.