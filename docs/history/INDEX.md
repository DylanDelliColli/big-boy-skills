```doc-meta
role: working
lifecycle: active
```

# Archive pointer index

Archived working records live as content-addressed Git objects kept
reachable through the protected mainline; recover any row with
git show <commit>:<path>. Rows are unique by (path, commit).

| path | commit | source_blob | claim |
|---|---|---|---|
