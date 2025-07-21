# Python + gRPC

1. `make venv`
2. `make grpc_gen`.
3. ```bash
   make start_server
   make start_client
   ```

> [!TIP]
>
> ```bash
> python -m grpc_tools.protoc -I src/protobufs \
>   --pyi_out=src/stubs \
>   --python_out=src/stubs \
>   --grpc_python_out=src/stubs \
>   src/protobufs/*.proto
> ```
>
> - Generates Python code from the protobufs by running the protobuf compiler.
> - `python -m grpc_tools.protoc`: will generate Python code from the protobuf code.
> - `-I src/protobufs`: where to find files that your protobuf code imports.
> - `--pyi_out=src/stubs` will auto generate classes and types you need.
> - `--python_out=src/stubs --grpc_python_out=src/stubs`: where to output the Python files.
> - `src/protobufs/*.proto`: the path to the protobuf file.

> [!CAUTION]
>
> - All fields in proto3 are optional, so you’ll need to validate that they’re all set. If you leave one unset, then it'll default to zero for numeric types or to an empty string for strings. And will be skipped when being sent over the wire.
> - You should validate that all the fields have good data. This is always true for any server regardless of whether you use protobufs, JSON, or anything else. Always validate input.
