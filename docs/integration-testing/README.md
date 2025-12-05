# Integration Testing

- When `pytest` runs a test case or another fixture, it looks at the argument names of that function/method, for each argument, `pytest` tries to find a fixture with exactly the same name as the argument. E.g. here, `test_example` receives the value 123 because there's a fixture named `foo`, and `pytest` matches the argument `foo` in `test_example` to the fixture name:

  ```py
  @pytest.fixture
  def foo():
      return 123

  def test_example(foo):
      assert foo == 123
  ```

## [Mock gRPC API](./mock-grpc-api/README.md).

## [Testcontainers](https://testcontainers.com/)

### [Mock RabbitMQ](./rabbitmq-testcontainers/README.md).

### [Mocked RESTful API + RabbitMQ](./wiremock-and-rabbitmq-testcontainers/README.md)
