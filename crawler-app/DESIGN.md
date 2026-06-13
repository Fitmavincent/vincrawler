# VinCrawler Frontend Design Guide

This document records the current frontend design direction so future sessions can extend the app consistently.

## Product Intent

VinCrawler is a utility dashboard for quickly scanning deals across retail channels. The UI should prioritize fast access to channel tabs, search, product cards, and tables. Avoid marketing-style hero sections, explanatory copy, and decorative metrics that push products below the first viewport.

The first screen should get users into the workflow immediately:

- Brand/status bar at the top.
- Channel tabs near the top of the first viewport.
- Active channel heading, search, and results visible without scrolling where practical.
- Extra descriptive text should be removed unless it directly helps scanning or filtering deals.

## Layout Model

The app shell lives in `src/components/Home.vue`.

- Keep the hero compact. It is a branded header, not a landing page.
- Current header content is only the `VinCrawler` brand lockup and the `Live deal scanner` status pill.
- The results panel overlaps the compact header slightly using negative margin.
- Do not reintroduce the previous headline, supporting paragraph, or metric cards.

The channel workspace lives in `src/components/Results.vue`.

- `Results.vue` owns the tab shell and channel accent variables.
- Channel components own their content styling: heading, search, table/cards, and empty states.
- `BackToTop` must remain outside `.results-panel`; `backdrop-filter` on the panel creates a fixed-position containing block in browsers, which breaks floating button placement if nested inside it.

## Color System

Use a neutral warm app shell plus channel-specific accents. Do not use dark green as a global accent because it clashes with Woolworths.

Global app chrome:

- Page background: `#faf8f3`
- Header overlay: dark neutral/warm brown gradient using `rgba(18, 18, 20, 0.95)` and `rgba(57, 44, 27, 0.9)`
- Global amber accent: `#f59e0b`
- Global amber text/accent: `#fbbf24`
- Warm text for floating action/loader: `#78350f`

Channel accent variables are defined in `Results.vue`:

- Default/generic: `#f59e0b`
- OzBargain: `#f37021`
- Coles: `#e01a22`
- Woolworths: `#178841`

Each new channel should add a new class in `Results.vue`, for example:

```css
.results-panel.channel-amazon {
  --channel-accent: #ff9900;
  --channel-accent-soft: #fff7ed;
  --channel-accent-border: rgba(255, 153, 0, 0.28);
}
```

Then update the `channelClasses` array in `Results.vue` to map the tab index to that class.

## Channel Branding

Channel colors should appear in channel-specific places only:

- Active tab pill.
- Channel badge.
- Channel heading tint/background.
- Price/highlight text for that channel.
- Hover state for product/deal links.

Avoid applying a retailer color to the whole app shell. The shell must remain neutral so Amazon, Chemist Warehouse, supermarkets, and future retailers can sit together without the page reading as one retailer brand.

Current channel files:

- OzBargain: `src/components/OzbResults.vue`, orange-led.
- Coles: `src/components/ColesResults.vue`, red-led.
- Woolworths: `src/components/WooliesResults.vue`, green-led.

## Components And Styling

### Results Panel

- Rounded panel: `1rem` radius.
- Subtle translucent white panel and shadow.
- `backdrop-filter: blur(18px)` is used on `.results-panel`; remember this affects fixed descendants.
- Mobile tab nav must have enough bottom padding so active pills and shadows do not look clipped.
- Horizontal tab scrolling should stay available for future channels.

### Tabs

Tabs are compact pill buttons.

- Mobile: smaller text and padding.
- Active tab uses `var(--channel-accent)`.
- Mobile active tab shadow is intentionally lighter than desktop to prevent clipping.
- Do not remove the extra bottom padding under `.p-tabview-nav`; it prevents the bottom crop bug.

### Search

Search is a full-width control inside each active channel.

- Keep it prominent and visible early in the first viewport.
- It uses the shared `SearchInput.vue`.
- Avoid adding explanatory text around it.

### Loading

The loading overlay uses a custom CSS spinner instead of relying on the default `vue-loading-overlay` SVG animation.

- Styles live in `src/index.css` as `.vc-loading-card`, `.vc-loading-ring`, and `@keyframes vc-loader-spin`.
- Spinner accent is global amber (`#f59e0b`), not retailer green.

### Back To Top

`BackToTop.vue` is a plain semantic `<button>`, not a PrimeVue button.

- White circular surface.
- Brown/amber icon: `#78350f`.
- Fixed to viewport bottom-right.
- Keep it outside `.results-panel`.

## Responsive Rules

Required checks before finishing frontend changes:

- 320px mobile width: no horizontal document overflow.
- 390px mobile width: tabs fit or scroll internally without cropping.
- Desktop width: results panel, tabs, and first channel content remain visible and aligned.
- Back-to-top button remains inside the viewport after scrolling.

Known regression risks:

- `body { min-width: 320px; }` caused horizontal overflow on narrow mobile viewports. Do not re-add it.
- Putting `BackToTop` inside `.results-panel` breaks fixed positioning because of `backdrop-filter`.
- Removing bottom padding from `.p-tabview-nav` causes tab pills to appear cut at the bottom on mobile.

## Design Principles For Future Channels

When adding Amazon, Chemist Warehouse, or other retailers:

- Add channel-specific color tokens in `Results.vue`.
- Keep the shell neutral.
- Keep channel heading and cards dense and scan-focused.
- Do not add landing-page copy or metrics.
- Ensure the tab strip remains horizontally scrollable on mobile.
- Prefer product data density over decorative cards.

## Verification

Minimum command:

```bash
npm run build
```

Visual QA should be done in the browser at:

- Mobile: 320px wide.
- Mobile: 390px wide.
- Desktop: 1280px wide.

Useful DOM checks:

- `document.documentElement.scrollWidth > document.documentElement.clientWidth` should be `false`.
- The active tab link should have visible clearance below it.
- `.back-to-top` should be fixed, visible after scroll, and inside the viewport.
