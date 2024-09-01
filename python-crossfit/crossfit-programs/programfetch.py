import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
def fetch_latest_workout():
    today_date = datetime.now().strftime('%y%m%d')
    url = f'https://www.crossfit.com/240831'
    
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'utf-8'  
        return response.text
    else:
        raise Exception(f"Failed to fetch the workout page. Status code: {response.status_code}")

def parse_workout(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    article = soup.find('article')
    
    if article:
        paragraphs = []
        for element in article.find_all(['p', 'br']):
            if element.name == 'p':
                if element.find('strong'):
                    paragraphs.append({"type": "strong", "text": element.get_text(strip=True)})
                else:
                    paragraphs.append({"type": "normal", "text": element.get_text(strip=True)})
            elif element.name == 'br':
                paragraphs.append({"type": "newline"})
        
        workout_data = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "workout_details": paragraphs
        }
        return workout_data
    else:
        raise Exception("Failed to find the workout article in the HTML content.")

@app.route('/api/workout', methods=['GET'])
def get_workout():
    try:
        html_content = fetch_latest_workout()
        workout = parse_workout(html_content)
        return jsonify(workout)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
