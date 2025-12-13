# Ontos Agent Instructions

## Commands

### "Ontos" (Activate)
1. Check for `Ontos_Context_Map.md`
2. If missing: `python3 .ontos/scripts/ontos_generate_context_map.py`
3. Read map, identify relevant IDs for user's request
4. Read ONLY those files
5. Respond: "Loaded: [id1, id2]"

### "Archive Ontos" (End Session)
1. Run: `python3 .ontos/scripts/ontos_generate_context_map.py`
2. Run: `python3 .ontos/scripts/ontos_end_session.py "slug" -s "Your Name" -e <type>`
3. Read generated log, fill placeholders (Goal, Decisions, Changes, Next Steps)
4. Commit

Event types: `feature`, `fix`, `refactor`, `exploration`, `chore`

**Pre-push blocking:** Push fails without archived session. Run Archive Ontos first. Emergency: `git push --no-verify`

### "Maintain Ontos" (Weekly)
1. `python3 .ontos/scripts/ontos_migrate_frontmatter.py`
2. `python3 .ontos/scripts/ontos_generate_context_map.py`
3. Fix any errors, commit map

### "Update Ontos"
1. `python3 .ontos/scripts/ontos_update.py`

## Type Hierarchy

| Type | Rank | Depends On |
|------|------|-----------|
| kernel | 0 | nothing |
| strategy | 1 | kernel |
| product | 2 | kernel, strategy |
| atom | 3 | kernel, strategy, product, atom |
| log | 4 | uses `impacts`, not `depends_on` |

Rule: Dependencies flow DOWN (atom → product → strategy → kernel).

## Validation Errors

| Error | Fix |
|-------|-----|
| `[BROKEN LINK]` | Create referenced doc or remove from depends_on |
| `[CYCLE]` | Remove one dependency in the loop |
| `[ORPHAN]` | Add to another doc's depends_on |
| `[ARCHITECTURE]` | Lower-rank can't depend on higher-rank |

## Changelogs

- `Ontos_CHANGELOG.md` — Only for Ontos tooling changes
- `CHANGELOG.md` — For project using Ontos (use `--changelog` flag)

## Context Selection

1. Start with IDs matching user's request
2. Follow `depends_on` chains upward
3. Stop at kernel or sufficient context
4. Prefer fewer, more relevant docs
