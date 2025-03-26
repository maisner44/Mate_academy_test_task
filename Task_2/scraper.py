import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def click_show_more(driver):
    try:
        show_more = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.ProfessionsListSectionTemplate_button__zcWRS"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", show_more)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", show_more)
        time.sleep(3)
    except Exception as e:
        print("Button not found", e)

def scrape_courses(driver, url="https://mate.academy/"):
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    courses_section = wait.until(
        EC.presence_of_element_located((By.ID, "all-courses"))
    )
    click_show_more(driver)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.ProfessionCard_cardWrapper__BCg0O")))
    try:
        cards_wrapper = courses_section.find_element(By.CLASS_NAME, "ProfessionsListSectionTemplate_cardsWrapper__un6ny")
    except Exception as e:
        return []
    course_elements = cards_wrapper.find_elements(By.TAG_NAME, "a")
    courses = []
    for course in course_elements:
        course_data = {"course_name": "", "description": "", "duration": ""}
        try:
            title_elem = course.find_element(By.CSS_SELECTOR, "h3.ProfessionCard_title__m7uno")
            course_data["course_name"] = title_elem.text.strip()
        except Exception as e:
            try:
                title_elem = course.find_element(By.TAG_NAME, "h3")
                course_data["course_name"] = title_elem.text.strip()
            except Exception as e:
                print("Could not get course name")
                print(course.get_attribute("outerHTML"))
        try:
            description_elem = course.find_element(By.CSS_SELECTOR, "p.ProfessionCard_description__K8weo")
            description_text = description_elem.get_attribute("textContent").strip()
            course_data["description"] = description_text
        except Exception as e:
            print("Could not get course description", course_data["course_name"])
        try:
            duration_elem = course.find_element(By.CSS_SELECTOR, "p.ProfessionCard_duration__13PwX")
            course_data["duration"] = duration_elem.text.strip()
        except Exception as e:
            print("Could not get course duration", course_data["course_name"])
        courses.append(course_data)
    return courses

if __name__ == "__main__":
    driver = init_driver()
    try:
        courses = scrape_courses(driver)
        with open("courses.json", "w", encoding="utf-8") as f:
            json.dump(courses, f, ensure_ascii=False, indent=4)
    finally:
        driver.quit()
