---
name: sdd-lite
description: Turn a small development request into a short, testable task brief and implement it when requested. Use for lightweight specification-driven development without a full specification process.
---

# SDD Lite

Use the user's language. Keep the task brief to about one page; a small change may need only a few sentences.

## Establish the task

Read the relevant project instructions and inspect the existing behavior before proposing changes. Reuse an existing issue or task brief when it already defines the work.

Capture only what helps implementation:

- **Goal:** who needs what outcome, and why.
- **Scope:** the requested behavior and any explicit exclusions or constraints.
- **Acceptance:** observable examples, including an important failure case when relevant.
- **Approach:** the smallest useful change and any decision that affects the user.
- **Verification:** how to demonstrate the acceptance criteria.

Distinguish confirmed requirements from open questions. Ask immediately when an unknown changes the intended behavior; continue independent inspection while waiting. Do not invent missing requirements.

## Carry out the requested work

If the user asked only for a plan, return the brief. Save it only when requested or when the project already has a task-document convention.

If implementation is already authorized, use the brief as the working baseline and proceed without adding a separate approval ceremony. Preserve unrelated changes and existing user-facing features.

Implement a small complete slice. Run the checks that actually establish its behavior; include a regression test when the risk warrants one. Record what passed, what was not checked, and any unmet acceptance criterion.

If new evidence changes the task, update the brief and explain the material change. Ask before expanding scope or taking an external action that the user has not authorized.

Finish with the result, verification evidence, and any remaining limitation. Never describe a plan or an untested implementation as completed behavior.
