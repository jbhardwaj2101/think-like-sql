# How SQL Thinks

### A practical field guide to hard SQL made simple

**By Jagjot Bhardwaj · Self-study edition 1.0**

Stop memorizing query templates. Learn to reason about output grain, joins, NULL, aggregates, subqueries, windows, and real-world edge cases.

## Start here

1. **Download the practice files:** `practice/practice.sqlite` and `practice/practice.py` from this repository (or download the full repository ZIP from GitHub's **Code → Download ZIP**).
2. **Install Python 3** if needed. Open Terminal or PowerShell in the folder containing both files.
3. **Launch:** `python practice.py` (macOS may require `python3 practice.py`).
4. **Test:** enter `SELECT name, salary FROM employees ORDER BY name;` and press Enter.
5. **Read:** [the complete self-study book](book/How_SQL_Thinks.md). Work through THINK → DO → REMIX → LEVEL UP → SELF-GRADE.
6. **Check answers only after attempting the exercises:** [Answer key](book/Answer_Key.md).

You can also open `practice.sqlite` with DB Browser for SQLite and use its Execute SQL tab.

## The five-question method

**OUTPUT → NEED → MISSING → CALCULATE → COMBINE**

What does one result row represent? What data do you need? What must be calculated? How can you calculate it? How do you combine it without breaking the grain?

## What you will learn

12 labs cover SQL logical processing, output grain, join multiplication, NULL, conditional aggregation, CTEs, correlated subqueries, window functions, top-N ties, LAG and running totals, EXISTS/NOT EXISTS, and debugging query plans. The workbook includes a seven-day learning plan, diagrams, self-grading, and five final challenges.

## PDF availability

The illustrated reader PDF and separate answer-key PDF are available in the companion downloadable release package shared in ChatGPT. The PDF files are **not yet hosted in this GitHub branch**. The Markdown book is readable directly on GitHub.

## Notes

- **Dialect:** SQLite. Other SQL engines differ in some syntax and behavior.
- **Data:** Entirely synthetic educational examples.
- **License:** © 2026 Jagjot Bhardwaj. Text licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code license not yet specified.

## Publication status

This is a **review branch**. Merge only after checking the practice database and PDFs, then create a GitHub Release for public distribution.
