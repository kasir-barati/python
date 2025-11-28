# Mock gRPC API -- Integration Testing

Here is how you might wanna mock a gRPC API.

## How to Start it

1. `cd python/docs/integration-testing/mock-grpc-api`.
2. `make init`.
3. `make test`.

## Fixtures

I am auto loading all fixtures here to make adding new fixtures easier, but keeep in mind that your fixture file name should be like: `*_fixture.py`.

### Fixture Loading and Execution Timing

Fixtures are **NOT** loaded at the beginning and cached forever. Fixtures in pytest have scope and lifecycle:

- `function` scope (default): Created/destroyed for each test function.
- `class` scope: Created once per test class.
- `module` scope: Created once per test file.
- `session` scope: Created once per entire test session.
