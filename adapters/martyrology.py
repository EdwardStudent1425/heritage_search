from .base_adapter import ArchiveAdapter
import requests
from bs4 import BeautifulSoup

class MartyrologyAdapter(ArchiveAdapter):
    """
    The adapter for searching in the martyrology
    """

    @property
    def url(self):
        return "https://martyrology.org.ua/"

    def search(self, query: dict) -> list:
        '''
        searches the martyrology. 
        '''
        print("=== SEARCH CALLED ===")
        print(f"Query: {query}")

        res_url = 'https://martyrology.org.ua/result'
        page = 1
        all_cards = []
        max_page = 0
        params = {
            'SearchForm[surnameUA]':'',
            'SearchForm[nameUA]':'',
            'SearchForm[patronymicUA]':'',
            'SearchForm[surnameRU]': '',
            'SearchForm[birthRegion]': '',
            'SearchForm[militaryUnit]': '',
            'SearchForm[burialRegion]': '',
            'SearchForm[burialCity]': '',
            'SearchForm[burialVillage]': '',
            'SearchForm[burialPlace]': '',
            'page': page,
            'per-page': 100
            # in general, it finds everything on request, but the problem was that if
            # for example, the maximum number of pages is 417, then with a page number of 25, it would return 425
            # that is, something else was added (some copies).
        }

        query_to_param_map = {
            "surname": "SearchForm[surnameUA]",
            "name": "SearchForm[nameUA]",
            "patronymic": "SearchForm[patronymicUA]",
            "birth_region": "SearchForm[birthRegion]",
            "military_unit": "SearchForm[militaryUnit]",
            "burial_region": "SearchForm[burialRegion]",
            "burial_city": "SearchForm[burialCity]",
            "burial_village": "SearchForm[burialVillage]",
            "burial_place": "SearchForm[burialPlace]",
        }

        for query_key, param_key in query_to_param_map.items():
            params[param_key] = query.get(query_key, '')

        while page <= max_page or max_page == 0:
            params['page'] = page
            response = requests.get(url=res_url, params=params, verify=False, timeout=100)
            print(f"Page {page}: Status {response.status_code}")
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')

            # max page determination
            if max_page == 0:
                pagination_links = soup.select('.pagination_icon_wrapper a.pagination_icon')
                page_numbers = [
                    int(link.get_text(strip=True)) for link in pagination_links if link.get_text(strip=True).isdigit()
                ]
                max_page = max(page_numbers, default=1)
                print(f"Detected max_page = {max_page}")

            table = soup.find('table')
            if not table:
                break  

            tbody = table.find('tbody')
            tr_list = tbody.find_all('tr')
            if not tr_list or len(tr_list) == 0:
                print(f"Page {page} is empty. Stopping.")
                break  
            


            for tr in tr_list:
                if not tr:
                    print("Stopped: No rows found on this page")
                    break
                card = []
                td_list = tr.find_all('td')
                for td in td_list:
                    text = td.get_text(strip=True)
                    card.append(text if text else '-')
                all_cards.append(card)

            print(f"Page {page} rows: {len(tr_list)}")
            if page >= max_page:
                print("Reached last available page.")
                break
            page += 1  

        return all_cards
    
# there was a problem with infinite cycle, because the website returns the last page
# if i send a get request to get the data from the page with a larger number than it is.
# You can check the MAX number of pages.
