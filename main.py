from logging import exception
from tabnanny import check
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from captchaBypass import captchaSolve



#################################

# Put Your Payment Details Here.

Name_of_the_card = "Your name"
Card_number = "5105105105105100"
Valid_date = "03/2023"
card_varification_number = "333"
ruth = "153369492714"


url = "https://moredrops.cl"


#####################################



chromedriver = "chromedriver.exe"
options = Options()
options.binary_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"


driver = webdriver.Chrome(chromedriver, options=options)

driver.get(url+"/login")
driver.maximize_window()

def loginPageWait():
    print("wait for ligin page")
    if get_title == "Login | Tienda Drops":
        time.sleep(2)
    else:
        time.sleep(5)
        return loginPageWait()

get_title = driver.title
if get_title != "Login | Tienda Drops":
    try:
        captchaSolve(driver)
    except:
        loginPageWait()



loginPageWait()



def checkCart():
    
    cartItem = driver.find_element(By.CLASS_NAME, "nav-items-total").get_attribute("innerHTML")[0]

    if cartItem == "1":
        pass
    else:
        time.sleep(2)
        return checkCart()


checkCart()


def checkoutwait():
    driver.get(url+"/cart")
    try:
        checkout = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[3]/div[1]/div/div[2]/div/div/div/div[1]/button"))).click()
    except TimeoutException as ex:
        driver.refresh()
        return checkoutwait()

checkoutwait()

def pickbookAdd():
    try:
        bookMark = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/button").click()
        pickBookmark = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH,"/html/body/div[4]/div[1]/div[2]/div[2]/div[1]/div/div/form/button"))).click()
        
    except TimeoutException:
        driver.refresh()
        return pickbookAdd()


pickbookAdd()

followAdd = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/button").click()
followCard = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/button").click()


def enterPaymentDetails():
    try:
        CardName = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/form/div[2]/input")
        CardNo = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/form/div[3]/input")
        date = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/form/div[4]/div[1]/input")
        vcc = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/form/div[4]/div[2]/div/input")
        rut= driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/form/div[5]/input").clear()
        rut= driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/form/div[5]/input")

        CardName.send_keys(Name_of_the_card)
        CardNo.send_keys(Card_number)
        date.send_keys(Valid_date)
        vcc.send_keys(card_varification_number)
        rut.send_keys(ruth)

        time.sleep(3)
        dropDown = Select(driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/form/div[6]/select"))
        time.sleep(3)
        dropDown.select_by_value('1')
    except Exception as e:
        driver.refresh()
        return enterPaymentDetails()

enterPaymentDetails()

followPayment = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[1]/div[2]/div/form/button").click()

def checkBox():
    try:
        checkbox = driver.find_element(By.ID, "Terms1")
        ActionChains(driver).move_to_element(checkbox).click(checkbox).perform()

        time.sleep(3)
        finish = driver.find_element(By.XPATH, "/html/body/main/div[2]/div/div[2]/div[3]/form/button").submit()

    except Exception as e:
        return checkBox()


checkBox()


# End of the code