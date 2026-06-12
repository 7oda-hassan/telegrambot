# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - Production Release

### Added
- Implemented full support for Telegram's native `sendRichMessage` API endpoint binding.
- Implemented `EntityASTBuilder` pipeline for seamless, zero-loss parsing of Telegram's native UTF-16 code unit formatting entities.
- Full compatibility with native block-level features: Headings, Blockquotes, Checklists, Math Blocks, and Tables.
- Full compatibility with native inline-level features: Bold, Italic, Strikethrough, Spoilers, Inline Code, and Links.
- Added graceful failure fallback system to automatically strip `RICH_MESSAGE_PHOTO_URL_INVALID` errors and successfully resend affected payloads.
- Added comprehensive Pytest suite guaranteeing parser offset stability against multibyte emoji shifts.
- Implemented a unified `Tokenizer` engine for seamless detection of unformatted text fragments.

### Removed
- Fully purged all experimental/legacy custom inline Tokenizer regex plugins (`bold.py`, `italic.py`, `spoiler.py`).
- Deleted temporary Sandbox and prototyping code paths (`test_ast.py`, `debug_middleware.py`, `utils/debug.py`).

### Security
- Integrated `GlobalErrorMiddleware` to trap system exceptions and suppress internal stack traces from leaking to end-users.
