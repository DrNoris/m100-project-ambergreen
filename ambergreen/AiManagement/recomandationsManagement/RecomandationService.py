from ollama import chat


def getRecomandations(data):
    response = chat(
        model='llama3.2',
        messages=[
            {
                'role': 'user',
                'content': f"{data['month']}: {data['co2_emissions']}."
                           f"Based on this data, identify the categories where the building can improve."
                           f"For each category, suggest actionable steps the building managers can take to reduce its environmental impact, and estimate the potential percentage reduction achievable for each action."
                           f"I want you to format the reponse in this way:"
                           f"Recomandations for energy: "
                           f"..."
                           f"Recomandations for gas: "
                           f"..."
                           f"Recomandations for water: "
                           f"..."
                           f"I dont want you to use any characters like '*', '#'"
                           f"Please provide your suggestions, and begin each one with a - character."
                           f"I dont want you to write anything else after the recomandations such as 'Please note ...'"
                           f"I dont want you to write recomandations for anything else just these 3 categories (energy, gas, water)"
            }
        ],
        options={"stream": False,
                 "temperature": 0}
    )
    return response['message']['content']

