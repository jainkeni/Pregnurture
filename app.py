# Import the necessary libraries
import openai
from flask import Flask,render_template ,request

# Set your OpenAI API key here
openai.api_key = "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"

# Initialize the Flask app
app = Flask(__name__)

# Function to fetch exercise plan from the OpenAI API
def fetch_exercise_plan(weight, months_pregnant, injuries_details, health_issues_details):
    prompt = f"Pregnant woman with weight {weight} kg and {months_pregnant} months pregnant."

    if health_issues_details:
        prompt += f" Health issues: {health_issues_details}."

    if injuries_details:
        prompt += f" Injuries: {injuries_details}."

    prompt += " Suggest a daily exercise plan for every day of a week."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500,
        stop=None,
        n=1,
        timeout=15,
    )

    return response.choices[0].text.strip()


# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user inputs from the form
        weight = float(request.form['weight'])
        months_pregnant = int(request.form['months_pregnant'])
        health_issues_details = request.form['health_issues_details']
        injuries_details = request.form['injuries_details']

        # Fetch the exercise plan from the OpenAI API
        exercise_plan = fetch_exercise_plan(weight, months_pregnant, injuries_details, health_issues_details)

        if exercise_plan:
            # Display the exercise plan on the result page
            return render_template('result.html', weight=weight, months_pregnant=months_pregnant,
                                   health_issues_details=health_issues_details, injuries_details=injuries_details,
                                   exercise_plan=exercise_plan)
        else:
            return "Failed to fetch the exercise plan. Please try again later."
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
