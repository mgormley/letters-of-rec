import litellm
from litellm import completion

litellm.drop_params = True

def call_llm(
    messages: list,
    model: str = "gpt-5.1",
    temperature: float = 1.0,
) -> str:
    """Vendor-agnostic LLM call."""
    resp = completion(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]