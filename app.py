from flask import Flask , request , jsonify , render_template
import requests
import hashlib
from bs4 import BeautifulSoup
import urllib
import string
import random

app  = Flask(__name__, template_folder='templates')
#auto-reload template
app.config['TEMPLATES_AUTO_RELOAD'] = True

url_data = {} #dict to store url data

def generate_short_url():
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase+string.digits, k=6))

def shorten_url(long_url):
    for short_url, info in url_data.items():
        if info['long_url'] == long_url:
            return short_url

    hash_object = hashlib.md5(long_url.encode())
    hex_dig = hash_object.hexdigest()[:6] 
    short_url = hex_dig

    while short_url in url_data:
        hex_dig += 'a'
        short_url = hex_dig[:6]

    url_data[short_url] = {
        'long_url': long_url,
        'hits': 0,
        'title': get_title_from_url(long_url)
    }

    return short_url

def get_title_from_url(url):
    try:
        print("Fetching URL:", url)
        response = requests.get(url)
        response.raise_for_status()
        print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')
        print('Title: ', title_tag)
        if title_tag:
            return title_tag.text.strip()
        else:
            return "Title not found"
    except requests.exceptions.RequestException as e:
        return str(e)
    except Exception as e:
        return str(e)


@app.route('/create' , methods = ['POST'])
def create():
    data = request.get_json()
    long_url = data.get('long_url')
    if not long_url:
        return jsonify({'error': 'Long URL not found'}), 400

    title = data.get('title', get_title_from_url(long_url))

    for short_url, info in url_data.items():
        if info['long_url'] == long_url:
            return jsonify({'short_url': short_url, 'title': title})

    short_url = shorten_url(long_url)
    url_data[short_url] = {
        'long_url': long_url,
        'hits': 0,
        'title': title
    }
    return jsonify({'short_url': short_url, 'title': url_data[short_url]['title']})

@app.route('/<short_url>' , methods = ['GET'])
def redirect(short_url):
    data = url_data.get(short_url)
    if not data:
        return jsonify({"error":'Invlaid Short URL'}),400
    data['hits'] += 1
    return jsonify(data)

@app.route('/api/<short_url>', methods=['GET'])
def get_metadata(short_url):
    data = url_data.get(short_url)
    if not data:
        return jsonify({'error' : 'Invalid Short URL'}),400
    response = {
        'short_url' : short_url,
        'long_url' : data['long_url'],
        'hits':data['hits'],
        'title':data['title']
      
    }
    return jsonify(response)

@app.route('/search' , methods=['GET'])
def search():
    search_term = request.args.get('term')
    results = []

    for short_url, data in url_data.items():
        title = data.get('title' , '')
        if search_term.lower() in title.lower():
            results.append({
                'short_url' : short_url,
                'long_url': data['long_url'],
                'title':title
            })
    return jsonify(results)
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

