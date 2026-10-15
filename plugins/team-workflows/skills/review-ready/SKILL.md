---
name: review-ready
description: Prepare an evidence-backed pull request description and review handoff from an actual development diff. Use when a change is ready for review or the user asks to prepare a PR.
---

# Review Ready

Use the user's language. Help a reviewer understand the final change without requiring the conversation history.

## Inspect the change

Read the project's contribution instructions and PR template. Check the working tree, current branch, intended base, and complete relevant diff. Do not include unrelated work or change Git identity.

Explain the concrete problem and resulting behavior. For a behavior change, a short before/after example is often clearer than a list of modified files.

Check for contradictions between the task and implementation, accidental removals, exposed credentials, and missing error handling relevant to the change. Fix issues only within the user's authorized scope; report unresolved issues plainly.

## Establish evidence

Use checks appropriate to the change. Record the actual command or observable result and any meaningful limitation. A passing build does not establish authenticated behavior, successful deployment, or external-provider success.

For visible UI changes, include screenshots when requested or useful and available. Confirm they show the current implementation. Avoid adding tests that merely repeat the implementation.

## Prepare the handoff

Follow the repository template; otherwise draft a concise description covering:

- The problem and resulting behavior.
- Material implementation choices or tradeoffs, if needed for review.
- Verification performed and any remaining gap.

Do not manufacture issue links, test results, deployment claims, or reviewer approval. Identify draft or incomplete work explicitly.

Preparing a PR does not authorize pushing, creating, merging, or messaging reviewers. Perform those actions only when requested or already authorized. When creation is authorized, verify the target repository and base, create the PR, and return its URL; use any host-required attachment tool.

End with the reviewable artifact and verification result. Surface an unresolved blocker instead of marking the work ready.
