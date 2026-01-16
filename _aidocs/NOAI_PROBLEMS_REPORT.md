# NOAI Problems Report

This document tracks issues encountered with tests marked as `NOAI` (immutable to AI agents). When the AI detects a problem with a NOAI-tagged test but cannot modify it, the issue is logged here for human review.

**Last Updated**: 2026-01-16  
**Report Version**: 1.0

---

## Report Structure

Each issue is logged with:
- **Timestamp**: When the issue was detected
- **Test Location**: File and test function name
- **Problem Description**: What the AI tried to do and why
- **Blocking Reason**: Why NOAI prevented the change
- **Recommendation**: Suggested fix for human developer
- **Priority**: Low/Medium/High/Critical
- **Status**: Open/In Review/Resolved

---

## Authentication Issues

### Section Status: No issues reported

---

## Client Communication Issues

### Section Status: No issues reported

---

## Model Validation Issues

### Section Status: No issues reported

---

## Resource Operations Issues

### Invoices

#### Section Status: No issues reported

### Contractors

#### Section Status: No issues reported

### Goods

#### Section Status: No issues reported

### Warehouse

#### Section Status: No issues reported

### Payments

#### Section Status: No issues reported

### Employees

#### Section Status: No issues reported

### Company

#### Section Status: No issues reported

---

## Integration Issues

### Section Status: No issues reported

---

## Configuration Issues

### Section Status: No issues reported

---

## General Guidelines for Human Review

When reviewing issues in this report:

1. **Verify the Problem**: Check if the AI's assessment is correct
2. **Consider Impact**: Is this blocking development or just optimization?
3. **Decide Action**:
   - If NOAI test is wrong: Update test, remove NOAI tag temporarily, get new AI completion
   - If NOAI test is correct: Update implementation to match test expectations
   - If both are correct: May indicate API change or documentation update needed
4. **Update Status**: Mark as "In Review" when investigating, "Resolved" when fixed
5. **Document Resolution**: Add notes about how the issue was resolved

---

## Issue Template

Use this template when manually adding issues:

```markdown
### [YYYY-MM-DD HH:MM] Issue in test_file.py::test_function_name

**Problem**: Brief description of what went wrong

**Test Tagged NOAI**: Yes

**Attempted Change**: What the AI tried to do

**Reason Blocked**: Why NOAI prevented it (e.g., "Test is immutable, marked NOAI on 2026-01-15")

**Recommendation**: Suggested fix for human developer

**Priority**: Low/Medium/High/Critical

**Status**: Open

**Resolution**: (filled when resolved)
```

---

## Statistics

- **Total Issues Reported**: 0
- **Open Issues**: 0
- **In Review**: 0
- **Resolved**: 0

---

## Notes

- This file is created at project initialization and remains empty until the first NOAI conflict
- AI agents MUST log issues here before stopping work on blocked features
- Human developers should review this file regularly during development
- Resolved issues should be kept for historical reference

---

**AI Agent Instructions**:
- Before attempting to modify any test, check for NOAI tag
- If NOAI tag found, DO NOT modify the test
- Log the issue in the appropriate section above
- Continue with other work if possible
- Inform user about the blocked issue

---

**Terminal Fallback Note**:
If terminal commands hang or become unresponsive, AI agents should execute commands with output redirection:
```bash
command > /tmp/wfirma_output.txt 2>&1
```
Then read the output file using the `read_file` tool.

