# Git workflow (all devices)

Before modifying a repository: inspect status, remotes, recent commits, repository instructions and relevant source.

```bash
# Display the current repository state.
git status --short

# Display configured Git remotes.
git remote -v

# Display recent commits.
git log --oneline -10
```

Flow: inspect → targeted edit → format → build/test → inspect `git diff` → report. Keep commits focused and descriptive, but **do not commit automatically** unless requested. Never reset, clean, rebase, force-push or discard local work without explicit authorization. User's GitHub: `https://github.com/PhateValleyman`.
