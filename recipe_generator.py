
import os
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"

GEMINI_MODEL = "gemini-3.8-flash"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)


def get_gemini_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        import streamlit as st
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""


def generate_recipe(
    ingredients,
    cuisine="Any",
    meal_type="Any",
    dietary_preference="None",
    servings=2,
    cooking_time=30,
):
    if not ingredients or not ingredients.strip():
        return "Please enter at least one ingredient."

    prompt = f"""
You are ChefGenie, a helpful recipe assistant.

Create ONE practical recipe using these requirements.

Available ingredients: {ingredients}
Cuisine: {cuisine}
Meal type: {meal_type}
Dietary preference: {dietary_preference}
Servings: {servings}
Maximum total preparation and cooking time: {cooking_time} minutes

Rules:
1. Give a suitable recipe name.
2. List ingredients with quantities for the requested servings.
3. Give numbered cooking instructions.
4. Provide separate preparation and cooking times.
5. Try to respect the requested time limit.
6. Respect the cuisine and dietary preferences.
7. Do not include unrelated recipes.
8. Do not claim the recipe is guaranteed safe.

Use this format:

Recipe Name:
Preparation Time:
Cooking Time:
Servings:
Ingredients:
Instructions:
"""

    api_key = get_gemini_api_key()

    try:
        if api_key:
            return generate_with_gemini(prompt, api_key)

        return generate_with_ollama(prompt)

    except requests.exceptions.HTTPError as error:
        status = error.response.status_code if error.response is not None else 0

        if status == 401:
            return (
                "Gemini authentication failed (401). Check that the "
                "GEMINI_API_KEY secret is valid and active."
            )

        if status == 403:
            return (
                "Gemini access denied (403). Check API permissions "
                "and project access."
            )

        if status == 404:
            return (
                f"Gemini returned 404 for model {GEMINI_MODEL}. "
                "Check whether the model is available to your API key."
            )

        if status == 429:
            return (
                "Gemini usage limit reached. Please wait and try again."
            )

        return f"Recipe service returned HTTP {status}."

    except requests.exceptions.ConnectionError:
        return (
            "Cannot connect to the recipe-generation service. "
            "Check your internet connection or make sure Ollama "
            "is running for local generation."
        )

    except requests.exceptions.Timeout:
        return "Recipe generation timed out. Please try again."

    except requests.exceptions.RequestException:
        return "A network error occurred during recipe generation."

    except (KeyError, IndexError, TypeError, ValueError):
        return (
            "The model returned an unexpected response. "
            "Please try generating the recipe again."
        )


def generate_with_gemini(prompt, api_key):
    response = requests.post(
        GEMINI_URL,
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        json={
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.8,
                "topK": 50,
                "maxOutputTokens": 500,
            },
        },
        timeout=120,
    )

    response.raise_for_status()
    data = response.json()

    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

    if not text:
        return "No recipe was generated. Please try again."

    return text


def generate_with_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_k": 50,
                "num_predict": 500,
            },
        },
        timeout=180,
    )

    response.raise_for_status()
    result = response.json().get("response", "").strip()

    if not result:
        return "No recipe was generated. Please try again."

    return result
