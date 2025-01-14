from manager import ImageDownloaderManager
import json, requests

if __name__ == "__main__":
    searches = []
    # response = requests.get("http://localhost:8000/api/v1/items/?page_size=1000")
    # items_already = response.json()['results']
    # items = requests.get("https://api.sheety.co/40121a2386838b1553a7e75ed35d7874/catalogoCasaMaya/catalogo").json()["catalogo"]
    # items_already_downloaded = [product["name"] for product in items_already]
    searches = ["Tecate emblema logo", "after life festival logo", "louis tomlinson tour", "F1 mexico logo", "Ceremonia"]
    # for item in items:
    #     if 'precio' in item and item['productos'] not in items_already_downloaded:
    #         searches.append(item['productos'])
    #         searches = []
    manager = ImageDownloaderManager(searches)
    manager.fetch_urls()