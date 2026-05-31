# Changelog

All notable changes are documented here in reverse chronological order.

---

## [2.2.0] - 2026-05-31
### Added
- Migrated from Render → **Hugging Face Spaces (Docker)** — always-on, zero cold starts
- Added `Dockerfile` for HF Spaces deployment
- Added `/api/version` and `/api/changelog` endpoints
- Added What's New changelog visible in the UI header

### Changed
- Updated README with HF Spaces YAML metadata

---

## [2.1.0] - 2026-05-26
### Added
- Interactive contact modal replacing broken mailto link
- Resume Bullet Point Optimizer with clipboard copy buttons
- Local scan history saved to browser `localStorage`
- Toast notification system
- PDF export with clean print media stylesheet

### Fixed
- Fixed broken footer mailto link

---

## [2.0.0] - 2026-05-26
### Added (GrailAI v2.0 - Full Rewrite)
- Complete migration from Streamlit → FastAPI + premium Vanilla JS SPA
- Mock Interview Coach: AI generates 3 targeted questions based on your gaps
- Resume Rewrite Tool: AI rewrites resume bullets to match JD keywords
- Cover Letter Generator: instant personalized cover letter from resume + JD
- Radar/spider chart for multi-dimensional skill scoring (Technical, Domain, Experience, Soft Skills)
- Shareable score card generation
- Glassmorphic dark-mode UI with animated ATS score gauge
- Drag-and-drop PDF resume uploader
- Visual skill matrix (matched/missing badges)
- Prompt injection guard on all AI endpoints
- Model fallback chain: gemini-2.5-flash → 2.0-flash → 2.0-flash-lite
- Security: input sanitization, PDF size limits, session analysis limits

### Removed
- Removed Streamlit dependency
- Removed Render cold-start limitations (migrating to HF Spaces)

---

## [1.0.0] - 2025-01-01
### Initial Release
- Streamlit app with PDF upload and basic Gemini ATS analysis
- Simple match percentage output
