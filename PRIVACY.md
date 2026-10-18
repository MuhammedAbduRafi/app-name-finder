# Privacy Policy: App Name Finder

_Last updated: 18 October 2026_

App Name Finder is an open-source Claude skill. It has no servers, no accounts, and no analytics. The author does not receive, collect or store any data from people who use it.

## What data is sent, and where

To check whether a domain is available, the skill sends **only the candidate domain names being checked** (for example `nimbly.com`) to these public services:

| Destination | Why |
|---|---|
| `data.iana.org` (IANA) | Downloads the public list of registry lookup (RDAP) servers. No domain names are sent here. |
| The official RDAP server of each domain ending checked, e.g. Verisign (`.com`, `.net`), Google Registry (`.app`, `.dev`), Identity Digital (`.io`) | Asks whether the domain is registered. |
| Your device's DNS resolver | A fallback check of whether the domain is in use. |

Claude may also run ordinary web searches on finalist names to spot existing apps with the same name. Those searches go through Claude's own web search tool and are covered by Anthropic's privacy policy.

## What is not sent

The skill does not send your app idea, your answers to its questions, your conversation, your name, email or any other personal information to any of the services above. It uses no API keys or cookies.

## Storage

The skill stores nothing. Results exist only in your Claude conversation.

## Third parties

Domain registries operate under their own privacy policies. Use of Claude is governed by [Anthropic's Privacy Policy](https://www.anthropic.com/legal/privacy).

## Contact

Questions or concerns: open an issue at https://github.com/MuhammedAbduRafi/app-name-finder/issues
