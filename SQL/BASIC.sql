-- BASIC
-- 1.Retrieve the names and cities of all customers.
 SELECT NAME, CITY
 FROM CUSTOMER;

-- 2.Display the details of customers who have provided an email address (i.e., email is not NULL).
SELECT *
FROM CUSTOMER
WHERE EMAIL IS NOT NULL;

-- 3.List all customers who belong to the city 'Delhi'.
SELECT *
FROM CUSTOMER 
WHERE CITY = 'DELHI';

-- 4.Find all orders where the quantity ordered is greater than 1.
SELECT *
FROM ORDERS
WHERE QUANTITY > 1;

-- 5.Show all transactions with the status 'Success'.
SELECT * 
FROM TRANSACTION 
WHERE STATUS='SUCCESS';

-- 6.List the names of customers who do not have any associated transaction ID.
SELECT NAME 
FROM CUSTOMER
WHERE TRANSACTION_ID IS NULL;

