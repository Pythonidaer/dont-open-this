# freeCodeCamp News Explorer

A searchable personal-learning catalog of English-language freeCodeCamp News, adapted from the private Sites version. This is an independent project, not affiliated with or endorsed by freeCodeCamp.

## Deployments

- Private QA Site: https://fcc-news-explorer-johnny.codefolio-work.chatgpt.site
- GitHub Pages publishes `dist/` on pushes to `main`, using `.github/workflows/deploy-pages.yml`.
- Article title links open the original freeCodeCamp article in a new tab. Topic labels filter the catalog instead.

## Sites as QA, GitHub Pages as production

The two deployments are separate. Changes made in Sites do not automatically update GitHub Pages, and GitHub changes do not automatically update Sites.

1. Make and publish a fix to the existing private Site.
2. Check it in Sites. Test mobile layout and search/filter behavior; also check external links in an ordinary browser, since ChatGPT's embedded view may handle new tabs differently.
3. From this repository, copy the reviewed Site checkout:

   ```sh
   python3 scripts/promote-from-site.py /absolute/path/to/site-checkout
   python3 scripts/prepare-data.py
   node --check dist/app.js
   ```

4. Review the diff. The promotion script copies only `dist/` and the inventory record; it never transfers the Site's hosting manifest, credentials, or Git metadata. It does not commit or publish.
5. Commit and push the reviewed version to `main` to deploy GitHub Pages. Verify the Actions run and the live page after publication.

A private Site is a useful QA deployment, not a full replica of GitHub Pages hosting. Check path handling and external links on Pages as well. Keep a change out of GitHub `main` until it is ready for production.

## Verified snapshot

October 28, 2026: **13,118 unique English News sitemap URLs**, each matched to metadata from **525 public listing pages**. The collection includes **1,259 primary-topic labels** and listing publication dates spanning **2013–2026**.

All records contain titles and publication dates. The public listings omit an author credit for 6,668 records and a primary topic for 235; these remain missing. Primary topics are the labels exposed by listing cards, not a complete per-article tag inventory. Broad categories are our own overlapping keyword groupings, not freeCodeCamp's official taxonomy.

This count verifies the sitemap/listing inventory, not the current availability or editorial uniqueness of every article. Article bodies and images are not republished. `INVENTORY.json` records the source scope and collection counts.

The initial production assets are copied unchanged from Site source commit `446dbc5e93d49754482ecf07fa24646cb82abeec`. The uncompressed article JSON has SHA-256 `20590888e40a74a2f9e1d3754c2999758eacfab947f5c8b8275ae0ee7b914ebe`.

## Local preview and data

No framework or dependency installation is required:

```sh
python3 scripts/prepare-data.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/. Asset links and filters work under the GitHub Pages repository subpath.

`data/articles.json.gz` preserves the reviewed metadata compactly. `scripts/prepare-data.py` restores the exact JSON to `dist/articles.json` before deployment; the browser receives ordinary JSON, with no client decompression requirement. The generated file is ignored by Git.

`collect.py` documents the original collection process using public sitemap/listing pages, four workers, caching, bounded timeouts, and a stop on 403/429. It is a manual refresh tool, not an automatic recurring sync. Inspect and reconcile any refreshed inventory before publication.

## Typography and checks

Typography follows the freeCodeCamp study at https://pythonidaer.github.io/can-i-case-study-generate-websites/: Lato headings, 18px/27px reading text, 19.8px listing titles, 14px metadata, and system sans-serif section headings. Responsive sizes are catalog adaptations, not measured freeCodeCamp mobile values. Self-hosted Lato regular/bold fonts retain the SIL OFL in `dist/fonts/OFL.txt`.

The original Site passed desktop search, category/topic/year filtering, sorting, pagination, reset/empty state, filter URL restoration, dialog focus/close/Escape, and overflow checks. Mobile styling is implemented; the available browser did not support viewport resizing for visual mobile QA. This transfer additionally validates byte equality with the reviewed Site, JSON reconciliation, JavaScript syntax, local asset paths, and deployment behavior.

## Category-scoped topics

Promoted from reviewed Site commit `6cb436190c08c08eb286ed803f9734c86d44ee03`. Selecting a category narrows Topic options and counts to that category, independently of search and year filters. Valid topic selections stay; unavailable topics reset to All topics and are removed from the URL. Reset filters restores all 1,259 topics.

Desktop browser QA verified Security (114 topics), Frontend (390 topics), scoped counts matching results, valid selection retention, invalid selection reset, and full reset. Mobile visual QA remains limited as described above. JavaScript syntax and unchanged article-data checksum were checked during promotion.
