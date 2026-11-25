# Spike: iPhone test bench (chantier E)

Static PWA that checks, on a real iPhone 14, what the PRD needs from the browser:
GPS in the foreground, Wake Lock (and its return after the app comes back), French
voices and `boundary` events, sound unlock by a tap, and OPFS storage of 14 MB
(the size of the corridor PMTiles), read back in airplane mode.

The report button copies results only: accuracy, counts, durations. No position,
no personal data.

Hosting: temporary GitHub Pages site from the `gh-pages` branch, for this test only.
It is turned off after the test. Final hosting is still open (Cloudflare, Supabase
or Vercel).

Local run: `python -I -m http.server 8080` from this folder (GPS and install need
HTTPS, so the real test runs on the Pages URL).

Result and decision: `docs/adr/0009-banc-iphone.md` (after the test).
