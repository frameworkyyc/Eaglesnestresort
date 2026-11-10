# Eagle's Nest Resort website (feature/wilderness-redesign)

Static site built with [Eleventy](https://www.11ty.dev/). The branch deploys to https://eaglesnest.frameworktools.ca
(preview, noindex). Production (eaglesnestresort.ca) is a separate deployment and is not affected by this branch.

## Layout
- `src/` source: `index.njk` (homepage), `_includes/` layout and partials, `_data/site.js` (facts used site-wide),
  `styles/` (tokens, base, components, home), `scripts/main.js`, `art/` (web illustrations), `photos/` (real photographs).
- `art-masters/` full-resolution illustration originals plus provenance (never edit; re-export from them).
- `legacy/` the previous site. Pages not yet rebuilt are copied as-is into the output, so every link keeps working.
- `public/` build output. It is committed so the Worker can deploy it without a build step.

## Commands
- `npm install` then `npm run build` rebuilds CSS, JS, images and pages into `public/`. Commit the result.
- `npm start` serves a live-reloading copy.
- Set `ELEVENTY_ENV=production` for a production build: removes the noindex header/meta and publishes a real robots.txt.

## Design system
Tokens in `src/styles/tokens.css`; reusable pieces (buttons, plates, chips, header, footer) in `components.css`.
Rules: all meaningful content is HTML text; illustrations are decorative (`alt=""`); real photographs keep descriptive alt text;
animation only runs on-screen and stops for `prefers-reduced-motion` and the footer "Quiet mode" switch.
