# Security Policy

`deadlock-external` is an **educational** external cheat tool for Deadlock.
It is not designed or maintained for use in live, competitive matches.
Doing so likely violates the game's Terms of Service and will get you
banned. The maintainers accept no responsibility for account action,
hardware bans, or any other consequences of misuse.

## Scope

This project reads process memory and draws an overlay. It does **not**
ship kernel drivers, does **not** include anti-cheat bypasses, and does
**not** include HWID spoofers. PRs adding any of those will be closed.

## Reporting a vulnerability

If you find a security issue **in this repository** (e.g. a code path that
writes outside the target process, a dependency problem, or a way the tool
could be weaponized beyond its stated scope), please report it privately:

- Open a GitHub Security Advisory, **or**
- Email the maintainers listed in `pyproject.toml` / repository metadata.

Please do **not** open a public issue for security reports.

## What is out of scope

- "I got banned" reports — expected, not a vulnerability.
- Requests for anti-cheat bypasses — will be closed.
- Reports about Valve / Deadlock — contact Valve directly.
</parameter>