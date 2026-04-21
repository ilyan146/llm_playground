from loguru import logger

from .clients import get_clients
from .config import COMPILE_COMMAND, LANGUAGE
from .system_info import retrieve_system_info, rust_toolchain_info

_system_info = retrieve_system_info()
_rust_info = rust_toolchain_info()

SYSTEM_PROMPT = f"""
Your task is to convert Python code into high performance {LANGUAGE} code.
Respond only with {LANGUAGE} code. Do not provide any explanation other than occasional comments.
The {LANGUAGE} response needs to produce an identical output in the fastest possible time.
"""


def _user_prompt(python: str) -> str:
    return f"""
Port this Python code to {LANGUAGE} with the fastest possible implementation that produces identical output in the least time.
The system information is:
{_system_info}
The Rust toolchain information is:
{_rust_info}
Your response will be written to a file called main.{LANGUAGE} and then compiled and executed; the compilation command is:
{COMPILE_COMMAND}
Respond only with {LANGUAGE} code.
Python code to port:

```python
{python}
```
"""


def port(model: str, python: str) -> str:
    client = get_clients()[model]
    logger.info(f"Using model {model} with client {client}")
    kwargs: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _user_prompt(python)},
        ],
    }
    if "gpt-5" in model:
        kwargs["reasoning_effort"] = "high"
    response = client.chat.completions.create(**kwargs)
    reply = response.choices[0].message.content
    return reply.replace("```cpp", "").replace("```rust", "").replace("```", "")
