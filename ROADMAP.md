# Roadmap
- ❌ Cancelled/Postponed
- 📝 Under Consideration
- ✨ Planned
- 🚧 In Progress
- ✅ Complete
**Legend**:

---

- Features may be moved between versions based on priority
- Dates are estimates and may shift
  - Security considerations
  - Resource availability
  - wFirma API changes
  - Community feedback
- Roadmap is subject to change based on:

## Notes

---

| 1.0.x   | Q4 2026      | Q4 2028 (min) | Planned |
| 0.3.x   | Q3 2026      | 1.0.0 release | Planned |
| 0.2.x   | Q2 2026      | 1.0.0 release | Planned |
| 0.1.x   | Q1 2026      | 1.0.0 release | In Development |
|---------|--------------|---------------|--------|
| Version | Release Date | Support Until | Status |

## Version Support Policy

---

4. **Voting**: React to existing feature requests with 👍
3. **Pull Requests**: Implement features and submit PRs
2. **Discussions**: Join conversations in GitHub Discussions
1. **GitHub Issues**: Open an issue with tag `feature-request`

Want to influence the roadmap? Here's how:

## Contributing to Roadmap

---

*No requests yet - check GitHub Issues for active discussions*

### Requested Features

This section tracks feature requests from the community. Upvote by adding your GitHub username.

## Community Requests

---

- 📝 Offline mode with sync
- 📝 Reduced memory footprint
- 📝 Mobile-optimized examples
#### Mobile Support

- 📝 Financial analytics helpers
- 📝 Data visualization utilities
- 📝 Built-in reporting engine
- 📝 Pandas DataFrame export
#### Data Analysis Tools

- 📝 Email service integrations
- 📝 Payment gateway integrations
- 📝 E-commerce platform plugins (Shopify, WooCommerce)
- 📝 Accounting software integrations (e.g., GnuCash)
#### Additional Integrations

- 📝 Invoice designer/preview
- 📝 Real-time API monitoring dashboard
- 📝 Visual query builder
- 📝 Web-based API explorer
#### GUI/Web Interface

- 📝 Reporting and analytics
- 📝 Bulk import/export utilities
- 📝 Configuration wizard
- 📝 Interactive mode
- 📝 Full-featured CLI application
#### CLI Tool Enhancement

### Potential Features (Not Committed)

## Future Considerations (Beyond 1.0)

---

- ✨ Migration tooling for breaking changes
- ✨ Deprecation timeline (minimum 6 months notice)
- ✨ Backward compatibility guarantees
- ✨ Security update policy
- ✨ Semantic versioning commitment
#### Long-Term Support

- ✨ Case studies
- ✨ Best practices guide
- ✨ Architecture deep-dive
- ✨ Interactive examples
- ✨ Video tutorials
#### Enhanced Documentation

- ✨ Performance documentation
- ✨ Optimization recommendations
- ✨ Comparison with other libraries
- ✨ Performance regression testing
- ✨ Benchmark suite for common operations
#### Performance Benchmarks

- ✨ Edge case handling
- ✨ Resource cleanup verification
- ✨ Connection pool optimization
- ✨ Memory leak analysis and fixes
- ✨ Extensive load testing
#### Production Hardening

- ✨ Deprecation warnings
- ✨ Migration guides between versions
- ✨ Version-specific models and endpoints
- ✨ Version negotiation and fallback
- ✨ Support multiple wFirma API versions
#### API Versioning Support

### Features

- Performance benchmarks
- Comprehensive documentation
- Long-term support commitment
- Production-ready stability
### Goals

**Target Release**: Q4 2026
**Status**: 📋 Planned  

## Version 1.0.0 (Stable Release)

---

- ✨ Health check endpoints
- ✨ Performance profiling tools
- ✨ Structured logging with correlation IDs
- ✨ Metrics collection (request counts, latencies, errors)
- ✨ OpenTelemetry integration
#### Monitoring & Observability

- ✨ SQL-like or GraphQL-inspired syntax (if beneficial)
- ✨ Query composition and reuse
- ✨ Advanced sorting and pagination
- ✨ Type-safe filtering
- ✨ Fluent API for building complex queries
#### Query Builder

- ✨ Plugin documentation and examples
  - Custom serializers
  - Event listeners
  - Response transformers
  - Custom authentication providers
- ✨ Example plugins:
- ✨ Plugin discovery and loading
- ✨ Plugin interface definition
#### Plugin Architecture

- ✨ Per-resource middleware configuration
- ✨ Middleware chaining and ordering
- ✨ Custom middleware support
- ✨ Built-in middleware: logging, timing, debugging
- ✨ Middleware architecture for request processing
#### Request/Response Middleware

- ✨ Rate limit statistics and reporting
- ✨ Multi-threaded/async rate limit coordination
- ✨ Rate limit prediction and queuing
- ✨ Adaptive rate limiting based on API responses
#### Rate Limiting Intelligence

### Features

- Enhanced debugging and monitoring
- Plugin architecture
- Advanced API features
### Goals

**Target Release**: Q3 2026
**Status**: 📋 Planned  

## Version 0.3.0 (Advanced Features)

---

- ✨ Error aggregation for bulk operations
- ✨ Detailed error context and suggestions
- ✨ Circuit breaker pattern for failing endpoints
- ✨ Automatic retry with exponential backoff (already planned)
#### Enhanced Error Handling

- ✨ Example webhook server (Flask/FastAPI)
- ✨ Webhook handler utilities
- ✨ Event payload parsing
- ✨ Webhook signature verification
#### Webhook Support

- ✨ Error handling for partial failures
- ✨ Progress tracking for bulk operations
- ✨ Bulk delete with confirmation
- ✨ Bulk update with batch support
- ✨ Optimized bulk create operations
#### Bulk Operations

- ✨ Cache bypass options
- ✨ TTL configuration per resource type
- ✨ Cache invalidation strategies
- ✨ Configurable cache backends (memory, Redis, file)
- ✨ Optional response caching layer
#### Response Caching

- ✨ Test data factory for realistic scenarios
- ✨ CI configuration for optional integration runs
- ✨ Integration test documentation
- ✨ Credential management for sandbox testing
- ✨ Optional integration tests against wFirma sandbox
#### Integration Tests (Phase 3.C)

### Features

- Enhanced developer experience
- Performance optimization
- Integration testing against real API
### Goals

**Target Release**: Q2 2026
**Status**: 📋 Planned  

## Version 0.2.0 (Integration & Optimization)

---

- 🚧 CI/CD pipeline
- 🚧 Usage examples
- 🚧 Sphinx documentation
- 🚧 Pagination helpers
  - Employees
  - Warehouse
  - Payments
  - Invoices
  - Goods
  - Contractors
  - Company/Settings
- 🚧 Resource implementations:
- 🚧 Base HTTP client (sync/async)
- 🚧 OAuth authentication (sync/async)
- 🚧 Pydantic data models (with pydantic-xml)
- 🚧 Configuration management
- 🚧 Exception hierarchy
- 🚧 API documentation scraping
- ✅ Project setup and infrastructure
### Features

- Basic examples and usage guides
- Complete API documentation
- Comprehensive test coverage (>90%)
- Full synchronous and asynchronous support
- Core API functionality for all major resources
### Goals

**Target Release**: Q1 2026
**Status**: 🚧 In Progress  

## Version 0.1.0 (Current - In Development)

---

**Last Updated**: 2026-01-16
**Current Version**: 0.1.0  

This document outlines planned features and enhancements for future versions of python-wfirma.


