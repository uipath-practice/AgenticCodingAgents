# Source prose

Existing written content for a migrated course, one file per lesson:

```
source/<exercise-slug>/<N-lesson-slug>.md
```

`/new-lesson` Step 0 treats a file here as the **authoritative text** for that lesson: it reshapes
the prose into the lesson template rather than rewriting it. `<<IMG:n>>` tokens mark where each
screenshot appeared in the original document.

This directory is committed — it is the provenance record for migrated content. Harvest scratch
(raw HTML, unsorted images) belongs in `staging/`, which is gitignored.
