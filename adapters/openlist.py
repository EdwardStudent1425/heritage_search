from .base_adapter import ArchiveAdapter
import requests
from bs4 import BeautifulSoup

class OpenlistAdapter:

    @property
    def url(self):
        return "https://ua.openlist.wiki/%D0%A1%D0%BF%D0%B5%D1%86%D1%96%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0:OlSearch"
    
    def search(self, query: dict) -> list:
        "searches the open lists of repressed people"

        all_cards = []

        params = {
            'olsearch-name': '',
            'olsearch-birth_min': '',
            'olsearch-birth_max': '',
            'olsearch-death_min': '',
            'olsearch-death_max': '',
            'olsearch-birthplace': '',
            'olsearch-liveplace': '',
            'olsearch-nationality': '',
            'olsearch-social': '',
            'olsearch-profession': '',
            'olsearch-deathplace': '',
            'olsearch-burialplace': '',
            'olsearch-body': '',
            'olsearch-categories': '',
            'olsearch-arrest_min': '',
            'olsearch-arrest_max': '',
            'olsearch-indictment': '',
            'olsearch-conviction_min': '',
            'olsearch-conviction_max': '',
            'olsearch-conviction-org': '',
            'olsearch-sentence': '',
            'olsearch-detentionplace': '',
            'olsearch-release_min': '',
            'olsearch-release_max': '',
            'olsearch-execution_min': '',
            'olsearch-execution_max': '',
            'olsearch-archive-case-number': '',
            'olsearch-run': '1',
            'olsearch-advform': '1',
            'olsearch-page': '1'
        }


        query_to_param_map = {
            
            "birth_min": "olsearch-birth_min",
            "birth_max": "olsearch-birth_max",
            "death_min": "olsearch-death_min",
            "death_max": "olsearch-death_max",
            "birthplace": "olsearch-birthplace",
            "liveplace": "olsearch-liveplace",
            "nationality": "olsearch-nationality",
            "social": "olsearch-social",
            "profession": "olsearch-profession",
            "deathplace": "olsearch-deathplace",
            "burialplace": "olsearch-burialplace",
            "body": "olsearch-body",
            "categories": "olsearch-categories",
            "arrest_min": "olsearch-arrest_min",
            "arrest_max": "olsearch-arrest_max",
            "indictment": "olsearch-indictment",
            "conviction_min": "olsearch-conviction_min",
            "conviction_max": "olsearch-conviction_max",
            "conviction_org": "olsearch-conviction-org",
            "sentence": "olsearch-sentence",
            "detentionplace": "olsearch-detentionplace",
            "release_min": "olsearch-release_min",
            "release_max": "olsearch-release_max",
            "execution_min": "olsearch-execution_min",
            "execution_max": "olsearch-execution_max",
            "archive_case_number": "olsearch-archive-case-number"
        }
                
        for query_key, param_key in query_to_param_map.items():
            params[param_key] = query.get(query_key, '')

        full_name_parts = [
                        query.get('surname', ""),
                        query.get('name', ''),
                        query.get('patronymic', '')
                        ]
        full_name = ' '.join(part for part in full_name_parts if part).strip()
        params['olsearch-name'] = full_name

        page = 1
        while True:
            params['olsearch-page'] = str(page)
            response = requests.get(url=self.url, params=params, timeout=30)

            print("Status:", response.status_code)
            # print("Final URL:", response.url)
            # print("First 500 characters of HTML:")
            # print(response.text[:500])

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            if not table:
                break

            thead = table.find('thead')
            # tr = thead.find('tr')
            td_list = thead.find_all('td')
            headers = [td.get_text(strip=True) for td in td_list]

            tbody = table.find('tbody')
            tr_list = tbody.find_all('tr')
            if not tr_list or len(tr_list) == 0:
                print(f"Page is empty. Stopping.")
                break
            for tr in tr_list:
                if not tr:
                    break
                card = []
                td_list = tr.find_all('td')
                for td in td_list:
                    # if there is the tag <a>, pull out the piece of text and href
                    a_tag = td.find('a')
                    if a_tag:
                        name_text = a_tag.get_text(strip=True)
                        href = a_tag.get('href', '')
                        full_link = f"https://ua.openlist.wiki{href}"
                        card.append(name_text)
                        card.append(full_link)
                    else:
                        text = td.get_text(strip=True)
                        card.append(text if text else '-')

                if card:
                    all_cards.append(card)

            page += 1
        return all_cards