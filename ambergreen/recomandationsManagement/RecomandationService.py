from ollama import chat

class RecomandationService:
    def getRecomandations(self, data):
        response = chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'user',
                    'content': f"{data['year']}, {data['building']}: {data['consumption']}."
                               f"Based on this data, identify the categories where the building can improve."
                               f"For each category, suggest actionable steps the company can take to reduce its environmental impact, and estimate the potential percentage reduction achievable for each action."
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
                }
            ],
            options={"stream": False,
                     "temperature": 0.2}
        )
        return response['message']['content']