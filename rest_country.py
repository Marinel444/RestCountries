import requests


class RestCountry:
    def __init__(self, url: str) -> None:
        self.url = url

    def get_countries_data(self) -> dict:
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()

    def get_country_list(self) -> str:
        messages = ""
        data = self.get_countries_data()
        for country in data:
            messages += (
                f"| country: {country['name']['common']} | "
                f"capital: {country['capital'][0] if country['capital'] else ''} | "
                f"flag: {country['flags']['png']} |\n")

        return messages


if __name__ == "__main__":
    rest = RestCountry("https://restcountries.com/v3.1/all?fields=name,capital,flags")
    print(rest.get_country_list())
