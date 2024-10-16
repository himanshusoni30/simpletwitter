from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from linkedintwitter import LinkedInTwitter
from selenium.webdriver.chrome.service import Service
import requests
from lxml import etree
import time
import json
import time

'''LOCATORS'''
TWITTER_URL = "https://twitter.com/i/flow/login"
EMAIL = ".//input[@name='text']"
NEXT_BUTTON = ".//span[contains(text(),'Next')]/parent::span/parent::div[@dir='ltr']"
PASSWORD = ".//input[@name='password']"
LOGIN_BUTTON = ".//button[@data-testid='LoginForm_Login_Button']"
POST_BUTTON = ".//a[@href='/compose/post']"
TWEET_TEXT = "(.//div[@aria-label='Post text'])[1]"
SEARCH_BOX = ".//input[@placeholder='Search']"
TWEETS = "//article[@role='article']"
LIKE_BUTTONS = "//button[@data-testid='like']"
LIKE_BUTTON = "(//button[@data-testid='like'])[1]"
POST_TWEET_BUTTON = "//button[@data-testid='tweetButton']"
PROFILE_BUTTON = "//a[@aria-label='Profile']"
LIKE_TAB_IN_PROFILE = "//span[contains(text(),'Likes')]"
UNLIKE_BUTTONS = "//button[@data-testid='unlike']"
REPOST_BUTTONS = "//button[@data-testid='retweet']"
RETWEET_CONFIRM_BUTTON = "//div[@data-testid='retweetConfirm']"
CLOSE_BAR_BUTTON = "(.//button[@role='button'][@type='button'])[2]"

class SimpleTwitter:
    def __init__(self, email, password, no_of_tweets, user_name):
        self.email = email
        self.password = password
        self.no_of_tweets = no_of_tweets
        self.user_name = user_name
        self.s = Service(ChromeDriverManager().install())
        self.bot = webdriver.Chrome(service=self.s)
        self.bot.maximize_window()
        self.wait = WebDriverWait(self.bot, 20)


    def login(self):
        bot = self.bot
        bot.get(TWITTER_URL)
        print("Attempt1")
        try:
            email_path = self.wait.until(EC.presence_of_element_located((By.XPATH, EMAIL))).send_keys(self.email)
            login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, NEXT_BUTTON))).click()
            try:
                username = self.wait.until(EC.presence_of_element_located((By.XPATH, EMAIL))).send_keys(self.user_name)
                next_button = self.wait.until(EC.presence_of_element_located((By.XPATH, NEXT_BUTTON))).click()
            except:
                pass
            password = self.wait.until(EC.presence_of_element_located((By.XPATH, PASSWORD))).send_keys(self.password)
            time.sleep(1)
            login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON))).click()
            time.sleep(5)
        except:
            print("Attempt2")
            email = self.wait.until(EC.presence_of_element_located((By.XPATH, EMAIL))).send_keys(self.email)
            next_button = self.wait.until(EC.presence_of_element_located((By.XPATH, NEXT_BUTTON))).click()
            try:
                print("Attempt3")
                username = self.wait.until(EC.presence_of_element_located((By.XPATH, EMAIL))).send_keys(self.user_name)
                next_button = self.wait.until(EC.presence_of_element_located((By.XPATH, NEXT_BUTTON))).click()
            except:
                pass
            password = self.wait.until(EC.presence_of_element_located((By.XPATH, PASSWORD))).send_keys(self.password)
            login_button = self.wait.until(EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON))).click()
        time.sleep(5)


    def like_tweet(self, hashtag):
        for x in hashtag:
            tweet_button_XPATH = self.wait.until(EC.presence_of_element_located((By.XPATH, SEARCH_BOX)))
            self.bot.execute_script("arguments[0].click();", tweet_button_XPATH)
            tweet_button_XPATH.send_keys(Keys.CONTROL+"a")
            tweet_button_XPATH.send_keys(Keys.DELETE)
            time.sleep(1)
            tweet_button_XPATH.send_keys(x)
            tweet_button_XPATH.send_keys(Keys.ENTER)

            for i in range(self.no_of_tweets):
                print(i)
                try:
                    likes = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, LIKE_BUTTONS)))
                    #like tweet for the given range of i
                    likes[i].click()
                    time.sleep(2)
                    print("liked_image")
                except:
                    self.bot.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
                    time.sleep(2)
                    continue

        time.sleep(1)
        print("Next hashtag")


    def only_like_top_tweet(self, hashtag):
        for x in hashtag:
            tweet_button_XPATH = self.wait.until(EC.presence_of_element_located((By.XPATH, SEARCH_BOX)))
            self.bot.execute_script("arguments[0].click();", tweet_button_XPATH)
            tweet_button_XPATH.send_keys(Keys.CONTROL + "a")
            tweet_button_XPATH.send_keys(Keys.DELETE)
            time.sleep(1)
            tweet_button_XPATH.send_keys(x)
            tweet_button_XPATH.send_keys(Keys.ENTER)

            try:
                like = self.wait.until(EC.presence_of_element_located((By.XPATH, LIKE_BUTTON))).click()
                print("liked_image")
            except:
                self.bot.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")

        time.sleep(1)
        print("Next hashtag")


    def tweet(self, tweet_body):
        tweet_button_XPATH = self.wait.until(EC.presence_of_element_located((By.XPATH, POST_BUTTON))).click()
        print("Tweet Button Clicked", tweet_body)
        message_XPATH = self.wait.until(EC.presence_of_element_located((By.XPATH, TWEET_TEXT))).send_keys(tweet_body)

        try:
            send_tweet_XPATH = self.wait.until(EC.element_to_be_clickable((By.XPATH, POST_TWEET_BUTTON))).click()
            time.sleep(2)
        except:
            self.bot.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")


    def unlike_liked_tweets(self, length):
        time.sleep(5)
        goto_profile_XPATH = self.wait.until(EC.presence_of_element_located((By.XPATH, PROFILE_BUTTON))).click()
        time.sleep(5)
        goto_liked_tweets_XPATH = self.wait.until(EC.presence_of_element_located((By.XPATH, LIKE_TAB_IN_PROFILE))).click()

        for i in range(length):
            try:
                unlikes = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, UNLIKE_BUTTONS)))
                unlikes[i].click()
                time.sleep(2)
                print("unliked_image")
            except:
                self.bot.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
                time.sleep(2)
                continue

        time.sleep(1)
        print("Next hashtag")


    def retweet(self, hashtag):
        for x in hashtag:
            tweet_button_XPATH = self.wait.until(EC.presence_of_element_located((By.XPATH, SEARCH_BOX)))
            self.bot.execute_script("arguments[0].click();", tweet_button_XPATH)
            tweet_button_XPATH.send_keys(Keys.CONTROL + "a")
            tweet_button_XPATH.send_keys(Keys.DELETE)
            tweet_button_XPATH.send_keys(x)
            tweet_button_XPATH.send_keys(Keys.ENTER)
            time.sleep(2)
            for i in range(self.no_of_tweets):
                print(i)
                try:
                    retweets = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, REPOST_BUTTONS)))
                    retweets[i].click()
                    time.sleep(1)
                    retweet_confirm_click = self.wait.until(EC.presence_of_element_located((By.XPATH, RETWEET_CONFIRM_BUTTON))).click()
                    time.sleep(2)
                    close_confirm_bar = self.wait.until(EC.presence_of_element_located((By.XPATH, CLOSE_BAR_BUTTON)))
                    self.bot.execute_script("arguments[0].click();", close_confirm_bar)
                    print("retweet")
                    self.wait.until(EC.presence_of_element_located((By.XPATH, SEARCH_BOX)))
                except:
                    self.bot.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight/4);"
                    )
                    time.sleep(2)
                    continue
        time.sleep(1)
        print("Next hashtag")


    def post_tech_news(self, no_of_tweets):
        tech = []
        tech_image = []
        techlink = []
        for i in range(0, no_of_tweets):
            print("page: ", i)
            URL = "https://www.indiatoday.in/technology/news?page=" + str(i)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id="content")
            elements = results.find_all("div", class_="catagory-listing")
            for job_element in elements:
                title_element = job_element.find("h2")
                image = job_element.find("img")
                tech_image.append(image["src"])
                tech.append(title_element.text.strip())
                if job_element.find("a", href=True):
                    location_element = job_element.find("a", href=True)
                    if location_element == "":
                        techlink.append("none")
                    else:
                        link = "https://www.indiatoday.in" + \
                            location_element["href"]
                        techlink.append(link)
        x = [
            {"news": name, "image": image, "link": link}
            for name, image, link in zip(tech, tech_image, techlink)
        ]
        for key in x:
            m = []
            for attribute, value in key.items():
                m.append(value)
            hashtag = m[0].split(' ', 1)[0]
            z = f"News: \n{m[0]}\nSource link: \n{m[2]}\n#{hashtag} "
            self.tweet(z)
            time.sleep(2)
        return x
    
    # def postLinkedIn(self, content):
    #    x = LinkedInTwitter(content)
    #    self.tweet(x)

       
if __name__ == 'main':
    app.run(debug=True)
