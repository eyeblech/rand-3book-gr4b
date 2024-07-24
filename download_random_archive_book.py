import requests
import random
import os

def print_ascii_art():
    art = """
░█▀▀▄░█▀▀▄░█▀▀▄░█▀▄░▄▀▀▄░█▀▄▀█░░░█▀▀░░░░█▀▀▄░▄▀▀▄░▄▀▀▄░█░▄░░░█▀▀▀░█▀▀▄░█▀▀▄░█▀▀▄░█▀▀▄░█▀▀░█▀▀▄
░█▄▄▀░█▄▄█░█░▒█░█░█░█░░█░█░▀░█░░░█▀▀░▀▀░█▀▀▄░█░░█░█░░█░█▀▄░░░█░▀▄░█▄▄▀░█▄▄█░█▀▀▄░█▀▀▄░█▀▀░█▄▄▀
░▀░▀▀░▀░░▀░▀░░▀░▀▀░░░▀▀░░▀░░▒▀░░░▀▀▀░░░░▀▀▀▀░░▀▀░░░▀▀░░▀░▀░░░▀▀▀▀░▀░▀▀░▀░░▀░▀▀▀▀░▀▀▀▀░▀▀▀░▀░▀▀
                                                 
    """
    print(art)

def search_books(query=''):
    url = f'https://archive.org/advancedsearch.php?q={query}&fl[]=identifier,title,creator&sort[]=random&rows=50&start=0&output=json'
    print(f"Requesting URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data['response']['docs']
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON from response.")
            print("Response content:", response.text)
            return []
    else:
        print(f"Request failed with status code {response.status_code}")
        return []

def get_download_links(identifier):
    url = f'https://archive.org/metadata/{identifier}'
    print(f"Requesting URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            files = data.get('files', [])
            download_links = []
            for file in files:
                if file['name'].endswith(('.txt', '.epub', '.pdf', '.mobi')):
                    download_links.append(f"https://archive.org/download/{identifier}/{file['name']}")
            return download_links
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON from response.")
            print("Response content:", response.text)
            return []
    else:
        print(f"Request failed with status code {response.status_code}")
        return []

def download_file(file_url, save_path):
    response = requests.get(file_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded and saved as '{save_path}'")

def main():
    print_ascii_art()
    books = search_books('subject:books')
    if books:
        book = random.choice(books)
        identifier = book['identifier']
        title = book.get('title', 'Unknown Title').replace('/', '_')
        creator = book.get('creator', 'Unknown Creator').replace('/', '_')
        print(f"Selected book: {title} by {creator}")
        
        download_links = get_download_links(identifier)
        if download_links:
            # Prefer .epub format if available
            download_link = next((link for link in download_links if '.epub' in link), download_links[0])
            extension = download_link.split('.')[-1]
            save_path = os.path.join(os.path.expanduser('~'), 'Downloads', f'{title}_{creator}.{extension}')
            print(f"Downloading from: {download_link}")
            download_file(download_link, save_path)
        else:
            print("No downloadable link found for the selected book.")
    else:
        print("Could not fetch books from the Internet Archive.")

if __name__ == "__main__":
    main()

