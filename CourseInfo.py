import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# Set up Chrome options
#chrome_options = Options()
#chrome_options.add_argument("--headless")

# Set up Chrome driver
#driver = webdriver.Chrome(options=chrome_options)

def format_time(time_str):
    if ':00' in time_str:
        return time_str.replace(':00', '')
    return time_str

def format_prof_name(prof_name):
    # Convert 'Y.Song' to 'Y. Song' for comparison
    parts = prof_name.split('.')
    return f"{parts[0]}. {parts[1]}"

def get_open_sections(course, term, time, include_online, prof,driver,criteria):
    if criteria==False:
        if term == "F":
            term = 202401
        elif term == "W":
            term = 202402
        elif term == "S":
            term = 202403

        # Format the time string if not skipped
        if time.lower() != 'skip' and time != '':
            start_time, end_time = time.split('-')
            formatted_time = f"{format_time(start_time)}-{format_time(end_time)}"
        else:
            formatted_time = None

        
        # Format professor name for comparison
        formatted_prof = format_prof_name(prof) if prof.lower() != 'skip' else None

        # Open the link
        driver.get(f"https://classes.oregonstate.edu/?keyword={course}&srcdb={term}")

        # Wait for the results to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.result")))

        sections = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.result")))
        for i, section in enumerate(sections):
            try:
                print(f"Processing section {i+1}...")
                
                section = driver.find_elements(By.CSS_SELECTOR, "div.result")[i]

                # Skip if the section is full
                is_full_icons = section.find_elements(By.CSS_SELECTOR, "i.icon--warn[title='This section is full']")
                if is_full_icons:
                    
                    print(f"Section {i+1} is full, skipping...")
                    continue

                # Get section information
                result_link = section.find_element(By.CSS_SELECTOR, "a.result__link")
                section_info = result_link.find_element(By.CSS_SELECTOR, ".result__flex--3").text.strip()
                meet_time = result_link.find_element(By.CSS_SELECTOR, ".flex--grow").text.strip()
                instructor = result_link.find_element(By.CSS_SELECTOR, ".result__flex--9.text--right").text.strip()

                # Skip online classes if not included
                section_number = ''.join(filter(str.isdigit, section_info))
                if section_number and not include_online and 400 <= int(section_number) <= 550:
                    
                    print(f"Section {section_number} is an online class, skipping...")
                    continue

                # Time filtering
                if formatted_time and formatted_time not in meet_time:
                    
                    print(f"Section {i+1} is not at the right time, skipping...")
                    continue

                # Professor filtering
                if formatted_prof and formatted_prof.lower() not in instructor.lower():
                    
                    print(f"Section {i+1} is not taught by {prof}, skipping...")
                    continue
                

                # Print the section information
                print(f"{section_info}\n{meet_time}\n{instructor}")
                #return (f"{section_info}\n{meet_time}\n{instructor}")
            except StaleElementReferenceException:
                print(f"Stale element reference at section {i+1}, retrying...")
                continue
            except Exception as e:
                print(f"An error occurred while processing section {i+1}: {e}")
        return False
    elif criteria==True:
        if term == "F":
            term = 202401
        elif term == "W":
            term = 202402
        elif term == "S":
            term = 202403

        # Format the time string if not skipped
        if time.lower() != 'skip' and time != '':
            start_time, end_time = time.split('-')
            formatted_time = f"{format_time(start_time)}-{format_time(end_time)}"
        else:
            formatted_time = None

        
        # Format professor name for comparison
        formatted_prof = format_prof_name(prof) if prof.lower() != 'skip' else None

        # Open the link
        driver.get(f"https://classes.oregonstate.edu/?keyword={course}&srcdb={term}")

        # Wait for the results to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.result")))

        sections = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.result")))

        sections_to_choose={}
        for i, section in enumerate(sections):
            try:
                print(f"Processing section {i+1}...")
                meets_criteria = True
                section = driver.find_elements(By.CSS_SELECTOR, "div.result")[i]

                # Skip if the section is full
                is_full_icons = section.find_elements(By.CSS_SELECTOR, "i.icon--warn[title='This section is full']")
                if is_full_icons:
                    meets_criteria = False
                    print(f"Section {i+1} is full, skipping...")
                    continue

                # Get section information
                result_link = section.find_element(By.CSS_SELECTOR, "a.result__link")
                section_info = result_link.find_element(By.CSS_SELECTOR, ".result__flex--3").text.strip()
                meet_time = result_link.find_element(By.CSS_SELECTOR, ".flex--grow").text.strip()
                instructor = result_link.find_element(By.CSS_SELECTOR, ".result__flex--9.text--right").text.strip()

                # Skip online classes if not included
                section_number = ''.join(filter(str.isdigit, section_info))
                if section_number and not include_online and 400 <= int(section_number) <= 550:
                    meets_criteria = False
                    print(f"Section {section_number} is an online class, skipping...")
                    continue

                # Time filtering
                if formatted_time and formatted_time not in meet_time:
                    meets_criteria = False
                    print(f"Section {i+1} is not at the right time, skipping...")
                    continue

                # Professor filtering
                if formatted_prof and formatted_prof.lower() not in instructor.lower():
                    meets_criteria = False
                    print(f"Section {i+1} is not taught by {prof}, skipping...")
                    continue
                if meets_criteria:
                    print(f"Section {i+1} meets the criteria!")
                    #print(f"Found open sections for {course} with {prof} at {time}")
                    crn=course
                    sections_to_choose[crn]=section_number

                    
                else:
                    print(f"Section {i+1} does not meet the criteria!")
                    #print(f"No open sections for {course} with {prof} at {time}")

                # Print the section information
                print(f"{section_info}\n{meet_time}\n{instructor}")
                #return (f"{section_info}\n{meet_time}\n{instructor}")
            except StaleElementReferenceException:
                print(f"Stale element reference at section {i+1}, retrying...")
                continue
            except Exception as e:
                print(f"An error occurred while processing section {i+1}: {e}")
        
        return sections_to_choose
    





if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python CourseInfo.py <course> <term> <time> <include_online(T/F)> <professor>")
        sys.exit(1)

    course = sys.argv[1]
    term = sys.argv[2]
    time = sys.argv[3]
    include_online = sys.argv[4].lower() == 't'
    prof = sys.argv[5]

    get_open_sections(course, term, time, include_online, prof)
    
