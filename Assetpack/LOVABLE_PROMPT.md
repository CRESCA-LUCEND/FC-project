# Lovable prompt — Fizzy & Crush website

Paste everything below the line into Lovable. Upload the files listed under "Assets" first (drag the `web` folder plus the SVGs and label PNGs into the chat or the project's `public/assets` folder).

---

Build a one-page, award-level, highly interactive marketing site for **Fizzy & Crush**, a creamy soda brand. It should feel like an Awwwards Site of the Day: bold, playful, tactile and smooth, never like a template. The site sells two flavours in 500 ml cans and the kraft six-packs they come in.

## Two references and what to take from each

**1. https://www.slight-twist.co.nz (structure — how a drinks site is built).** Take its page flow and its commerce logic:
- a hero with a short promise and a "Shop now" button
- a strip of product facts
- a "why it's good" block
- a looping marquee line
- a draggable "Our range" carousel ("Drag to view") with an ingredient line on each card
- one full-bleed section per flavour in that flavour's colour, each with a big name, an ingredient line, three short taste notes and a "Shop now" button
- a multipack section listing what is inside
- a newsletter sign-up, stockists and a footer

Leave out its age gate (this is a soft drink).

**2. https://casadisolare.com (design and interaction — the main inspiration).** Take its art direction and interaction quality:
- a calm preloader that opens into the site through a growing circular clip-mask
- huge, confident display type set in staggered lines with words in different styles inside one headline (e.g. "A *creamy* soda / inspired by / the MELT of / VANILLA*")
- a glowing, slowly moving WebGL shape as the emotional centrepiece
- sections that reveal through circular and rounded clip-masks while you scroll
- a sticky minimal top bar with section names and a live dot showing where you are (Intro · Flavours · Six-packs · Taste · Find us), plus a pill CTA on the right ("Buy a six-pack")
- an interactive list where hovering an item restyles a huge headline (their weight list)
- a tester with sliders that changes the content live (their type tester)
- a "hover to reveal illustration" story block
- a "Thank you for visiting" footer with huge type

Smooth, inertial scrolling throughout. Implement as much of the Casa di Solare interaction language as possible; that is the point of this site.

## Brand

- **Name:** Fizzy & Crush. Always written with the "&".
- **What it is:** creamy soda in 500 ml aluminium cans. It pairs bright fruit with smooth vanilla. Two flavours:
  - **Rhubarb & Vanilla:** owns BLUE.
  - **Lemon & Vanilla:** owns PINK.
- **Look:** playful, retro, sunny. A bubbly rounded wordmark sits over a flowing cream "melt" pattern.
- **Six-packs:** printed kraft cartons with die-cut logo windows, so the cans show through, and a kraft carry handle.

### Colours

Use these as CSS variables. They come from `color_palette.svg`.

| Token | Hex | Use |
|---|---|---|
| `--cream` | `#fce0b2` | Main light background, melt pattern, text on colour |
| `--ink` | `#140105` | Near-black text, dark sections |
| `--rhubarb` | `#3f88c5` | Rhubarb flavour colour |
| `--lemon` | `#f7345d` | Lemon flavour colour (pink) |
| `--berry` | `#c40831` | Deep red accent, hover states, & |
| `--sun` | `#f5d547` | Lemon yellow, highlights, bubbles |
| `--honey` | `#f7c550` | Warm secondary yellow |
| `--vanilla` | `#dfa06e` | Vanilla pod / kraft tone, six-pack section |
| `--mint` | `#9dcdc0` | Soft cool accent |
| `--leaf` | `#4cbb17` | Rhubarb leaf green (illustration accents only) |
| `--forest` | `#33673b` | Dark green (illustration accents only) |

The page background and text colour should **morph smoothly between sections**: cream for intro, blue for rhubarb, pink for lemon, warm kraft (`--vanilla` mixed with cream) for the six-packs, ink for the footer. Drive it with GSAP ScrollTrigger, tweening the CSS variables on `<body>`.

### Typography

- **Display:** "Fraunces" (Google Fonts, variable, with SOFT and WONK axes). Animate weight and softness the way Casa di Solare animates its variable font: on hover, on scroll, and in the taste tester.
- **Secondary display:** "Bricolage Grotesque" ExtraBold, for labels, tickers and buttons. It echoes Slight Twist's chunky rounded type.
- **Body:** "Bricolage Grotesque" Regular.
- **Wordmark:** use the real wordmark from `fizzy&crush_logo.svg`. Never set the logo in a font.

## Assets (all in the uploaded pack)

**3D**
- `web/can_rhubarb.glb`, `web/can_lemon.glb`
  - The real 500 ml can: body with the printed label, lid, tab and base.
  - Real-world metres, base at the origin, Y-up.
  - Draco-compressed, about 1 MB each. Load them with drei's `useGLTF` (Draco enabled).
  - The original `can_3d.blend` is the source file only and cannot be used in the browser.

**Renders (WebP, up to 2400 px)**
- `web/rhubarb_float_front_alpha.webp`, `web/lemon_float_front_alpha.webp`: floating cans with transparency.
- `web/rhubarb_name_closeup.webp`, `web/lemon_name_closeup.webp`: macro shots of the flavour name.
- `web/duo_pattern.webp`: both cans on the brand pattern. `web/duo_alpha.webp`: both cans, transparent.
- `web/sixpack_rhubarb.webp`, `web/sixpack_lemon.webp`, `web/sixpack_pair.webp`, `web/sixpack_rhubarb_diff.webp`, `web/sixpack_lemon_diff.webp`: six-pack cartons (the `_diff` files are alternate shots).

**Vector**
- `fizzy&crush_logo.svg`: the wordmark (pink outline plate, cream letters).
- `brand_pattern.svg`: the flowing "melt" pattern (pink and cream paths).
- `rhubarb.svg`, `Lemon.svg`, `vanilla.svg`: flavour illustrations.

**Textures:** `label_rhubarb_500ml_final.png`, `label_lemon_500ml_final.png` (the flat can labels, for texture swaps).

Fallback: use the WebP renders wherever WebGL is unavailable or the device is low-power.

## Tech

- React + Vite + TypeScript + Tailwind (Lovable default).
- **3D:** `three`, `@react-three/fiber`, `@react-three/drei`.
  - Use **one persistent full-screen `<Canvas>`** fixed behind the page. Each DOM section places the can in it through drei `<View>` (or a scroll-driven camera rig), so the can never reloads and can travel between sections.
  - Lighting: `<Environment preset="studio">`, ACES or AgX tone mapping, sRGB output.
  - Materials: aluminium parts MeshPhysicalMaterial with metalness 1, roughness about 0.28; label clearcoat about 0.5 so it reads like a varnished print.
  - `dpr={[1, 2]}`, with `<AdaptiveDpr>` and `<PerformanceMonitor>` to scale down.
- **Motion:**
  - `gsap` + `ScrollTrigger` for all scroll choreography.
  - `lenis` for smooth scrolling, synced to the ScrollTrigger ticker.
  - SplitType (or GSAP SplitText) for line/word/character reveals.
- Respect `prefers-reduced-motion`: no smooth-scroll hijack, no auto-rotation, fades instead of masks.
- Lighthouse targets: performance ≥ 85 on desktop, LCP < 2.5 s. Lazy-load everything below the hero. Preload the hero GLB and fonts.
- Fully responsive. On mobile:
  - The 3D can stays, but drag-to-rotate replaces hover effects.
  - Clip-mask reveals stay.
  - Horizontal carousels become swipeable.

## Global interaction system (everywhere)

- **Custom cursor:**
  - A small cream bubble with a thin ink ring.
  - It grows and shows a word on hover: "DRAG" on carousels, "TASTE" on flavours, "SHOP" on buy buttons, "SPIN" over the 3D can.
  - Inside it, it carries little fizz bubbles that trail with lag.
  - Hidden on touch devices.
- **Magnetic buttons:** pill-shaped, ink on cream. On hover they fill with the current flavour colour from the cursor point (a circular clip grow).
- **Fizz particles:** a lightweight canvas or instanced-mesh layer of rising bubbles. Their density and speed tie to scroll velocity, and they burst around the cursor on click.
- **Scroll-velocity skew** on the big marquees and huge headlines (small, max 6°).
- **Sticky top bar:**
  - Left: the logo (small).
  - Centre: section names with an active dot that slides between them.
  - Right: a "Buy a six-pack" pill.
  - It hides when scrolling down and returns when scrolling up.
- **Every heading reveals by line from a clip mask** (Casa style). Body copy fades up word by word in small groups.
- **Section transitions:** circular clip-path wipes that grow from the can's on-screen position into the next section's colour.

## Page, section by section

### 0. Preloader

- Cream screen. The wordmark's letters drop in one by one with a squash-and-stretch bounce.
- A counter (0–100) counts in Bricolage Grotesque, small, bottom right.
- When loaded, a circular mask grows from the centre and reveals the hero. The bubbles from the cursor system start rising.

### 1. Hero — "Intro"

- **The 3D can is the star**, centred, slightly tilted, floating with a gentle bob.
  - It rotates slowly on its own, and the user can drag it to spin with inertia (OrbitControls: rotation only, no zoom or pan, limited polar angle).
  - It tilts a little toward the cursor (parallax).
- **Behind it**, a soft glowing blob, our version of Casa di Solare's WebGL sun: a large, slowly morphing, noise-displaced radial gradient in the current flavour colour, cream at the core.
- **Huge headline behind and around the can**, staggered lines, mixed styles:
  - "*Fruit,* meet / VANILLA. / A creamy soda / with a CRUSH."
- **A flavour switch pill** (Rhubarb | Lemon).
  - Switching does a "melt" wipe: the brand pattern sweeps across as a mask.
  - The can swaps model or label with a quick 360° spin.
  - The glow and the page colour morph between blue and pink.
- "Scroll to fizz ↓" hint at the bottom with a bouncing bubble.
- CTA: "Shop the six-packs".

### 2. Fact ticker

A full-width marquee band in ink with cream text, skewing with scroll velocity:

`CREAMY SODA · BRIGHT FRUIT · SMOOTH VANILLA · 500 ML CANS · LIGHTLY SPARKLING · TWO FLAVOURS · ONE CRUSH ·`

Only use these facts. Do not invent nutrition or health claims.

### 3. Manifesto — "The melt" (Casa "sanctuary" block)

- A cream section that reveals through a growing rounded clip-mask.
- `brand_pattern.svg` animates as a slow, liquid "melt": an SVG `feTurbulence` + `feDisplacementMap`, or a shader on a plane, drifting with scroll.
- Huge staggered headline:
  - "A SODA / *made for* / slow SIPS / and big / GRINS*"
- Copy:
  > Fizzy & Crush started with a simple crush: the cream soda you remember, grown up a little. We pair bright, real-tasting fruit with smooth vanilla and just enough fizz to make it dance. Two flavours, one mood: sunny, silly and very drinkable.

### 4. Flavours — two full-bleed sections (Slight Twist flavour panels, Casa interactions)

For each flavour:
- The section is pinned for about 150 vh while scrolling.
- The 3D can stays centred and **rotates with scroll** through 360° so the whole label is shown.
- The name builds up in giant type around it.
- **Background:** the flavour colour, with the melt pattern in cream at 15% opacity.
- **Left column:** the flavour name, very large (Fraunces, weight animating from 300 to 900 as the section enters).
  - Under it, the ingredient line in Bricolage caps: "RHUBARB · VANILLA · BUBBLES" / "LEMON · VANILLA · BUBBLES".
  - Then three taste notes that pop in one by one as the can turns, each with a tiny icon.
- **Right column:** the macro render (`*_name_closeup.webp`) in a rounded mask that follows the cursor slightly (parallax).
- **Illustrations:**
  - The flavour illustrations (`rhubarb.svg` + `vanilla.svg`, or `Lemon.svg` + `vanilla.svg`) float around the can in parallax depth.
  - **Casa "hover to reveal":** hovering the flavour name reveals the illustration large under the cursor through a circular mask.
- **CTA:** "Shop Rhubarb & Vanilla" / "Shop Lemon & Vanilla".
- **Transition** from rhubarb to lemon: a circular wipe from the can.

**Rhubarb & Vanilla** (blue):
- Tagline: "*Tart* meets *tender.*"
- Notes:
  - "Tangy pink rhubarb up front"
  - "Smooth vanilla cream in the middle"
  - "A soft, fizzy finish"
- Copy:
  > Rhubarb brings the snap: bright, tart and a little bit cheeky. Vanilla rounds it off like a scoop of ice cream on a crumble. It's the garden-party soda you didn't know you needed.

**Lemon & Vanilla** (pink):
- Tagline: "*Zesty* meets *dreamy.*"
- Notes:
  - "Sunny lemon zest"
  - "Silky vanilla, like lemon cream pie"
  - "Light, lively bubbles"
- Copy:
  > Lemon wakes you up, vanilla calms you down. Together they taste like a lemon meringue on a summer afternoon, bright, creamy and gone far too fast.

### 5. Taste tester — "Taste" (Casa type-tester, reimagined)

A playful "Mix your mood" tool. It only changes the visuals and copy. It is not a real product configurator.

Three sliders:
- **FRUIT ←→ VANILLA**
- **FIZZ: still ←→ wild**
- **MOOD: chill ←→ party**

What the sliders change live:
- **FRUIT ←→ VANILLA:**
  - the background blends between the flavour colour and cream
  - the headline's Fraunces SOFT/weight axes change
  - the vanilla illustration grows or shrinks
- **FIZZ:** bubble density and speed
- **MOOD:** headline letter-spacing and wobble

A rhubarb/lemon toggle sits on top. A big sample sentence updates; let the user type their own (like Casa's pangram) and add a "Generate a new one" button that cycles fun lines:
- "Crush on you, fizz forever."
- "Vanilla called, rhubarb answered."
- "Zest friends."

A small 3D can sits beside it and fills with liquid as FIZZ goes up (a simple animated plane inside the can, optional).

### 6. Our range — "Drag to view" (Slight Twist carousel)

- A horizontal, inertial, drag carousel with the custom "DRAG" cursor. Cards tilt in 3D toward the cursor.
- Five cards:
  1. Rhubarb & Vanilla can (alpha render)
  2. Lemon & Vanilla can
  3. Rhubarb six-pack
  4. Lemon six-pack
  5. The pair (`sixpack_pair.webp`)
- Each card shows: the name, an ingredient line, the size (500 ml / 6 × 500 ml) and a "Shop" button.
- Hovering a card floods the section background with that product's colour.

### 7. Six-packs — "Six-packs" (multipack block)

- Warm kraft-coloured section.
- **The six-pack renders are the hero here.** A pinned scroll scene where the rhubarb six-pack slides in, rotates slightly, then cross-fades or flips to the lemon six-pack (use the `_diff` alternate shots as the second angle).
- **Hotspots** on the carton reveal tooltips on hover:
  - "Die-cut logo windows: say hi to the cans inside"
  - "Recyclable kraft board"
  - "Carry handle built in"
  - "6 × 500 ml"
- Copy:
  > Six cans, one carton, zero chill required. Our kraft six-packs wear the Fizzy & Crush melt on the outside and show off the cans through die-cut logo windows. Grab one of each, or go all in on your favourite.
- Lists like Slight Twist's variety pack:
  - **Rhubarb six-pack:** 6 × Rhubarb & Vanilla (6 × 500 ml)
  - **Lemon six-pack:** 6 × Lemon & Vanilla (6 × 500 ml)
- CTA buttons: "Buy the Rhubarb six" / "Buy the Lemon six".
- Prices are placeholders, clearly marked `TODO`.

### 8. Pick your side (Casa weight-list interaction)

- A split screen, blue left and pink right, each with its can render (`*_float_front_alpha.webp`) and a giant name.
- Hovering one side expands it to about 70% width with an elastic ease. Its name grows in weight while the other shrinks and desaturates.
- On mobile it is a tap toggle.
- Centre line text: "Team Rhubarb or Team Lemon?"
- Clicking a side scrolls to that flavour's section.

### 9. Friendship is fizzing (newsletter)

- Pink or cream section with `duo_pattern.webp` as a parallax backdrop.
- Copy: "Get first sips of new flavours, drops and pop-ups." Placeholder offer text marked `TODO`; do not promise a discount.
- Email field and button; on submit, bubbles burst.
- No backend: store submissions in a mock handler, or connect Supabase if available.

### 10. Footer — "Find us"

- Ink background.
- A huge cream wordmark from the SVG that scales with scroll. Its letters wobble on hover, one by one.
- A marquee: "THANK YOU FOR STOPPING BY · STAY FIZZY · ".
- Columns:
  - stockists (placeholder: "hello@fizzyandcrush.com" marked `TODO`)
  - socials (Instagram, TikTok placeholders)
  - legal links (Privacy, Terms, Shipping)
- A tiny line: "500 ml cans · Creamy soda · Made with a crush".

## Quality bar and details

- Generous spacing on a 12-column grid. Headlines run edge to edge. Mix italic and upright words inside headlines, and add little asterisks or superscripts for charm (Casa style).
- Rounded corners everywhere (24–40 px). Buttons are pills.
- Every interactive element has a hover, focus and active state. Keyboard accessible, with a visible focus ring in `--berry`.
- Semantic HTML, alt text on every image, `aria-live` for the flavour switch.
- SEO title: "Fizzy & Crush — Creamy soda with a crush". Meta description from the brand copy. OG image: `duo_pattern.webp`.
- Componentise: `Preloader`, `Cursor`, `Nav`, `CanStage` (the persistent R3F canvas), `Hero`, `Ticker`, `Manifesto`, `FlavourSection`, `TasteTester`, `RangeCarousel`, `SixPacks`, `PickYourSide`, `Newsletter`, `Footer`.
- All copy goes in one `content.ts` so it is easy to edit.
- Do not add an age gate, alcohol language, health claims, fake reviews or fake prices.
