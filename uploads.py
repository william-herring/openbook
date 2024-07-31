import requests

def get_textbook_data(repository: str):
    print(requests.get('https://raw.githack.com/' + repository[18:] + '/release/options.json'))
    data = requests.get('https://raw.githack.com/' + repository[18:] + '/release/options.json').json()
    return data

def generate_book_code(title: str):
    if 'Units 1 & 2' in title:
        return title[:3] + '12'
    elif 'Units 3 & 4' in title:
        return title[:3] + '34'
    else:
        return title[:5]