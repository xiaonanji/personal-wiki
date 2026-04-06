# Implement Skill Loader Component

This file is an implementation instruction for Codex or another coding agent.

Your task is to add a **skill loader component** to the target agent project. The component must follow the common Agent Skills model: discover skills, parse `SKILL.md`, expose a lightweight catalog, and load full instructions only when needed.

Do not assume a specific framework or language until you inspect the repository. Adapt the design to the existing codebase conventions.

## Goal

Implement a reusable skill-loading subsystem that allows the agent to:

1. discover installed skills
2. parse and validate `SKILL.md`
3. expose a lightweight skill catalog to the model
4. load full skill instructions on activation
5. resolve skill-relative resources correctly
6. support progressive disclosure so only relevant skill content enters context

## First Step

Before writing code:

1. inspect the repository structure
2. find the current agent bootstrap/session initialization flow
3. find where prompts, tool definitions, context assembly, and file access are implemented
4. identify the best module boundary for a new skill loader
5. identify whether the model already has file-read capability or whether a dedicated skill activation tool is required

Do not start coding until you understand those integration points.

## Functional Requirements

### 1. Skill discovery

Implement discovery for skill directories that contain a file named exactly `SKILL.md`.

Support these scopes when they fit the host agent:

- project-level client directory: `<project>/.<client-name>/skills/`
- project-level shared directory: `<project>/.agents/skills/`
- user-level client directory: `~/.<client-name>/skills/`
- user-level shared directory: `~/.agents/skills/`

If the host project already has an established config convention, integrate with that convention instead of forcing a new one.

Discovery rules:

- scan only for directories containing `SKILL.md`
- ignore obvious junk directories such as `.git`, `node_modules`, build output, caches
- impose sane scan limits to avoid runaway filesystem traversal
- produce deterministic results

### 2. Trust model

Project-level skills may come from untrusted repositories.

If the host project already has a concept of trusted workspaces, integrate with it and gate project-level skill loading behind that trust mechanism.

If no trust mechanism exists:

- keep the implementation safe and explicit
- at minimum, structure the code so trust checks can be added later
- document the security implication clearly

### 3. Parse `SKILL.md`

Each skill is anchored by `SKILL.md` with:

- YAML frontmatter
- markdown body

Parse and extract at minimum:

- `name`
- `description`
- `location` or equivalent source path
- `base directory`
- body content

Validation rules:

- `name` and `description` are required for a skill to be usable
- if YAML is completely unreadable, skip the skill and surface a diagnostic
- if there are recoverable formatting issues, be lenient where practical

Examples of lenient behavior:

- tolerate common malformed YAML patterns if the fix is safe and obvious
- warn on non-critical format mismatches instead of rejecting the skill immediately

### 4. Canonical skill registry

Implement an in-memory registry keyed by skill name.

Each skill record should contain at least:

- `name`
- `description`
- absolute `skillMdPath`
- `baseDir`
- parsed frontmatter
- body text or a lazy loader for body text
- scope/source information such as `project`, `user`, or `built-in`

The registry must support:

- listing all available skills
- looking up one skill by name
- reporting diagnostics for skipped or shadowed skills

### 5. Name collisions and precedence

When two skills share the same `name`, resolve deterministically.

Default precedence:

1. project-level skill
2. user-level skill
3. built-in or bundled skill

Within the same scope, use a deterministic tie-breaker and document it.

Also:

- emit a warning or diagnostic when one skill shadows another
- do not allow nondeterministic selection

### 6. Progressive disclosure

The implementation must follow progressive disclosure:

- Tier 1: expose only a skill catalog at session start
- Tier 2: load full `SKILL.md` only when a skill is activated
- Tier 3: load referenced files only when the instructions call for them

Do not eagerly inject every installed skill into the model context.

### 7. Skill catalog output

Provide a way for the agent runtime to generate a lightweight catalog for model disclosure.

Each catalog entry should include:

- skill `name`
- skill `description`
- activation reference, such as path or skill name

The catalog should be small enough to include at session start.

### 8. Skill activation

Support activation through whichever mechanism matches the host project:

- file-read activation if the model can directly read files
- dedicated activation tool if the model cannot read files directly or if the codebase already uses tool-mediated content loading

Activation result must include:

- full skill instructions
- enough metadata to resolve relative resource paths

If the project uses a dedicated activation tool, return structured data rather than raw untyped text when practical.

### 9. Relative resource resolution

When a skill refers to paths like `scripts/foo.py` or `references/bar.md`, resolve them relative to the skill base directory.

Provide a helper for:

- resolving a relative path safely
- rejecting escapes outside the skill directory when required by the host security model

### 10. Context retention

If the host agent has context compaction or pruning, make it possible to preserve activated skill instructions so they do not disappear silently mid-session.

At minimum:

- mark skill content clearly in the data model
- structure the integration so future compaction logic can detect and preserve loaded skills

### 11. Deduplication

If a skill is already active in the current session, avoid injecting it repeatedly unless the implementation explicitly wants a refresh.

Track activation state per session or conversation if that concept exists in the host project.

## Implementation Requirements

### Design constraints

- follow existing repo conventions
- prefer small, composable modules
- avoid unnecessary dependencies
- keep the loader separate from UI or prompt rendering concerns
- make the core skill loader testable without the full agent runtime

### Suggested component boundaries

Adapt naming to the target language, but the implementation should roughly separate:

- discovery
- parsing
- registry/state
- activation/loading
- formatting for model disclosure

### Suggested public API

Adapt the exact interface to the codebase, but the component should offer equivalents of:

- `discoverSkills(...)`
- `listSkills()`
- `getSkill(name)`
- `loadSkill(name)`
- `buildSkillCatalog()`
- `resolveSkillResource(name, relativePath)`
- `getDiagnostics()`

If the codebase uses classes, services, or dependency injection, fit the API to those patterns.

## Testing Requirements

Add tests that cover at least:

1. discovery of valid skill directories
2. skipping directories without `SKILL.md`
3. parsing valid frontmatter and body
4. rejecting or warning on malformed skill files
5. precedence behavior for duplicate names
6. activation returning full instructions
7. correct relative-path resolution from the skill directory
8. catalog output containing only lightweight metadata

If the project has existing integration or end-to-end tests, add one small integration test showing that the agent can see a skill in the catalog and load it when requested.

## Documentation Requirements

After implementation:

1. document where skills are discovered from
2. document how activation works
3. document any trust assumptions
4. document how to add a new skill
5. document any environment-specific limitations

If the project has an existing docs or README location, update it instead of creating redundant docs.

## Acceptance Criteria

The task is complete only when all of the following are true:

- the agent can discover skills from supported directories
- the agent can parse `SKILL.md` files into a usable registry
- the model can be shown a lightweight skill catalog
- the agent can load full skill instructions on demand
- referenced resource paths resolve relative to the skill directory
- collisions are resolved deterministically
- tests are added or updated
- documentation is updated

## Output Format

When you finish the implementation:

1. summarize the design you chose
2. list the files you changed
3. explain any assumptions or unresolved tradeoffs
4. mention any follow-up work that would improve safety or ergonomics

## Notes

- Do not implement a toy version that hardcodes one skill path unless the repository is intentionally minimal.
- Do not eagerly load all skill bodies into model context.
- Do not bypass existing trust or permission systems if the host project already has them.
- Prefer compatibility with the common `SKILL.md`-based skill standard and `.agents/skills/` interoperability.
