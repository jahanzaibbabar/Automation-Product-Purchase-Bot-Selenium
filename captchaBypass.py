import random
import urllib
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import sys
import time


audioToTextDelay = 7
delayTime = 2
audioFile = "\\payload.mp3"
URL = "https://www.google.com/recaptcha/api2/demo"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"

def captchaSolve(driver):

    def delay():
        time.sleep(random.randint(2, 3))

    def audioToText(audioFile):
        driver.execute_script('''window.open("","_blank")''')
        driver.switch_to.window(driver.window_handles[1])
        driver.get(SpeechToTextURL)

        delay()
        audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
        audioInput.send_keys(audioFile)

        time.sleep(audioToTextDelay)

        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
        while text is None:
            text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

        result = text.text

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        return result


    # try:
    #     # create chrome driver
    #     option = webdriver.ChromeOptions()
    #     option.add_argument('--disable-notifications')
    #     # option.add_argument('--mute-audio')
    #     # option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    #     driver = webdriver.Chrome("F:\Freelancing\webDriver\chromedriver.exe", options=option)
    #     delay()
    #     # go to website which have recaptcha protection
    #     driver.get(URL)
    # except Exception as e:
    #     sys.exit(
    #         "[-] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

    # 
    time.sleep(1)
    driver.find_element(By.ID, "challenge-container").click()
    # g_recaptcha = driver.find_elements_by_class_name('g-recaptcha')[0]
    # outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
    # outerIframe.click()

    iframes = driver.find_elements(By.TAG_NAME,'iframe')
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(iframes)):
        driver.switch_to.default_content()
        iframe = driver.find_elements(By.TAG_NAME,'iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element(By.ID, "recaptcha-audio-button")
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass

    if audioBtnFound:
        try:
            while True:
                # get the mp3 audio file
                src = driver.find_element(By.ID, "audio-source").get_attribute("src")
                print("[INFO] Audio src: %s" % src)

                # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, os.getcwd() + audioFile)

                # Speech To Text Conversion
                key = audioToText(os.getcwd() + audioFile)
                print("[INFO] Recaptcha Key: %s" % key)

                driver.switch_to.default_content()
                iframe = driver.find_elements(By.TAG_NAME,'iframe')[audioBtnIndex]
                driver.switch_to.frame(iframe)

                # key in results and submit
                inputField = driver.find_element(By.ID, "audio-response")
                inputField.send_keys(key)
                delay()
                inputField.send_keys(Keys.ENTER)
                delay()

                err = driver.find_elements(By.CLASS_NAME, 'rc-audiochallenge-error-message')[0]
                if err.text == "" or err.value_of_css_property('display') == 'none':
                    print("[INFO] Success!")
                    break

        except Exception as e:
            print(e)
            sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
    else:
        sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
