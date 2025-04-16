from quart import Quart, render_template, request
from dotenv import load_dotenv
import markdown2
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI()

app = Quart(__name__)

@app.route('/', methods=['GET'])
async def index():
    return await render_template('trip.html', assistant_reply="")

@app.route('/chat', methods=['POST'])
async def chat():
    try:
        # Get user input from the form
        form_data = await request.form
        destination = form_data['destination']
        time_of_year = form_data['time_of_year']

        # Structured prompt for trip planning
        prompt = (
            f"I'm planning a trip to {destination} during {time_of_year}. "
            "Can you suggest some fun activities, must-see attractions, and good places to eat?"
        )

        # Get OpenAI response
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        assistant_response = response.choices[0].message.content

        # Convert markdown to HTML
        assistant_html = markdown2.markdown(assistant_response)

        return await render_template('trip.html', assistant_reply=assistant_html)

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return await render_template("trip.html", assistant_reply="Something went wrong, please try again.")

if __name__ == "__main__":
    app.run(debug=True)