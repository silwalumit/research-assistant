from typing import Literal

from pydantic import HttpUrl
from pydantic.functional_validators import model_validator

from src.config.base import BaseSettingsModel

LLMProviderLiteral = Literal["Ollama", "Bedrock", "Openai"]


class OllamaLLMSettings(BaseSettingsModel):
    model_name: str = "mistral:7b"
    base_uri: HttpUrl


class OpenAILLMSettings(BaseSettingsModel):
    api_key: str
    model_name: str


class BedrockLLMSettings(BaseSettingsModel):
    model_arn: str
    credential_profile_name: str


class LLMSettings(BaseSettingsModel):
    ollama: OllamaLLMSettings | None = None
    openai: OpenAILLMSettings | None = None
    bedrock: BedrockLLMSettings | None = None

    @model_validator(mode="after")
    def ensure_one_config_provided(self):
        if not any([self.ollama, self.openai, self.bedrock]):
            raise ValueError("At least one LLM config should be provided")
        return self
