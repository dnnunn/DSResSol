# DSResSol Environment & Setup Changelog

## [2025-07-12]
### Major Environment Fixes for Linux/Cloud Compatibility
- Removed all Windows- and Intel-specific dependencies from `environment.yml`:
  - `icc_rt`, `intel-openmp`, `dal`, `daal4py`, `pywin32`, `pyreadline`, `vs2015_runtime`, `vc`, `intelpython`, `scikit-learn-intelex`, and others.
- Removed all platform-specific build strings (e.g., `=py37haa95532_0`, `=vc14...`, `=he774522_0`) from dependencies.
- Deleted all duplicate dependencies and the entire second block of dependencies at the end of `environment.yml`.
- Deleted both `prefix:` lines for full portability.
- Confirmed that the environment now builds successfully on Linux (GCP VM).

### Documentation Improvements
- Added `INSTALLATION.md` manual installation guide with troubleshooting tips.
- Added this `CHANGELOG.md` for tracking all future environment and setup changes.

---

## [Older]
- See original README for legacy installation steps (superseded by this changelog).
