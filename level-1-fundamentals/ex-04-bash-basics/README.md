# Ex-1.4 — Structured Bash Script

**Level:** 1
**Estimated time:** 1h
**Track:** Bash → basics

---

## Goal

A Bash script that scans a directory for files with a given extension, lists them,
and reports their count and total size. Mirrors the kind of pre-deploy checks and
cleanup scripts common in CI/CD pipelines.

---

## Concepts covered

- Positional arguments: `$1`, `$2`, `$#`
- Functions in Bash: declaration, `local` variables, return codes
- `usage()` pattern for self-documenting scripts
- `set -e`: abort on first error
- Directory validation with `[ ! -d ]`
- `find` vs `ls` for safe file listing
- `stdout` vs `stderr`: errors on `>&2`, data on `stdout`
- Exit codes `0` / `1` and their role in CI/CD
- Robust size reporting with `xargs du -ch`
- Optional argument handling with `${3:-}`
- Interactive confirmation with `read`

---

## Folder structure

```
ex-1.4/
├── solution.sh
└── data/
    ├── deploy-2024-01-15.log
    ├── deploy-2024-01-16.log
    ├── deploy-2024-01-17.log
    ├── session_abc123.tmp
    ├── cache_xyz789.tmp
    ├── build_001.tmp
    ├── instances.csv
    └── costs.csv
```

---

## Instructions

**Input:** a directory path and a file extension (e.g. `.log`, `.tmp`).

The script must:

1. Show a `usage()` message on `stderr` and exit 1 if fewer than 2 arguments are provided.
2. Validate that the first argument is an existing directory (`check_dir`); exit 1 on failure.
3. List matching files, their count, and total size (`analyze`).
4. If a third argument `--delete` is passed, prompt for confirmation then delete the files.

---

## Functions to implement

```bash
# Print usage to stderr and exit 1.
usage()

# Verify $1 is an existing directory; print error to stderr and exit 1 if not.
check_dir() { local dir="$1"; ... }

# List files matching $2 in $1, print count and total size.
analyze() { local dir="$1"; local ext="$2"; ... }

# Print a yes/no prompt; return 0 on y/Y, 1 otherwise.
confirm() { local prompt="$1"; ... }

# Delete files matching $2 in $1 after confirmation.
delete_files() { local dir="$1"; local ext="$2"; ... }
```

---

## Constraints

- `set -e` on the first line after the shebang
- Error messages on `stderr` (`>&2`), normal output on `stdout`
- One responsibility per function
- Script must be executable (`chmod +x`)
- Use `find` to list files — never `ls` inside a script
- Size must be computed with `xargs du -ch | tail -1` — not by parsing `du` output with `awk`

---

## Expected output

```
$ ./solution.sh data .log
Analyzed directory : data
Extension          : .log

Files found:
  deploy-2024-01-15.log
  deploy-2024-01-16.log
  deploy-2024-01-17.log

Total: 3 file(s)
Size : 4.0K

$ ./solution.sh data .tmp --delete
Analyzed directory : data
Extension          : .tmp
...
Delete all .tmp files in data? [y/N] y
Deleted.

$ ./solution.sh
Usage: ./solution.sh <directory> <extension>  (e.g. ./solution.sh ./data .log)
Provide a directory to scan and the file extension to search for.
# exits with code 1
```

---

## Key takeaways

1. **`stderr` vs `stdout` is not optional in CI.** Pipelines (`|`, `&&`, `||`) operate on `stdout`. An error message mixed into `stdout` silently corrupts the output of the next command; putting it on `stderr` keeps the channels clean and lets the exit code do its job.

2. **`find` over `ls` — always.** `ls` output is formatted for humans: it collapses spaces, adds colour codes, and varies by locale. `find` returns one path per line and handles whitespace in filenames correctly. In a script, `ls` is a bug waiting to happen.

3. **`set -e` is a safety net, not a substitute for explicit checks.** It stops the script on any unexpected non-zero exit, but it won't catch logic errors inside `[[ ]]` expressions or commands whose failure you intentionally ignore. Explicit `check_dir` + `exit 1` patterns remain necessary for user-facing error messages.