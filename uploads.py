import requests

def get_textbook_data(repository: str):
    data = requests.get('https://raw.githack.com/' + repository[18:] + '/release/options.json').json()
    return data
