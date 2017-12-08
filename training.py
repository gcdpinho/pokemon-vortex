from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import sys
import random

class User():

    def __init__(self, driver, url):
        self.username = input("Usuário: ")
        self.password = getpass.getpass("Senha: ")
        self.driver = driver
        self.url = url
        

    def login(self):
        self.driver.get(self.url)
        self.driver.find_element_by_class_name("login-header").click()
        self.driver.find_element_by_id("myusername").send_keys(self.username)
        self.driver.find_element_by_id("mypassword").send_keys(self.password)
        self.driver.find_element_by_id("submit").click()
        
        if "dashboard" in self.driver.current_url:
            print("Login realizado com sucesso!\n")
            return True
        else:
            print("Usuário ou senha inválida!\n")
            return False       


def training():
    url = "https://www.pokemon-vortex.com/"
    driver = webdriver.PhantomJS()
    leaders = [("BUG","415355"), ("DARK", "840815"), ("DRAGON", "415125"), ("FIRE", "19935"), ("FIRE", "381236"),
                ("FLYING", "42587"), ("FLYING", "415267"), ("FLYING", "404027"), ("GHOST", "101386"), ("ELETRIC", "381236"),
                ("ELETRIC", "301042"), ("FAIRY", "414997"), ("FAIRY", "413288"), ("FIGHINT", "544881"), ("FIGHINT", "889435"),
                ("GRASS", "502380"), ("GRASS", "381258"), ("GROUND", "112251"), ("GROUND", "413963"), ("ICE", "381236"),
                ("NORMAL", "140845"), ("NORMAL", "70794"), ("POISON", "405797"), ("POISON", "416906"), ("PSYCHIC", "280993"),
                ("PSYCHIC", "498104"), ("ROCK", "381236"), ("STEEL", "133733"), ("STEEL", "414302"), ("WATER", "396804"),
                ("WATER", "315235"), ("WATER", "843606")]
    ###### LOGIN ######
    user = User(driver, url)
    while not user.login():
        user = User(driver, url)
    ###### END_LOGIN ######

    ###### TRAINING ######
    url = driver.current_url.replace("dashboard/", "")
    while True:
        natureLeaders = []
        nature = input("Tipo do Pókemon: ").upper()
        
        if nature == "EXIT":
            sys.exit(0)
        
        for leader in leaders:
            if leader[0] == nature:
                natureLeaders.append(leader)
        
        choice = random.randint(0, len(natureLeaders)-1)
        url += "battle-user/" + natureLeaders[choice][-1]
        driver.get(url)

        nextPage = driver.find_elements_by_class_name("button-small")
        for element in nextPage:
            if "Continue" in element.get_attribute("value"):
                element.click()
                print("Battle start!")
                break
        



if __name__ == "__main__":
    training()
