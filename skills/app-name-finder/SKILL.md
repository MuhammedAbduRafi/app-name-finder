---
name: app-name-finder
description: Find a name for an app, startup, SaaS, product or side project and check which domains are actually available. Use whenever the user shares an app idea and wants a name, brand name, or domain — e.g. "what should I call my app", "name ideas for my startup", "find me a domain for X", "is getX.com taken", or "help me brand this idea" — even if they never say "domain".
---

# App Name Finder

Turn an app idea into a short list of strong names that each come with a domain the user can register today. A name with no available domain is mostly useless to someone about to launch, so availability is part of the answer, not an afterthought.

## 1. Understand the idea (briefly)

Read what the user gave you. If it already covers what the app does and who it's for, skip straight to step 2 and state your assumptions in one line. Otherwise ask a single round of up to 4 short questions — use the AskUserQuestion tool if you have it (multiple-choice is fastest for the user), otherwise ask in plain text. Pick only the questions whose answers would actually change the names:

- **Core job & audience** — what problem it solves and for whom (consumers, developers, businesses, a niche like teachers or gym owners).
- **Tone** — playful, premium, trustworthy/serious, techy, friendly/human.
- **Name style** — descriptive (says what it does), invented/brandable (like Spotify), real-word metaphor (like Notion), or no preference.
- **Domain rules** — must it be .com, or are .app / .io / .ai / .co / country TLDs fine? Prefixes like "get" / "try" OK?
- Optional: markets/languages to watch for bad meanings, words to include or avoid, names they already like.

Don't interrogate. One round, then proceed — the user can steer after seeing names.

## 2. Brainstorm wide, then cut hard

Privately generate ~40 candidates across several styles so the shortlist isn't all one flavor:

- **Descriptive / compound** — two plain words joined (Dropbox, Mailchimp).
- **Metaphor / evocative** — a real word that suggests the feeling or outcome (Slack, Notion, Asana).
- **Invented / blended** — portmanteaus or coined words (Pinterest, Spotify, Zillow).
- **Altered real word** — dropped vowel, -ly/-io/-ify, or a swapped letter (Tumblr, Grammarly). Use sparingly; they're harder to spell when heard.
- **Foreign or root words** — Latin/Greek/Sanskrit/etc. roots tied to the idea (Strava, Veritas).

Cut anything that fails these, because each one costs the user later:
- Over ~3 syllables or ~10 letters (hard to remember, type and fit on an icon).
- Can't be spelled after hearing it once (word-of-mouth breaks).
- Hyphens or digits.
- Too close to a well-known brand, especially in the same category (trademark risk, confusion).
- Negative or awkward meaning in English or the user's stated markets.
- Generic to the point of being unownable ("TaskApp").

Keep ~15–20 survivors to check.

## 3. Check domain availability

Check the preferred TLD (default .com) for every survivor, plus 1–2 secondary TLDs the user accepted. When a great name's .com is taken, try a few close variants before discarding it: `get<name>.com`, `try<name>.com`, `<name>app.com`, `<name>hq.com`, or the .app/.io version.

Use the first method that works:

**A. Bundled script (best).** If you can run shell commands with network access, run the script in this skill's `scripts/` folder:
```
python scripts/check_domains.py --names name1,name2,name3 --tlds com,app,io
python scripts/check_domains.py getname2.com name3app.com      # exact domains
```
It asks each TLD's official registry via RDAP (the modern WHOIS) and prints TAKEN / AVAILABLE / UNKNOWN. Exit code 2 means it had no network at all — move to method B.

**B. Fetch RDAP directly.** If you have a web-fetch tool, fetch the registry's RDAP URL for each domain. A registered domain returns a record (registration date, registrar); an unregistered one returns HTTP 404, which fetch tools usually report as an error. Treat "error/404" as *likely available* and a returned record as *taken*. Working endpoints:
- .com → `https://rdap.verisign.com/com/v1/domain/NAME.com`
- .net → `https://rdap.verisign.com/net/v1/domain/NAME.net`
- .app / .dev → `https://pubapi.registry.google/rdap/domain/NAME.app`
- .io → `https://rdap.identitydigital.services/rdap/domain/NAME.io`

Because a fetch tool may report every failure the same way, first fetch one known-registered domain on the same endpoint (e.g. `google.com`, `web.dev`, `github.io`) as a control. If the control returns a record, errors on your candidates mean "not found" → likely available. If the control fails too, that endpoint isn't reachable — use method C for that TLD. Other TLDs (.ai, .co, …) often block fetch tools; treat them as unverified unless method A worked.

**C. Can't verify.** If neither works (or a TLD can't be checked), say so plainly, mark those domains "unverified", and give the user a one-click check link like `https://www.namecheap.com/domains/registration/results/?domain=NAME.com`. Never present an unchecked domain as available — that's the one mistake that makes this whole exercise worthless.

Run checks in batches (several fetches in parallel) rather than one at a time.

## 4. Quick conflict scan for the finalists

For your top 3–5, if you have web search, do one quick search each (e.g. `"Name" app`) to catch an existing app or company with the same name in the same space. Mention anything you find. This is a sanity check, not a trademark search — say so once.

## 5. Present the shortlist

Lead with the shortlist; keep the prose tight. Use this shape:

**Top pick: Name — name.com ✅**
One or two sentences on why it fits this idea and audience.

| Name | Domain | Status | Style | Why it works |
|---|---|---|---|---|
| Name | name.com | ✅ available | Invented | … |
| Other | getother.com | ✅ available (.com taken) | Metaphor | … |
| … | other.app | ⚠️ unverified | … | … |

Aim for 5–8 names, each with at least one available (or clearly-flagged unverified) domain. Then add, briefly:
- A few strong names you liked whose domains were all taken (the user may want to buy one or use a different TLD).
- Caveats in one line: availability can change within hours, so register soon; RDAP doesn't reveal "premium" pricing, so confirm the price at a registrar; run a proper trademark search (e.g. USPTO, WIPO, or the user's national office) before committing.
- Offer to iterate: more in a style they liked, different TLDs, or a deeper check on one favorite (social handles, app-store name).

## Iterating

When the user reacts ("I like the second one's vibe", "too playful", "must be .com"), treat it as new constraints: generate a fresh batch in that direction, re-check domains, and present a new short table. Don't repeat names already rejected.
