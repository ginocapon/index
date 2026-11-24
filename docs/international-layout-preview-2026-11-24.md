# Righetto International layout preview, 24 November 2026

Prepared from public main c7efc7f (23 November 2026). Final rounded-button preview approved for publication by Gino on WhatsApp, 24 November 2026 at 18:12 CET.

Scope: 14 English International layout pages, one language chooser, six local image assets plus isolated CSS/JS, and entry links on the existing Italian home. The Italian home keeps its sections, background, brand and photographs. Desktop navigation spacing is reduced to fit the new entries. Mobile language entry remains beside, not over, the menu button.

Every new HTML document has robots noindex,nofollow in the initial head. No sitemap, robots.txt, workflow, admin or database change. No claim that noindex makes the pages private. No live catalogue feed. Contact form is a demonstration and never submits. Other languages are marked planned.

Verification before publication: all 15 new views rendered at 320, 390 and 1280 CSS px, no horizontal overflow; internal URL targets exist; language search empty/reset verified. Final desktop and phone home screenshots approved. Live deployment checks follow the push. Home screenshots compared separately.

Deployment pipeline: existing .github/workflows/static.yml deploys pushes on main. Its sync_og_immobili.py script reads active properties with HTTP GET and writes only generated files to the deployment artifact; no Supabase write is present in that script. Do not manually run any Supabase workflow for this release.

Release procedure after user approval: fetch current main and reconcile changes; create backup branch/tag at exact pre-release head; commit only index.html, international/ and this log; push once; monitor the Pages workflow; inspect live home, chooser and all 14 routes, status codes, source noindex, images and mobile navigation. Record commit and workflow URL in follow-up.

Rollback: revert only this release commit on latest main and redeploy. Do not reset main or restore unrelated files. Verify the original Italian navigation returns and new routes are absent. No database rollback is needed. The private prototype is unaffected.
