# HOW SQL THINKS — ANSWER KEY

## Worked lab output (SQLite seed dataset)

### 01 • The SQL mental model

Expected 2 rows:

```text
('Ava', 90000)
('Cara', 90000)
```

### 02 • Grain before syntax

Expected 3 rows:

```text
(1, 3)
(2, 3)
(3, 3)
```

### 03 • Joins and invisible duplication

Expected 5 rows:

```text
(1, 'North', 3)
(2, 'South', 2)
(3, 'Central', 2)
(4, 'New', 1)
(5, 'Silent', 0)
```

### 04 • NULL and three-valued logic

Expected 1 rows:

```text
(10, 'Joy')
```

### 05 • Conditional aggregation

Expected 5 rows:

```text
(1, 2, 1)
(2, 2, 0)
(3, 2, 0)
(4, 0, 0)
(5, 0, 0)
```

### 06 • Subqueries versus CTEs

Expected 6 rows:

```text
('Dan', 120000)
('Eli', 95000)
('Fay', 95000)
('Ava', 90000)
('Cara', 90000)
('Joy', 80000)
```

### 07 • Correlated subqueries

Expected 4 rows:

```text
('Ava', 1, 90000)
('Cara', 1, 90000)
('Dan', 2, 120000)
('Gia', 3, 60000)
```

### 08 • Window functions

Expected 4 rows:

```text
('Ava', 1, 90000)
('Cara', 1, 90000)
('Dan', 2, 120000)
('Gia', 3, 60000)
```

### 09 • Top N per group and ties

Expected 6 rows:

```text
('Ava', 1, 90000)
('Cara', 1, 90000)
('Dan', 2, 120000)
('Eli', 2, 95000)
('Gia', 3, 60000)
('Hal', 3, 50000)
```

### 10 • LAG and running totals

Expected 6 rows:

```text
(1, 101, 100, None)
(1, 102, 200, 100)
(2, 104, 80, None)
(2, 105, 120, 80)
(3, 106, 300, None)
(3, 107, 300, 300)
```

### 11 • EXISTS and anti-joins

Expected 1 rows:

```text
(5, 'Silent')
```

### 12 • Real-world debugging and performance

Expected 2 rows:

```text
('East', 900)
('West', 200)
```

## Final boss solutions

### A
```sql
WITH x AS (SELECT dept_id,name,salary,DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r FROM employees WHERE dept_id IS NOT NULL) SELECT * FROM x WHERE r<=3 ORDER BY dept_id,r,name;
```
Expected 9 rows: `[(1, 'Ava', 90000, 1), (1, 'Cara', 90000, 1), (1, 'Ben', 70000, 2), (2, 'Dan', 120000, 1), (2, 'Eli', 95000, 2), (2, 'Fay', 95000, 2), (3, 'Gia', 60000, 1), (3, 'Hal', 50000, 2), (3, 'Ian', 45000, 3)]`

### B
```sql
WITH totals AS (SELECT c.customer_id,COALESCE(SUM(CASE WHEN o.status='paid' THEN o.amount ELSE 0 END),0) AS spend FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id GROUP BY c.customer_id) SELECT * FROM totals WHERE spend>(SELECT AVG(spend) FROM totals);
```
Expected 2 rows: `[(1, 300), (3, 600)]`

### C
```sql
WITH x AS (SELECT *,ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date DESC,order_id DESC) AS rn FROM orders WHERE status='paid') SELECT customer_id,order_id,order_date,amount FROM x WHERE rn=1;
```
Expected 3 rows: `[(1, 102, '2026-01-07', 200), (2, 105, '2026-02-11', 120), (3, 107, '2026-02-12', 300)]`

### D
```sql
SELECT d.dept_id,d.dept_name,COUNT(e.emp_id) AS headcount,AVG(e.salary) AS avg_salary FROM departments d LEFT JOIN employees e ON e.dept_id=d.dept_id GROUP BY d.dept_id,d.dept_name ORDER BY d.dept_id;
```
Expected 4 rows: `[(1, 'Analytics', 3, 83333.33333333333), (2, 'Engineering', 3, 103333.33333333333), (3, 'Operations', 3, 51666.666666666664), (4, 'Legal', 0, None)]`

### E
```sql
SELECT c.customer_id,c.customer_name,MIN(o.order_date) AS first_order FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id GROUP BY c.customer_id,c.customer_name ORDER BY c.customer_id;
```
Expected 5 rows: `[(1, 'North', '2026-01-03'), (2, 'South', '2026-01-09'), (3, 'Central', '2026-02-12'), (4, 'New', '2026-03-01'), (5, 'Silent', None)]`

## Level-up challenge solutions (verified against practice.sqlite)

### Lab 01

```sql
SELECT name,salary FROM employees WHERE dept_id=1 AND salary>=70000 ORDER BY salary DESC,name;
```

Expected result (3 rows):
```text
('Ava', 90000)
('Cara', 90000)
('Ben', 70000)
```

### Lab 02

```sql
SELECT d.dept_name,COUNT(e.emp_id) AS headcount FROM departments d LEFT JOIN employees e ON e.dept_id=d.dept_id GROUP BY d.dept_id,d.dept_name ORDER BY d.dept_id;
```

Expected result (4 rows):
```text
('Analytics', 3)
('Engineering', 3)
('Operations', 3)
('Legal', 0)
```

### Lab 03

```sql
SELECT c.customer_name,COALESCE(SUM(CASE WHEN o.status='paid' THEN o.amount ELSE 0 END),0) AS revenue FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id GROUP BY c.customer_id,c.customer_name ORDER BY c.customer_id;
```

Expected result (5 rows):
```text
('North', 300)
('South', 200)
('Central', 600)
('New', 0)
('Silent', 0)
```

### Lab 04

```sql
SELECT order_id FROM orders WHERE amount IS NULL ORDER BY order_id;
```

Expected result (1 rows):
```text
(108,)
```

### Lab 05

```sql
SELECT c.customer_id,CASE WHEN COUNT(o.order_id)=0 THEN NULL ELSE ROUND(100.0*SUM(CASE WHEN o.status='paid' THEN 1 ELSE 0 END)/COUNT(o.order_id),1) END AS paid_pct FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id GROUP BY c.customer_id ORDER BY c.customer_id;
```

Expected result (5 rows):
```text
(1, 66.7)
(2, 100.0)
(3, 100.0)
(4, 0.0)
(5, None)
```

### Lab 06

```sql
SELECT name,salary,(SELECT AVG(salary) FROM employees) AS overall_avg FROM employees WHERE salary<(SELECT AVG(salary) FROM employees) ORDER BY salary,name;
```

Expected result (4 rows):
```text
('Ian', 45000, 79500.0)
('Hal', 50000, 79500.0)
('Gia', 60000, 79500.0)
('Ben', 70000, 79500.0)
```

### Lab 07

```sql
SELECT name,dept_id,salary,AVG(salary) OVER(PARTITION BY dept_id) AS dept_avg FROM employees ORDER BY emp_id;
```

Expected result (10 rows):
```text
('Ava', 1, 90000, 83333.33333333333)
('Ben', 1, 70000, 83333.33333333333)
('Cara', 1, 90000, 83333.33333333333)
('Dan', 2, 120000, 103333.33333333333)
('Eli', 2, 95000, 103333.33333333333)
('Fay', 2, 95000, 103333.33333333333)
('Gia', 3, 60000, 51666.666666666664)
('Hal', 3, 50000, 51666.666666666664)
('Ian', 3, 45000, 51666.666666666664)
('Joy', None, 80000, 80000.0)
```

### Lab 08

```sql
SELECT name,dept_id,salary,salary-AVG(salary) OVER(PARTITION BY dept_id) AS delta FROM employees WHERE dept_id IS NOT NULL ORDER BY dept_id,name;
```

Expected result (9 rows):
```text
('Ava', 1, 90000, 6666.6666666666715)
('Ben', 1, 70000, -13333.333333333328)
('Cara', 1, 90000, 6666.6666666666715)
('Dan', 2, 120000, 16666.66666666667)
('Eli', 2, 95000, -8333.333333333328)
('Fay', 2, 95000, -8333.333333333328)
('Gia', 3, 60000, 8333.333333333336)
('Hal', 3, 50000, -1666.6666666666642)
('Ian', 3, 45000, -6666.666666666664)
```

### Lab 09

```sql
WITH x AS (SELECT name,dept_id,salary,DENSE_RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) AS r FROM employees WHERE dept_id IS NOT NULL) SELECT name,dept_id,salary FROM x WHERE r=1 ORDER BY dept_id,name;
```

Expected result (4 rows):
```text
('Ava', 1, 90000)
('Cara', 1, 90000)
('Dan', 2, 120000)
('Gia', 3, 60000)
```

### Lab 10

```sql
SELECT customer_id,order_id,amount,SUM(amount) OVER(PARTITION BY customer_id ORDER BY order_date,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_revenue FROM orders WHERE status='paid' ORDER BY customer_id,order_date,order_id;
```

Expected result (6 rows):
```text
(1, 101, 100, 100)
(1, 102, 200, 300)
(2, 104, 80, 80)
(2, 105, 120, 200)
(3, 106, 300, 300)
(3, 107, 300, 600)
```

### Lab 11

```sql
SELECT c.customer_id,c.customer_name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id AND o.status='paid') ORDER BY c.customer_id;
```

Expected result (2 rows):
```text
(4, 'New')
(5, 'Silent')
```

### Lab 12

```sql
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id=1 AND status='paid';
```

Expected result (1 rows):
```text
(2, 0, 0, 'SCAN orders')
```



## Debugging clinic — explanations

**Bug 1:** A WHERE predicate on the right-hand table removes NULL-extended rows. Move the paid condition into the JOIN predicate, then COUNT(o.order_id):

```sql
SELECT c.customer_id, COUNT(o.order_id) AS paid_orders
FROM customers c LEFT JOIN orders o
  ON o.customer_id=c.customer_id AND o.status='paid'
GROUP BY c.customer_id ORDER BY c.customer_id;
```

**Bug 2:** COUNT(*) counts the NULL-extended left-join row. COUNT(o.order_id) counts only matched orders.

**Bug 3:** ROW_NUMBER() without a unique tie-breaker can assign different positions to equal salaries. Use ORDER BY salary DESC, emp_id ASC.

**Bug 4:** Use COUNT(o.order_id) as denominator; use NULLIF(COUNT(o.order_id),0) to avoid dividing by zero, and COALESCE(...,0) if zero-order customers should display 0%.

## Self-assessment rubric

Give 2 points for an independently correct query with correct grain and a stated edge case; 1 point for a correct query after a hint or with a missing explanation; 0 for incorrect or unsolved. The aim is understanding, not speed.


## Debugging clinic — explanations

**Bug 1:** A WHERE predicate on the right-hand table removes NULL-extended rows. Move the paid condition into the JOIN predicate, then COUNT(o.order_id):

```sql
SELECT c.customer_id, COUNT(o.order_id) AS paid_orders
FROM customers c LEFT JOIN orders o
  ON o.customer_id=c.customer_id AND o.status='paid'
GROUP BY c.customer_id ORDER BY c.customer_id;
```

**Bug 2:** COUNT(*) counts the NULL-extended left-join row. COUNT(o.order_id) counts only matched orders.

**Bug 3:** ROW_NUMBER() without a unique tie-breaker can assign different positions to equal salaries. Use ORDER BY salary DESC, emp_id ASC.

**Bug 4:** Use COUNT(o.order_id) as denominator; use NULLIF(COUNT(o.order_id),0) to avoid dividing by zero, and COALESCE(...,0) if zero-order customers should display 0%.

## Self-assessment rubric

Give 2 points for an independently correct query with correct grain and a stated edge case; 1 point for a correct query after a hint or with a missing explanation; 0 for incorrect or unsolved. The aim is understanding, not speed.