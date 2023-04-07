from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def get_soup(TARGET_URL):
     page = requests.get(TARGET_URL)
     soup = BeautifulSoup(page.text, 'html.parser')
     return soup

BASE_URL = "https://www.hepsiemlak.com/istanbul-kiralik/daire?p37=120403"

soup = get_soup(BASE_URL)


def get_product_link(url):
     response = requests.get(url)
     soup = BeautifulSoup(response.content, "html.parser")
     product_links = soup.find_all("a", class_="card-link")

     product_urls = []
     for link in product_links:
          url = link["href"]
          product_url = url
          product_urls.append(product_url)
     return product_urls

def scrape_product_info(url):
     full_url = "https://www.hepsiemlak.com"+url
     response = requests.get(full_url)
     soup = BeautifulSoup(response.content, "html.parser")
     lists = soup.find_all("li", class_="spec-item")
     price = soup.find_all("div", class_="right")

     col_names = []
     product_data = []
     for i in lists:
          col_name_tag = i.find("span", class_="txt")
          if col_name_tag:
               col_name = col_name_tag.text.replace('\n', '')
          else:
               col_name = "None"

          col_value_tag = i.find("span", class_="txt", string=col_name).find_next_sibling("span")
          if col_value_tag:
               col_value = col_value_tag.text.replace('\n', '')
          else:
               col_value = "None"


          col_names.append(col_name)
          product_data.append(col_value)

     df = pd.DataFrame([product_data], columns=col_names)

     price_value = ""
     for i in price:
               price_value = i.find("p", class_="fontRB fz24 price").text.replace('\n', '').replace(" ", "")
               break

     col_names.append("Price")
     product_data.append(price_value)

     df = pd.DataFrame([product_data], columns=col_names)
     return df


all_data= []
for i in range(1, 120):
     urls = f"https://www.hepsiemlak.com/istanbul-kiralik/daire?p37=120403&page={i}"
     product_links = get_product_link(urls)
     print(f"Found {len(product_links)} links on page {i}")
     for link in product_links:
          product_info = scrape_product_info(link)
          all_data.append(product_info.iloc[0])
          time.sleep(2)
          #print(product_info)


df = pd.DataFrame(all_data)
df.to_csv("hepsiemlak.csv", index=False)














