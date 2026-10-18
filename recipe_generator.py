
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def generate_recipe(
    ingredients,
    cuisine="Any",
    meal_type="Any",
    dietary_preference="None",
    servings=2,
    cooking_time=30,
):
    if not ingredients.strip():
        return "Please enter at least one ingredient."

    prompt = f"""
You are ChefGenie, a helpful recipe assistant.

Create ONE practical recipe using these requirements.

Available ingredients: {ingredients}
Cuisine: {cuisine}
Meal type: {meal_type}
Dietary preference: {dietary_preference}
Servings: {servings}
Maximum total cooking time: {cooking_time} minutes

Follow these rules:
1. Give a suitable recipe name.
2. List ingredients with quantities for exactly {servings} servings.
3. Give numbered cooking instructions.
4. Keep the estimated total preparation and cooking time within
   {cooking_time} minutes, if feasible.
5. Respect the requested cuisine and dietary preference.
6. Do not include unrelated recipes, advertisements, or nutrition claims.
7. If the requirements cannot reasonably be met, explain why.
8. Do not claim that the recipe is guaranteed safe.

Use this exact format:

Recipe Name:
Preparation Time:
Cooking Time:
Servings:
Ingredients:
Instructions:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.8,
            "top_k": 50,
            "num_predict": 500,
        },
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=180,
        )
        response.raise_for_status()

        result = response.json().get("response", "").strip()

        if not result:
            return "No recipe was generated. Please try again."

        return result

    except requests.exceptions.ConnectionError:
        return (
            "Cannot connect to Ollama. "
            "Make sure the Ollama service is running."
        )

    except requests.exceptions.Timeout:
        return "Recipe generation timed out. Please try again."

    except requests.exceptions.RequestException as error:
        return f"Recipe generation failed: {error}"
