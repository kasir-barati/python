from strawberry.asgi import GraphQL

from api.src.schema import schema

app = GraphQL(schema)
