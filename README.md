# ChefGenie AI 🍳

ChefGenie is a recipe-generation application that uses a locally hosted language model to create recipes based on available ingredients and user preferences.

## Features

- Generate recipes from available ingredients
- Choose cuisine and meal type
- Specify dietary preferences
- Select the number of servings
- Set a maximum cooking-time limit
- Display generated recipes with ingredients and instructions
- Basic cooking-time validation and error handling

## Tech Stack

- Python
- Streamlit
- Ollama
- Qwen2.5 3B
- Requests

## How It Works

1. The user enters ingredients and selects recipe preferences.
2. The application creates a prompt from the selected inputs.
3. Ollama sends the prompt to the Qwen2.5 3B language model.
4. The generated recipe is displayed in the Streamlit interface.

## Run Locally

1. Install Python and Ollama.
2. Download the model:

   ollama pull qwen2.5:3b

3. Install dependencies:

   pip install -r requirements.txt

4. Start the application:

   streamlit run app.py

## Note

Ollama must be running locally for recipe generation to work. Public cloud deployment requires an accessible model-serving setup.

## Disclaimer

Generated recipes may contain inaccurate ingredients, quantities, or cooking instructions. Always verify food safety and dietary suitability.
