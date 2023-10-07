import json
import time
from src.utils.SeleniumUtils import UserActivity
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup as bs


def main():
    driver = UserActivity(headless=True).driver

    url = "https://finance.vietstock.vn/chung-khoan-phai-sinh/cw-thong-ke-giao-dich.htm"
    driver.get(url)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "statistic-price")))

    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

    print('Done')


def parse():
    with open('test.html', 'r', encoding='utf-8') as f:
        soup = bs(f.read(), 'html.parser')

    data = []

    table = soup.find('div', {'id': 'statistic-price'})
    body = table.find('tbody')
    rows = body.find_all('tr')

    for row in rows:
        cells = row.find_all('td')
        data_cell = {
            'stt': cells[0].text.strip(),
            'ngay': cells[1].text.strip(),
            'ma_ck': cells[2].text.strip(),
            'CW': cells[3].text.strip(),
            'ngay_gdcc': cells[4].text.strip(),
            'tham_chieu': cells[5].text.strip(),
            'mo_cua': cells[6].text.strip(),
            'dong_cua': cells[7].text.strip(),
            'cao_nhat': cells[8].text.strip(),
            'thap_nhat': cells[9].text.strip(),
            'trung_binh': cells[10].text.strip(),
            'thaydoi_value': cells[11].text.strip(),
            'thaydoi_percent': cells[12].text.strip(),
            'khop_lenh_khoi_luong': cells[12].text.strip(),
            'khop_lenh_gia_tri': cells[12].text.strip()
        }

        data.append(data_cell)

    # Convert to JSON
    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    with open('test.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


if __name__ == "__main__":
    # main()
    parse()
