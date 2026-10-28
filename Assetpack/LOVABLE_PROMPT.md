# Lovable prompt — Fizzy & Crush website (v2, built from the site mockup)

Paste everything below the line into Lovable. Upload the `web` folder first (it holds the GLB cans, WebP renders, fonts and the ready-made interactive SVGs) together with `reference/site_mockup.jpg`, and put the files in the project's `public/assets` folder (fonts in `public/fonts`).

---

Build a one-page marketing site for **Fizzy & Crush**, a creamy soda in 500 ml cans that pairs bright fruit with smooth vanilla. **The layout must match the attached mockup `reference/site_mockup.jpg` section by section**: same order, same colours, same type, same composition. Do not add sections, a top navigation bar, carousels or extra UI that is not in the mockup. Where this prompt describes motion, the mockup shows the resting state.

The page has eight parts, top to bottom:

0. Loading screen (logo fills with soda)
1. Hero: "Fruit meets vanilla", interactive 3D can, flavour switch
2. Story: "A soda made for slow sips and big grins", straw fills while scrolling
3. "80 kcal / can" with an image or video frame
4. Rhubarb & Vanilla (blue)
5. Lemon & Vanilla (red)
6. Six-pack: "Six cans in one crush"
7. Footer with the IconBev logo

## Brand tokens

Set these as CSS variables on `:root`.

| Token | Hex | Use |
|---|---|---|
| `--cream` | `#fce9be` | Page background, logo letters, text on colour |
| `--kraft` | `#dfa06e` | Vanilla/kraft tone: hero pattern lines, logo outline, "80 kcal" panel |
| `--ink` | `#140105` | Headlines, body text on cream, footer background |
| `--rhubarb` | `#3f88c5` | Rhubarb flavour, blue section |
| `--rhubarb-2` | `#5196c4` | Second tone of the blue pattern |
| `--lemon` | `#f7345d` | Lemon flavour pink (can colour, 80 kcal frame) |
| `--berry` | `#c40831` | Red section background, lips |
| `--berry-2` | `#ce103a` | Second tone of the red pattern |
| `--sun` | `#f5d547` | Lemon yellow accents |

## Typography

Load `web/fonts/fc-font.css` (self-hosted, no Google Fonts).

- **Headlines:** `"FC Display"` (`FCDisplay-Regular.woff2`). Always uppercase, tight leading (~0.9), ink on cream or cream on colour. Very large: hero headline ~ 7–8 vw on desktop, section headlines ~ 6 vw.
- **Small caps lines and body copy:** `"FC Font Info Bold"`. Always uppercase, 15–18 px, leading ~1.25, max ~ 46 ch per line, as in the mockup.
- **Logo:** never set in a font. Use the SVGs.

## Assets

| File | Where it goes |
|---|---|
| `web/svg/logo_loader.svg` | Loading screen logo. Inline it (import with `?raw` and `dangerouslySetInnerHTML`, or convert it to a React component). It has a built-in liquid layer clipped to the letters, driven by the CSS variable `--fill` (0 → 1). |
| `web/svg/straw_fill.svg` | Lips + striped straw for the story section. Inline it. `--fill` (0 → 1) makes the patterned liquid travel up the straw from the bottom end to the lips. |
| `web/svg/pattern_cream.svg` | Hero and loader background (kraft lines on cream). |
| `web/svg/pattern_rhubarb.svg` | Rhubarb section background (two blues). |
| `web/svg/pattern_lemon.svg` | Lemon section background (two reds). |
| `web/svg/demo.html` | Reference only: shows the two interactive SVGs at different fill levels. |
| `web/can_rhubarb.glb`, `web/can_lemon.glb` | The real 500 ml cans for the hero 3D can (Draco, Y-up, base at the origin). |
| `web/lemon_float_front.webp` | Lemon can floating on a pink backdrop: the "80 kcal" frame. `web/rhubarb_float_front.webp` is the blue alternative. |
| `web/rhubarb_name_closeup.webp`, `web/lemon_name_closeup.webp` | Transparent close-ups of the can with the flavour name, for the flavour sections. |
| `web/sixpack_pair.webp` | Transparent render of both six-packs, for the six-pack section. |
| `web/rhubarb_float_front_alpha.webp`, `web/lemon_float_front_alpha.webp` | Transparent floating cans: fallback for the 3D can when WebGL is unavailable. |
| `Lemon.svg`, `rhubarb.svg`, `vanilla.svg` | Flavour illustrations: hero flavour buttons, vanilla flower next to the hero headline, floating props in the 80 kcal frame. |
| `iconbev_logo.svg` | IconBev company mark for the footer (cream). |
| `fizzy&crush_logo.svg` | Static wordmark (for the favicon and OG image only). |

## Tech

- React + Vite + TypeScript + Tailwind.
- `three`, `@react-three/fiber`, `@react-three/drei` for the hero can only.
- `gsap` + `ScrollTrigger` for scroll-driven effects, `lenis` for smooth scrolling (synced to the ScrollTrigger ticker).
- All copy in one `content.ts`.
- Respect `prefers-reduced-motion`: no smooth-scroll hijack, patterns stop flowing, the loader and straw jump straight to their end state, the can does not shake.
- Responsive: on mobile every two-column section stacks (image above text), headlines scale down with `clamp()`.

## Shared component: `<FlowingPattern variant="cream | rhubarb | lemon" />`

The mockup's arrows mean the pattern backgrounds are alive: they slowly **flow like liquid**. Build one reusable full-bleed background component:

- Preferred: a small WebGL plane (a fullscreen `<canvas>` with a fragment shader, using `ogl` or a separate lightweight R3F canvas) that samples the pattern SVG rasterised to a 2048 px texture, repeats it (the pattern tiles horizontally), drifts it slowly sideways (about one tile per 60–90 s) and warps the UVs with a gentle low-frequency noise (amplitude ~ 0.01–0.015, speed slow) so the lines ripple like melting cream. Scroll velocity may add a little extra drift.
- Fallback (no WebGL, low-power or reduced motion): the SVG as a CSS `background-image` (`background-size: 1100px auto`, repeat) with a slow `background-position` drift animation, or static for reduced motion.
- Pause when the section is off-screen (IntersectionObserver).
- Pattern scale should match the mockup: on a 1728 px wide screen one pattern tile is roughly 1100 px wide.

## 0. Loading screen

Full-screen, fixed, above everything.

- Background: `<FlowingPattern variant="cream" />` (the "live background"), so it continues seamlessly into the hero.
- Centre: the inline `logo_loader.svg`, about 40 vw wide (min 280 px, max 720 px).
- **The loading effect is someone pouring the soda into the logo.** Set the SVG's `--fill` from real load progress: drei `useProgress` for the GLBs, plus `document.fonts.ready` and the hero images. Smooth the value (lerp or a GSAP tween) so it never jumps, and keep a minimum duration of about 1.8 s so the pour is visible. The liquid rises only inside the cream letters; the kraft outline plate never changes. The built-in waves slide and small bubbles rise inside the letters.
- The liquid colour follows the default flavour (rhubarb blue: `--liquid: #3f88c5; --liquid-top: #5196c4`).
- Small progress number under the logo in FC Font Info Bold, e.g. "64%" (optional, keep it subtle).
- At 100%: hold 300 ms, give the logo a small squash-and-stretch "full" bounce, then the logo scales down and fades while the loader fades out, revealing the hero (the pattern underneath stays still, so it feels like one continuous background).
- Block scrolling while the loader is showing.

## 1. Hero — "Fruit meets vanilla"

Full viewport height. Background: `<FlowingPattern variant="cream" />`.

**Left half: the 3D can (interactive, but limited).**
- One `<Canvas>` with the GLB can, tilted about 25° to the left as in the mockup, floating with a slow vertical bob and a soft contact shadow on the pattern below.
- Lighting: `<Environment preset="studio">`, ACES/AgX tone mapping. Aluminium parts metalness 1, roughness ~0.28; label clearcoat ~0.5.
- **Interaction:** the user can grab and drag the can to turn it around its own long axis, **but only about ±60° from the rest pose** (clamp it). On release it springs back to the rest pose with a soft overshoot (a damped spring, e.g. `@react-spring/three` or a GSAP elastic ease). No zoom, no pan, no full 360° spin.
- While the cursor hovers the can, it does a small playful **shake** (a quick ±4° wobble, a "fizz" jiggle) once per hover. The cursor becomes `grab` / `grabbing`.
- Small parallax: the can tilts a few degrees toward the cursor.
- On touch devices horizontal drag turns the can (same ±60° clamp); vertical swipes must still scroll the page.
- Fallback without WebGL: `rhubarb_float_front_alpha.webp` / `lemon_float_front_alpha.webp`.

**Right half:**
- `vanilla.svg` (vanilla flower and pod) sits overlapping the top-left of the headline, as in the mockup, with a gentle sway.
- Headline in FC Display, ink, three lines: **FRUIT / MEETS / VANILLA**. Reveal line by line from a clip mask after the loader.
- Small line in FC Font Info Bold: **TRY THE FLAVOURS BELOW ↓**
- **Two flavour buttons**: `Lemon.svg` and `rhubarb.svg` as icons (~110 px), no text, `aria-label="Lemon & Vanilla"` / `"Rhubarb & Vanilla"`, `aria-pressed`. Hover: lift and rotate a few degrees. The active one is slightly larger with a soft cream glow underneath.
- **Clicking an icon switches the can**: the can does a quick full spin while the label swaps (load the other GLB, or swap the label texture), then settles back to the rest pose. Rhubarb is the default. The active flavour is global state: it also sets the straw liquid colour in section 2.

**Bottom centre:** **↓ SCROLL FOR MORE ↓** in FC Font Info Bold, with the arrows bobbing gently. Clicking it smooth-scrolls to section 2. It fades out once the user starts scrolling.

## 2. Story — "A soda made for slow sips and big grins"

Plain `--cream` background, generous height (about 100 vh).

- **Left:** headline in FC Display, ink, five lines: **A SODA / MADE FOR / SLOW SIPS / AND BIG / GRINS**.
- **Right:** the inline `straw_fill.svg`: the red lips at the top right, the striped straw running diagonally down and out of the bottom of the section (let it overflow the section bottom and overlap the top of section 3, as in the mockup).
- Body copy under the lips, in FC Font Info Bold:
  > FIZZY & CRUSH STARTED WITH A SIMPLE CRUSH. THE CREAM SODA YOU REMEMBER, GROWN UP A LITTLE. WE PAIR BRIGHT, REAL-TASTING FRUIT WITH SMOOTH VANILLA AND JUST ENOUGH FIZZ TO MAKE IT DANCE. TWO FLAVOURS, ONE MOOD: SUNNY, SILLY AND VERY DRINKABLE.
- **Scroll effect: the straw fills as you scroll.** Drive the SVG's `--fill` from 0 to 1 with a ScrollTrigger scrub: start when the section top reaches 80% of the viewport, end when the section's centre passes the top third. The liquid is the brand pattern in the active flavour's colours and travels up the straw from the bottom end to the lips, following the bend.
  - Rhubarb: `--liq-a: #3f88c5; --liq-b: #fce9be`
  - Lemon: `--liq-a: #c40831; --liq-b: #fce9be`
- When `--fill` reaches 1, the lips do one small "sip" squash (scaleY 0.96 and back) and three tiny cream bubbles pop out of the corner of the mouth.
- Scrolling back up drains the straw again (the scrub is reversible).

## 3. "80 kcal / can"

A full-width band about 70 vh tall, split in two:

- **Left ~35%:** solid `--kraft` panel with **80 / KCAL / /CAN** in FC Display, ink, three lines.
- **Right ~65%:** a media frame. By default it shows `lemon_float_front.webp` (lemon can floating on pink), `object-fit: cover`, with `Lemon.svg` and two `vanilla.svg` flowers floating around the can at different parallax depths, as in the mockup. The image slowly zooms (scale 1.08 → 1) as the section scrolls into view.
- Build the frame as a `<MediaFrame>` that also accepts a video: if `content.ts` has `kcalVideo` set (e.g. `/assets/kcal_loop.mp4`), render a muted, looping, `playsInline` autoplay `<video>` with the image as its poster instead.

## 4. Rhubarb & Vanilla

Full-width section about 80 vh tall. Background: `<FlowingPattern variant="rhubarb" />`.

- `rhubarb_name_closeup.webp` (transparent) placed top-centre and **bleeding off the top edge**, tilted as in the mockup, so the can looks like it is dipping into the section. Subtle parallax (moves ~60 px slower than the scroll).
- Headline in FC Display, cream: **RHUBARB & / VANILLA**, bottom left.
- Body copy, cream, FC Font Info Bold:
  > RHUBARB BRINGS THE SNAP: BRIGHT, TART AND A LITTLE BIT CHEEKY. VANILLA ROUNDS IT OFF LIKE A SCOOP OF ICE CREAM ON A CRUMBLE. IT'S THE GARDEN-PARTY SODA YOU DIDN'T KNOW YOU NEEDED.
- Headline and copy reveal from a clip mask when the section enters.

## 5. Lemon & Vanilla

Same layout as section 4. Background: `<FlowingPattern variant="lemon" />`.

- `lemon_name_closeup.webp` bleeding off the top edge.
- Headline in FC Display, cream: **LEMON & / VANILLA**.
- Body copy, cream:
  > LEMON WAKES YOU UP, VANILLA CALMS YOU DOWN. TOGETHER THEY TASTE LIKE A LEMON MERINGUE ON A SUMMER AFTERNOON: BRIGHT, CREAMY AND GONE FAR TOO FAST.

## 6. Six-pack — "Six cans in one crush"

`--cream` background.

- `sixpack_pair.webp` (both cartons, transparent) centred near the top, with a slow float and a soft shadow. It rises into place as the section enters.
- Headline in FC Display, ink, two lines: **SIX CANS / IN ONE CRUSH**.
- Body copy, ink:
  > SIX CANS, ONE CARTON, ZERO CHILL REQUIRED. OUR KRAFT SIX-PACKS WEAR THE FIZZY & CRUSH MELT ON THE OUTSIDE AND SHOW OFF THE CANS THROUGH DIE-CUT LOGO WINDOWS. GRAB ONE FOR YOUR NEXT PICNIC.

## 7. Footer

`--ink` background, compact (about 30 vh).

- `iconbev_logo.svg` centred (~70 px wide, cream).
- Under it, in FC Font Info Bold, cream: **©2026 IconBev A/S**.

## Quality bar

- Match the mockup's proportions: wide margins (~6 vw), big headlines, lots of air.
- Every interactive element has hover, focus and active states; keyboard accessible with a visible focus ring in `--berry`.
- Alt text on every image. The flavour switch announces the change with `aria-live="polite"`.
- SEO title: "Fizzy & Crush — Creamy soda with a crush". OG image: the hero composition or `duo_pattern.webp`.
- Lighthouse performance ≥ 85 on desktop. Preload the default GLB, the fonts and `pattern_cream.svg`; lazy-load everything below the hero.
- Component names: `Loader`, `FlowingPattern`, `HeroCan`, `Hero`, `FlavourSwitch`, `StorySection` (with `StrawFill`), `KcalSection` (with `MediaFrame`), `FlavourSection`, `SixPackSection`, `Footer`.
- No age gate, no alcohol language, no health claims beyond the "80 kcal / can" line, no fake reviews or prices.
