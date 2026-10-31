# HOW SQL THINKS
## A practical field guide to hard SQL made simple
**Jagjot Bhardwaj** · Self-study edition 1.0 · October 2026

**Promise:** You will spend more time writing queries than reading explanations.

**Getting started:** Install Python 3, download `practice.sqlite` and `practice.py` into the same directory, and run `python practice.py`. Alternatively, open the database in DB Browser for SQLite. No server or paid account is needed. Type SQL ending in `;`; type `quit` to exit.

**How to use:** Open `practice.sqlite` in any SQLite client (or run `python practice.py`). Read the mental model, predict the result, run the example, then solve the remix without looking at the answer. Each lab takes roughly 10–20 minutes.

**The five-question method:**
1. OUTPUT — What should one row represent?
2. NEED — Which columns and tables contain the answer?
3. MISSING — What number, rank, or comparison must be calculated?
4. CALCULATE — Which grouping, subquery, or window produces it?
5. COMBINE — How do we filter or join without changing the grain?

**Dialect:** Executable SQLite SQL. Dates are stored as ISO text; production systems may have native date types and different syntax.

**Dataset map:** `departments(dept_id, dept_name)` → `employees(emp_id,name,dept_id,salary,manager_id,hire_date)`; `customers(customer_id,customer_name,region)` → `orders(order_id,customer_id,order_date,amount,status)`; `events(user_id,event_time,event_type)`. Intentional edge cases: missing department, empty department, customers with no orders, ties, NULL amounts, and refunded orders.

**What success looks like:** For every challenge, state the expected output grain, predict at least one row, run the query, and explain one edge case. Check your work with `Answer_Key.md`.

**Challenge rule:** Before running each query, write the expected row count and describe one tricky edge case.



## START HERE — Real setup instructions

**1. Download and extract the ZIP.** Keep `practice.py` and `practice.sqlite` in the same folder. You do not need a paid account or SQL server.

**2. Open a terminal in that folder.** On Windows, open PowerShell; on macOS, open Terminal. Run `python --version`. If macOS says command not found, try `python3 --version`. Install Python 3 if needed.

**3. Start the SQL practice runner.** Run `python practice.py` (or `python3 practice.py`). It should print `How SQL Thinks: enter SQL`.

**4. Run your first query.** Enter `SELECT name, salary FROM employees ORDER BY name;` and press Enter. A semicolon ends a query. Type `quit` to exit.

**5. Study one lab at a time.** Predict the row count, run DO, solve REMIX and LEVEL UP, and only then open the separate answer key.

**If stuck:** A `...>` prompt means you need a semicolon. `No such table` means you are using the wrong database. You can also open `practice.sqlite` in DB Browser for SQLite and run queries in the Execute SQL tab. To reset your data, extract a fresh copy of the database.

## THE FIVE-QUESTION METHOD — A worked example

Your manager asks: **Which employees earn more than their own department average?**

**OUTPUT:** One row per qualifying employee, not one row per department.

**NEED:** Names, salaries, and department IDs from `employees`.

**MISSING:** Each department's average salary.

**CALCULATE:** Group by department inside a CTE.

**COMBINE:** Join averages back to employees on `dept_id`, then compare salaries.

```sql
WITH dept_avg AS (
  SELECT dept_id, AVG(salary) AS avg_salary
  FROM employees
  WHERE dept_id IS NOT NULL
  GROUP BY dept_id
)
SELECT e.name, e.dept_id, e.salary, d.avg_salary
FROM employees e
JOIN dept_avg d ON e.dept_id = d.dept_id
WHERE e.salary > d.avg_salary
ORDER BY e.dept_id, e.name;
```

**Why it works:** The CTE produces one row per department. The join attaches the correct average to each employee without losing employee-level detail. The final filter compares each salary to its own department average. **Try:** Change `>` to `>=` and predict which extra employees appear.

## VISUAL GUIDE — Three diagrams worth remembering

**Diagram 1: Plan before writing syntax**

```text
BUSINESS QUESTION
       |
       v
OUTPUT GRAIN ---> TABLES & COLUMNS
       |                |
       v                v
MISSING VALUE ----> CALCULATE
                         |
                         v
                   COMBINE + VERIFY
```

**Diagram 2: A LEFT JOIN multiplies matches**

```text
CUSTOMER          ORDER            RESULT
North  ---------> 101           North / 101
       ---------> 102           North / 102
Silent ---------> no match      Silent / NULL

COUNT(*) = 1 for Silent, but COUNT(order_id) = 0.
```

**Diagram 3: GROUP BY versus window functions**

```text
INPUT ROWS:
Ava  / Analytics / 90000
Ben  / Analytics / 70000
Cara / Analytics / 90000

GROUP BY department: ONE row -> Analytics / 83333.33
WINDOW AVG: THREE rows -> Ava, Ben, Cara each
                         with department avg 83333.33
```

**Remember:** GROUP BY changes grain. A window calculation preserves the input rows.

## Your independent study plan

**Prerequisite:** You can write a basic SELECT, WHERE, and ORDER BY query. If not, practice those first using SQLBolt. **Time:** 7 days at 45–60 minutes daily, or 14 days at 20–30 minutes. You need only Python 3 and the supplied files.

| Day | Labs | Goal |
|---|---|---|
| 1 | 01–02 | Predict output and define grain |
| 2 | 03–04 | Find join and NULL traps |
| 3 | 05–06 | Build correct aggregates and CTEs |
| 4 | 07–08 | Compare correlated and window approaches |
| 5 | 09–10 | Rank and calculate sequences |
| 6 | 11–12 | Test absence and debug performance |
| 7 | Final Boss A–E | Solve without solutions, then correct mistakes |

**Per-lab routine (20–30 minutes):** (1) Read THINK (2 min). (2) Write the predicted row count and grain on paper (2 min). (3) Run DO and compare (3 min). (4) Solve REMIX without the key (7 min). (5) Solve LEVEL UP (10 min). (6) Explain an edge case and grade yourself (3 min). If stuck, inspect the DO query, try a smaller subset of rows, then consult the key. Return to missed exercises the next day.

**Scoring:** 0 = cannot start; 1 = works with hints; 2 = works independently and explains NULLs, ties, and grain. Record a score for REMIX and LEVEL UP in each lab (maximum 48 points). Target at least 40/48 and solve four of five Final Boss tasks unaided. These are learning targets, not certification claims.

**Study log:** For each lab write: date / predicted rows / actual rows / REMIX 0–2 / LEVEL UP 0–2 / mistake learned / revisit date.

**Safe practice:** Work only in the supplied sample database. To reset it, extract a fresh copy from the ZIP. CREATE INDEX changes the local sample database.


## LAB 01 • The SQL mental model

**THINK (30 seconds):** FROM/JOIN → WHERE → GROUP BY → HAVING → window calculations → SELECT output → DISTINCT → ORDER BY → LIMIT is a simplified logical reasoning sequence, not a physical execution plan. SQL engines may optimize execution differently; aliases and window placement have dialect-specific rules.

**WHY THIS MATTERS:** Filters apply before display ordering; test the boundary values.

**DO:** Find Analytics employees with salary above 75,000. Predict row count first.

```sql
SELECT name, salary FROM employees WHERE dept_id = 1 AND salary > 75000 ORDER BY name;
```

**REMIX — no solution shown here:** Change the filter to salary >= 90000. Explain why the count changes.

**PREDICT:** Predict the exact two names returned before running the example.

**LEVEL UP:** Return Analytics employees earning at least 70,000, ordered by salary descending and name ascending.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 02 • Grain before syntax

**THINK (30 seconds):** Grain = what one output row represents. GROUP BY changes grain; window functions preserve it.

**WHY THIS MATTERS:** Define one output row before choosing GROUP BY or a window.

**DO:** Return one row per department with headcount, including only assigned employees.

```sql
SELECT dept_id, COUNT(*) AS headcount FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id ORDER BY dept_id;
```

**REMIX — no solution shown here:** Return one row per employee with the department headcount using a window.

**PREDICT:** Explain why the result has three rows although four departments exist.

**LEVEL UP:** List every department including empty Legal with a zero headcount.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 03 • Joins and invisible duplication

**THINK (30 seconds):** A join matches rows, not concepts. One-to-many matches multiply rows. Always compare counts before and after.

**WHY THIS MATTERS:** A one-to-many join can multiply rows. Count matched IDs, not synthetic rows.

**DO:** Show every customer and their number of orders, including customers with none.

```sql
SELECT c.customer_id,c.customer_name,COUNT(o.order_id) AS order_count FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id GROUP BY c.customer_id,c.customer_name ORDER BY c.customer_id;
```

**REMIX — no solution shown here:** Explain why COUNT(*) gives 1 for Silent.

**PREDICT:** Predict the order count for Silent and explain why a LEFT JOIN retains it.

**LEVEL UP:** List customers and total paid revenue, without counting refunded orders.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 04 • NULL and three-valued logic

**THINK (30 seconds):** NULL is unknown, not zero. = NULL is never true; use IS NULL. COUNT(column) ignores NULL.

**WHY THIS MATTERS:** NULL is not zero: use IS NULL, and remember COUNT(column) skips NULL.

**DO:** Find employees with no assigned department.

```sql
SELECT emp_id,name FROM employees WHERE dept_id IS NULL;
```

**REMIX — no solution shown here:** Compare COUNT(*) with COUNT(amount) on orders.

**PREDICT:** Predict whether `amount = NULL` finds any rows.

**LEVEL UP:** Return order IDs with missing amounts and count them.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 05 • Conditional aggregation

**THINK (30 seconds):** CASE turns business rules into columns. Decide whether your denominator counts rows, people, or non-NULL values.

**WHY THIS MATTERS:** Write the business rule for the numerator and denominator before using CASE.

**DO:** Count paid and refunded orders per customer, including zero-order customers.

```sql
SELECT c.customer_id,SUM(CASE WHEN o.status = 'paid' THEN 1 ELSE 0 END) AS paid_count,SUM(CASE WHEN o.status = 'refunded' THEN 1 ELSE 0 END) AS refunded_count FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id GROUP BY c.customer_id ORDER BY c.customer_id;
```

**REMIX — no solution shown here:** Calculate paid revenue per customer; do not count pending or refunded amounts.

**PREDICT:** Explain why pending orders must not be counted as paid.

**LEVEL UP:** Show each customer’s paid-order percentage; define zero-order behavior.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 06 • Subqueries versus CTEs

**THINK (30 seconds):** A CTE names an intermediate result. It is not automatically a materialized temporary table.

**WHY THIS MATTERS:** A CTE names a calculation; it is not automatically a stored temporary table.

**DO:** Find employees earning above the overall average salary.

```sql
WITH avg_pay AS (SELECT AVG(salary) AS a FROM employees) SELECT e.name,e.salary FROM employees e CROSS JOIN avg_pay x WHERE e.salary > x.a ORDER BY e.salary DESC,e.emp_id;
```

**REMIX — no solution shown here:** Rewrite with a scalar subquery.

**PREDICT:** Predict which employees exceed the overall average.

**LEVEL UP:** Show employees earning below the overall average, with the average beside each row.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 07 • Correlated subqueries

**THINK (30 seconds):** For each outer row, compare against a group defined by that row. Think logically per row; optimizer execution may differ.

**WHY THIS MATTERS:** A correlated query must compare each row to the correct outer-group key.

**DO:** Find employees earning above their own department average; omit unassigned employees.

```sql
SELECT e.name,e.dept_id,e.salary FROM employees e WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id=e.dept_id) ORDER BY e.dept_id,e.name;
```

**REMIX — no solution shown here:** Find paid orders above the average paid order for the same customer.

**PREDICT:** Explain why an employee is compared with their own department.

**LEVEL UP:** Return every employee and their department average; preserve unassigned employees.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 08 • Window functions

**THINK (30 seconds):** OVER(PARTITION BY ...) computes group statistics without collapsing rows. Filter the result in an outer query.

**WHY THIS MATTERS:** Window functions preserve rows; use a CTE to filter window results.

**DO:** Solve department-above-average with a window function.

```sql
WITH scored AS (SELECT name,dept_id,salary,AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg FROM employees WHERE dept_id IS NOT NULL) SELECT name,dept_id,salary FROM scored WHERE salary > dept_avg ORDER BY dept_id,name;
```

**REMIX — no solution shown here:** Show each employee and the difference from department average.

**PREDICT:** Predict whether a window function reduces the employee row count.

**LEVEL UP:** Show salary minus department average for each assigned employee.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 09 • Top N per group and ties

**THINK (30 seconds):** ROW_NUMBER gives exactly N positions; RANK can return more than N when tied. Always define a tie-breaker for deterministic ROW_NUMBER.

**WHY THIS MATTERS:** ROW_NUMBER, RANK, and DENSE_RANK handle ties differently.

**DO:** Find the two highest-paid employees per department, breaking ties by emp_id.

```sql
WITH ranked AS (SELECT name,dept_id,salary,ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC,emp_id) AS rn FROM employees WHERE dept_id IS NOT NULL) SELECT name,dept_id,salary FROM ranked WHERE rn <= 2 ORDER BY dept_id,rn;
```

**REMIX — no solution shown here:** Use RANK instead and explain why Analytics may return three people for rank <= 2.

**PREDICT:** Explain the difference between ROW_NUMBER, RANK, and DENSE_RANK for salary ties.

**LEVEL UP:** Return all employees tied for the highest salary in each department.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 10 • LAG and running totals

**THINK (30 seconds):** LAG compares neighboring ordered rows. Running totals need an explicit ROWS frame and deterministic order.

**WHY THIS MATTERS:** LAG needs an explicit ordering and usually a PARTITION BY entity.

**DO:** For each customer, show each paid order and the previous paid amount.

```sql
SELECT customer_id,order_id,amount,LAG(amount) OVER(PARTITION BY customer_id ORDER BY order_date,order_id) AS previous_amount FROM orders WHERE status = 'paid' ORDER BY customer_id,order_date,order_id;
```

**REMIX — no solution shown here:** Calculate running paid revenue by customer using ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.

**PREDICT:** Predict the previous paid order amount for order 102.

**LEVEL UP:** Compute each customer’s cumulative paid revenue in order date/order ID sequence.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 11 • EXISTS and anti-joins

**THINK (30 seconds):** EXISTS asks whether a match exists; NOT EXISTS handles no-match questions without NOT IN NULL traps.

**WHY THIS MATTERS:** NOT EXISTS safely checks absence even when nullable values are present.

**DO:** Find customers who have never placed an order.

```sql
SELECT c.customer_id,c.customer_name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id);
```

**REMIX — no solution shown here:** Find customers with a paid order but no refunded order.

**PREDICT:** Explain why NOT EXISTS is safer than NOT IN with NULL-producing subqueries.

**LEVEL UP:** Find customers with no paid orders, including customers with only pending orders.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## LAB 12 • Real-world debugging and performance

**THINK (30 seconds):** Verify grain, row counts, join keys, NULL behavior, ties, and date boundaries. EXPLAIN QUERY PLAN helps inspect SQLite access choices.

**WHY THIS MATTERS:** Verify correctness and row counts before interpreting query plans.

**DO:** Find total paid revenue per region without accidentally counting refunds.

```sql
SELECT c.region,SUM(CASE WHEN o.status = 'paid' THEN COALESCE(o.amount,0) ELSE 0 END) AS paid_revenue FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id GROUP BY c.region ORDER BY c.region;
```

**REMIX — no solution shown here:** Add an index on orders(customer_id,status) and compare EXPLAIN QUERY PLAN before and after.

**PREDICT:** Explain why summing all order amounts would overstate paid revenue.

**LEVEL UP:** Compare the query plan for a filtered order lookup before and after an index.

**SELF-GRADE:** Score REMIX and LEVEL UP 0–2 each. State the output grain, predict one exact row, and explain a relevant NULL, tie, or missing-match edge case. Record one mistake to revisit tomorrow.


---
## Debugging clinic — fix before checking the answer

**Bug 1: LEFT JOIN turns into an INNER JOIN.** Why does this query omit customers without paid orders? Rewrite it to preserve all customers and show paid order counts, including zero.

```sql
SELECT c.customer_id, COUNT(o.order_id)
FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id
WHERE o.status='paid'
GROUP BY c.customer_id;
```

**Bug 2: misleading order count.** Why does COUNT(*) return one for a customer with no orders after a LEFT JOIN? Replace it with the appropriate count.

**Bug 3: unstable top-N.** What happens if two employees have equal salaries in ROW_NUMBER() without a secondary ORDER BY key? Make the result deterministic.

**Bug 4: wrong denominator.** A paid-order percentage should divide paid orders by all actual orders, not the synthetic row from a LEFT JOIN. Write a safe zero-order expression.

---
## FINAL BOSS — Solve without peeking

**A.** Top 3 salaries per department, including everyone tied at the third-highest *distinct salary*.

**B.** Customers whose total paid spending is above the average total paid spending among *all customers*, including customers with zero paid spending.

**C.** Each customer's latest paid order, breaking date ties by higher order_id.

**D.** Show every department, even Legal, with headcount and average salary.

**E.** Find the first order date for each customer, keeping customers without orders.

**Self-test:** Can you explain grain, ties, missing matches, and NULLs before writing each query? If yes, you are thinking in SQL.

## Independent final exam

Allow 45 minutes. Solve Final Boss A–E using only the database and this manuscript, not the answer key. For each answer provide SQL, grain, expected row count, and a one-sentence edge-case explanation. Check against the key only after finishing. If fewer than four are correct, repeat labs related to your mistakes, then retry after 24 hours.

## Verification checklist

- [ ] I can describe one output row in plain English.
- [ ] I checked whether joins can multiply rows.
- [ ] I tested empty groups, missing matches, NULLs, and ties.
- [ ] I used a deterministic ORDER BY whenever the order matters.
- [ ] I checked my results against the seed data rather than trusting a plausible-looking query.

## Pocket reference

- `WHERE`: filter input rows; `HAVING`: filter groups.
- `GROUP BY`: collapse to group grain; `OVER`: keep row grain.
- `ROW_NUMBER`: deterministic top N with complete ORDER BY; `RANK`: preserve ties.
- `NOT EXISTS`: safe absence test; `NOT IN`: watch for NULLs.
- `COUNT(*)`: all rows; `COUNT(col)`: non-NULL values.
- `LEFT JOIN`: unmatched left rows survive; right-table predicates in WHERE can remove them.
- `UNION`: deduplicates; `UNION ALL`: preserves duplicates.
- `EXPLAIN QUERY PLAN`: inspect the access strategy, not a runtime guarantee.

## Sources and further practice

- PostgreSQL 18 official SQL SELECT and window-function documentation: https://www.postgresql.org/docs/current/sql-select.html and https://www.postgresql.org/docs/current/tutorial-window.html
- SQLBolt interactive fundamentals: https://sqlbolt.com/

## License

Copyright © 2026 Jagjot Bhardwaj. Released under Creative Commons Attribution 4.0 International (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/ . Attribute the author when reusing. Dataset and SQL examples are original teaching material.