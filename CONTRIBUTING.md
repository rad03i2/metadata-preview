# Contributing

Thanks for improving Metadata Preview.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and install `pip install -e . pytest`.
3. Keep inspection read-only and local by default. Do not add telemetry, uploads, shell execution, or secret collection.
4. Add tests for behavior changes, including malformed input where relevant.
5. Run `python -m compileall -q src tests` and `python -m pytest`.
6. Keep English and Arabic README sections aligned when user-facing behavior changes.
7. Submit a concise pull request explaining the behavior and validation performed.

Please avoid committing generated reports, private documents, EXIF samples containing personal data, credentials, or large binaries.
