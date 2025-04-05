import os
from flask import Flask, render_template, request
from langchain_community.document_loaders import WebBaseLoader
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.form['url']
    try:
        # Load webpage content
        loader = WebBaseLoader([url])
        webpage_data = loader.load().pop().page_content

        # Generate summary
        prompt = f"""
        Summarise the following webpage content in short:
        {webpage_data}
        """
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        summary = response.text
        return render_template('result.html', summary=summary, url=url)
    
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
