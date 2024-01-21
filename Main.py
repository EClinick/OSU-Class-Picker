from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.wait as wait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, NoSuchWindowException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import CourseInfo as CI
import time
import os
import sys
#import env file .env
from dotenv import load_dotenv
chrome_options = Options()


#driver = webdriver.Edge(chrome_options)

""" options=uc.ChromeOptions()
options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
driver=uc.Chrome(options=options)
url="https://classes.oregonstate.edu/?keyword=CS261&srcdb=202402"

#driver.get(url)
orginal_window=driver.current_window_handle """
load_dotenv()
username=os.getenv("USER")

password=os.getenv("PASSWORD")



def get_user_input():
    global set_up_classes
    set_up_classes= input("Have you set up classes already?")


""" def main(args):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Set up Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    if len(args)<7:
        print("Please enter in the following format: python WorkingOneWithoutComments.py <Search/Submit> <Course(CS261)> <term(F,W,S)> <time(HH:MM-HH:MM(p/a) or SKIP)> <include_online(T/F)> <professor>")
        sys.exit(1)
    elif args[1].lower() == "search":
        #help
    course=args[1]
    term=args[2]
    time=args[3]
    include_online=args[4].lower()=='t'
    prof=args[5]

    CI.get_open_sections(course, term, time, include_online, prof,driver)
    #for section in sections:
        #print(section)
 """

def main(args):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    if len(args) < 2:
        print("Usage: python script.py <search/submit> [additional arguments]")
        sys.exit(1)

    mode = args[1].lower()
    print(f"Mode selected: {mode}")  # Debug print

    if mode == "submit":
        # The hardcoded file path for 'submit' mode
        file_path = 'C:\\Users\\ethan\\OneDrive\\Documents\\Comp sci\\Scraping OSU myclass\\github_submission\\Look-up-a-Course\\example.txt'
        print("Submit mode activated, processing courses from file.")  # Debug print
        processing_courses(file_path, driver)
    elif mode == "search":
        if len(args) != 7:
            print("Usage: python script.py search <Course> <Term> <Time> <Include_Online> <Professor>")
            sys.exit(1)
        course = args[2]
        term = args[3]
        time = args[4]
        include_online = args[5].lower() == 't'
        prof = args[6]
        print("Search mode activated, searching for courses.")  # Debug print
        CI.get_open_sections(course, term, time, include_online, prof, driver, criteria=False)
    else:
        print("Invalid mode. Please choose 'search' or 'submit'.")
        sys.exit(1)

    driver.quit()

# Rest of your functions ...

def read_course_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()  # Read all lines in the file into a list

    # Extract the details from the lines
    # Make sure to check that there are enough lines in the file
    courses = lines[0].strip().split(",") if len(lines) > 0 else []
    term = lines[1].strip() if len(lines) > 1 else ""
    times = lines[2].strip().split(",") if len(lines) > 2 else []
    include_online = lines[3].strip().lower() == 't' if len(lines) > 3 else False
    profs = lines[4].strip().split(",") if len(lines) > 4 else []

    return courses, term, times, include_online, profs
def check_course_availability(driver, course, term, time, include_online, prof):
    return CI.get_open_sections(course, term, time, include_online, prof,driver,criteria=True)
def processing_courses(file_path, driver):
    print("Processing courses")
    try:
        courses, term, times, include_online, profs = read_course_file(file_path)
    except IndexError as e:
        print(f"Error reading file: {e}")
        return
    print(f"Checking availability for {len(courses)} courses")
    for course, time, prof in zip(courses, times, profs):
        print(f"Checking availability for {course} with {prof} at {time}")
        availability = CI.get_open_sections(course, term, time, include_online, prof, driver, criteria=True)
        if availability:
            print(f"Found open sections for {course} with {prof} at {time}")
        else:
            print(f"No open sections for {course} with {prof} at {time}")
        print(availability)
    confirm_classes(driver, course, term, availability)
#def choosing_classes(driver, course, term,sections_to_choose):
        
def confirm_classes(driver, course, term,availability):
    user=input("Do you want to continue and submit those classes?(Y/N)")
    if term == "F":
        term = 202401
    elif term == "W":
        term = 202402
    elif term == "S":
        term = 202403
    if user.upper() == "Y":
        print(f"Currently debugging please manually submit classes https://classes.oregonstate.edu/?keyword={course}&srcdb={term}\n Continuing submitting classes...")
        driver.quit()
        main_part(term)
        #choosing_classes(course, term, availability)
""" 
def choosing_classes(course, term,sections_to_choose):
    uc_options=uc.ChromeOptions()
    uc_options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    driver=uc.Chrome(options=uc_options)
    driver.get(f"https://classes.oregonstate.edu/?keyword={course}&srcdb={term}")

   
    for crn, info in sections_to_choose.items():

        try: 
           #//*[@id="crit-keyword"]
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="crit-keyword"]')))
            course_input=driver.find_element(By.XPATH, '//*[@id="crit-keyword"]')
            course_input.clear()
            course_input.send_keys(info)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="crit-srcdb"]')))
            term_input=driver.find_element(By.XPATH, '//*[@id="crit-srcdb"]')
            term_input.clear()
            term_input.send_keys(term)

            #//*[@id="search-button"]
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="search-button"]')))
            search_button=driver.find_element(By.XPATH, '//*[@id="search-button"]')
            search_button.click()   
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".result__flex--3")))
            crn=driver.find_element(By.CSS_SELECTOR, ".result__flex--3").text.strip()
            crn.click()

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn")))
            add_to_cart=driver.find_element(By.CLASS_NAME, "btn")
            add_to_cart.click()

        except NoSuchElementException:
            print(f"Stale element reference at section {term}, retrying...")   
        except Exception as e:
            print(f"An error occurred while processing section {term}: {e}")

 """

#/html[1]/body[1]/header[1]/div[2]/a[1]
def main_part(term):
    options=uc.ChromeOptions()
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    driver=uc.Chrome(options=options)
    url=f"https://classes.oregonstate.edu/?keyword=CS261&srcdb={term}"
    print("url thats fucked"+url)
    driver.get(url)
    orginal_window=driver.current_window_handle
    try:
        
        the_url=driver.find_element(by=By.XPATH, value="/html[1]/body[1]/header[1]/div[2]/a[1]")
        print(the_url.get_attribute("href"))
        the_url.click()
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            print(driver.current_url)
            login_url=driver.current_url
            
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username")))
            username_driver=driver.find_element(by=By.ID, value="username").send_keys(username)
            time.sleep(3)

            password_selector="#password"
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, password_selector)))

            password_driver=driver.find_element(by=By.CSS_SELECTOR, value=password_selector)

            for char in password:
                password_driver.send_keys(char)
                time.sleep(0.2)

            button_driver=driver.find_element(by=By.CSS_SELECTOR, value="body > main > form > div:nth-child(4) > button").click()

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#auth-view-wrapper > div:nth-child(2) > div.row.display-flex.align-flex-justify-content-center.verification-code")))
            code=driver.find_element(by=By.CSS_SELECTOR, value="#auth-view-wrapper > div:nth-child(2) > div.row.display-flex.align-flex-justify-content-center.verification-code").text
            DUO= driver.current_url
            print("Please type in DUO CODE:"+code)
            windows=driver.window_handles
            if len(windows) > 1:
                driver.switch_to.window(windows[1])
            else:
                print("No DUO window found")
            #Sleep until driver.current_window_handle is not DUO
            time.sleep(15)
            #try:

            #/html/body
            ##dont-trust-browser-button
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#dont-trust-browser-button")))
            trust_button = driver.find_element(by=By.CSS_SELECTOR, value="#dont-trust-browser-button")
            print("attempting to click")
            trust_button.click()
            print("clicked")
            WebDriverWait(driver, 10).until(EC.staleness_of(trust_button))
            time.sleep(10)
            print("Clicked on 'Yes, this is my device' button.")
        
            #time.sleep(10)
            driver.switch_to.window(orginal_window)
        
            print("Before switching to default" +str(driver.current_url))
            
            #choosing_classes(driver)

            #Clicks on primary cart button
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/main[1]/div[1]/div[1]/div[2]/form[1]/div[5]/div[1]/div[1]/button[1]")))
            enroll = driver.find_element(by=By.XPATH, value="/html[1]/body[1]/main[1]/div[1]/div[1]/div[2]/form[1]/div[5]/div[1]/div[1]/button[1]")
            enroll.click()
            
            #click on submit schedule button
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/main[1]/div[2]/div[1]/div[4]/div[1]/button[2]")))
            submit_schedule = driver.find_element(by=By.XPATH, value="/html[1]/body[1]/main[1]/div[2]/div[1]/div[4]/div[1]/button[2]")
            original_window = driver.current_window_handle

            # Click to open the 2nd tab
            submit_schedule.click()

            # Wait for the 2nd tab and switch to it
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            windows_handles = driver.window_handles
            second_tab = [window for window in windows_handles if window != original_window][0]
            driver.switch_to.window(second_tab)
            print("Switched to second tab")

            # Click to open the 3rd tab
            #abs xpath is: /html[1]/body[1]/div[4]/div[2]/div[4]/div[2]/span[1]/div[1]/a[1]/button[1]/div[1]/div[1]
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[4]/div[2]/div[4]/div[2]/span[1]/div[1]/a[1]/button[1]/div[1]/div[1]")))
            get_registered = driver.find_element(by=By.XPATH, value="/html[1]/body[1]/div[4]/div[2]/div[4]/div[2]/span[1]/div[1]/a[1]/button[1]/div[1]/div[1]")
            get_registered.click()    
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(3))
            windows_handles = driver.window_handles
            third_tab = [window for window in windows_handles if window not in [original_window, second_tab]][0]
            driver.switch_to.window(third_tab)
            print("Switched to third tab")


            select2_dropdown = driver.find_element(by=By.CSS_SELECTOR, value="#s2id_txt_term > a")
            select2_dropdown.click()

            # Step 2: Ensure the input box inside the dropdown is visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".select2-input"))
            )
            select2_search_box = driver.find_element(by=By.CSS_SELECTOR, value=".select2-input")

            # Step 3: Use ActionChains to type "Winter 2024" with a slight delay between keys
            actions = ActionChains(driver)
            actions.move_to_element(select2_search_box)
            if term == 202401:
                term = "Fall 2024"
            elif term == 202402:
                term = "Winter 2024"
            elif term == 202403:
                term = "Spring 2024"
            for char in term:
                actions.send_keys(char)
                actions.pause(0.5)  # Pause between key presses
            actions.perform()

            # Step 4: Wait for the results to show up and become clickable
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='202402']"))
            )
            #//*[@id="202402"]
            # Step 5: Click the "Winter 2024" option in the results
            winter_2024_option = driver.find_element(
                by=By.XPATH, 
                value="//*[@id='202402']"
            )
            actions = ActionChains(driver)
            actions.move_to_element(winter_2024_option).click().perform()

            # Step 6: Click the "Submit" button
            #//*[@id="term-go"]
            # Scroll the "Continue" button into view and then click
            # Wait for any AJAX calls to complete before clicking the button
            # Wait for JavaScript to confirm that no overlays are present and the page is ready
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )  

            # Additional custom JavaScript conditions can be added, such as:
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return !!window.jQuery && jQuery.active == 0')
            )

            # Then click the "Continue" button
            continue_button = driver.find_element(by=By.CSS_SELECTOR, value="#term-go")
            driver.execute_script("arguments[0].click();", continue_button)


            prompt_user=input("Do you want to manually do it?(Y/N)")
            if prompt_user == "Y":
                time.sleep(300)
            else:
                print("Continuing with program")

            #clicking ok button
            #//*[@id="notification-center"]/div/ul[2]/li/div[2]/button

            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='notification-center']/div/ul[2]/li/div[2]/button")))
            ok_button = driver.find_element(by=By.XPATH, value="//*[@id='notification-center']/div/ul[2]/li/div[2]/button")
            ok_button.click()


            #add all button
            #//*[@id="planAccordion"]/div[1]/div/button
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='planAccordion']/div[1]/div/button")))
            add_all_button = driver.find_element(by=By.XPATH, value="//*[@id='planAccordion']/div[1]/div/button")
            add_all_button.click()

            #submit button
            #//*[@id="saveButton"]
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='saveButton']")))
            submit_button = driver.find_element(by=By.XPATH, value="//*[@id='saveButton']")
            submit_button.click()

            #calendar
            #//*[@id="scheduleCalViewLink"]/span
            #take a screenshoot then scroll to the bottom

            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='scheduleCalViewLink']/span")))
            calendar_button = driver.find_element(by=By.XPATH, value="//*[@id='scheduleCalViewLink']/span")
            calendar_button.click()

            #Screenshot of calendar
            calendar_button.screenshot("calendar.png")
        
            #scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            calendar_button.screenshot("calendar_bottom.png")


            #Registered status
            #//*[@id="summaryBody"]/div[1]/div/table/tbody/tr[1]/td[6]/span
            ##summaryBody > div.grid-wrapper.grid-without-title > div > table > tbody > tr:nth-child(2) > td:nth-child(6)
            #data-property="status"

            time.sleep(20)
    except (NoSuchElementException, StaleElementReferenceException, NoSuchWindowException) as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main(sys.argv)
    #main_part()
    