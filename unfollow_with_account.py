from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import random


from args import get_args_wa



class InstaScrapFollow():
    def __init__(self,
                 username,
                 password):
        self.username = username
        self.password = password
        self.identifier_substring = "'s profile picture"
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.followers = set()
        self.following = set()
        self.no_follower = int(0)
        self.no_following = int(0)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        self.allow_cookies()

        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")

        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)
        sleep(random.uniform(6, 12))

    def allow_cookies(self):
        try:
            cookie_accept_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Allow all cookies']")))
            cookie_accept_button.click()
        except Exception as e:
            print("No cookie consent button found or an issue occurred while clicking it.")
        sleep(random.uniform(6, 12))

    def go_to_target_profile(self, target_account):
        self.driver.get(f"https://www.instagram.com/{target_account}/")
        sleep(random.uniform(6, 12))

    def init_follower_button(self):
        self.followers_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]")))
        self.no_follower = int(self.followers_button.text.split()[0])

    def init_following_button(self):
        self.following_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following/')]")))
        self.no_following = int(self.following_button.text.split()[0])

    def get_accounts_loop(self, accounts_set, no_accounts):
        stalled_scrolls = 0
        max_scrolls = 5
        while len(accounts_set) < no_accounts:
            lst_len_accounts_set = len(accounts_set)
            self.extract_names(accounts_set)
            print(f"# extracted: {len(accounts_set)} of total {no_accounts}")
            self.scroll()
            sleep(3)
            if lst_len_accounts_set == len(accounts_set):
                stalled_scrolls += 1
            else:
                stalled_scrolls = 0

            if stalled_scrolls >= max_scrolls:
                raise RuntimeError(
                """
                No new accounts visible after {} scrolls.
                Only got {} out of a total of {} accounts.
                Instagram may be limiting the list. This account might be (shadow) banned.
                It worked for me once target and scrape account were the same. But more risky.""".format(max_scrolls,
                                                                                                         len(accounts_set),
                                                                                                         no_accounts)
                )
            self.quit()
        print('All account names are extracted')

    def extract_names(self, name_set):
        elements = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//div[@role='button']")
        name_set.update({el.accessible_name.split(self.identifier_substring)[0] for el in elements})

    def scroll(self):
        modal = self.driver.find_element(By.XPATH, "(//div[@role='dialog']//div)[last()]")
        actions = ActionChains(self.driver)
        actions.move_to_element(modal).perform()
        sleep(3)

    def get_followers(self):
        self.init_follower_button()
        self.followers_button.click()
        self.get_accounts_loop(self.followers, self.no_follower)


    def get_following(self):
        self.init_following_button()
        self.following_button.click()
        self.get_accounts_loop(self.following, self.no_following)


    def print_href_to_unfollow(self):
        not_following_back = self.following - self.followers
        for name in not_following_back:
            print(f"https://www.instagram.com/{name}")

    def quit(self):
        self.driver.quit()



if __name__ == "__main__":
    args, _ = get_args_wa()

    InstaScraper = InstaScrapFollow(args.username, args.password)
    InstaScraper.login()
    InstaScraper.go_to_target_profile(args.target_account)
    print("Start extracting follower account names")
    InstaScraper.get_followers()
    InstaScraper.go_to_target_profile(args.target_account)
    print("Start extracting following account names")
    InstaScraper.get_following()
    InstaScraper.print_href_to_unfollow()
    InstaScraper.quit()
