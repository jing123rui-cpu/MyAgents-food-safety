# AI Provider Architecture

## Overview

The AI Provider Framework is a pluggable abstraction layer that allows the Food Audit Agent to use multiple Chinese AI models without changing any business logic.

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                  Application Layer                      鈹?鈹? (CLI, FastAPI, Web UI, Desktop UI, Mobile)              鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                       鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                ProviderManager                          鈹?鈹? (registry, lifecycle, switching, caching)               鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?        鈹?         鈹?         鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈻尖攢鈹€鈹?鈹屸攢鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹?鈹屸攢鈹€鈻尖攢鈹€鈹€鈹€鈹€鈹?鈹屸攢鈹€鈻尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?DeepSeek 鈹?鈹?Qwen   鈹?鈹?GLM    鈹?鈹?Doubao       鈹? 鈫?DISABLED
鈹?(future) 鈹?鈹?(future)鈹?鈹?future)鈹?鈹?(future)     鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

---

## Layer Architecture

### 1. Provider Layer (`script/ai/base.py`)

Abstract base class `AIProvider` defines the contract every provider must implement:

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `initialize()` | 鈥?| `None` | Load config, validate credentials |
| `health()` | 鈥?| `bool` | Ping the provider |
| `chat()` | `AIRequest` | `AIResponse` | Chat completion |
| `analyze_text()` | `str` | `AIResponse` | Analyse audit notes |
| `analyze_image()` | `str` (path) | `ImageAnalysis` | Analyse audit photo |
| `analyze_document()` | `str` (path) | `DocumentAnalysis` | Analyse audit document |
| `generate_report()` | `str` (context) | `ReportDraft` | Draft audit report |

### 2. Schema Layer (`script/ai/schemas.py`)

Pure dataclasses 鈥?no logic:

| Schema | Fields |
|--------|--------|
| `AIMessage` | role, content, metadata |
| `AIRequest` | messages, system_prompt, temperature, max_tokens, model |
| `AIResponse` | content, model, usage, finish_reason |
| `ImageAnalysis` | checkpoint_id, description, findings, risk_level, confidence |
| `DocumentAnalysis` | checkpoint_id, summary, key_points, compliance_issues, confidence |
| `ReportDraft` | title, summary, sections, recommendations |
| `PromptTemplate` | template, variables, description |

### 3. Registry Layer (`script/ai/registry.py`)

`ProviderRegistry` maps provider names to provider classes. The default provider is `"deepseek"`. All providers are registered as `"DISABLED"` 鈥?no SDK import, no API call.

### 4. Manager Layer (`script/ai/provider.py`)

`ProviderManager` is the runtime facade:

```python
manager = ProviderManager()
manager.register("deepseek", DeepSeekProvider)   # future
provider = manager.get_provider("deepseek")       # None today
```

### 5. Prompt Layer (`script/ai/prompts.py`)

Placeholder builders that will construct structured prompts when providers are integrated:

| Builder | Purpose |
|---------|---------|
| `build_checkpoint_prompt()` | Evaluate a single checkpoint against evidence |
| `build_image_prompt()` | Analyse an audit photograph |
| `build_document_prompt()` | Analyse a scanned document |
| `build_report_prompt()` | Draft a full audit report |

### 6. Exception Layer (`script/ai/exceptions.py`)

| Exception | When Raised |
|-----------|-------------|
| `AIProviderError` | Base 鈥?any AI error |
| `ProviderUnavailable` | Provider unreachable or not initialised |
| `PromptError` | Malformed prompt or over length limit |
| `AuthenticationError` | Invalid or missing API credentials |
| `RateLimitError` | Rate limit exceeded |
| `ModelError` | Unexpected model response |

---

## File Structure

```
script/ai/
鈹溾攢鈹€ __init__.py      鈥?Public API exports
鈹溾攢鈹€ base.py          鈥?AIProvider abstract base class
鈹溾攢鈹€ schemas.py       鈥?Dataclass schemas (AIMessage, AIRequest, AIResponse, 鈥?
鈹溾攢鈹€ provider.py      鈥?ProviderManager (register, get, switch, lifecycle)
鈹溾攢鈹€ registry.py      鈥?ProviderRegistry (name 鈫?class mapping, default: deepseek)
鈹溾攢鈹€ prompts.py       鈥?Prompt template builders (placeholders)
鈹斺攢鈹€ exceptions.py    鈥?Error hierarchy (6 classes)
```

---

## Future DeepSeek Integration

When a real provider is added (e.g. DeepSeek):

```python
from core.ai import AIProvider, AIRequest, AIResponse

class DeepSeekProvider(AIProvider):
    provider_name = "deepseek"
    model_name = "deepseek-chat"

    def initialize(self) -> None:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        self.client = OpenAI(base_url="https://api.deepseek.com", api_key=api_key)

    def chat(self, request: AIRequest) -> AIResponse:
        response = self.client.chat.completions.create(...)
        return AIResponse(content=response.choices[0].message.content)
```

Registration:

```python
from core.ai import ProviderManager
manager = ProviderManager()
manager.register("deepseek", DeepSeekProvider)
manager.initialize_provider("deepseek")
```

---

## Model Switching

Providers can be switched at runtime without restarting the agent:

```python
provider_a = manager.get_provider("deepseek")
result_a = provider_a.analyze_text(...)

provider_b = manager.get_provider("tongyi-qwen")
result_b = provider_b.analyze_text(...)
```

---

## Security

- No API keys are stored in the codebase.
- Credentials should be provided via environment variables at deployment.
- The provider framework validates authentication during `initialize()`.
- All provider communication should use HTTPS.

---

## Offline Support

- The provider framework does not require any internet connection to load.
- Providers return meaningful errors when offline (`ProviderUnavailable`).
- The rule engine and evidence engine work entirely offline 鈥?the AI layer enhances but does not replace them.

---

## Provider Lifecycle

```
register(name, class)
       鈹?       鈻?initialize_provider(name)   鈫?ProviderUnavailable if not registered
       鈹?       鈻?  get_provider(name)         鈫?returns cached instance
       鈹?       鈻?  shutdown_all()             鈫?clears all instances
```

---

## Dependency Rule

```
Application Layer
    鈹?    鈻?ProviderManager  鈹€鈹€鈻? AIProvider (abstract)
    鈹?                      鈹?    鈻?                      鈻?ProviderRegistry     DeepSeekProvider (future)
                         鈹?                         鈻?                   openai / httpx (future)
```

No layer depends on a concrete provider. The application only depends on `AIProvider` (the interface). Providers can be added, removed, or swapped without changing any application code.
