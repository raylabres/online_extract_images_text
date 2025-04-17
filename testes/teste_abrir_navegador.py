from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep

site = "https://www.bing.com/chat?q=Microsoft+Copilot&FORM=hpcodx"
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
navegador.get(site)
navegador.maximize_window()
sleep(15)
acoes = ActionChains(navegador)
acoes.send_keys("O que é IA")
acoes.send_keys(Keys.ENTER)
acoes.perform()
sleep(15)
rejeitar_cookies = navegador.find_element(By.XPATH, '//*[@id="bnp_btn_reject"]').click()
sleep(5)
navegador.save_screenshot("resposta.png")
