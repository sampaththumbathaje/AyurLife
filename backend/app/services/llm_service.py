"""
llm_service.py
--------------

Service layer for Large Language Model (LLM) integration
using Ollama with the Phi model.

Used to:
- Generate human-like chatbot responses
- Explain remedies, precautions, and Ayurveda concepts
- Enhance conversational experience (non-diagnostic)

Model:
- phi (via Ollama)
"""

import subprocess
import json


# -----------------------------
# Ollama Configuration
# -----------------------------
OLLAMA_MODEL = "phi"


# -----------------------------
# Core LLM Call
# -----------------------------
def call_ollama(prompt: str, temperature: float = 0.4) -> str:
    """
    Calls Ollama CLI with the Phi model.

    Parameters
    ----------
    prompt : str
        Prompt to send to the LLM
    temperature : float
        Controls creativity (lower = more factual)

    Returns
    -------
    str
        Generated text response
    """

    try:
        process = subprocess.run(
            [
                "ollama",
                "run",
                OLLAMA_MODEL
            ],
            input=prompt,
            text=True,
            capture_output=True,
            check=True
        )

        return process.stdout.strip()

    except Exception as e:
        return (
            "I'm having trouble generating a response right now. "
            "Please try again later."
        )


# -----------------------------
# Prompt Builders
# -----------------------------
def build_chat_prompt(user_message: str, context: str = None) -> str:
    """
    Builds a safe, controlled prompt for the chatbot.

    Ensures:
    - No medical diagnosis
    - Ayurveda-only explanations
    - Friendly tone

    Parameters
    ----------
    user_message : str
        Raw user input
    context : str, optional
        Extra context (e.g., ML prediction)

    Returns
    -------
    str
        Prompt for LLM
    """

    system_prompt = (
        "You are an Ayurvedic wellness assistant. "
        "Do not provide medical diagnosis. "
        "Only explain Ayurvedic concepts, remedies, and precautions "
        "in a friendly and simple manner."
    )

    full_prompt = system_prompt + "\n\n"

    if context:
        full_prompt += f"Context: {context}\n\n"

    full_prompt += f"User: {user_message}\nAssistant:"

    return full_prompt


# -----------------------------
# Public Service APIs
# -----------------------------
def generate_chat_response(user_message: str, context: str = None) -> str:
    """
    Generates a human-like chatbot response.

    Used by:
    - chatbot_controller
    """

    prompt = build_chat_prompt(user_message, context)
    return call_ollama(prompt)


def explain_remedy(remedy_name: str, uses: list, precautions: list) -> str:
    """
    Generates a natural-language explanation of a remedy.

    Used after ML prediction.
    """

    prompt = (
        f"Explain the Ayurvedic remedy '{remedy_name}'.\n"
        f"Uses: {', '.join(uses)}.\n"
        f"Precautions: {', '.join(precautions)}.\n"
        "Explain in simple, friendly language."
    )

    return call_ollama(prompt)


def explain_prakriti(prakriti_type: str) -> str:
    """
    Explains Prakriti in simple language.
    """

    prompt = (
        f"Explain the Ayurvedic body constitution '{prakriti_type}' "
        "and give general lifestyle advice in simple terms."
    )

    return call_ollama(prompt)
