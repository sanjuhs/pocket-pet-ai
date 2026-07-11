# Security Policy

## Supported Versions

This project is pre-release research software. Security fixes are applied to the latest commit on the default branch; older snapshots are not supported.

## Reporting a Vulnerability

Do not open a public issue for suspected vulnerabilities. Use GitHub's **Report a vulnerability** / private security advisory feature for the repository. If that feature is unavailable, contact the repository owner privately through their verified GitHub profile and include a way to continue the conversation securely.

Include the affected revision, reproduction steps, impact, prerequisites, and any suggested mitigation. Avoid accessing data that is not yours, degrading services, or testing against third-party accounts without permission. Maintainers should acknowledge a report within 7 days and provide a status update within 14 days; these are response goals, not guarantees.

## High-Risk Areas

- Tool execution and action authorization
- Authentication tokens and connector credentials
- Local memory, recordings, and personal data
- Browser, accessibility, phone, and desktop automation
- Model and dataset supply chain
- Downloaded model deserialization and generated code
- Public benchmark infrastructure

## Prototype Warning

Do not grant this prototype broad device or account permissions. Use test accounts and disposable data. Model-generated actions are untrusted input and must pass deterministic validation and explicit confirmation policies.
