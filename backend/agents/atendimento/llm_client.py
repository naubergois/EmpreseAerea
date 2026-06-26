"""Cliente LLM (DeepSeek API compatível com OpenAI)."""
import logging

import httpx

from config import get_settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Você é o assistente virtual da SkyAgent, companhia aérea brasileira.
Responda sempre em português do Brasil, de forma clara, empática e objetiva.

Você pode ajudar com:
- Status de reservas (PNR)
- Políticas de bagagem, cancelamento e reembolso (ANAC)
- Check-in online (abre 48h antes)
- Documentos para voos internacionais (passaporte 6 meses)
- Programa de milhas (1 milha a cada R$10)
- Alterações e cancelamentos de voo

Se não souber algo ou o cliente estiver muito insatisfeito, diga que vai escalar
para um atendente humano e inclua [ESCALAR] no final da resposta.
NÃO use [ESCALAR] para dúvidas informativas simples (bagagem, milhas, check-in).
Respostas curtas (máximo 3 parágrafos)."""


class LLMClient:
    def __init__(self):
        self.settings = get_settings()
        self._client: httpx.AsyncClient | None = None

    @property
    def enabled(self) -> bool:
        return bool(self.settings.llm_api_key)

    def _get_client(self) -> httpx.AsyncClient:
        """Client assíncrono reutilizado (mantém pool de conexões/TLS)."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.settings.llm_timeout_seconds,
                limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
            )
        return self._client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def chat(self, mensagem: str, contexto: str = "") -> str:
        if not self.enabled:
            raise RuntimeError("LLM_API_KEY não configurada")

        user_content = mensagem
        if contexto:
            user_content = f"Contexto do sistema:\n{contexto}\n\nPergunta do cliente:\n{mensagem}"

        payload = {
            "model": self.settings.llm_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            "temperature": 0.7,
            "max_tokens": 500,
        }
        url = f"{self.settings.llm_base_url.rstrip('/')}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.settings.llm_api_key}",
            "Content-Type": "application/json",
        }

        response = await self._get_client().post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"].strip()


llm_client = LLMClient()
