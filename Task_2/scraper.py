import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)

def click_show_more(driver):
    # Find the "Show More" button using its CSS selector and click on it.
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

def scrape_course_detail(driver, url):
    # Open course page in a new tab.
    driver.execute_script("window.open(arguments[0]);", url)
    driver.switch_to.window(driver.window_handles[-1])
    topics = ""
    modules = 0
    about_course = ""
    try:
        # Wait for the section with ID "course-program" to load.
        course_program_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "course-program"))
        )
        # Get the topics count from the element within this section.
        topics_elem = course_program_section.find_element(By.CSS_SELECTOR, "p.FactBlockIcon_factNumber__FTmxv.mb-8")
        topics = topics_elem.text.strip()
    except Exception as e:
        print("Could not get topics count from", url, e)
    try:
        # Get the number of modules by counting the <p> elements with the specified class inside the "course-program" section.
        module_elems = course_program_section.find_elements(By.CSS_SELECTOR, "p.CourseModulesList_topicName__7vxtk")
        modules = str(len(module_elems))
    except Exception as e:
        print("Could not get modules count from", url, e)
    try:
        # Get the course description from the element that contains additional course info.
        about_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.CourseModulesList_aboutCourse__gmavO"))
        )
        about_course = about_elem.text.strip()
    except Exception as e:
        print("Could not get about course info from", url, e)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return {"topics_count": topics, "modules_count": modules, "about_course": about_course}

def scrape_courses(driver, url="https://mate.academy/"):
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    courses_section = wait.until(EC.presence_of_element_located((By.ID, "all-courses")))
    click_show_more(driver)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.ProfessionCard_cardWrapper__BCg0O")))
    try:
        cards_wrapper = courses_section.find_element(By.CLASS_NAME, "ProfessionsListSectionTemplate_cardsWrapper__un6ny")
    except Exception:
        return []
    course_elements = cards_wrapper.find_elements(By.TAG_NAME, "a")
    courses = []
    for course in course_elements:
        course_data = {"course_name": "", "description": "", "duration": "", "topics_count": "", "modules_count": ""}
        # Get the course name from the <h3> element with class "ProfessionCard_title__m7uno".
        try:
            title_elem = course.find_element(By.CSS_SELECTOR, "h3.ProfessionCard_title__m7uno")
            course_data["course_name"] = title_elem.text.strip()
        except Exception:
            print("Could not get course name")
        # Get the course duration from the <p> element with class "ProfessionCard_duration__13PwX".
        try:
            duration_elem = course.find_element(By.CSS_SELECTOR, "p.ProfessionCard_duration__13PwX")
            course_data["duration"] = duration_elem.text.strip()
        except Exception:
            print("Could not get course duration", course_data["course_name"])
        try:
            href = course.get_attribute("href")
            if href:
                detail = scrape_course_detail(driver, href)
                course_data["topics_count"] = detail["topics_count"]
                course_data["modules_count"] = detail["modules_count"]
                course_data["description"] = detail["about_course"]
        except Exception:
            print("Could not get course detail", course_data["course_name"])
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
