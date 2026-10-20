import os
import time
import logging

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLM:
    def __init__(self):
        """Initialize the Gemini language model."""

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Please add it to your .env file."
            )

        self.client = genai.Client(api_key=api_key)

        # Keep the model configured for this project.
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash",
        )

    def generate(self, prompt, max_retries=3):
        """
        Generate a response using Gemini.

        Retries temporary server errors and rate limits.
        Returns the generated text when successful.
        """

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )

                if response is None or not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return response.text.strip()

            except errors.APIError as exc:
                status_code = getattr(exc, "code", None)

                # Retry temporary server errors and rate limits.
                retryable = status_code in (429, 500, 502, 503, 504)

                if not retryable:
                    logger.error(
                        "Gemini API error: %s",
                        exc,
                    )
                    raise

                if attempt == max_retries - 1:
                    logger.error(
                        "Gemini remained unavailable after %s attempts.",
                        max_retries,
                    )
                    raise

                wait_seconds = 2 ** (attempt + 1)

                logger.warning(
                    "Gemini returned HTTP %s. "
                    "Retrying in %s seconds (attempt %s/%s).",
                    status_code,
                    wait_seconds,
                    attempt + 1,
                    max_retries,
                )

                time.sleep(wait_seconds)

            except (TimeoutError, ConnectionError) as exc:
                if attempt == max_retries - 1:
                    logger.error(
                        "Gemini connection failed after retries: %s",
                        exc,
                    )
                    raise

                wait_seconds = 2 ** (attempt + 1)

                logger.warning(
                    "Connection problem. Retrying in %s seconds.",
                    wait_seconds,
                )

                time.sleep(wait_seconds)

        raise RuntimeError(
            "Unable to generate a response after multiple attempts."
        )


# Optional alias for projects that import GeminiLLM.
GeminiLLM = LLM