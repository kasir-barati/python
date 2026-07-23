"""
Enforces pydantic `Annotated[T, ...]` metadata (StringConstraints, EmailStr, Field, AfterValidator, ...) on every resolver argument — including fields of `@strawberry.input` objects — without requiring custom scalar types.

Wire it globally via `apply_pydantic_validation(Query, Mutation)` BEFORE constructing `strawberry.Schema`, so no per-field decoration is needed.
"""

from __future__ import annotations

from typing import Annotated, Any, Callable, get_args, get_origin, get_type_hints

from pydantic import TypeAdapter, ValidationError, create_model
from strawberry.extensions.field_extension import FieldExtension
from strawberry.types import Info
from strawberry.types.field import StrawberryField


class PydanticConstraintsExtension(FieldExtension):
    """
    Validate resolver kwargs against their `Annotated[...]` metadata.
    """

    def apply(self, field: StrawberryField) -> None:
        """
        Inspect each argument's annotation.

        If it carries pydantic metadata directly, or is a `@strawberry.input` type whose fields carry pydantic metadata, we build a `TypeAdapter` for it. At resolve time, every incoming kwarg is run through its adapter. `TypeAdapter.validate_python` raises `ValidationError` on violations, which Strawberry surfaces as a GraphQL error — exactly what we want.
        """
        self._validators: dict[str, tuple[TypeAdapter[Any], bool]] = {}
        resolver = field.base_resolver

        if resolver is None:
            return

        try:
            hints = get_type_hints(resolver.wrapped_func, include_extras=True)
        except Exception:
            # Forward refs we can't resolve: skip silently rather than blow up schema construction.
            return

        for arg in field.arguments:
            hint = hints.get(arg.python_name)
            if hint is None:
                continue

            # Case 1: scalar arg with pydantic metadata, e.g. text: Annotated[str, StringConstraints(...)]
            if get_origin(hint) is Annotated:
                _, *meta = get_args(hint)
                if any(_is_pydantic_metadata(m) for m in meta):
                    self._validators[arg.python_name] = (TypeAdapter(hint), False)
                    continue

            # Case 2: arg is a @strawberry.input class whose fields carry pydantic metadata.
            input_cls = _strawberry_input_class(hint)
            if input_cls is not None:
                adapter = _build_input_adapter(input_cls)
                if adapter is not None:
                    self._validators[arg.python_name] = (adapter, True)

    def resolve(
        self,
        next_: Callable[..., Any],
        source: Any,
        info: Info,
        **kwargs: Any,
    ) -> Any:
        return next_(source, info, **self._validate(kwargs))

    async def resolve_async(
        self,
        next_: Callable[..., Any],
        source: Any,
        info: Info,
        **kwargs: Any,
    ) -> Any:
        result = next_(source, info, **self._validate(kwargs))
        # `next_` may or may not return a coroutine.
        if hasattr(result, "__await__"):
            return await result
        return result

    def _validate(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        for name, (adapter, is_input) in self._validators.items():
            if name not in kwargs or kwargs[name] is None:
                continue
            value = kwargs[name]
            try:
                if is_input:
                    # Validate the input object's data, then write the
                    # (potentially coerced) values back onto the same
                    # instance so the resolver still sees its input type.
                    validated_model = adapter.validate_python(_input_as_dict(value))
                    for field_name, field_value in validated_model.model_dump().items():
                        setattr(value, field_name, field_value)
                else:
                    kwargs[name] = adapter.validate_python(value)
            except ValidationError as exc:
                first = exc.errors()[0]
                loc = ".".join(str(p) for p in first["loc"]) or name
                raise ValueError(
                    f"Invalid value for argument '{name}."
                    f"{loc}': {first['msg']}"
                    if is_input
                    else f"Invalid value for argument '{name}': {first['msg']}"
                ) from exc
        return kwargs


def _is_pydantic_metadata(obj: Any) -> bool:
    """
    Anything defined under `pydantic` or `annotated_types` counts as validation metadata worth honouring.
    """
    module = type(obj).__module__ or ""

    return module.startswith("pydantic") or module.startswith("annotated_types")


def _strawberry_input_class(hint: Any) -> type | None:
    """
    Return the underlying class if `hint` refers to a `@strawberry.input`,
    unwrapping `Annotated[...]` if present. Otherwise return None.
    """
    if get_origin(hint) is Annotated:
        hint = get_args(hint)[0]

    if not isinstance(hint, type):
        return None

    definition = getattr(hint, "__strawberry_definition__", None)

    if definition is None:
        return None

    # Strawberry marks input types with `is_input=True` on the definition.
    if not getattr(definition, "is_input", False):
        return None

    return hint


def _build_input_adapter(input_cls: type) -> TypeAdapter[Any] | None:
    """
    Build a `TypeAdapter[dict]` that validates the fields of a
    `@strawberry.input` class using their original `Annotated[...]`
    metadata. Returns None if no field carries pydantic metadata.
    """
    try:
        hints = get_type_hints(input_cls, include_extras=True)
    except Exception:
        return None

    fields: dict[str, Any] = {}
    has_metadata = False

    for name, hint in hints.items():
        # Skip private / dunder / ClassVar-ish attrs (get_type_hints already drops ClassVar in most cases).
        if name.startswith("_"):
            continue

        fields[name] = (hint, ...)

        if get_origin(hint) is Annotated:
            _, *meta = get_args(hint)
            if any(_is_pydantic_metadata(m) for m in meta):
                has_metadata = True

    if not has_metadata:
        return None

    model = create_model(f"{input_cls.__name__}__Validator", **fields)
    # Adapter over the model itself gives us a dict-in / dict-out validator.
    adapter: TypeAdapter[Any] = TypeAdapter(model)

    return adapter


def _input_as_dict(instance: Any) -> dict[str, Any]:
    """
    Best-effort conversion of a @strawberry.input instance to a plain dict of its declared field values.
    """
    if isinstance(instance, dict):
        return instance

    # Strawberry input types are dataclasses under the hood.
    if hasattr(instance, "__dict__"):
        return {k: v for k, v in vars(instance).items() if not k.startswith("_")}

    raise TypeError(f"Cannot extract fields from {instance!r}")


def apply_pydantic_validation(*types: type) -> None:
    """
    Attach `PydanticConstraintsExtension` to every field on the given Strawberry types, in place. Call this before building the schema.

    Usage:
        apply_pydantic_validation(Query, Mutation)
        schema = strawberry.Schema(query=Query, mutation=Mutation)
    """
    seen: set[int] = set()

    def _visit(tp: type) -> None:
        definition = getattr(tp, "__strawberry_definition__", None)

        if definition is None:
            return

        if id(definition) in seen:
            return

        seen.add(id(definition))

        for field in definition.fields:
            # Idempotent: don't stack the same extension on repeat calls.
            if any(
                isinstance(ext, PydanticConstraintsExtension)
                for ext in field.extensions
            ):
                continue

            ext = PydanticConstraintsExtension()
            ext.apply(field)
            field.extensions.append(ext)

    for tp in types:
        _visit(tp)


__all__ = ["PydanticConstraintsExtension", "apply_pydantic_validation"]
