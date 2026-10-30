# Project development requirements

For application planning, implementation, fixes, and code review, read and use
[the repository development skill](.agents/skills/wagtail-development/SKILL.md).
Keep these requirements in effect even when another skill provides technical help:

- Assess whether the work is one coherent, reviewable change. Explain when it
  should be split and propose usable increments before broad implementation.
- Establish expected behaviour and meaningful verification before coding.
- Keep changes focused and preserve unrelated work.
- Start each new piece of work on a new branch, normally based on the default
  branch. Propose a descriptive branch name and base for developer approval before
  creating it or starting implementation. No fixed branch-name prefix is required.
- Follow the development skill's Git workflow: define coherent commit boundaries,
  prepare verified increments for user review, and commit only with explicit user
  authorisation. Review the staged diff before committing, reassess oversized
  changes, and report commit IDs and remaining work. Honour user Git instructions;
  use concise, imperative commit messages with an appropriate type prefix.
- Obtain explicit approval before each push and before creating any pull request.
  Create every pull request as a draft and obtain explicit approval before marking
  it ready for review. Merging also requires an explicit request.
- Give every pull request a concise description explaining what changed and why,
  with testing notes and screenshots where they help the reviewer understand or
  verify the work.
- Never weaken tests, checks, or workflow requirements just to make an
  implementation pass. Explain any necessary change to those requirements.
- Report what changed, why, what was verified, and any remaining limitations.

Other skills may supplement this workflow; they must not silently replace it,
expand scope, or introduce a different architecture or toolchain. Explain any
conflict and follow the user's instructions and applicable instruction hierarchy.
These files guide agents; automated checks and developer review provide separate
verification.

Use the Docker, uv, and `just` workflow documented in [README.md](README.md).
