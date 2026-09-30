# SpicyChat AI Club

Independent, static editorial guide for adults. The site uses the images supplied in `spicychat-ai-club.zip` and is designed for Cloudflare Pages.

## Updating content

Edit `build.py`, then run `python3 build.py`. All HTML pages, `sitemap.xml`, and `robots.txt` are generated from the same page list, then copied to `dist/` with public assets. Pricing is deliberately linked to the official subscription page because displayed prices may vary by date and region.

Promotional buttons currently point to the Playbox affiliate URL `https://www.playbox.com/?ref=eushing`. Set `SPICYCHAT_DESTINATION` when building to use a different approved referral URL. This must be a full HTTPS URL. The build script marks referral links as sponsored and labels Playbox buttons clearly.

## Deployment

Run `python3 build.py && npx --yes wrangler@4.136.2 deploy`. The GitHub Actions workflow does this automatically on pushes to `main`.
