# Strawberry + `pydantic.StringConstraints`

Strawberry won't auto-apply pydantic `StringConstraints` supplied via `Annotated[...]` on a scalar mutation arguments. To fix this issue you can define a global validator.

## Run

Any of these work. Pick whichever matches your workflow.

```bash
make init
make start # make test
```

## Tradeoffs

- Doesn't recurse into `@strawberry.input` fields. If you use Annotated metadata on input-type attributes, you'd extend `apply()` to also `TypeAdapter(arg.type)` when arg.type is a strawberry input. Easy addition if you need it.
- Errors surface as GraphQL errors on the field, not as Invalid value during query parsing. That's inherent to doing this at resolve time — Strawberry doesn't expose the metadata at the schema/AST layer, so we can't push it into GraphQL argument coercion.
- The uvicorn console shows a traceback on validation failures because Strawberry logs resolver exceptions; the client still receives a normal GraphQL error entry. Set Schema(config=StrawberryConfig(...)) or a custom error_formatter/process_errors if you want to silence the log.
