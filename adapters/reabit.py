from .base_adapter import ArchiveAdapter
import requests
from bs4 import BeautifulSoup

class ReabitAdapter(ArchiveAdapter):

    @property
    def url(self):
        return 'https://www.reabit.org.ua/nbr/'

    def search(self, query: dict) -> list:
        "Searches the Reabit database of repressed individuals"
        all_cards = []

        base_params = {
            'st': '4',
            'region': '',
            'ss': '',
            'logic': 'or',
            'f1_type': 'begins',
            'f1_str': '',
            'f2_type': 'begins',
            'f2_str': '',
            'f3_type': 'begins',
            'f3_str': '',
            'f4_from': '',
            'f4_till': '',
            'f7[]': ['all'],
            'f14[]': ['all']
        }

        query_to_param_map = {
            'birth_region': 'region',
            'last_living': 'ss',
            'surname': 'f1_str',
            'name': 'f2_str',
            'type_param': 'f3_type',
            'patronymic': 'f3_str',
            'birth_min': 'f4_from',
            'birth_max': 'f4_till'
        }

        for query_key, param_key in query_to_param_map.items():
            base_params[param_key] = query.get(query_key, '')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Referer': 'https://www.reabit.org.ua/nbr/',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive'
        }

        # the 1st request to get the number of pages
        response = requests.get(self.url, params=base_params, headers=headers, timeout=30)
        print(f"Status: {response.status_code} | Page: 1")
        soup = BeautifulSoup(response.text, 'html.parser')

        # find the last START
        last_start = 0
        nav_div = soup.find('div', class_='bootom_pspl')
        if nav_div:
            for a in nav_div.find_all('a', href=True):
                href = a['href']
                if 'START=' in href:
                    try:
                        start_str = href.split('START=')[1].split('&')[0]
                        start_num = int(start_str)
                        last_start = max(last_start, start_num)
                    except ValueError:
                        continue

        last_page = (last_start // 50) + 1
        print(f"Total pages: {last_page}")


        # going through each page
        for page in range(1, last_page + 1):
            start_param = (page - 1) * 50
            params = base_params.copy()
            params['START'] = str(start_param)

            response = requests.get(self.url, params=params, headers=headers, timeout=30)
            print(f"Status: {response.status_code} | Page: {page}")

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', class_='nbr_list')
            if not table:
                print("No table found, stopping.")
                break

            # знайти <thead> у таблиці
            thead = table.find('thead')
            headers = []

            if thead:
                header_row = thead.find('tr')
                if header_row:
                    for th in header_row.find_all('th'):
                        button = th.find('button')
                        if button:
                            text = button.get_text(separator=' ', strip=True)
                        else:
                            text = th.get_text(strip=True)
                        text = text.replace('\xa0', ' ').strip()
                        headers.append(text)

            print("Заголовки таблиці:", headers)


            tbody = table.find('tbody')
            if not tbody:
                print("No tbody found, stopping.")
                break

            tr_list = tbody.find_all('tr')
            if not tr_list:
                print("No rows in tbody, stopping.")
                break

            for tr in tr_list:
                card = []

                onclick = tr.get('onclick', '')
                link = None
                if "/nbr/?ID=" in onclick:
                    start = onclick.find("/nbr/?ID=")
                    end = onclick.find("'", start)
                    href = onclick[start:end] if end != -1 else onclick[start:]
                    link = f"https://www.reabit.org.ua{href}"

                td_list = tr.find_all('td')
                text_data = [td.get_text(strip=True) for td in td_list]

                if text_data:
                    card.extend(text_data)
                    card.append(link or '-')

                row_dict = {}
                for i, header in enumerate(headers):
                    row_dict[header] = text_data[i] if i < len(text_data) else ''

                row_dict['Посилання'] = link or '-'

                all_cards.append(row_dict)

        return all_cards
