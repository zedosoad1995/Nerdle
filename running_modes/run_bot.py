from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from helpers.helper import load_all_moves
from helpers.main_functions import filter_combinations, get_suggestions


NO_COLOR = '#989484'
RED = '#820458'
BLACK = '#161803'
GREEN = '#398874'


def open_webpage(website):
   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
   driver.implicitly_wait(2)
   driver.get(website)

   return driver


def remove_popups(driver):
   iframe = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//iframe[@title="SP Consent Message"]')))
   driver.switch_to.frame(iframe)

   # Get rid of initial popups (cookies, instructions)
   driver.find_element(by=By.XPATH, value='//button[@title="Accept"]').click()
   driver.switch_to.default_content()
   driver.find_element(by=By.XPATH, value='//button[@aria-label="Home" and @class="focus:outline-none"]').click()


def write_calculation_guess(driver, action_str):
   for ch in list(action_str):
      if ch == '-':
         ch = 'minus'

      driver.find_element(by=By.XPATH, value=f'//button[contains(@aria-label,"{ch}")]').click()

   driver.find_element(by=By.XPATH, value=f'//button[@aria-label="ENTER "]').click()


def get_color_by_class(str):
   if RED in str:
      return 'r'
   elif GREEN in str:
      return 'g'
   elif BLACK in str:
      return 'b'

   raise Exception('Invalid color')


def get_cmd(slots, calculations):
   return ' '.join([calculations[i] + get_color_by_class(slot.get_attribute("class")) for i, slot in enumerate(slots)])


def is_win(cmd):
   return cmd.count('g') == 8


def play_online(driver, game_type: str, possible_combinations, action_str):
   row_num = 1
   if game_type == 'normal':
      write_calculation_guess(driver, action_str)

   while True:
      next_row = driver.find_element(by=By.XPATH, value=f'//div[contains(@class,"flex justify-center mb-1")][{row_num}]')
      slots = WebDriverWait(next_row, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, f'div[not(contains(@class,"{NO_COLOR}"))]'))
      )

      action_str = ''.join([slot.get_attribute("aria-label")[0] for slot in slots])

      cmd = get_cmd(slots, action_str)
      if is_win(cmd):
         return

      possible_combinations = filter_combinations(possible_combinations, cmd)
      action_str = get_suggestions(possible_combinations)[0][0]

      write_calculation_guess(driver, action_str)

      row_num += 1


def run_bot(urls, guess, all):
   possible_combinations = load_all_moves()

   if all:
      urls = ['https://nerdlegame.com/', 'https://speed.nerdlegame.com/', 'https://instant.nerdlegame.com/']
   else:
      urls = [urls]

   for url in urls:
      driver = open_webpage(url)
      remove_popups(driver)

      game_type = 'normal'
      if any(game_keyword for game_keyword in ['instant', 'speed'] if game_keyword in url):
         game_type = 'reactive'

      play_online(driver, game_type, possible_combinations, guess)

   sleep(1000)

   driver.close()
