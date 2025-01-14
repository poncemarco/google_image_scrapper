from selenium import webdriver
from selenium.webdriver.common.by import By
import requests, time, random
from selenium.webdriver.safari.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
from tqdm import tqdm


class ImageDownloaderManager:
    
    def __init__(self, searchs, options=2) -> None:
        self.web_options = Options()
        #self.web_options.add_argument('--disable-blink-features=AutomationControlled')
        self.searchs = searchs
        self.driver = webdriver.Safari()
        self.driver.implicitly_wait(0.5)
        self.urls = []
        self.options = options
        
    
    def get_urls(self):
        try:
            for search in tqdm(self.searchs):
                if search == "VASO HAIBALL SANTOS # 115":
                    continue
                search = search.replace(" ", "+").rstrip('.').replace("/", "-").replace(".", "_").replace("#", "")
                self.driver.get(f"https://www.google.com/search?q={search}&sca_esv=600164613&hl=en&tbm=isch&sxsrf=ACQVn0_yIU0HA3pYKwSi")
                
                # Esperar a que aparezca el elemento con ID 'islrg' (o ajusta según tu necesidad)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "islrg")))
                

                try:
                    div_choose = random.choice([1, 2, 3, 4])
                    self.driver.find_element(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{div_choose}]/a[1]').click()
                    
                    # Establecer un tiempo máximo de espera para el elemento de la imagen
                    WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]')))
                    
                    image_url = self.driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]').get_attribute('src')
                    if len(image_url) < 1000:    
                        self.urls.append((search, image_url))

                    # Introduce una pausa aleatoria entre búsquedas para simular el comportamiento humano
                    time.sleep(random.uniform(0.5, 2))
                    
                except Exception as e:
                    # Puedes agregar un manejo específico de excepciones si es necesario
                    print(e)
                    
                    # Si se detecta que Google está bloqueando, detén la ejecución
                    if "unusual traffic" in self.driver.page_source:
        
                        return

        except Exception as e:
            print(e)
        finally:
            self.driver.quit()
            
        
    def fetch_urls(self):
        self.get_urls()
        print(self.urls)
        self.download_images()
        
    def download_image(self, url, name):
        try:
            response = requests.get(url.split("?")[0])
            if response.status_code == 200:
                
                image = Image.open(BytesIO(response.content))
                
                image = self.resize_and_fill_background(image)
                name = name
                with open(f'products_images/{name}.png', 'wb') as file:
                    image.save(file, format="PNG")
            else:
                print("Failed to download image.")
        except Exception as e:
            print(e)
            
    def resize_and_fill_background(self, image, target_size=(1000, 1000), background_color=(255, 255, 255, 255)):
        # Create a new image with the desired background color
        new_image = Image.new("RGBA", target_size, background_color)

        # Calculate the position to paste the original image at the center
        paste_position = ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2)

        # Create a mask for pasting the original image
        mask = Image.new("L", image.size, 255)
        new_image.paste(image, paste_position, mask)

        return new_image
    
    def download_images(self):
        for name, url in self.urls:
            self.download_image(url, name)
            
    def create_thumbnail(self, image):
        image.thumbnail((100, 100))
        return image
        
    
    