/* *********************
Section 2: Databases

Setup PostgreSQL database for sales transactions of an e-commerce company.
***********************/
-- Create admin user and database
CREATE USER dbadmin WITH ENCRYPTED PASSWORD 'dbadmin';
CREATE DATABASE sales OWNER dbadmin; -- needed for dbadmin to be able to create tables in sales

-- Create tables in sales database
\connect sales

CREATE TABLE members (
    member_id text PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    date_of_birth text NOT NULL,
    email text NOT NULL,
    mobile_no text NOT NULL
);

CREATE TABLE items (
    item_id text PRIMARY KEY,
    item_name text NOT NULL,
    manufacturer_name text NOT NULL,
    cost numeric NOT NULL,
    weight_kg numeric NOT NULL    
);

CREATE TYPE transaction_status as ENUM (
    'ordered and paid',
    'preparing',
    'in-transit',
    'delivered',
    'receipt-acknowledged',
    'completed'
);

CREATE TABLE transactions (
    txn_id text PRIMARY KEY,
    member_id text REFERENCES members (member_id),
    total_items_price numeric NOT NULL,
    total_items_weight numeric NOT NULL,
    txn_status transaction_status NOT NULL
);

CREATE TABLE txn_details (
    id bigint PRIMARY KEY,
    txn_id text REFERENCES transactions (txn_id),
    item_id text REFERENCES items (item_id),
    quantity numeric NOT NULL
);

-- Transfer ownership of tables to admin user
ALTER TABLE members OWNER TO dbadmin;
ALTER TABLE items OWNER TO dbadmin;
ALTER TABLE transactions OWNER TO dbadmin;
ALTER TABLE txn_details OWNER TO dbadmin;


/*************************************************
Section 3: System Design

Design 1: Role-Based Access Strategy for logistics, analytics and sales users. 
*************************************************/
-- Create group roles for accessing specific tables in the database
CREATE ROLE logistics_user;
CREATE ROLE analytics_user;
CREATE ROLE sales_user;

-- Grant specific permissions for each role
GRANT SELECT on items, txn_details, transactions to logistics_user;
GRANT INSERT, UPDATE on transactions to logistics_user;
GRANT SELECT on members, items, transactions, txn_details to analytics_user;
GRANT SELECT, INSERT, UPDATE, DELETE on items to sales_user;

-- Create new users and assign roles to them
CREATE USER log_user1 WITH ENCRYPTED PASSWORD 'log_user1';
CREATE USER ana_user1 WITH ENCRYPTED PASSWORD 'ana_user1';
CREATE USER sal_user1 WITH ENCRYPTED PASSWORD 'sal_user1';
GRANT logistics_user to log_user1;
GRANT analytics_user to ana_user1;
GRANT sales_user to sal_user1;


/*****************************************************
Section 2: Databases

Write SQL Statements for the following questions.
*****************************************************/
-- Q1. Which are the top 10 members by spending
SELECT transactions.member_id, members.first_name, members.last_name, sum(transactions.total_items_price) as total_spending
FROM transactions
INNER JOIN members
ON transactions.member_id = members.member_id
GROUP BY (transactions.member_id, members.first_name, members.last_name)
ORDER BY total_spending DESC
LIMIT 10;

-- Q2. Which are the top 3 items that are frequently brought by members
SELECT txn_details.item_id, items.item_name, sum(txn_details.quantity) as total_quantity
FROM txn_details
INNER JOIN items
ON txn_details.item_id = items.item_id
GROUP BY (txn_details.item_id, items.item_name)
ORDER BY total_quantity DESC
LIMIT 3;

