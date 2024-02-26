import requests
import time


class SwapiAPIConnector:
    BASE_URL = 'https://swapi.dev/api/'
    SPECIES_URL = f'{BASE_URL}/species/'
    FILM_URL = f'{BASE_URL}/films/'
    PEOPLE_URL = f'{BASE_URL}/people/'
    VEHICLES_URL = f'{BASE_URL}/vehicles/'

    def get_people_first_film(self, people_id):
        url = f'{self.PEOPLE_URL}{people_id}/'
        response = requests.get(url=url)

        if response.ok and response.json():
            films = response.json().get('films', [])
            film_url = films[0] if films else None

            if film_url:
                response_film = requests.get(film_url)
                if response_film.ok:
                    film_data = response_film.json()
                    film_name = film_data.get('title', '')
                    return film_name
        return ''

    def get_max_speed(self):
        response = requests.get(url=self.VEHICLES_URL)

        if response.ok and response.json():
            vehicles = response.json().get('results', [])
            data = []

            for speed in vehicles:
                all_speeds = speed.get('max_atmosphering_speed', '')
                data.append(int(all_speeds))
            return max(data)

        return None

    def get_all_eye_colors(self):
        response = requests.get(url=self.SPECIES_URL)

        if response.ok and response.json():
            species = response.json().get('results', [])
            data = []

            for color_eyes in species:
                colors = color_eyes.get('eye_colors', '')
                if colors != 'n/a':
                    data.append(colors)
            all_colors = [color.strip() for colors in data for color in colors.split(',')]
            return list(set(all_colors))

        return []

    def get_species_by_hair_color(self, color: str):
        response = requests.get(url=self.SPECIES_URL)

        if response.ok and response.json():
            species = response.json().get('results', [])
            data = {}

            for specie in species:
                name = specie.get('name', '')
                hair_colors = specie.get('hair_colors', '')
                data.update({name: hair_colors})
            list_of_species = [name for name, hair_colors in data.items() if color in hair_colors]
            return list_of_species

        return []

    def get_average_count_characters(self):
        response = requests.get(url=self.FILM_URL)

        if response.ok and response.json():
            films = response.json().get('results', [])
            all_characters = []

            for character in films:
                count = len(character.get('characters', []))

                all_characters.append(count)

            avg_count = sum(all_characters) / len(all_characters)
            return int(avg_count)

        return None


swapi_conn = SwapiAPIConnector()
print(swapi_conn.get_average_count_characters())
time.sleep(2)
print(swapi_conn.get_species_by_hair_color(color='brown'))
time.sleep(2)
print(swapi_conn.get_all_eye_colors())
time.sleep(2)
print(swapi_conn.get_max_speed())
time.sleep(2)
print(swapi_conn.get_people_first_film(people_id=10))
time.sleep(2)


class OpenLibraryAPIConnector:
    BASE_URL = 'https://openlibrary.org/'

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    @staticmethod
    def get_headers():
        headers = {'Content-type': 'application/json'}
        return headers

    def get(self, url, **kwargs):
        response = requests.get(url=url, headers=self.get_headers())
        return response

    def post(self, url, json, **kwargs):
        auth = (self.username, self.password)
        response = requests.post(url=url, json=json, headers=self.get_headers(), auth=auth)
        return response

    def get_top_book_of_author(self, author_name):
        url = f'{self.BASE_URL}search/authors.json?q={author_name}'
        response = self.get(url=url, headers=self.get_headers())
        if response.ok:
            data = response.json()
            authors = data.get('docs', [])

            author = authors[0] if authors else {}
            top_work = author.get('top_work', '')
            return top_work

        else:
            return ""

    def check_language_for_book(self, book_name, lang):
        url = f'{self.BASE_URL}search.json?q={book_name}'
        response = self.get(url=url, headers=self.get_headers())

        if response.ok:
            data = response.json()
            books = data.get('docs', [])

            book = books[0] if books else {}
            languages = book.get('language', [])
            return lang in languages

        else:
            return ''

    def get_amazon_link(self, book_name):
        url = f'{self.BASE_URL}search.json?q={book_name}'
        response = self.get(url=url, headers=self.get_headers())

        if response.ok:
            data = response.json()
            books = data.get('docs', [])

            book = books[0] if books else {}
            amazon_ids = [value for value in book.get('id_amazon', []) if value != '']
            amazon_id = amazon_ids[0] if amazon_ids else ''
            return f'https://www.amazon.com/dp/{amazon_id}'

        else:
            return ''

    def compare_authors(self, authors_list):
        authors_info = {}

        for author_name in authors_list:
            url = f'{self.BASE_URL}search/authors.json?q={author_name}'
            response = self.get(url=url, headers=self.get_headers())

            if response.ok:
                data = response.json()
                authors = data.get('docs', [])

                author = authors[0] if authors else {}
                author_name = author.get('name', '')
                count_works = author.get('work_count', 0)
                authors_info.update({author_name: count_works})
            else:
                return ''

        top_author = max(authors_info, key=authors_info.get)
        return top_author

    def create_book_list(self, username, list_name):
        url = f'{self.BASE_URL}people/{username}/lists'
        data = {
            "name": list_name
        }
        response = self.post(url=url, json=data, headers=self.get_headers())
        return response.status_code


ol_conn = OpenLibraryAPIConnector()
print(ol_conn.get_top_book_of_author(author_name='Hemingway'))
time.sleep(2)
print(ol_conn.check_language_for_book(book_name='The Old Man and the Sea', lang='ita'))
time.sleep(2)
print(ol_conn.compare_authors(authors_list=['Hemingway', 'Tolkien', 'Fitzgerald']))

print('Thank You!')
