-- 1.1. The number of created leads per week grouped by course type
SELECT
  DATE_TRUNC('week', l.created_at) AS week,
  c.type AS course_type,
  COUNT(*) AS num_leads
FROM leads l
JOIN courses c ON l.course_id = c.id
GROUP BY week, c.type
ORDER BY week;

--1.2. The number of WON flex leads per country created from 01.01.2024
SELECT
  d.country_name,
  COUNT(CASE
          WHEN l.created_at >= '2024-01-01'
            AND l.status = 'WON'
            AND c.type = 'FLEX'
          THEN 1
        END) AS won_flex_leads
FROM domains d
LEFT JOIN users u ON d.id = u.domain_id
LEFT JOIN leads l ON u.id = l.user_id
LEFT JOIN courses c ON l.course_id = c.id
GROUP BY d.country_name;

--1.3. User email, lead id and lost reason for users who have lost flex leads from 01.07.2024
SELECT u.email,
       l.id AS lead_id,
       l.lost_reason
FROM users u
JOIN leads l ON u.id = l.user_id
WHERE l.id IN (
    SELECT l2.id
    FROM leads l2
    JOIN courses c ON l2.course_id = c.id
    WHERE l2.created_at >= '2024-07-01'
      AND l2.status = 'LOST'
      AND c.type = 'FLEX'
);