CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(50),
    domain_id INT,
    language_id INT
);

CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    course_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    lost_reason TEXT
);

CREATE TABLE domains (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100),
    country_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100),
    type VARCHAR(50),
    language_id INT,
    sort INT
);


INSERT INTO users (id, email, first_name, last_name, phone, domain_id, language_id)
VALUES
  (35, 'jsmith@example.com', 'John', 'Smith', '(123) 456-7890', 1, 1),
  (47, 'ldoe@example.com', 'Laura', 'Doe', '(987) 654-3210', 1, 1),
  (51, 'mbrown@example.com', 'Michael', 'Brown', '(555) 123-4567', 4, 5),
  (62, 'newuser@example.com', 'New', 'User', '(000) 000-0000', 1, 1);

INSERT INTO leads (id, user_id, course_id, created_at, updated_at, status, lost_reason)
VALUES
  (10, 35, 25, '2024-01-14 11:17:29.664+00', '2024-02-26 17:28:13.647+00', 'LOST', 'NO_CONTACT'),
  (16, 35, 38, '2024-01-13 18:42:38.671+00', '2024-01-30 12:01:44.473+00', 'WON', NULL),
  (45, 62, 27, '2024-01-12 16:49:15.082+00', '2024-02-13 09:13:07.151+00', 'NEW', NULL);


INSERT INTO domains (id, slug, country_name, created_at, updated_at, active)
VALUES
  (1, 'ua', 'Ukraine', '2023-07-27 09:31:22.147845+00', '2024-02-26 10:21:53.046+00', TRUE),
  (3, 'pl', 'Poland', '2023-12-21 09:14:32.8806+00', '2024-02-15 11:24:51.941+00', FALSE);


INSERT INTO courses (id, slug, type, language_id, sort)
VALUES
  (12, 'python_basics', 'MODULE', 1, 3),
  (25, 'frontend', 'FULL_TIME', 1, 5),
  (27, 'devops', 'FLEX', 1, 1);

