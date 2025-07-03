from base_adapter import ArchiveAdapter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

class PrainAdapter(ArchiveAdapter):
    
    @property
    def url(self):
        return 'https://pra.in.ua/uk/search'
    
    def search(self, query: dict) -> list:
        options = Options()
        options.add_argument("--headless")  # зніми, якщо хочеш бачити браузер
        options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(self.url)
        wait = WebDriverWait(driver, 10)

        # Мапінг ключів query до атрибутів name у формі
        field_mapping = {
            'surname': 'lastname',                  # textarea
            'name': 'firstname',
            'birth_year_min': 'year_from',
            'birth_year_max': 'year_to',
            'district_id': 'district_id',           # select
            'settlement_name': 'settlement_name'
        }

        for query_key, field_name in field_mapping.items():
            value = query.get(query_key)
            if not value:
                continue


            try:
                if field_name == 'lastname':
                    # textarea, not input
                    textarea = driver.find_element(By.NAME, field_name)
                    textarea.clear()
                    textarea.send_keys(value)
                
                elif field_name == 'district_id':
                    # select field
                    select = Select(driver.find_element(By.NAME, field_name))
                    select.select_by_value(str(value))
                
                else:
                    field = driver.find_element(By.NAME, field_name)
                    field.clear()
                    field.send_keys(value)
            except Exception as e:
                print(f"Error setting field {field_name}: {e}")

        
        try:
            search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            time.sleep(1) 
            search_button.click()
        except Exception as e:
            print("Search button click failed:", e)
            driver.quit()
            return []


        all_results = []
        page = 1

        while True:
            print(f"[Page {page}]")
            try:
                # wait untill a table loads
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.table-striped tbody")))
            except Exception as e:
                print("Timeout waiting for results table:", e)
                break

            table = driver.find_element(By.CSS_SELECTOR, "table.table.table-striped")
            rows = table.find_elements(By.TAG_NAME, "tr")

            if len(rows) <= 1:
                print("No data rows found.")
                break

            for row in rows[1:]:  # pass a title
                cols = row.find_elements(By.TAG_NAME, "td")
                if not cols:
                    continue

                try:
                    pib_elem = cols[0].find_element(By.TAG_NAME, "a")
                    pib = pib_elem.text.strip()
                except:
                    pib = ""

                try:
                    father_name_elem = cols[0].find_element(By.CSS_SELECTOR, "small.text-muted")
                    father_name = father_name_elem.text.replace("Ім'я батька:", "").strip()
                except:
                    father_name = ""

                birth = cols[1].text.strip()
                death = cols[2].text.strip()
                mention = cols[3].text.strip()

                district_elems = cols[4].find_elements(By.TAG_NAME, "small")
                district = district_elems[0].text.strip() if len(district_elems) > 0 else ""
                oblast = district_elems[1].text.strip() if len(district_elems) > 1 else ""

                try:
                    settlement_elem = cols[5].find_element(By.TAG_NAME, "a")
                    settlement = settlement_elem.text.strip()
                except:
                    settlement = ""

                all_results.append({
                    "ПІБ": pib,
                    "Ім'я батька": father_name,
                    "Народження": birth,
                    "Смерть": death,
                    "Згадка": mention,
                    "Район": district,
                    "Область": oblast,
                    "Поселення": settlement,
                })

            # check an existence of the button "Наступна"
            try:
                next_button = driver.find_element(By.LINK_TEXT, "Наступна")
                if 'disabled' in next_button.get_attribute("class"):
                    break
                next_button.click()
                time.sleep(1)
                page += 1
            except Exception:
                break

        driver.quit()
        return all_results
    
