```py
from typing import Generic, TypeVar
from typing_extensions import TypedDict


# Define a base TypedDict for the required 'shared_field' field
class RequiredBody(TypedDict):
    shared_field: str


# Create a generic TypeVar for custom message bodies
Body = TypeVar("Body", bound=TypedDict)


# Define the main RabbitmqMessage as a generic TypedDict
class RabbitmqMessage(TypedDict, Generic[Body]):
    body: Body  # Body must include RequiredBody fields


# Define your specific message body
class SomeMsgBody(RequiredBody):  # Inherits shared_field
    id: str


# Create an instance that satisfies the structure
something: RabbitmqMessage[SomeMsgBody] = {
    "body": {"shared_field": "", "id": ""}  # Required from base  # Specific to SomeMsgBody
}
```
