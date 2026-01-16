# _aidocs - Internal Project Documentation

This directory contains **internal documentation** for the development team and AI agents working on the python-wfirma library implementation.

## Purpose

This documentation is intended for:
- 🤖 AI agents implementing the library
- 👥 Core maintainers and developers
- 📋 Project management and planning

**NOT for end users** - User-facing documentation is in:
- `/README.md` - Quick start for library users
- `/CONTRIBUTING.md` - For external contributors
- `/docs/` - Sphinx documentation for library API
- `/CHANGELOG.md` - Version history
- `/LICENSE` - Legal information

## Contents

### Core Planning Documents
- **IMPLEMENTATION_PLAN.md** - Complete 16-phase implementation plan (112 hours)
- **PROJECT_STATUS.md** - Current phase, todos, and progress tracking
- **ROADMAP.md** - Feature roadmap (user-facing, should move to root if needed)

### AI Agent Workflow
- **AI_WORKING_INSTRUCTIONS.md** - Detailed workflow guide for AI agents
- **START_HERE.md** - Quick start guide for new work sessions
- **NOAI_PROBLEMS_REPORT.md** - Log of issues with NOAI-protected tests

### Phase Reports
- **PHASE_0_COMPLETION.md** - Detailed Phase 0 completion report
- **PHASE_0_SUMMARY.md** - Quick summary of Phase 0
- **COMPLETION_SUMMARY.txt** - Text-based summary

### Utilities
- **verify_phase0.sh** - Verification script for Phase 0 completion
- **PROJECT_TREE.txt** - Project structure snapshot

## Guidelines

### When to Add Documents Here
- Implementation plans and technical specifications
- AI agent instructions and prompts
- Internal progress reports and phase completions
- Development workflow documentation
- Quality assurance checklists
- NOAI system documentation

### When to Keep in Root
- User-facing README
- Contributor guidelines (CONTRIBUTING.md)
- Legal files (LICENSE)
- Changelog for users (CHANGELOG.md)

### When to Keep in /docs
- Sphinx documentation
- API reference
- User guides and tutorials
- Installation instructions

## TDD & NOAI System

This directory contains crucial information about:
- **Test-Driven Development** workflow
- **NOAI protection system** for immutable tests
- **AICOMPLETE tagging** for tests ready for review

All AI agents MUST read:
1. `AI_WORKING_INSTRUCTIONS.md` before starting work
2. `PROJECT_STATUS.md` to understand current phase
3. `NOAI_PROBLEMS_REPORT.md` to check for blockers

## Maintenance

- Keep this directory organized
- Update PROJECT_STATUS.md after each phase
- Log all NOAI conflicts in NOAI_PROBLEMS_REPORT.md
- Create phase completion reports after major milestones

---

**Last Updated:** 2026-01-16  
**Project:** python-wfirma  
**Version:** 0.1.0-dev

