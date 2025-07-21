# Changelog

All notable changes to this project will be documented in this file.


## [v1.0.8] - 2025-07-21
### Added
- Support for testing environments.
- Observability tooling with Prometheus and Grafana.

### Fixed
- Fallback to local database when deployed DB is unavailable.
- Main application now supports local execution.
- Instrumentator updated for improved metrics tracking.
- Enhanced environment support for both local and deployed setups.

---

## [v1.0.7] - 2025-07-13
### Fixed
- Corrected HTTP `Bearer` usage in authentication headers.

### Added
- MongoDB integration as the main database.
- Updated `config.py` with environment-related changes.

### Changed
- Refactored request and response schemas for consistency.
- Improved API documentation.

---

## [v1.0.6] - 2025-07-12
### Changed
- Separated user logic from endpoints.
- Separated authentication logic and response builders for better modularity.

### Added
- New `verify-token` endpoint to allow inter-service validation.

---

## [v1.0.5] - 2025-07-10
### Fixed
- Corrected the response model for the `DELETE` endpoint.

### Added
- Implemented user deletion endpoint.

---

## [v1.0.4] - 2025-07-10
### Added
- Reset password flow using SMTP and Gmail.
- Reset email rendering via templates.
- Custom email styles for password reset.

---

## [v1.0.3] - 2025-07-10
### Added
- Data validation with custom validators for user and auth input.
- Exception handlers to sanitize and standardize validation error responses.

---

## [v1.0.2] - 2025-07-10
### Added
- Token revocation logic and logout endpoint.

---

## [v1.0.1] - 2025-07-10
### Added
- Password management endpoints, including password reset with a new token type.

---

## [v1.0.0] - 2025-07-10
### Added
- Initial project structure using FastAPI.
- Basic authentication logic: registration and login.
- Profile endpoints: retrieve and update user data using token-based authentication.
- CI setup with `branch_protection.yml` and `branch_validation.yml`.

---