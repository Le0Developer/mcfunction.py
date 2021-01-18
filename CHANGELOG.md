# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Changed

- UUIDs are now case insensitive
- JSON no longers escapes non-ascii characters

## [0.2.0]

### Added

- McFunction file parser and reconstructer (#1)

### Changed

- Rename from `mcast` to `mcfunction(.py)`
- Double precision is now 14 places  (was the default 6 before)
- Entity parser now accepts UUIDs as selectors
- ScoreboardEntity now accepts almost everything

## [0.1.0]

### Added

- First commit


[Unreleased]: https://github.com/Le0Developer/mcfunction.py/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Le0Developer/mcfunction.py/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Le0Developer/mcfunction.py/releases/tag/v0.1.0
