# Brand & Design Tokens, NDSU Bison Fund

So a pitch looks like the fund, not like a generic template. The palette and typefaces
below are taken from the NDSU College of Business / Bison Fund site (ndsu.edu/business),
inspected October 2026, and mapped onto shadcn/ui's token names so they drop straight into
a presentation build. The drop-in stylesheet is `templates/ndsu-design-tokens.css`.

## Palette (source values)

| Name | Hex | RGB | Role |
|---|---|---|---|
| NDSU Green | `#00583D` | 0,88,61 | brand primary, headers, primary buttons |
| Green dark | `#003524` | 0,53,36 | headings, sidebar rail |
| Green deepest | `#00221B` | 0,34,27 | text on yellow, dark surfaces |
| Green 100 | `#D4ECE6` | 212,236,230 | hover/accent surface |
| Teal (green 400) | `#51AB9F` | 81,171,159 | secondary accent, dark-mode primary |
| NDSU Yellow | `#FFC425` | 255,196,37 | brand secondary, highlights |
| Gold (yellow 400) | `#E5B01A` | 229,176,26 | accent lines |
| Harvest | `#BE5D27` | 190,93,39 | tertiary accent |
| Body text | `#282C2F` | 40,44,47 | default text |
| Subtle text | `#686E6D` | 104,110,109 | captions, helper text |
| Background | `#F2F3F3` | 242,243,243 | page background |
| Off-white | `#FBFBF9` | 251,251,249 | elevated cards |
| Border | `#D7DADB` | 215,218,219 | borders, dividers |
| Link / button text | `#785D03` | 120,93,3 | link color on light |
| Error | `#C62828` | 198,40,40 | negative / risk |

## Token mapping (shadcn/ui)

The drop-in file assigns these semantic tokens, per shadcn's theming convention
(`references`: `background`/`foreground` pairs, plus `chart-1..5` and `sidebar-*`):

| shadcn token | Light value | Meaning here |
|---|---|---|
| `--background` / `--foreground` | `#F2F3F3` / `#282C2F` | page shell + default text |
| `--card` / `--card-foreground` | `#FFFFFF` / `#282C2F` | slide and panel surfaces |
| `--primary` / `--primary-foreground` | `#00583D` / `#FFFFFF` | NDSU Green, headline brand surface |
| `--secondary` / `--secondary-foreground` | `#FFC425` / `#003524` | NDSU Yellow, supporting fills |
| `--muted` / `--muted-foreground` | `#F2F3F3` / `#686E6D` | subdued surfaces, captions |
| `--accent` / `--accent-foreground` | `#D4ECE6` / `#003524` | hover / highlight |
| `--destructive` | `#C62828` | negative figures, risk |
| `--border` / `--input` | `#D7DADB` | dividers, form controls |
| `--ring` | `#00583D` | focus ring |
| `--chart-1..5` | green, yellow, teal, harvest, night | chart palette |
| `--sidebar-*` | dark-green rail | dark navigation |

Dark mode overrides the same names inside `.dark` (green lifts to teal `#51AB9F` for
contrast, per shadcn's convention of inverting `primary` on dark).

Brand swatches are also exposed directly as `--ndsu-green`, `--ndsu-yellow`,
`--ndsu-teal`, `--ndsu-harvest`, so utilities like `bg-ndsu-green` / `text-ndsu-yellow`
work without going through the semantic tokens.

## Typography

- **Body:** Gotham (geometric sans), weights 300–600.
- **Headings:** New Spirit (serif), used at weight 300, light and high-contrast.

**Both are licensed typefaces.** Free, close substitutes (used in the drop-in file's font
stacks so decks render on any machine):

- Gotham → **Montserrat** (or Poppins).
- New Spirit → **Source Serif 4** (or Spectral), set at weight 300 for headings.

If the fund has licensed Gotham/New Spirit installed, the stack uses them automatically;
the substitutes are the fallback.

## Building presentation materials

Cheapest path that looks right, in order:

1. **HTML / shadcn mockup deck**, scaffold shadcn, paste in `ndsu-design-tokens.css`, then
  build each slide as a component using `bg-background`, `text-foreground`, `bg-primary`,
  `bg-ndsu-yellow`, `border-border`. Best control, and the deck can be presented live from a
  browser or exported to PDF. See the `design-mockup` and `shadcn-design-system` skills.
2. **PowerPoint / Google Slides**, set theme colors to `#00583D` (primary), `#FFC425`
  (accent), `#282C2F` (text), `#F2F3F3` (background); set the heading font to a serif at
  light weight and body to the sans stack above.
3. **Docs / handouts**, carry the same palette and font stack into Word, Google Docs, or Notion.

## Guardrail

The palette mirrors the university's own site so student materials look like the fund's.
The NDSU name, logo, and bison mark are governed by university brand rules, use them only
as the fund's own student materials permit, and don't invent new marks or recolor the logo.
This file is about consistency, not about claiming a license to the marks.
