-- 1. Find the customers who have made a transaction but have never placed an order.
select c.name , c.customer_id
from customer c 
join orders o
using(customer_id)
where c.transaction_id is not null and o.order_id is null;

-- 2. Identify the customer(s) who made the highest transaction.
select 	c.customer_id,max(amount) as max_amount,c.name
from customer c
join transaction t 
group by c.customer_id
order by max_amount desc
limit 1;
-- or
select 	c.customer_id,t.amount,c.name
from customer c
join transaction t 
using(transaction_id)
where t.amount = (select max(amount) as max_amount from transaction);

-- 3. For each city, display the number of customers, number of orders placed, and the total transaction amount.
select c.city, count(distinct c.customer_id) as no_of_customers, count(distinct o.order_id) as order_count, sum(t.amount) as total_amount
from customer c 
left join transaction t
using(transaction_id)
left join orders o 
using(customer_id)    -- in order to get all the values given in the question i have used the left join.
group by city
order by total_amount desc;

-- 4. List the customers whose transaction status is 'Pending' and who have placed at least one order.
select distinct c.customer_id,c.name,t.status
from customer c
join transaction t
using(transaction_id)
where t.status = 'pending' and c.customer_id in (select customer_id from orders);

-- 5. Display customer details who have placed the most number of orders.
select c.customer_id,c.name, count(o.order_id) as no_of_orders
from customer c 
join orders o 
using(customer_id)
group by c.customer_id,c.name
order by no_of_orders desc
limit 1;
-- or 
SELECT c.customer_id, c.name, COUNT(o.order_id) AS total_orders
FROM Customer c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) = (
    SELECT MAX(order_count) FROM (
        SELECT customer_id, COUNT(order_id) AS order_count
        FROM Orders
        GROUP BY customer_id
    ) AS order_counts
);

-- 6. Retrieve customers whose total transaction amount is below the average transaction amount of all customers.
select c.customer_id,c.name, sum(t.amount) as total_amount
from customer c              -- reason for using the sum() is beacause there might be the customer buy more than once.
join transaction t
using(transaction_id)
where t.amount is not null
group by c.name,c.customer_id
having avg(t.amount) < (select avg(amount) from transaction where amount is not null);



