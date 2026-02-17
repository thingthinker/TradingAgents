import os
from typing import Any, Optional

from langchain_aws import ChatBedrockConverse

from .base_client import BaseLLMClient
from .validators import validate_model


class BedrockClient(BaseLLMClient):
    """Client for AWS Bedrock models (Claude, Llama, Mistral, etc.)."""

    def __init__(self, model: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(model, base_url, **kwargs)

    def get_llm(self) -> Any:
        """Return configured ChatBedrockConverse instance.

        Authentication uses the standard boto3 credential chain:
          - Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
          - AWS config/credentials files (~/.aws/credentials)
          - IAM role (EC2/ECS/Lambda)
          - SSO session

        Set AWS_DEFAULT_REGION or pass region_name in kwargs.
        """
        llm_kwargs = {"model": self.model}

        region = self.kwargs.get("region_name") or os.environ.get(
            "AWS_DEFAULT_REGION", "us-east-1"
        )
        llm_kwargs["region_name"] = region

        for key in (
            "credentials_profile_name",
            "max_tokens",
            "temperature",
            "top_p",
            "callbacks",
        ):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        return ChatBedrockConverse(**llm_kwargs)

    def validate_model(self) -> bool:
        """Validate model for Bedrock."""
        return validate_model("bedrock", self.model)
