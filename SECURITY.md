# Security Policy

## Supported version
The latest release on `main` receives security fixes.

## Privacy and safety model
Metadata Preview reads files locally and never uploads them, executes their contents, or performs network requests. It is intentionally read-only. Symbolic links are rejected to reduce accidental inspection outside the intended path. `--hash` reads the complete file only to calculate SHA-256.

Treat metadata as potentially sensitive: EXIF and PDF fields can contain names, software identifiers, timestamps, or location information. Review reports before sharing them.

## Reporting
Please open a GitHub security advisory when available, or a minimal issue that does not disclose exploit details or private file contents. Do not attach sensitive sample documents.

Maintainer: Radwan Abdulhadi Ahmed (@rad03i2)
