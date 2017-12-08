from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import sys
import random
import time

class User():

    def __init__(self, driver, url):
        #self.username = input("Usuário: ")
        #self.password = getpass.getpass("Senha: ")
        self.username = "gcdpinho"
        self.password = "gustavo4878286"
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
    driver.implicitly_wait(5)
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
    repeat = False
    while True:
        natureLeaders = []
        nature = input("Tipo do Pókemon: ").upper()
        
        if nature == "EXIT":
            sys.exit(0)
        
        for leader in leaders:
            if leader[0] == nature:
                natureLeaders.append(leader)

        if len(natureLeaders) == 0:
            print("Opção Inválida! Tente novamente.")
            continue
        # escolhe randomicamente um trainer do tipo escolhido
        choice = random.randint(0, len(natureLeaders)-1)
        driver.get(url + "battle-user/" + natureLeaders[choice][-1])
        # start Battle
        flag = True
        while flag:
            flag = False
            
            nextPage = driver.find_elements_by_class_name("button-small")
            for element in nextPage:
                if "select_attack" in element.get_attribute("value") or "attack" in element.get_attribute("value") or "pokechu" in element.get_attribute("value"):
                    print (element.get_attribute('value'))
                    element.submit()
                    time.sleep(5)
                    flag = True
                    break
        # show rewards
        
        #rewards = driver.find_element_by_id("ajax").find_elements_by_tag_name('p')
        for reward in rewards:
            print(reward.get_attribute('innerHTML'))




if __name__ == "__main__":
    training()
