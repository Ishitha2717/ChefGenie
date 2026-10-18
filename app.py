
import re
import streamlit as st
from recipe_generator import generate_recipe

st.set_page_config(
    page_title="ChefGenie AI",
    page_icon="🍳",
    layout="centered"
)

st.title("🍳 ChefGenie AI")
st.subheader("Your personal recipe generator")
st.write("Create recipe ideas using ingredients you already have.")

st.divider()

ingredients = st.text_area(
    "🥕 Available ingredients",
    placeholder="e.g. chicken, rice, onion"
)

col1, col2 = st.columns(2)

with col1:
    cuisine = st.selectbox(
        "🌎 Cuisine",
        ["Any", "Indian", "Italian", "Chinese", "Mexican", "Continental"]
    )

    meal_type = st.selectbox(
        "🍽️ Meal type",
        ["Any", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]
    )

with col2:
    dietary_preference = st.selectbox(
        "🥗 Dietary preference",
        ["None", "Vegetarian", "Vegan", "Gluten-free", "High-protein"]
    )

    servings = st.number_input(
        "👥 Number of servings",
        min_value=1,
        max_value=20,
        value=2
    )

cooking_time = st.slider(
    "⏱️ Maximum cooking time (minutes)",
    min_value=10,
    max_value=120,
    value=30,
    step=5
)


def extract_time(text, label):
    pattern = (
        rf"{label}\s*:\s*(\d+)\s*"
        rf"(minutes?|mins?|hours?|hrs?)?"
    )
    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return None

    value = int(match.group(1))
    unit = (match.group(2) or "minutes").lower()

    if unit.startswith("hour") or unit.startswith("hr"):
        value *= 60

    return value


if st.button("✨ Generate Recipe", use_container_width=True):
    if not ingredients.strip():
        st.warning("Please enter your available ingredients.")
    else:
        try:
            with st.spinner("ChefGenie is creating your recipe..."):
                recipe = generate_recipe(
                    ingredients=ingredients.strip(),
                    cuisine=cuisine,
                    meal_type=meal_type,
                    dietary_preference=dietary_preference,
                    servings=int(servings),
                    cooking_time=cooking_time
                )

            st.subheader("🍽️ Your Generated Recipe")
            st.markdown(recipe)

            prep_time = extract_time(recipe, "Preparation Time")
            recipe_cook_time = extract_time(recipe, "Cooking Time")

            if prep_time is not None and recipe_cook_time is not None:
                total_time = prep_time + recipe_cook_time

                st.caption(
                    f"Reported preparation + cooking time: "
                    f"{total_time} minutes"
                )

                if total_time > cooking_time:
                    st.warning(
                        "The recipe's reported preparation and cooking "
                        "times exceed your selected limit. Please review "
                        "the recipe before cooking."
                    )
                else:
                    st.success(
                        "The reported total time fits your selected limit."
                    )
            else:
                st.warning(
                    "Could not verify the total time because the recipe "
                    "did not provide clearly labelled preparation and "
                    "cooking times."
                )

            st.info(
                "Food safety: Verify ingredient quantities, cooking times, "
                "internal temperatures, and dietary suitability before "
                "cooking. Generated recipes may contain inaccurate "
                "information."
            )

        except Exception as error:
            st.error(f"Recipe generation failed: {error}")
