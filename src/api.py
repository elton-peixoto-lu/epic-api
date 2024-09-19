from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_status_data():
    """Obtém os dados de status dos serviços da página da Epic Games."""

    url = 'https://status.epicgames.com/'
    response = requests.get(url)
    response.raise_for_status()  # err trative
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    all_components = soup.select('.component-container, .child-components-container > .component-inner-container')

    status_data = []
    for component in all_components:
        name_element = component.find('span', class_='name')
        status_element = component.find('span', class_='component-status')

        if name_element and status_element:
            name = name_element.get_text(strip=True)
            status = status_element.get_text(strip=True)

            is_group = 'is-group' in component.get('class', [])

            if is_group:
                status_data.append({'type': 'group', 'name': name})
            else:
                status_data.append({'type': 'component', 'name': name, 'status': status})

    return status_data

@app.route('/epic-games-status')
def epic_games_status():
    """Endpoint da API que retorna os dados de status em formato JSON."""

    status_data = get_status_data()
    return jsonify(status_data)

if __name__ == '__main__':
    app.run(debug=True)  # Start Flask

    # GET 
    with app.test_client() as client:
        response = client.get('/epic-games-status')
        data = response.get_json()

    # PRINT
    print  (data)
