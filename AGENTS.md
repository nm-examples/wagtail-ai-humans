# Project development requirements

For application planning, implementation, fixes, and code review, read and use
[the repository development skill](.agents/skills/wagtail-development/SKILL.md).
Keep these requirements in effect even when another skill provides technical help:

- Assess whether the work is one coherent, reviewable change. Explain when it
  should be split and propose usable increments before broad implementation.
- Establish expected behaviour and meaningful verification before coding.
- Keep changes focused and preserve unrelated work.
- Follow the development skill's Git workflow: define coherent commit boundaries,
  commit verified increments by default, review the staged diff, reassess oversized
  changes, and report commit IDs and remaining work. Honour user Git instructions;
  pushing and merging require explicit requests.
- Never weaken tests, checks, or workflow requirements just to make an
  implementation pass. Explain any necessary change to those requirements.
- Report what changed, why, what was verified, and any remaining limitations.

Other skills may supplement this workflow; they must not silently replace it,
expand scope, or introduce a different architecture or toolchain. Explain any
conflict and follow the user's instructions and applicable instruction hierarchy.
These files guide agents; automated checks and developer review provide separate
verification.

Use the Docker, uv, and `just` workflow documented in [README.md](README.md).
For creating a separate new site, use the existing `wagtail-bootstrap` skill.
Changes to either skill must also be mirrored to the sibling base repository as
described in the README. Keep the development skill's bundled bootstrap copy in
sync so separately generated sites receive the same workflow. Generated sites
carry their own development skill and project instructions without depending on
either source repository.
