from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException

# List of scripted comments
comments = ['This is a brilliant picture!', 'Wow!', 'Lovely!', 'I like this vibe!', 'Beautiful!']

#  Global variables
#  *  Counter variables
count_action, count_likes, count_follows, count_comments = 0, 0, 0, 0

#  CONTROL PANEL
#  Login identifier
your_username = 'your_username'
your_password = 'your_password'

#  The newsfeed type equivalent to a hashtag (usually)
#  *  Exception: If you write here 'explore' then the automated process will run there.
newsfeed_type = 'digitalart'

#  How much content should I respond to?
num_of_reactions = 42

#  Chromedriver
w_driver = webdriver.Chrome()
#  *  Initial position
w_driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')


#  Non-existent xpath exception handler
def check_exists_by_xpath(xpath):
    try:
        w_driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


#  Random sleep length scheduler
def randomizator():
    base = 4
    bonus = random.randint(0, 6)
    bonus_plus = random.randint(0, 1)
    w_driver.implicitly_wait(base + bonus)  # Faster script running
    sleep(bonus_plus)


#  Take the action on explore's newsfeed
#  TODO: This not based on num_of_reactions variable yet... This function is recursive now.
#  TODO: Add the next button solution, but sometimes maybe close the post and reopen too.
#  TODO: Add follow function
def bot_by_explore():
    global count_action
    for y in range(1, 4):
        for x in range(1, 4):
            current_post = w_driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/div/div[' + str(y) + ']/div[' + str(x) + ']')
            current_post.click()
            randomizator()

            #  Send a like
            like_content = w_driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div[3]/section[1]/span[1]/button')
            like_content.click()
            randomizator()

            #  Send a comment
            text_area_path = '/html/body/div[6]/div[2]/div/article/div[3]/section[3]/div/form/textarea'
            comment = w_driver.find_element_by_xpath(text_area_path)
            comment.click()
            randomizator()
            comment = w_driver.find_element_by_xpath(text_area_path).send_keys(random.choice(comments))
            randomizator()
            comment_send = w_driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div[3]/section[3]/div/form/button[2]')
            comment_send.click()
            randomizator()

            #  TODO: Follow function.

            count_action += 1
            close_post = w_driver.find_element_by_xpath('/html/body/div[6]/div[3]/button')
            close_post.click()
            randomizator()
    bot_by_explore()


def bot_by_hashtag():
    global count_action, count_likes, count_follows, count_comments
    randomizator()

    print('............................')
    print(str(count_action + 1) + '. POST:')
    #  Send a like (frequent process)
    if bool(random.getrandbits(1)) or bool(random.getrandbits(1)):
        like_content = w_driver.find_element_by_xpath(
            '/html/body/div[6]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()
        print("Like sent...")
        count_likes += 1
        randomizator()
    else:
        print("Like skipped...")

    #  Send a comment (rare process)
    text_area_path = '/html/body/div[6]/div[2]/div/article/div[3]/section[3]/div/form/textarea'
    if bool(random.getrandbits(1)) and bool(random.getrandbits(1)) and check_exists_by_xpath(text_area_path):
        comment = w_driver.find_element_by_xpath(text_area_path).click()
        comment_txt = w_driver.find_element_by_xpath(text_area_path).send_keys(random.choice(comments))
        randomizator()
        comment_send = w_driver.find_element_by_xpath(
            '/html/body/div[6]/div[2]/div/article/div[3]/section[3]/div/form/button[2]')
        comment_send.click()
        print("Comment sent...")
        count_comments += 1
        sleep(4)
    else:
        print("Comment area not found or skipped...")

    #  Send a follow (legendary process)
    if bool(random.getrandbits(1) and random.getrandbits(1) and random.getrandbits(1)):
        follow_creator = w_driver.find_element_by_xpath(
            '/html/body/div[6]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
        print("Follow sent...")
        count_follows += 1
        followed_path = '/html/body/div[7]/div/div/div/div[3]/button[2]'
        #  If you followed that person in the past
        if check_exists_by_xpath(followed_path):
            undo = w_driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[3]/button[2]').click()
            count_follows -= 1
    else:
        print("Follow skipped...")

    #  Navigate to the next post
    next_post = w_driver.find_element_by_xpath('/html/body/div[6]/div[1]/div/div/a[2]').click()
    count_action += 1


def start():
    #  Login process
    #  *  Handle the cookie policy
    accept_cookies = w_driver.find_element_by_xpath('/html/body/div[4]/div/div/button[1]')
    accept_cookies.click()
    randomizator()

    #  *  Type the username
    username = w_driver.find_element_by_name('username')
    username.send_keys(your_username)
    randomizator()

    #  *  Type the password
    password = w_driver.find_element_by_name('password')
    password.send_keys(your_password)
    randomizator()

    #  *  Login the profile
    login_btn = w_driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button')
    login_btn.click()
    randomizator()

    #  *  Skip the pop-up notification feature
    notification = w_driver.find_element_by_xpath("//button[contains(text(), 'Not now')]")
    notification.click()
    randomizator()

    #  Starter position of the newsfeed
    if newsfeed_type == 'explore':
        w_driver.get('https://www.instagram.com/' + newsfeed_type)
        randomizator()
        bot_by_explore()
    else:
        w_driver.get('https://www.instagram.com/explore/tags/' + newsfeed_type)
        randomizator()
        post = w_driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div/div[2]')
        post.click()
        for _ in range(num_of_reactions):
            bot_by_hashtag()
    w_driver.quit()


#  The test begins...
start()
#  The board of statistics
print('############################')
print('#         SUMMARY          #')
print('############################')
print('----------------------------')
print('Sent likes:       ' + str(count_likes))
print('Skipped likes:    ' + str(count_action - count_likes))
print('----------------------------')
print('Sent follows:     ' + str(count_follows))
print('Skipped follows:  ' + str(count_action - count_follows))
print('----------------------------')
print('Sent comments:    ' + str(count_comments))
print('Skipped comments: ' + str(count_action - count_comments))
print('----------------------------')
print('----------------------------')
print('Total reaction: ' + str(count_action))
print('----------------------------')
