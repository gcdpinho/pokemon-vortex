# -*- coding: utf-8 -*-
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


def main():
    url = "https://www.pokemon-vortex.com/"
    driver = webdriver.PhantomJS()
    leaders = [("BUG","415355"), ("DARK", "840815"), ("DRAGON", "415125"), ("FIRE", "19935"), ("FIRE", "381236"),
                ("FLYING", "42587"), ("FLYING", "415267"), ("FLYING", "404027"), ("GHOST", "101386"), ("ELETRIC", "381236"),
                ("ELETRIC", "301042"), ("FAIRY", "414997"), ("FAIRY", "413288"), ("FIGHTING", "544881"), ("FIGHTING", "889435"),
                ("GRASS", "502380"), ("GRASS", "381258"), ("GROUND", "112251"), ("GROUND", "413963"), ("ICE", "381236"),
                ("NORMAL", "140845"), ("NORMAL", "70794"), ("POISON", "405797"), ("POISON", "416906"), ("PSYCHIC", "280993"),
                ("PSYCHIC", "498104"), ("ROCK", "381236"), ("STEEL", "133733"), ("STEEL", "414302"), ("WATER", "396804"),
                ("WATER", "315235"), ("WATER", "843606")]
    ###### LOGIN ######
    user = User(driver, url)
    while not user.login():
        user = User(driver, url)
    ###### END_LOGIN ######

    training(driver, url, leaders, False)

def training(driver, url, leaders, iteration):
    ###### TRAINING ######
    sleep = 3
    url = driver.current_url.replace("dashboard/", "")
    repeat = False
    while True:
        natureLeaders = []
        nature = input("Tipo do Pókemon: ").upper()
        
        if nature == "EXIT":
            sys.exit(0)
        # encontra um leader para treinar o tipo do pokemon
        for leader in leaders:
            if leader[0] == nature:
                natureLeaders.append(leader)
        # opção inválida
        if len(natureLeaders) == 0:
            print("Opção Inválida! Tente novamente.")
            continue
        # escolhe randomicamente um trainer do tipo escolhido
        choice = random.randint(0, len(natureLeaders)-1)
        driver.get(url + "battle-user/" + natureLeaders[choice][-1])
        # seleciona o ataque do pokemon
        att = selectAttack(driver, url, sleep)
        # start Battle
        print("start Battle!")
        flag = True
        first = True
        while flag:
            flag = False
            nextPage = driver.find_elements_by_class_name("button-small")
            for element in nextPage:
                # continue ou atack
                value = element.get_attribute("value")
                if "select_attack" in value or "attack" in value:
                    first = battleRound(driver, element, att, first, 50, sleep)
                    flag = True
                    break;
            if not flag:
                try:
                    # continue - morte de um pokemon
                    print ("Defeat")
                    onClick(driver.find_element_by_css_selector("input[value='pokechu']"), 1, sleep)
                    flag = True
                except:
                    # end battle
                    print("end Battle!\n")
                    # show rewards
                    rewards = driver.find_element_by_id("ajax").find_elements_by_tag_name('p')
                    print(rewards[-1].text.replace("\n", "", 1)+"\n")
                    if iteration:
                        decision = input("Rebattle Opponent (s/n): ").lower()
                    else:
                        # verifica o level do pokemon
                        onClick(driver.find_elements_by_class_name("menu-tab")[1], 0, sleep)
                        level = driver.find_elements_by_class_name("monster-container")[0].find_elements_by_tag_name("p")[0]
                        level = level.text.split(":")[1].split("\n")[0][1:]
                        decision = "n"
                        if int(level) < 100:
                            driver.get(url + "battle-user/" + natureLeaders[choice][-1])
                            flag = True
                        else:
                            print("Parabéns, você atingiu o level 100!")
                    if decision == "s":
                        # rebattle opponent
                        onClick(driver.find_elements_by_class_name("menu-tab")[0].find_element_by_tag_name("a"), 0, sleep)
                        flag = True
                    continue           

def selectAttack(driver, url, sleep):
    # permite escolher o ataque do pokemon
    onClick(driver.find_element_by_id("pokeName1"), 0, sleep)
    col = driver.find_elements_by_class_name("valign-top")[-1].find_elements_by_tag_name("td")[0]
    col = col.text.split("\n")
    for i in range(1, len(col)):
        print(str(i)+": "+col[i])
    choice = input("Escolha o attack: ")
    onClick(driver.find_element_by_id("pokedexTab"), 0, sleep)
    
    return int(choice)

def battleRound(driver, element, att, first, low, sleep):
    # round de batalha
    value = element.get_attribute("value")
    if "select_attack" in value:
        print("Continue")
    elif "attack" in value:   
        if first:
            print("Choice attack!")
            changeAttack(driver, att, sleep)
            first = False
        else:
            usePotion(driver, low, sleep)
        print("Attack")
    onClick(element, 1, sleep)

    return first

def usePotion(driver, low, sleep):
    # usar pot quando vida menor que low
    hp = driver.find_elements_by_tag_name("strong")[1].text.split(": ")[-1]
    if int(hp) <= low:
        onClick(driver.find_element_by_id("item1"), 0, sleep)
        bts = driver.finds_element_by_class_name("button-small")
        for bt in bts:
            if "Use Item" in bt.get_attribute("value"):
                print("HP: "+hp+". Use potion!")
                onClick(bt, 1, sleep)
                break
            
def changeAttack(driver, att, sleep):
     onClick(driver.find_element_by_class_name("attackForm").find_elements_by_tag_name("td")[att-1].find_element_by_tag_name("label"), 0, sleep)

def onClick(element, click, sleep):
    if click == 0:
        element.click()
    elif click == 1:
        element.submit()
    time.sleep(sleep)

if __name__ == "__main__":
    main()
