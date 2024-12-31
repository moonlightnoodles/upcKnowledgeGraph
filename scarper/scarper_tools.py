import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果响应状态码不是200，引发异常
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_specific_table(html_content, table_id='tblBody1'):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找具有特定 ID 的表格
    table = soup.find('table', id=table_id)
    if not table:
        print(f"No table found with id '{table_id}'.")
        return []

    rows = []
    for row in table.find_all('tr'):
        cells = row.find_all(['td', 'th'])
        row_data = [cell.get_text(strip=True) for cell in cells]
        rows.append(row_data)

    return rows


def save_to_csv(data, filename='output.csv'):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# def scarper():
    # for i in range(35):
    # https: // s.askci.com / stock / 0 - 0 - 0 / 1 /
    # url = f'https://s.askci.com/stock/0-0-0/24/'
    # html_content = fetch_page(url)
    # if html_content:
    #     table_data = parse_specific_table(html_content, table_id='myTable04')
    #     if table_data:
    #         save_to_csv(table_data,filename=f'./data/business_data_24.csv')
    # time.sleep(3)

# def scarper():
#     all_table_data = []
#     for i in range(2):
#         # https: // s.askci.com / stock / 0 - 0 - 0 / 1 /
#         url = f'https://s.askci.com/stock/0-0-0/{i+1}/'
#         try:
#             html_content = fetch_page(url)
#             if html_content:
#                 table_data = parse_specific_table(html_content, table_id='myTable04')
#                 if table_data:
#                     all_table_data.append(table_data)
#             time.sleep(2)
#         except Exception as e:
#             print(f"An error occurred while processing page {i+1}: {e}")
#     if all_table_data:
#         # print(all_table_data[:3])
#         save_to_csv(all_table_data, filename='./data/business_data_all.csv')

def scarper():
    for i in range(1):
        # https: // s.askci.com / stock / 0 - 0 - 0 / 1 /
        url = f'https://s.askci.com/stock/0-0-0/{i+1}/'
        html_content = fetch_page(url)
        if html_content:
            table_data = parse_specific_table(html_content, table_id='myTable04')
            if table_data:
                print(table_data)
                # save_to_csv(table_data,filename=f'./data/business_data_{i+1}.csv')
        time.sleep(2)


def hello():
    return "Hello HJY!"

def hello_hjy():
    return hello()

if __name__ == '__main__':
    scarper()