---
name: Cybernetic Obsidian
colors:
  surface: '#0f131c'
  surface-dim: '#0f131c'
  surface-bright: '#353942'
  surface-container-lowest: '#0a0e16'
  surface-container-low: '#181c24'
  surface-container: '#1c2028'
  surface-container-high: '#262a33'
  surface-container-highest: '#31353e'
  on-surface: '#dfe2ee'
  on-surface-variant: '#bac9cc'
  inverse-surface: '#dfe2ee'
  inverse-on-surface: '#2c3039'
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
  tertiary: '#ffe8dd'
  on-tertiary: '#522300'
  tertiary-container: '#ffc4a2'
  on-tertiary-container: '#914300'
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
  tertiary-fixed: '#ffdbc8'
  tertiary-fixed-dim: '#ffb68b'
  on-tertiary-fixed: '#321200'
  on-tertiary-fixed-variant: '#753400'
  background: '#0f131c'
  on-background: '#dfe2ee'
  surface-variant: '#31353e'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 3rem
    fontWeight: '800'
    lineHeight: 3.5rem
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 2rem
    fontWeight: '700'
    lineHeight: 2.5rem
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.5rem
    fontWeight: '700'
    lineHeight: 2rem
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: 2rem
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 1.125rem
    fontWeight: '600'
    lineHeight: 1.5rem
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1.125rem
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 0.875rem
    fontWeight: '500'
    lineHeight: 1.25rem
    letterSpacing: 0.02em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: 1rem
    letterSpacing: 0.03em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 0.6875rem
    fontWeight: '600'
    lineHeight: 0.875rem
    letterSpacing: 0.05em
  code-block:
    fontFamily: JetBrains Mono
    fontSize: 0.8125rem
    fontWeight: '400'
    lineHeight: 1.375rem
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-compact: 0.5rem
  margin: 1.5rem
  margin-mobile: 0.75rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system establishes the visual baseline for a specialized, performance-tuned workstation operating system environment. The aesthetic combines industrial cybernetics with focused minimalism, leveraging deep obsidian tones, tactical glassmorphic layers, and hyper-precise accent signals.

### Target Audience & Persona
Engineers, kernel developers, visual computing specialists, and Linux power users demanding extreme low-latency response, low visual fatigue during multi-monitor night sessions, and dense system telemetry.

### Visual Signature
- **Cybernetic Glassmorphism:** Controlled backdrops (`blur(16px)`), micro-thin structural borders (`1px rgba(255,255,255,0.08)`), and deep obsidian surfaces.
- **High-Density Signal Hierarchy:** Critical system states are broadcast through high-frequency neon accents—cyan for active compute, violet for core system primitives, and Guará orange for high-priority user alerts and process interventions.
- **Physical Precision:** Zero ornamental clutter. Every visual boundary defines a functional region (plasmoid, dock tile, telemetry metric, or console split).

## Colors

The palette operates on an absolute dark-mode architecture. Deep obsidian eliminates panel glare, while luminescent signals prioritize visual processing across high-density desktop surfaces.

### Semantic Tiers
- **Primary (`#00e5ff` / Cyan):** Active computation states, focused window chrome highlights, high-frequency interactive controls, and positive network telemetry.
- **Secondary (`#8b5cf6` / Cyber Violet):** Operating system system-level actions, Wayland compositor indicators, and daemon execution states.
- **Tertiary (`#ff7a00` / Guará Orange):** Identity hooks, Guará assistant interventions, compilation checkpoints, and hardware thermal thresholds.
- **Neutral Baseline (`#0b0f17` to `#161f30`):** Obsidian black canvas, layered containers, elevated plasmoids, and micro-delimiters.

### Functional Status Indicators
- **Success (`#10b981` / Emerald):** Nominal service state, kernel scheduler sync (`sched_ext`), healthy containers.
- **Warning (`#f59e0b` / Amber):** Memory limits approaching capacity, thermal throttling, package dependency notices.
- **Error (`#f43f5e` / Rose):** Kernel panic trace, failed daemon units, dropped network frames, dead lock alerts.
- **Info (`#0ea5e9` / Sky):** Passive status updates, background system syncs, daemon telemetry feeds.

## Typography

The type ecosystem relies on a functional duality:
1. **Plus Jakarta Sans** delivers humanist clarity to application menus, header breadcrumbs, window titles, and contextual body dialogue.
2. **JetBrains Mono** enforces structured numerical balance across live telemetry meters, CPU clock speeds, VRAM allocations, container IDs, and Konsole command streams. Tabular figures must remain enabled across all metrics to eliminate pixel shift during live value cycles.

## Layout & Spacing

A modular 8px spatial grid drives desktop workspace alignment, multi-monitor tiling geometries, and application shell structures.

### Workstation Layout Rules
- **Desktop Grid:** 12-column variable grid spanning dynamic ultrawide dimensions with strict 16px element gutters.
- **Floating Command Center:** Fixed width overlay of exactly 520px positioned on the screen margin with safe areas anchored at 16px from the screen edge.
- **Dock Metrics:** Persistent floating bottom pill at 64px height, floating 12px above the base edge, with internal icon gaps locked to `space-sm` (8px).
- **Konsole & Telemetry Panels:** Dense horizontal/vertical split interfaces utilize `gutter-compact` (8px) gaps to ensure visual cohesion without screen real estate waste.

## Elevation & Depth

Visual hierarchy uses physical backdrops, variable transparency, and luminous rim-lighting rather than drop shadows.

### Atmospheric Hierarchy
1. **Layer 0 (Canvas Base):** Deep Obsidian (`#0b0f17`), solid, 0 blur.
2. **Layer 1 (Workspace Tiling / Tiled Plasmoids):** `#0f1420` with 85% opacity, `backdrop-filter: blur(16px)`, border of `1px solid rgba(255, 255, 255, 0.08)`.
3. **Layer 2 (Floating System Overlays / Dock / Control Center):** `#141b2d` with 70% opacity, `backdrop-filter: blur(24px)`, border of `1px solid rgba(0, 229, 255, 0.18)`, ambient occlusion via `0 8px 32px -4px rgba(0, 0, 0, 0.65)`.
4. **Layer 3 (Modal Alerts & Contextual Menus):** `#1a233a` with 90% opacity, `backdrop-filter: blur(28px)`, perimeter rim stroke of `1px solid rgba(255, 122, 0, 0.35)` when triggered by critical daemons, or `1px solid rgba(139, 92, 246, 0.35)` for standard window options.

## Shapes

The design system standardizes on an 8px radius (`roundedness: 2`) across the entire user experience.

- **Base Radius (8px):** Standard inputs, Konsole terminal splits, plasmoid modules, notification cards, Docker container tiles.
- **Nested Controls (4px / Soft):** Hardware gauge pills, status badges, telemetry inline tags, micro sliders.
- **Floating Shells (12px to 16px / Large):** 520px Command Center panel, Quick Settings popups, and the desktop floating application dock.

## Components

### Buttons & Interactive Controls
- **Primary Action:** Solid background using Primary Cyan (`#00e5ff`) with black typography (`#0b0f17`, 700 weight). On hover: scale(1.02), background shifts to `#33ecff` with a 4px soft cyan ambient glow.
- **Secondary Action:** Glass substrate (`rgba(255, 255, 255, 0.04)`), `1px solid rgba(255, 255, 255, 0.12)`, text in white. On hover: border promotes to `#8b5cf6`, subtle purple glow.
- **Destructive/Kill:** Glass substrate bordered with Rose (`#f43f5e`), text `#f43f5e`. On active: solid `#f43f5e` with white text.

### Hardware Telemetry Badges (GPU / CPU / RAM)
- Compact monospaced cluster (`JetBrains Mono`, `label-sm`).
- Surface: `#0f1420` with 60% opacity, 1px border `rgba(255, 255, 255, 0.06)`.
- Architecture: Left key label (e.g., `NV-GPU 0`) in muted slate, right telemetry value (e.g., `68°C | 92%`) dynamically colored: Cyan (<70%), Amber (70-89%), Rose (90%+).

### Command Center Overlay (520px Panel)
- Rigid width: 520px, full-height desktop minus 32px vertical margins.
- Surface: Glassmorphic obsidian container (`#0b0f17` at 80% opacity, `backdrop-filter: blur(24px)`), right-anchored floating frame.
- Internal Segments: Top section houses the Guará Kernel Assistant & Scheduler Status (`sched_ext`), mid-section hosts dynamic Docker/Podman container runtimes, bottom segment integrates Quick Toggles (Night Shift, Compositor Bypass, Low Latency Audio).

### Konsole Terminal Split
- Background: `#080b11` flat base (zero glass blur to ensure zero GPU text-rendering overhead).
- Active Pane: 1px continuous accent line in Cyan (`#00e5ff`) along the split boundary. Inactive panes: 1px border in `rgba(255, 255, 255, 0.05)`.
- Tab indicators: Pure pill tabs with `label-md`, terminal activity indicated by a 4px Guará Orange dot.

### Floating Dock
- Position: Anchored bottom-center, floating 12px from display bottom.
- Surface: Layer 2 Glassmorphism with 1px border `rgba(255, 255, 255, 0.1)`.
- Indicators: Active application instances mapped via 3px x 3px rounded cyan dots beneath the app icon. Running containers mapped with violet indicators.

### Kernel & Container Status Badges
- **sched_ext active:** Mini badge with green indicator dot (`#10b981`), JetBrains Mono uppercase (`SCHED_EXT: BPF_LAVD`), border in `rgba(16, 185, 129, 0.2)`.
- **Podman/Docker instance:** Monospaced runtime hash tag, state indicator ring (emerald for running, amber for paused, rose for stopped).