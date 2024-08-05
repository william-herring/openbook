import requests

def get_textbook_options(repository: str):
    data = requests.get('https://raw.githack.com/' + repository[18:] + '/release/options.json').json()
    return data

def get_textbook_html_url(repository: str):
    url = 'https://raw.githack.com/' + repository[18:] + '/release/out/html/index.html'
    return url

def get_textbook_build_data(repository: str):
    data = requests.get('https://raw.githack.com/' + repository[18:] + '/release/out/data.json').json()
    return data

def generate_book_code(title: str):
    if 'Units 1 & 2' in title:
        return title[:3].upper() + '12'
    elif 'Units 3 & 4' in title:
        return title[:3].upper() + '34'
    else:
        return title[:5].upper()
