# Discriminated Unions

<table>
<thead><tr>
<th width="50%">Before</th>
<th width="50%">After</th>
</tr></thead>
<tbody><tr>
<td markdown="1" valign="top">One class, every variant's fields optional, matched by a string.</td>
<td markdown="1" valign="top">One class per variant, each with its own required fields.</td></tr>
<tr><td markdown="1" valign="top">

```py
from typing import Literal

from pydantic import BaseModel


class Settings(BaseModel):
    provider: Literal["bedrock", "anthropic"]
    bedrock: "BedrockConfig | None" = None
    anthropic: "AnthropicConfig | None" = None


class BedrockConfig(BaseModel):
    region: str


class AnthropicConfig(BaseModel):
    api_key: str


def build_before(settings: Settings) -> str:
    match settings.provider:
        case "bedrock":
            return settings.bedrock.region  # error: "bedrock" is possibly None
        case "anthropic":
            return settings.anthropic.api_key  # error: "anthropic" is possibly None
```

</td><td markdown="1" valign="top">

```py
class Bedrock(BaseModel):
    provider: Literal["bedrock"] = "bedrock"
    region: str


class Anthropic(BaseModel):
    provider: Literal["anthropic"] = "anthropic"
    api_key: str


type Choice = Bedrock | Anthropic  # in pydantic, add Field(discriminator="provider")


def build_after(choice: Choice) -> str:
    match choice:
        case Bedrock(region=region):
            return region  # str, never None
        case Anthropic(api_key=api_key):
            return api_key
    # No `case _` needed: the checker knows the match is exhaustive.
    # Add a third variant to Choice and it flags this function until handled.
```

</td>
</tr></tbody>
</table>

- Why "before" fails: matching on `settings.provider == "bedrock"` tells the checker nothing about `settings.bedrock`. The string and the optional field are unrelated, so every use needs an assert or a cast.
- Why "after" works: the class is the discriminator. `case Bedrock(region=region)` narrows the type and binds the required field in one step.
- Mismatch with the real code: `Choice` here is a plain union. The repo's `build_model` takes the open base class `ModelChoice`, which is why it ended up with `case _`.

---

X: https://x.com/kasir_barati/status/2124544882291151179
Instagram: https://www.instagram.com/p/DgDPsZKtPFY/?avpt=NTc4MTIwNjQ2YQ==
