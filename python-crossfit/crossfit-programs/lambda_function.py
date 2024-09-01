import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def fetch_latest_workout():
    today_date = datetime.now().strftime('%y%m%d')
    url = f'https://www.crossfit.com/{today_date}'
    
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

def lambda_handler(event, context):
    try:
        html_content = fetch_latest_workout()
        workout = parse_workout(html_content)
        return {
            'statusCode': 200,
            'body': json.dumps(workout),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
