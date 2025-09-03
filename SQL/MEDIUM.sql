-- MEDIUM
-- 1.Find the number of customers in each city.
SELECT CITY, COUNT(*) AS CUSTOMER_COUNT
FROM CUSTOMER
GROUP BY CITY;

-- 2.Retrieve the names of customers who have placed at least one order.
SELECT  distinct c.name
FROM Customer c
JOIN Orders o ON c.customer_id = o.customer_id;

-- 3.List the names and transaction amounts of customers who made a successful transaction with an amount greater than ₹5000.
SELECT C.NAME , T.AMOUNT
FROM CUSTOMER C
JOIN TRANSACTION T
USING(TRANSACTION_ID)
WHERE T.STATUS = 'SUCCESS' AND T.AMOUNT > 5000;

-- 4. Display the names and transaction amounts of all customers who have made a transaction.
SELECT C.NAME,T.AMOUNT
FROM CUSTOMER C 
JOIN TRANSACTION T
USING(TRANSACTION_ID);

-- 5.Get the products and quantities ordered by customers who are from the city 'Mumbai'.
SELECT O.PRODUCT, O.QUANTITY 
FROM CUSTOMER C 
JOIN ORDERS O 
USING(CUSTOMER_ID)
WHERE C.CITY ='MUMBAI';

-- 6. Get the NAMES AND CUSOTMER_ID WHERE the average transaction amount (excluding transactions with NULL amounts).
SELECT C.NAME,C.CUSTOMER_ID
FROM TRANSACTION T
JOIN CUSTOMER C 
USING(TRANSACTION_ID)
WHERE T.AMOUNT IS NOT NULL;


