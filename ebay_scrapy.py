import json

import requests

from bs4 import BeautifulSoup


class EbayScrapy:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;"
                  "q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
    }

    def __init__(self, url_to_product: str) -> None:
        self.url_to_product = url_to_product

    def get_product_page(self) -> str:
        response = requests.get(self.url_to_product, headers=self.headers)
        if response.status_code == 200:
            return response.text
        raise Exception(response.text)

    def create_json(self) -> str:
        images_url = []
        product_page = self.get_product_page()
        soup = BeautifulSoup(product_page, "lxml")
        product_name = soup.find("div", class_="vi-title__main").text
        images = soup.find_all("li", class_="image-treatment")
        for image in images:
            images_url.append(image.find("img").get("src"))
        price = soup.find("div", class_="x-price-primary").text
        seller_name = (
            soup.find("div", class_="x-sellercard-atf__info").
            find("span", class_="ux-textspans ux-textspans--PSEUDOLINK").text
        )
        data = {
            "product_name": product_name,
            "images": images_url,
            "product_url": self.url_to_product,
            "price": price,
            "seller_name": seller_name,
        }
        with open("ebay_scrapy.json", "w") as file:
            json.dump(data, file, indent=4)
        return "success"


if __name__ == "__main__":
    ebay = EbayScrapy("https://www.ebay.com/itm/335474295898?_trkparms=amclksrc%3DITM%26aid%3D1110006%26algo%3DHOMESPLICE.SIM%26ao%3D1%26asc%3D20221018081743%26meid%3D0476ef206fc1417588aa51cd828aea4f%26pid%3D101429%26rk%3D3%26rkt%3D12%26sd%3D166588920704%26itm%3D335474295898%26pmt%3D1%26noa%3D0%26pg%3D2332490%26algv%3DSimPLMWebV1EmbeddedAuctionsCPCAutoManualWithCIIXAIRecallsUpdatedRanker0424NoIMA%26brand%3DApple&_trksid=p2332490.c101429.m2460&itmprp=cksum%3A3354742958980476ef206fc1417588aa51cd828aea4f%7Cenc%3AAQAJAAABMEjZlC%252Fw6lxP728usnvbmmF6IQh6tnfnzntGabzCeJpCCr4SNJdAkEHRyl7vTkyBf4dAus4HjwExpJyz5uqCLXRmucXHasXHatyiO4Oso3sn8sVYp9QLo%252Fr6B59z8w3fqKOGvAHUxrnU3hXf4SD4G1mEj2tggiT75wg35se09l0u7fQUWI9pzID%252B8XBCov893hI3x0k2k0U6AJf7iWILKPK%252F8uEmNIQpLoIYEgVYAnycSdR8X4%252BpW6o%252FIn3%252FtkQ1jGZ%252F6pqhiHhUD65cah%252B4KjkWNyMLtyNM1gkb4WQECZES7yyTotn83kJiJlMs6ryP7XSWuXD3%252BIUu4IAC0WTDaEp%252Fn4scaHxhiT%252B5TCgWU1I0BxHE3OKIa1BE8YM29%252BIEHfWNYc8eBHt%252FJfStPEkLxsM%253D%7Campid%3APL_CLK%7Cclp%3A2332490&epid=7023712785&itmmeta=01J2BNXAN4DDNZHZ2ES5W0XJFP")
    print(ebay.create_json())
