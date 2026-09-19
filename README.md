# Code Review Guild

Code Review Guild is a skill-first plugin repository for principle-based code review and behavior-preserving code simplification. The core product is a shared `skills/` library for `DRY`, `KISS`, `YAGNI`, `SoC`, `SOLID`, a consolidated `all-principles` review, and the general `code-simplifier` workflow. Harness-specific packaging for Claude, Codex, Cursor, and GitHub Copilot is layered on top of those skills.

## Support model

Supported harnesses:

- Claude: packaged as a Claude Code plugin bundle, but loaded through Claude's plugin mechanisms rather than automatic pickup from a copied folder
- Codex: packaged as a Codex plugin bundle using the shared skills as source of truth
- Cursor: packaged as a local Cursor plugin under `~/.cursor/plugins/local/...`
- GitHub Copilot: project-scaffolded into `.github/` custom instructions and prompt files rather than installed as a plugin

Compatibility status:

- Claude: native plugin format, docs-aligned explicit loading required
- Codex: native skill/plugin packaging, public install flow is less explicitly documented
- Cursor: native local plugin install
- GitHub Copilot: native repository customization files, not plugin bootstrap

Automatic bootstrap is intentionally narrow. It exists to expose Code Review Guild’s review skills at session start where the harness supports it. This repo does not import the broader Superpowers workflow catalog.

## Public skill catalog

- `code-simplifier`: review recently changed code and apply safe maintainability simplifications without behavior or API drift
- `review-dry`: harmful duplication only
- `review-kiss`: unnecessary complexity only
- `review-yagni`: speculative design only
- `review-soc`: separation of concerns only
- `review-solid`: practical SOLID issues only
- `review-all-principles`: consolidate the five principle reviews into one final report

The bootstrap skill `using-code-review-guild` is internal support plumbing. It exposes the review skills and the report contract, but it is not part of the public review surface.

## Report contract

Every review writes into the target project’s `docs/reviews/` directory using these canonical filenames:

- `docs/reviews/latest-dry-review.md`
- `docs/reviews/latest-kiss-review.md`
- `docs/reviews/latest-yagni-review.md`
- `docs/reviews/latest-soc-review.md`
- `docs/reviews/latest-solid-review.md`
- `docs/reviews/latest-principles-review.md`

Every report must include:

- `## Scope`
- `## Summary`
- `## Must fix`
- `## Should consider`
- `## Acceptable tradeoff`
- `## Not a problem`
- `## Reusable project observations`

The example reports in `examples/python/reports/` remain the reference shape.

## Repository structure

```text
skills/                 Source of truth for reviewer behavior
hooks/                  Session-start bootstrap assets
agents/                 Thin harness wrappers around the skills
commands/               Thin command wrappers around the skills
.claude-plugin/         Claude-facing packaging metadata
.codex-plugin/          Codex-facing packaging metadata
.cursor-plugin/         Cursor-facing packaging metadata
integrations/           Remaining harness-specific assets, including Copilot prompts
docs/                   Harness-specific install and usage docs
examples/python/        Imperfect demo project and canonical report examples
tests/                  Repo integrity tests for the skill/plugin architecture
```

## Installation

Use the harness-specific installers for the integration model you need:

```bash
./install/install-claude.sh
./install/install-codex.sh
./install/install-cursor.sh
./install/install-copilot-vscode.sh --dest /path/to/your-project
```

All installers:

- accept `--dest PATH`
- refuse to overwrite an existing destination unless `--force` is passed, or for Copilot refuse to overwrite existing target files unless `--force` is passed
- add only the harness-specific assets relevant to that install target

Harness-specific behavior:

- `Claude`: prepares a plugin bundle. Load it with `claude --plugin-dir <path>` for local use, or install it through Claude's plugin configuration flow.
- `Codex`: prepares a Codex-oriented plugin bundle containing `.codex-plugin/`, `skills/`, and command wrappers.
- `Cursor`: installs a local plugin bundle under `~/.cursor/plugins/local/code-review-guild` by default.
- `GitHub Copilot`: scaffolds `.github/copilot-instructions.md` and `.github/prompts/*.prompt.md` into the target project.

PowerShell equivalents are provided next to each shell script.

## Session-start bootstrap

Where supported, the session-start bootstrap loads the narrow Code Review Guild context:

- `using-code-review-guild`
- canonical report destinations
- the six review entrypoints

The bootstrap message lives in `hooks/session-start.md` and is emitted by `hooks/session-start.sh`. Cursor also includes explicit hook wiring through `hooks/hooks-cursor.json`.

## Harness docs

- [Claude setup](docs/README.claude.md)
- [Codex setup](docs/README.codex.md)
- [Cursor setup](docs/README.cursor.md)
- [GitHub Copilot setup](docs/README.copilot.md)

## Example workflow

1. Install the package for the harness you use.
2. Load or enable the installed package using the harness-native mechanism for that tool.
3. Run one focused review such as `review-dry`.
4. Write the report to `docs/reviews/latest-dry-review.md`.
5. After the five focused reviews exist, run `review-all-principles` to write `docs/reviews/latest-principles-review.md`.

## Limitations

- GitHub Copilot support is prompt-oriented rather than true session-start bootstrap.
- Codex support uses native packaging conventions, but this repo does not claim a stronger public install guarantee than OpenAI currently documents.
- The repo ships judgment-based review skills, not AST or static-analysis tooling.
- The legacy `core/` and `integrations/` files may remain as compatibility/reference material, but `skills/` is the behavioral source of truth.

## Contributing

Edit the `skills/` content first.

When changing behavior:

- update the relevant `skills/*/SKILL.md`
- keep wrappers in `agents/`, `commands/`, and plugin manifests thin
- preserve the canonical report filenames and section schema
- update harness docs if the installation or invocation story changes
- run `python3 -m unittest tests/test_repo_integrity.py -v`
