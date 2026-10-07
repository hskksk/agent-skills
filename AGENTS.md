# AGENTS.md

Catalog of [Agent Skills](https://agentskills.io/specification) under `skills/`, installable via [skills.sh](https://skills.sh). Discovery artifacts are built in CI; releases are automated on `main` (see [README.md](README.md)).

Skill prose and references may be Japanese. **Commit messages, PR titles, PR bodies, CI workflow text, and other repo automation must use English** and [Conventional Commits](https://www.conventionalcommits.org/) so [semantic-release](https://semantic-release.gitbook.io/) can semver the catalog.

## Development

```bash
npm ci --ignore-scripts
node scripts/build-discovery-index.mjs https://example.com/skills
```

Do not commit `dist/`; release workflow attaches it to GitHub Releases.

## Commits and PR titles

Releases use semantic-release with [@semantic-release/commit-analyzer](https://github.com/semantic-release/commit-analyzer). Config matches [hskksk/gh-actions](https://github.com/hskksk/gh-actions) (see [`.releaserc.json`](.releaserc.json)).

**Merging to `main`:** use **merge commit** or **rebase and merge**, not squash. semantic-release reads each commit on `main`; squash titles hide `feat` / `fix` commits that lived only in the PR body.

Pull requests are checked by the [Conventional Commits](.github/workflows/conventional-commits.yml) workflow: valid **PR title** and **every commit** in the PR must follow Conventional Commits.

### Format

```
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

Examples:

```
feat: add japanese-writing skill
fix(japanese-writing): align SKILL.md with references
docs: document metadata.version release flow
ci: validate PR titles for conventional commits
chore: bump yaml dependency
```

Rules:

- Use the imperative mood (`add`, not `added` / `adds`).
- Keep the subject line ≤ 72 characters; no trailing period.
- Scope is optional; use a skill id (`japanese-writing`) or area (`ci`, `discovery`, `release`) when it helps.
- Reference issues in the footer when useful: `Fixes #123`.

### Version bump mapping (this repo)

Configured in [`.releaserc.json`](.releaserc.json). Repo tag `v*.*.*` drives GitHub Release and, for changed skills, `metadata.version` in `SKILL.md`.

| Prefix / signal | Release |
| --- | --- |
| `feat:` | **minor** |
| Any other conventional commit (`fix:`, `perf:`, `refactor:`, `docs:`, `chore:`, `ci:`, `test:`, …) | **patch** (catch-all rule) |
| `BREAKING CHANGE:` in footer, or `!` after type/scope (e.g. `feat!:`) | **major** |

Use `feat:` for new skills or user-visible skill behavior changes. Use `fix:` for corrections to skill content or packaging. Non-feature work still triggers at least a patch release here.

### Breaking changes

Prefer an explicit footer:

```
feat!: remove deprecated skill layout

BREAKING CHANGE: skills must live only under skills/<name>/SKILL.md
```

Or the shorthand form: `feat!: remove deprecated skill layout`.

### What to avoid

- Vague subjects: `update`, `fix stuff`, `WIP`.
- PR titles that do not start with a recognized type when the change should ship in the next release.
- Mixing unrelated changes under one `feat:` / `fix:` — split PRs when release notes would be misleading.
- Editing `metadata.version` by hand in `SKILL.md` for release purposes — release bumps it for skills changed since the last tag.
