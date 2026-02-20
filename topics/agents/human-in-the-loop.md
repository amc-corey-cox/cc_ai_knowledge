---
id: kb-2025-024
title: "Human-in-the-Loop Patterns for AI Agents"
created: 2026-02-19
updated: 2026-02-19

author: human
curation_type: ai_assisted

sources:
  - id: src-001
    type: primary
    title: "Building Effective Agents"
    authors: ["Anthropic"]
    url: "https://www.anthropic.com/engineering/building-effective-agents"
    accessed: 2026-02-19
    quotes:
      - text: "Prioritize transparency by explicitly showing the agent's planning steps."
        location: "Summary"
      - text: "Maintain simplicity in your agent's design."
        location: "Summary"
  - id: src-002
    type: primary
    title: "Claude Code Documentation"
    url: "https://code.claude.com/docs"
    accessed: 2026-02-19
    quotes:
      - text: "Hooks let you run shell commands before or after Claude Code actions, like auto-formatting after every file edit or running lint before a commit."
        location: "Overview - Customize section"
      - text: "CLAUDE.md is a markdown file you add to your project root that Claude Code reads at the start of every session."
        location: "Overview - Customize section"
  - id: src-003
    type: primary
    title: "Constitutional AI: Harmlessness from AI Feedback"
    authors: ["Bai et al."]
    url: "https://arxiv.org/abs/2212.08073"
    accessed: 2026-02-19
    published: 2022-12-15
    arxiv: "2212.08073"
    quotes:
      - text: "We experiment with methods for training a harmless AI assistant through a process we call constitutional AI (CAI)."
        location: "Abstract"

topics:
  - human-in-the-loop
  - agents
  - agent-configuration
  - agentic-coding

confidence: high
verified: false
verified_by: unverified
verification_notes: "AI-assisted draft; quotes sourced from official documentation and papers but need human verification"

ai_metadata:
  model: claude-opus-4-6
  generation_date: 2026-02-19
  reviewed_by: pending
---

# Human-in-the-Loop Patterns for AI Agents

## Overview

Every AI agent operates somewhere on a spectrum between fully autonomous and fully human-controlled. At one end, the agent takes actions without any human involvement. At the other, every action requires explicit approval. Neither extreme works well in practice: full autonomy is unsafe for high-stakes tasks, and full control defeats the purpose of having an agent at all.

Human-in-the-loop (HITL) is the set of design patterns that manage where an agent sits on this spectrum. The goal is to let agents move fast on safe, reversible actions while ensuring humans review actions that are risky, irreversible, or high-stakes. Getting this balance right is one of the most important design decisions in any agent system.

This article examines HITL patterns through the lens of agentic coding tools -- particularly Claude Code -- but the principles apply broadly to any agent that takes actions in the real world.

## Why Human Oversight Matters

Four forces drive the need for HITL patterns:

**Safety.** Agents make mistakes. A coding agent might delete the wrong file, overwrite working code, or execute a destructive shell command. Human oversight catches these errors before they cause damage. The more powerful the agent's tools, the more important the safety net.

**Correctness.** Even when an agent's actions are safe, they may not be correct. A refactoring might preserve behavior but violate the team's architecture. Human review catches semantic errors that the agent cannot detect because it lacks the full context of the project's goals.

**Trust building.** Trust between humans and agents is earned incrementally, just like trust with a new team member. HITL patterns provide the mechanism: start with tight oversight, observe behavior, and relax controls as confidence builds.

**Compliance.** In regulated industries, human oversight of automated systems is a legal requirement. HITL patterns provide the audit trail and approval checkpoints that compliance frameworks demand.

## The Permission Model: Three Tiers of Autonomy

Claude Code implements a concrete permission model that illustrates how HITL patterns work in practice. The model has three operating tiers that progressively increase agent autonomy.

### Tier 1: Ask Mode (Maximum Oversight)

In ask mode, Claude Code requests confirmation before any action that modifies the environment. Reading files and searching code proceed freely -- these are observation-only operations with no side effects. But writing a file, editing code, or running a shell command all require explicit human approval.

This is the safest mode and the appropriate starting point for new users or unfamiliar codebases. The agent proposes, the human disposes. Every modification is reviewed before execution.

The cost is speed. For tasks that involve many small edits -- renaming a variable across a codebase, fixing formatting in dozens of files -- confirming each action individually is tedious. This is where approval fatigue becomes a real problem (discussed below).

### Tier 2: Auto-Edit Mode (Balanced Oversight)

In auto-edit mode, file modifications (Write, Edit) proceed without confirmation, but shell commands still require approval. This reflects an important safety distinction: file edits are bounded and reversible (you can always undo them with version control), while shell commands have unbounded side effects (a careless `rm -rf` or `git push --force` cannot be easily undone).

This tier is the practical sweet spot for most development work. The agent can freely read, search, and edit code, which covers the majority of coding tasks. The human only intervenes for shell commands, which are less frequent and more consequential.

### Tier 3: YOLO Mode (Full Autonomy)

In fully autonomous mode, all operations proceed without confirmation -- including shell commands. The human is entirely out of the loop during execution, reviewing results only after the agent finishes.

Despite the playful name, this mode has legitimate uses. For well-scoped, trusted tasks in isolated environments (CI pipelines, sandboxed containers, throwaway branches), the overhead of human confirmation adds latency without meaningful safety benefit. The key precondition is that the blast radius is limited: if the agent makes a mistake, the damage is contained and reversible.

YOLO mode is not the absence of HITL design -- it is a deliberate decision to remove the human checkpoint because the environment provides equivalent safety through other means (isolation, reversibility, monitoring).

## Confirmation Flows: When to Ask vs. When to Proceed

The core question in HITL design is: for any given action, should the agent ask for permission or proceed on its own? The answer depends on two properties of the action.

### Reversibility

Actions that can be easily undone are safer to execute autonomously. Reading a file, creating a branch, writing to a scratch file -- all reversible. Pushing to a shared remote, deleting data, sending an email -- all difficult or impossible to reverse.

The key insight is that **reversibility is contextual**. Editing a file is reversible if you are using version control. Running `DROP TABLE` is reversible if you have a backup. The agent's confidence about reversibility should inform its confirmation behavior.

### Blast Radius

Local actions that affect only the developer's environment are lower risk than actions that affect shared resources. Editing a local file affects one person. Pushing to main affects the whole team. Deploying to production affects users.

These two dimensions create a useful matrix:

```
                    Local/Private          Shared/External
                 ┌──────────────────┬──────────────────────┐
  Reversible     │  Proceed freely  │  Proceed with caution│
                 │  (edit files,    │  (push to branch,    │
                 │   run tests)     │   open PR)           │
                 ├──────────────────┼──────────────────────┤
  Irreversible   │  Ask first       │  Always ask          │
                 │  (delete local   │  (push --force,      │
                 │   files)         │   deploy, delete     │
                 │                  │   remote resources)  │
                 └──────────────────┴──────────────────────┘
```

Well-designed HITL systems encode this matrix into their permission logic. Claude Code's tiered permission model approximates it: read-only operations (local, reversible) are always allowed; file edits (local, reversible) can be auto-approved; shell commands (potentially shared, potentially irreversible) require confirmation by default.

## Trust Levels in Practice

Beyond the coarse tiers, HITL design benefits from thinking about trust at the level of individual actions:

**High-trust (freely taken)**: Reading files, searching code, running linters and tests, creating local branches, editing files under version control. These actions are **observable** and **reversible** -- no pre-approval needed.

**Medium-trust (proceed with notification)**: Installing dependencies, modifying configuration files, creating new files outside existing patterns, running unfamiliar commands. The agent might proceed but notify the human afterward, or proceed only if CLAUDE.md explicitly permits it.

**Low-trust (always confirm)**: Deleting files or directories, force-pushing to shared branches, modifying database schemas, running commands that affect shared infrastructure, changing security-sensitive code. These should always require explicit confirmation regardless of the overall autonomy tier.

## The Hooks System: Programmatic Guardrails

Permission tiers provide coarse-grained HITL control. For fine-grained, programmable control, Claude Code provides hooks -- user-defined scripts that run before or after agent actions. "Hooks let you run shell commands before or after Claude Code actions, like auto-formatting after every file edit or running lint before a commit" [src-002].

### Pre-Action Hooks

Pre-hooks run before a tool executes and can block the action. This enables custom validation rules:

- **Security boundaries**: Block edits to files in `security/` or `auth/` directories without explicit approval
- **Lint gates**: Reject code changes that would introduce lint errors
- **Pattern enforcement**: Ensure new files follow naming conventions
- **Dependency control**: Block `npm install` or `pip install` for unapproved packages

Pre-hooks are a form of automated oversight that supplements human review. They encode rules that a human would enforce manually ("don't modify the auth module without reviewing the change") and apply them consistently and instantly.

### Post-Action Hooks

Post-hooks run after a tool completes and can trigger follow-up actions:

- **Auto-formatting**: Run `prettier` or `black` after every file edit
- **Test execution**: Run affected tests after code changes
- **Audit logging**: Record every action for later review
- **Notification**: Alert the team when the agent modifies certain files

Post-hooks turn the agent's actions into triggers for broader workflows. They are particularly useful for maintaining consistency: instead of hoping the agent remembers to format code, a post-hook guarantees it.

### Hooks as Encoded Oversight

Hooks represent a middle ground between human-in-the-loop and fully autonomous operation. The human is not reviewing each action in real time, but they have encoded their review criteria into executable rules. This is a form of **asynchronous oversight**: the human's judgment is applied through pre-written rules rather than real-time approval.

This scales better than direct approval. A human reviewing every edit gets fatigued and starts rubber-stamping. A hook that checks every edit against project rules never gets tired and never misses a violation.

## Plan Mode: Review Before Execution

Some tasks benefit from a planning phase where the agent proposes a complete plan and the human reviews it before any execution begins. This is distinct from action-by-action confirmation: instead of approving each step as it happens, the human reviews the entire approach upfront.

### How Plan Mode Works

1. The human describes the task
2. The agent analyzes the codebase and proposes a plan (files to modify, approach, risks)
3. The human reviews, adjusts, or approves the plan
4. Only after approval does the agent execute

This pattern is especially valuable for:
- Large refactoring tasks where the approach matters more than individual edits
- Tasks where the human has context the agent lacks ("don't touch that module, it's being rewritten")
- Situations where the human wants to understand the agent's reasoning before committing

Plan mode aligns with Anthropic's recommendation to "prioritize transparency by explicitly showing the agent's planning steps" [src-001]. The plan itself is a transparency mechanism: it makes the agent's reasoning visible and reviewable before any action is taken.

### Plans as Contracts

A reviewed plan functions as a contract between human and agent. The human has agreed to the approach, so the agent can execute with more autonomy during the implementation phase. This combines the safety of human review with the efficiency of autonomous execution: review once at the plan level, then let the agent work.

The risk is plan deviation. If the agent encounters unexpected situations during execution and departs from the approved plan, the human's review of the original plan no longer provides full oversight. Good HITL design addresses this by having the agent pause and re-engage the human when the situation diverges from the plan.

## Constitutional AI: Values as Autonomous Guardrails

Constitutional AI (CAI) offers a different approach to oversight. Instead of requiring human approval for individual actions, the model is trained to follow a set of principles -- a "constitution" -- that guides its behavior autonomously. Bai et al. "experiment with methods for training a harmless AI assistant through a process we call constitutional AI (CAI)" [src-003].

### From Rules to Values

The traditional HITL approach is rule-based: "ask before running shell commands," "don't modify files in /prod/." Constitutional AI operates at the values level: "be helpful but avoid harm," "respect the user's intentions," "err on the side of caution with destructive actions."

This values-based approach is what allows a model like Claude to make reasonable HITL decisions even without explicit rules. When Claude Code encounters an ambiguous situation -- a command it has not been specifically told to block, but which seems potentially dangerous -- it can fall back on its constitutional training to decide whether to proceed or ask.

### CLAUDE.md as a Project Constitution

The CLAUDE.md file functions as a project-level constitution for the agent. "CLAUDE.md is a markdown file you add to your project root that Claude Code reads at the start of every session" [src-002]. While not constitutional AI in the technical sense (the instructions are in-context, not baked into model weights), the effect is similar: the agent internalizes a set of rules and values that guide its autonomous behavior.

Consider a CLAUDE.md that includes:

```markdown
## Autonomy Guidelines
- Simple edits (1-2 files, low risk): go ahead without asking
- Anything touching 3+ files: stop and check in first
- New architecture or structural changes: always ask first
- If a task turns out bigger than expected: stop and explain before continuing
```

This is a constitution in miniature. It encodes the human's oversight preferences as rules the agent follows autonomously. The agent does not need to ask about every action because it has internalized when to ask and when to proceed.

### Scope Creep Detection

One particularly valuable constitutional rule is scope creep detection. Agents are prone to expanding the scope of a task as they discover related issues: "While fixing this bug, I noticed the tests are also broken, and the configuration is outdated, and the documentation is stale..." Left unchecked, a simple bug fix becomes a sprawling refactoring.

A scope creep rule in CLAUDE.md tells the agent to recognize when it is drifting from the original task and pause for human input. This is HITL at the meta level: instead of reviewing individual actions, the human reviews the agent's trajectory to ensure it stays on track.

## The Autonomy Dial: Graduated Trust

In practice, the level of human oversight is not a fixed setting but a dial that teams adjust over time. The progression typically follows a pattern:

### Phase 1: Tight Oversight (Getting Started)

The team runs in ask mode with close attention. Every action is reviewed. The goal is to build a mental model of what the agent does well (routine edits, test generation, code search) and where it struggles (architecture decisions, domain-specific logic, subtle correctness).

### Phase 2: Selective Autonomy (Building Confidence)

The team moves to auto-edit mode and starts defining hooks. The CLAUDE.md grows to include explicit autonomy guidelines based on observed behavior. Per-developer autonomy levels may emerge: senior developers run more autonomously, while newer team members keep tighter controls.

### Phase 3: High Autonomy with Guardrails (Established Trust)

Mature teams rely on hooks, CLAUDE.md rules, and post-hoc review rather than pre-approval. The HITL pattern shifts from "gatekeeper" to "auditor" -- the human reviews results after the fact, catching issues in code review rather than in real-time confirmation dialogues.

### Phase 4: Full Automation for Scoped Tasks

For well-defined, repeatable tasks -- CI integration, automated PR descriptions, code formatting, test generation -- the human removes themselves from the loop entirely. The agent runs autonomously within a tightly scoped environment, and results are reviewed as part of the normal development workflow.

## Failure Modes

HITL patterns can fail in ways that undermine the oversight they are supposed to provide.

### Rubber-Stamping and Approval Fatigue

When a human is asked to confirm too many low-risk actions, they stop reading the confirmations and start approving everything reflexively. This provides the illusion of oversight without the substance. In its more extreme form -- approval fatigue -- the human disengages entirely, treating the agent as a black box and only engaging when something visibly breaks.

**Mitigation**: Reduce the volume of confirmations by increasing autonomy for low-risk actions. Use plan mode for complex tasks so the human engages once meaningfully rather than many times superficially. Use hooks to automate the checks a fatigued human would skip.

### Over-Restriction

The opposite failure: the human keeps oversight too tight, requiring confirmation for actions that are clearly safe. The agent spends more time waiting for approval than doing work, and the human spends more time clicking "approve" than they would spend doing the task themselves.

**Mitigation**: Track which confirmations are always approved. If an action is approved 100% of the time, it does not need confirmation. Use this data to adjust the permission tier or add the action to an auto-approve list.

### Misaligned Trust Calibration

The human trusts the agent too much for complex tasks (leading to unreviewed mistakes) or too little for simple tasks (leading to unnecessary overhead). This happens when the trust level is set globally rather than calibrated per task type.

**Mitigation**: Use contextual trust levels rather than a single global setting. CLAUDE.md autonomy guidelines should be specific: "go ahead for formatting changes, ask for architecture changes." Hooks can enforce task-specific trust boundaries even when the global tier is permissive.

### Invisible Failures

The agent takes an action that appears correct but is subtly wrong, and the human's review does not catch it because the error is not visible at the approval level. For example, the agent edits a function correctly in isolation, but the change breaks an invariant that is only visible in the context of the broader system.

**Mitigation**: Post-action verification (running tests, type checking, linting) catches many invisible failures. Code review of the final result -- not just individual actions -- provides the broader context needed to detect subtle issues.

## Practical Considerations

### Designing Your HITL Strategy

Start with the question: "What is the worst thing the agent could do in this context?" If the worst case is a bad edit that gets caught in code review, you can afford significant autonomy. If the worst case is data loss or a production outage, you need tight oversight.

Then layer your controls:
1. Set the permission tier based on the environment (development vs. production access)
2. Add CLAUDE.md rules for task-specific autonomy boundaries
3. Add hooks for automated validation of the rules humans would enforce manually
4. Use plan mode for complex tasks where the approach matters

### Measuring HITL Effectiveness

Good HITL design is measurable:
- **Approval rate**: If the human approves 99% of confirmations, the confirmation is too aggressive
- **Catch rate**: How often does the human reject an action that would have caused a problem?
- **Time-to-completion**: How much latency does the HITL process add?
- **Post-hoc error rate**: How often do unreviewed actions cause problems?

These metrics help tune the autonomy dial. Low catch rates suggest the tier can be relaxed. High post-hoc error rates suggest it should be tightened.

### HITL in Team Settings

Different team members may need different oversight levels. A senior developer who wrote the codebase might run in auto-edit mode, while a junior developer keeps ask mode. Claude Code supports this through the layered CLAUDE.md system: the project CLAUDE.md sets a team baseline, and individual developers override it in their personal configuration.

This mirrors how teams already work. Senior engineers review junior engineers' code more carefully than they review each other's. The same principle applies to reviewing an agent's work: the reviewer's expertise determines how much oversight is appropriate.

## Further Reading

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Anthropic's principles for agent design [src-001]
- [Claude Code Documentation](https://code.claude.com/docs) - Official reference for permission model and hooks [src-002]
- [Constitutional AI Paper](https://arxiv.org/abs/2212.08073) - Values-based alignment for autonomous behavior [src-003]
- [LLM Agent Architectures and Patterns](agent-architectures.md) - Foundational agent patterns
- [Sub-Agent Delegation](sub-agent-delegation.md) - HITL considerations when agents delegate to sub-agents
- [Claude Code Architecture](../agentic-coding/claude-code-architecture.md) - How the permission model fits into the broader system
- [CLAUDE.md and Agent Configuration](../agentic-coding/claude-md-agent-configuration.md) - Encoding oversight rules in configuration
