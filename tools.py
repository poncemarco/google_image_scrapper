from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
from PIL import Image
from io import BytesIO


def get_urls(options, search):
    
    
    search = search.replace(" ", "+")
    driver = webdriver.Chrome()

    driver.get(f"https://www.google.com/search?q={search}&sca_esv=600164613&hl=en&tbm=isch&sxsrf=ACQVn0_yIU0HA3pYKwSiViFEhUQQcUQWqQ%3A1705811820776&source=hp&biw=1202&bih=1176&ei=bJ-sZbDpLfeZkPIPlJGi4Ao&iflsig=ANes7DEAAAAAZaytfE_cBEfZSW3nxgWA2hbsY-VQkLNF&ved=0ahUKEwiwz4Sd1O2DAxX3DEQIHZSICKwQ4dUDCAY&uact=5&oq=coca+cola&gs_lp=EgNpbWciCWNvY2EgY29sYTIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARIhhpQkgdYhxlwBHgAkAEAmAFLoAGoBaoBAjEwuAEDyAEA-AEBigILZ3dzLXdpei1pbWeoAgrCAgcQIxjqAhgnwgIEECMYJw&sclient=img")

    driver.implicitly_wait(0.5)

    try: 
        images_url = []
        for i in range(1, options + 1):
            try:
                driver.find_element(By.XPATH, f'//*[@id="islrg"]/div[1]/div[{i}]/a[1]').click()

                time.sleep(2)
                image_url = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]').get_attribute('src')
                driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[1]/div/div[2]/div[2]/button').click()
                time.sleep(1)
                if len(image_url) < 1000:    
                    images_url.append(image_url)
            except Exception as e:
                print(e)
                driver.quit()
    except Exception as e:
        print(e)
        driver.quit()
    driver.quit()
    return images_url
        
def download_image(url, name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            
            image = Image.open(BytesIO(response.content))
            
            image = resize_and_fill_background(image)
            
            with open(f'products_images/{name}.png', 'wb') as file:
                image.save(file, format="PNG")
        else:
            print("Failed to download image.")
    except Exception as e:
        print(e)
        
            
        
        
def resize_and_fill_background(image, target_size=(1000, 1000), background_color=(255, 255, 255, 255)):
    # Create a new image with the desired background color
    new_image = Image.new("RGBA", target_size, background_color)

    # Calculate the position to paste the original image at the center
    paste_position = ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2)

    # Create a mask for pasting the original image
    mask = Image.new("L", image.size, 255)
    new_image.paste(image, paste_position, mask)

    return new_image
        
def get_products() -> list:
    url = 'https://api.sheety.co/40121a2386838b1553a7e75ed35d7874/productos/catalogo'
    response = requests.get(url)
    catalogo = response.json()['catalogo']
    return [producto['productos'] for producto in catalogo]



    