---
type: cheatsheet
area: CLI Tools
aliases: []
tags: [vcs]
status: stable
---

# git

> **Area:** [[CLI Tools]]

Quick reference for everyday work with `git`. The default branch is `main` in the examples —
substitute `master` if needed.

---

## 1. Setup & configuration

```bash
# Set identity (global, for all repos)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Default branch name for new repos
git config --global init.defaultBranch main

# Pick an editor (e.g. nano, vim, code)
git config --global core.editor "nano"

# Coloured output
git config --global color.ui auto

# Show current configuration
git config --list
git config --global --edit       # edit ~/.gitconfig directly

# Credential helper (remember login)
git config --global credential.helper cache              # 15 min in RAM
git config --global credential.helper "cache --timeout=3600"

# Create an SSH key for pushing (Ed25519 recommended)
ssh-keygen -t ed25519 -C "you@host"
# then add the public key (~/.ssh/id_ed25519.pub) to GitHub/GitLab
```

---

## 2. Create or clone a repo

```bash
# New repo in the current directory
git init

# New repo with main as default
git init -b main

# Clone a remote repo
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git           # via SSH
git clone https://... my-folder                  # into a custom folder name

# Clone a single branch, without history
git clone --depth 1 --branch main https://...

# Check status (you need this constantly!)
git status
git status -s                                    # short form
```

---

## 3. Tracking changes & committing

### Staging area

```bash
# Stage a single file for commit
git add file.txt

# Everything in the current folder
git add .

# Everything in the whole repo (including deletions)
git add -A

# Interactive: decide per hunk what goes in
git add -p

# Unstage a file (changes are kept)
git restore --staged file.txt
```

### Commits

```bash
# Standard commit (opens editor)
git commit

# Commit with message inline
git commit -m "Short description"

# Add + commit in one (only for already-tracked files!)
git commit -am "Message"

# Amend the last commit (change message or files)
git commit --amend                               # opens editor for the message
git commit --amend --no-edit                     # tack on files, keep message
git commit --amend -m "New message"

# CAUTION: amend changes the commit ID. Don't amend commits already pushed
# that others are building on.
```

### What changed?

```bash
# Show unstaged changes
git diff

# Staged changes (what goes into the next commit?)
git diff --staged

# Filenames only, no lines
git diff --stat

# Compare two commits or branches
git diff main..feature
git diff HEAD~3 HEAD
```

---

## 4. Branches

```bash
# All local branches
git branch

# All branches incl. remote
git branch -a

# Create a branch (don't switch yet)
git branch feature/firewall

# Create AND switch
git switch -c feature/firewall                   # modern way
git checkout -b feature/firewall                 # older way, also works

# Switch branch
git switch main
git checkout main                                # alternative

# Delete a branch (local, only if merged)
git branch -d feature/firewall

# Force-delete a branch (even if not merged)
git branch -D feature/firewall

# Rename a branch
git branch -m old-name new-name

# Delete a remote branch
git push origin --delete feature/firewall
```

---

## 5. Merge & rebase

```bash
# Switch to main and merge feature in
git switch main
git merge feature/firewall

# Merge without fast-forward (always create a merge commit)
git merge --no-ff feature/firewall

# Rebase the current branch onto main (linear history)
git switch feature/firewall
git rebase main

# Interactive rebase — reorder, squash, reword commits
git rebase -i HEAD~5

# Abort a merge/rebase that's going wrong
git merge --abort
git rebase --abort

# Resolve conflicts: edit files, then
git add conflict.txt
git merge --continue        # or
git rebase --continue
```

**Merge vs. rebase rule of thumb:** merge for public/shared branches, rebase only for your own
local branches that nobody else has seen yet.

---

## 6. Remote (push / pull / fetch)

```bash
# Show configured remotes
git remote -v

# Add a remote
git remote add origin git@github.com:user/repo.git

# Change a remote's URL
git remote set-url origin git@github.com:user/repo.git

# Fetch from remote without merging (safe)
git fetch
git fetch --all --prune                          # also tidy up stale branches

# Fetch + merge in one
git pull

# Cleaner: rebase instead of merge on pull
git pull --rebase

# Always rebase on pull, by default
git config --global pull.rebase true

# Upload local commits
git push

# First push of a new branch (set upstream)
git push -u origin feature/firewall

# Force-push after a rebase — but safely!
git push --force-with-lease                      # aborts if someone else has pushed
# git push --force                               # DON'T use — overwrites blindly
```

---

## 7. History & inspection

```bash
# Commit log
git log
git log --oneline                                # one line per commit
git log --oneline --graph --all --decorate       # pretty tree of all branches
git log -n 10                                     # just the last 10

# Who changed this line, and when?
git blame file.txt
git blame -L 20,40 file.txt                      # only lines 20–40

# Show a single commit
git show <commit-hash>
git show HEAD                                    # newest commit
git show HEAD~2                                  # two before

# View a file at a specific point in time
git show HEAD~3:path/to/file.txt

# History of a single file
git log -p file.txt                              # with diffs
git log --follow file.txt                        # across renames too

# Searching
git log --grep="firewall"                        # in commit messages
git log -S "iptables -A INPUT"                   # in code (when was a string added/removed?)
```

---

## 8. Messed up — how to undo?

```bash
# Discard working-directory changes (NOT yet staged)
git restore file.txt
git restore .                                    # everything in the current folder

# Unstage a file (changes are kept)
git restore --staged file.txt

# Undo the last commit, keep changes staged
git reset --soft HEAD~1

# Undo the last commit, keep changes in the working directory
git reset HEAD~1

# Undo the last commit AND throw away the changes (NOT reversible!)
git reset --hard HEAD~1

# "Undo" a commit via a new revert commit (safe for pushed branches)
git revert <commit-hash>

# Emergency rescue: reflog shows all HEAD movements of the last ~90 days
git reflog
git reset --hard HEAD@{2}                         # back to a reflog entry

# Wipe completely unknown/untracked files
git clean -n                                     # dry-run: what would be deleted?
git clean -fd                                    # actually delete (files + empty dirs)
```

**Rule of thumb:** `reset` for local commits, `revert` for already-pushed ones. The reflog is
your safety net — even after `reset --hard`, commits are reachable for ~90 days.

---

## 9. Stash — the scratch drawer

```bash
# Tuck away current changes; working directory becomes clean
git stash

# With a description
git stash push -m "half-finished firewall rules"

# Stash untracked files too
git stash -u

# List all stashes
git stash list

# Pop the latest stash (apply AND remove from the list)
git stash pop

# Apply a stash but keep it in the list
git stash apply

# Apply a specific stash
git stash apply stash@{2}

# Drop stashes
git stash drop stash@{0}
git stash clear                                  # delete all
```

---

## 10. Daily workflows

### Start the day — get the latest
```bash
git switch main
git pull --rebase
git switch -c feature/new-rule                   # new working branch
```

### Finish a feature and push
```bash
git status                                       # what did I change?
git add -p                                       # stage deliberately, per hunk
git commit -m "Add input drop rule"
git push -u origin feature/new-rule
# then: open a Pull/Merge Request in the web UI
```

### Stay in sync with main while a feature is in flight
```bash
git switch feature/new-rule
git fetch origin
git rebase origin/main
# resolve conflicts → git add → git rebase --continue
git push --force-with-lease                      # your own feature branch, so this is ok
```

### Quick detour (a hotfix in between)
```bash
git stash -u                                     # tuck away current work
git switch main
git switch -c hotfix/typo
# … fix, commit, push, merge …
git switch feature/new-rule
git stash pop                                    # back to the original work
```

### Amend the last commit (before pushing)
```bash
# forgot a file
git add forgotten-file.txt
git commit --amend --no-edit

# the commit message was bad
git commit --amend -m "Better description"
```

### "Oh no, I committed to the wrong branch"
```bash
git log --oneline -n 3                           # note the hash
git switch correct-branch
git cherry-pick <hash>
git switch wrong-branch
git reset --hard HEAD~1                          # remove it from the wrong branch
```

---

## 11. .gitignore — what doesn't belong in the repo

File `.gitignore` in the repo root:

```gitignore
# Build artefacts
*.o
*.log
build/
dist/

# Python
__pycache__/
*.pyc
.venv/

# Editor / OS cruft
.vscode/
.idea/
.DS_Store
Thumbs.db

# Secrets — NEVER in the repo!
.env
*.key
*.pem
config.local.yml
```

```bash
# Ignore an already-tracked file after the fact
git rm --cached config.local.yml
echo "config.local.yml" >> .gitignore
git commit -am "Ignore local config"

# See why a file is (not) ignored
git check-ignore -v file.txt
```

---

## 12. Useful extras

### Aliases (save typing)

```bash
git config --global alias.st "status -s"
git config --global alias.co "checkout"
git config --global alias.br "branch"
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 HEAD"
git config --global alias.unstage "restore --staged"
```

Then `git lg` is enough for the pretty tree view.

### Tags (mark releases)

```bash
git tag v1.0.0                                   # lightweight tag
git tag -a v1.0.0 -m "Release 1.0"               # annotated (recommended)
git tag                                          # list all tags
git push origin v1.0.0                           # push a single tag
git push --tags                                  # push all tags
git tag -d v1.0.0                                # delete locally
git push origin --delete v1.0.0                  # delete remotely
```

### Bisect — find a bug by binary search

```bash
git bisect start
git bisect bad                                   # current commit is broken
git bisect good v1.0.0                           # this version was still fine
# git checks out the midpoint automatically → test it
git bisect good          # or
git bisect bad
# … repeat until git names the guilty commit
git bisect reset                                 # back to the starting state
```

### Global .gitignore for editor/OS cruft

```bash
git config --global core.excludesfile ~/.gitignore_global
# in ~/.gitignore_global put e.g. .DS_Store, *.swp, Thumbs.db
```

### Sensible push/pull defaults

```ini
# in .git/config or ~/.gitconfig:
[push]
    default = current
[pull]
    rebase = true
```

---

## Golden rules

1. **Never force-push shared branches.** Use `--force-with-lease` on your own branches only.
2. **`reset` for local, `revert` for pushed.** The reflog will save you for ~90 days.
3. **Secrets never enter the repo** — and history is forever, so a leaked secret committed once
   stays in history even after you delete it.
4. **Stage deliberately** (`git add -p`) so commits stay small and reviewable.

## Further reading
- [Pro Git book](https://git-scm.com/book) · [git reference](https://git-scm.com/docs)
