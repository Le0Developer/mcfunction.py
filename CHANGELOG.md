# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added support for minecraft 1.17


## [0.3.1]

### Added

- `load`, `loads`, `dump` and `dumps` to mcfunction
- `oplevel` to commands (more info than `comamndblock`)


## [0.3.0]

### Added

- Command syntax of more minecraft versions (1.8 - 1.16)

### Fixed

- Typehint of `util.tokenize`


## [0.2.1]

### Changed

- UUIDs are now case insensitive  (#12)
- JSON no longers escapes non-ascii characters  (#14)


## [0.2.0]

### Added

- McFunction file parser and reconstructer (#1)

### Changed

- Rename from `mcast` to `mcfunction(.py)`
- Double precision is now 14 places  (was the default 6 before)  (#5)
- Entity parser now accepts UUIDs as selectors  (#9)
- ScoreboardEntity now accepts almost everything  (#10)

### Fixed

- Wrong parsing of `data modify <target> set value X`, parsing X as Double instead of Any  (#4)


## [0.1.0]

### Added

- First commit


[Unreleased]: https://github.com/Le0Developer/mcfunction.py/compare/v0.3.1...HEAD
[0.3.1]: https://github.com/Le0Developer/mcfunction.py/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/Le0Developer/mcfunction.py/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/Le0Developer/mcfunction.py/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/Le0Developer/mcfunction.py/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Le0Developer/mcfunction.py/releases/tag/v0.1.0
