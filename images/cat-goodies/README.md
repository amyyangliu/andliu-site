# Cat scene goodies

Three transparent pixel art assets for the contact-page cat scene:

- `sushi-roll.png` / `.svg`
- `cake-slice.png` / `.svg`
- `golf-ball.png` / `.svg`

Each sprite is drawn on a 24 × 24 grid. PNGs are 144 × 144 pixels with
transparency; SVGs preserve the original grid. Colors reuse the cat's cream,
pink, gray, and the site's coral, with the signpost's green accent.

For a crisp match with the cat, display PNGs at a multiple of 24 CSS pixels
and set `image-rendering: pixelated`. The SVGs use `shape-rendering="crispEdges"`.
Run `python3 generate.py` in this folder to regenerate the assets.
