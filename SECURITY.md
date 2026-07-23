# Security Policy

`steuer-assistent` is a local, offline-first tool: it has no network
connection, no server component, and no cloud upload. The primary
security-relevant surface is local file handling (SQLite store, ZIP export)
under the user's own home directory.

## Reporting a Vulnerability

Please report security issues privately via
[GitHub Private Vulnerability Reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability)
on this repository ("Security" tab → "Report a vulnerability"). Do not open a
public issue for suspected vulnerabilities.

Please include:

- A description of the issue and its potential impact.
- Steps to reproduce (minimal example preferred).
- The version/commit affected.

There is no fixed response-time SLA (independent, unfunded open-source
project), but reports are read and triaged as soon as possible.

## Scope

In scope: the `steuer_assistent` Python package and its CLI as published in
this repository. Out of scope: any downstream integration (e.g. a BACH
vendoring of this module), third-party forks, and the user's own operating
system or file-system permissions.
