from app.config import settings


class LLMService:
    def generate(self, prompt: str) -> str:
        if settings.llm_mode == "mock":
            return f"[MOCK_LLM_RESPONSE]\n{prompt[:500]}"

        # MVP 简化：保留接口，不强依赖 openai sdk
        # 你后续可改为 httpx 调 OpenAI-compatible API
        return f"[OPENAI_COMPAT_PLACEHOLDER]\n{prompt[:500]}"
