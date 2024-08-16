import streamlit as st
import anthropic

# Load the API key from Streamlit secrets
api_key = st.secrets["CLAUDE_API_KEY"]

client = anthropic.Anthropic(api_key=api_key)

def meal_plan_generate(fasting_sugar_level, pre_meal_sugar, post_meal_sugar, dietary_preferences):
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=808,
        temperature=0.2,
        system=f"You are a helpful medical assistant that takes the sugar levels of diabetic patient as input and recommends them food and recipes to eat in that day according to their sugar levels. Based on the users {fasting_sugar_level} and {pre_meal_sugar} and {post_meal_sugar}. Also take in accordance the dietary preferences which are {dietary_preferences}",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Task: recommend me to eat some food recipes based on my {fasting_sugar_level}, {pre_meal_sugar}, and {post_meal_sugar}. Also take into consideration my dietary preferences which are {dietary_preferences}\n\nConsiderations:\nConsider the user's fasting, pre-meal, and post-meal sugar levels.\nTake into account the user's dietary preferences.\nIncorporate the user's health goals into the recommendations.\nEnsure nutritional balance in the suggested food options.\nConsider portion sizes and provide personalized recommendations.\n"
                    }
                ]
            }
        ]
    )

    raw_context = message.content
    itinerary = raw_context[0].text
    return itinerary

def main():
    st.set_page_config(page_title="GlucoGuide", layout="wide")
    st.title("GlucoGuide")
    st.markdown("*GlucoGuide* is an innovative app designed to help you maintain a healthy lifestyle by providing personalized meal suggestions based on your sugar levels. Whether you are managing diabetes or simply aiming to improve your overall well-being, Gluco Guide is here to support you on your journey.")

    with st.container():
        st.subheader("How to Use")
        st.write("To get started with Gluco Guide, simply input your sugar levels using a glucose monitoring device or manually enter the readings. You can specify whether your sugar levels are fasting, pre-meal, or post-meal measurements. Additionally, the app allows you to provide information about your dietary preferences, such as vegetarian, vegan, or specific dietary restrictions.")
        st.write("Based on this information, Gluco Guide will generate meal recommendations that align with your dietary preferences, ensuring a balanced and enjoyable eating experience. Experience the convenience of having a personal health coach in your pocket with Gluco Guide. Take control of your health and make informed choices to achieve your wellness goals.")
        st.warning(":warning: Disclaimer: Gluco Guide's AI-generated meal suggestions are intended to support your health journey, but always consult with healthcare professionals for personalized medical advice and guidance regarding your specific condition and dietary needs.")

    with st.sidebar:
        st.header("Controls")
        st.write("Please provide your sugar levels and dietary preferences below to receive personalized meal suggestions tailored to your needs")
        sugar_level_before_fasting = st.text_area("Fasting: Measure your sugar level before having any food or drinks in the morning, typically after an overnight fast.", height=20)
        sugar_level_after_fasting = st.text_area("Pre-Meal: Measure your sugar level before a meal, ideally around 1-2 hours prior to eating.", height=20)
        sugar_level_post_meal = st.text_area("Post-Meal: Measure your sugar level after a meal, typically around 1-2 hours after finishing your meal.", height=20)
        dietary_preferences = st.text_area("Provide information about your dietary preferences, such as vegetarian, vegan, or specific dietary restrictions.", height=20)

        generate_plan_btn = st.button("Generate Meal Plan")

    if generate_plan_btn and sugar_level_after_fasting and sugar_level_before_fasting and dietary_preferences:
        with st.spinner("Creating a Meal Plan..."):
            generated_mealplan = meal_plan_generate(sugar_level_before_fasting, sugar_level_after_fasting, sugar_level_post_meal, dietary_preferences)
            st.subheader("Meal Plan:")
            st.markdown(generated_mealplan)

if __name__ == "__main__":
    main()
