## Task 1: SQL Queries

For this task, PostgreSQL was used to recreate a database with the following tables:
- `users`
- `leads`
- `domains`
- `courses`

### Files
- **create_table.sql**
  A SQL script that creates the tables and inserts sample values.
- **sql_queries.sql**
  Contains the SQL queries required to answer the task specifications.

---

## Task 2: Web Scraping

This task involves scraping the landing page of [mate.academy](https://mate.academy/) to extract course information. The scraper collects the following details for each course:
- **Course Name**
- **Short Description**
- **Course Duration**
- In the task the Course type (full-time or flex) is mentioned but it seems like every course can be full-time and flex

### Key Features
- **Headless Browser:** Uses Chrome in headless mode for efficient, non-GUI operation.
- **Dynamic Content Handling:**
  - Clicks the "Показати більше" ("Show More") button (using JavaScript) to load more courses.
- **Data Extraction:** Retrieves course name, description, and duration from each course card.
- **Output:** The scraped course data is saved to a JSON file (`courses.json`).

### How to Run the Scraper
1. Ensure you have Selenium and ChromeDriver installed.
2. Run the scraper script (e.g., using `python your_scraper.py`).
3. The output will be saved as `courses.json`.

requirements.txt also included

---
