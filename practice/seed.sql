-- How SQL Thinks: synthetic practice dataset (SQLite)
-- Run with: sqlite3 practice.sqlite < practice/seed.sql
BEGIN TRANSACTION;
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY,customer_name TEXT,region TEXT);
INSERT INTO customers VALUES(1,'North','East'),(2,'South','West'),(3,'Central','East'),(4,'New','West'),(5,'Silent','East');
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY,dept_name TEXT);
INSERT INTO departments VALUES(1,'Analytics'),(2,'Engineering'),(3,'Operations'),(4,'Legal');
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY,name TEXT,dept_id INTEGER,salary INTEGER,manager_id INTEGER,hire_date TEXT);
INSERT INTO employees VALUES(1,'Ava',1,90000,NULL,'2022-01-10'),(2,'Ben',1,70000,1,'2023-02-01'),(3,'Cara',1,90000,1,'2023-04-15'),(4,'Dan',2,120000,NULL,'2021-08-01'),(5,'Eli',2,95000,4,'2024-03-10'),(6,'Fay',2,95000,4,'2024-04-01'),(7,'Gia',3,60000,NULL,'2022-07-10'),(8,'Hal',3,50000,7,'2023-01-10'),(9,'Ian',3,45000,7,'2024-06-01'),(10,'Joy',NULL,80000,NULL,'2025-01-01');
CREATE TABLE events(user_id INTEGER,event_time TEXT,event_type TEXT);
INSERT INTO events VALUES(1,'2026-01-01','login'),(1,'2026-01-03','login'),(1,'2026-01-03','purchase'),(2,'2026-01-02','login'),(2,'2026-01-08','login'),(3,'2026-01-05','login');
CREATE TABLE orders(order_id INTEGER PRIMARY KEY,customer_id INTEGER,order_date TEXT,amount INTEGER,status TEXT);
INSERT INTO orders VALUES(101,1,'2026-01-03',100,'paid'),(102,1,'2026-01-07',200,'paid'),(103,1,'2026-02-03',200,'refunded'),(104,2,'2026-01-09',80,'paid'),(105,2,'2026-02-11',120,'paid'),(106,3,'2026-02-12',300,'paid'),(107,3,'2026-02-12',300,'paid'),(108,4,'2026-03-01',NULL,'pending');
COMMIT;
