-- (1) First query is a simple one... I wanted to display the businesses we had that were located in the city of Chicago
Select company, CONCAT(contact_first_name, ' ' , contact_last_name) AS contact_name, city FROM clients WHERE city = 'Chicago';
-- (1b) Lets count how many of those stores are in chicago
SELECT COUNT(*) AS Chicago_Clients FROM clients
WHERE city = 'Chicago';

/* (2) Each employee has a few clients, sometimes these will require in person visits. So I wanted to see Each employee and What cities they were traveling to.
In my company employees were randomly assigned clients. It makes more sense to reassign clients so that sales reps are representing clients in a closer area */
SELECT sales_reps.Employee_ID, last_name, city, zip 
FROM sales_reps INNER JOIN clients ON sales_reps.employee_id = clients.employee_id
ORDER BY sales_reps.Employee_ID;

-- (3) I wanted to see how many units we sold of each product and the total dollar amount sold for each product
SELECT products.name, type, SUM(quantity) AS units_sold, SUM(quantity * price) AS total_sales
FROM products INNER JOIN order_details ON products.product_id = order_details.product_id
INNER JOIN orders ON order_details.order_id = orders.order_id
GROUP BY products.name
ORDER BY total_sales DESC;

/* (4) The last query showed that 4 of our top 6 items sold by $ amount were tequilas.... Maybe we can maximize our efficiency by limiting what type of products we sell
So I wanted to see units sold and total sales by Category (liquor L, beer B, and wine W) */
SELECT category, SUM(quantity) AS units_sold, SUM(quantity * price) AS total_sales
FROM products INNER JOIN order_details ON products.product_id = order_details.product_id
INNER JOIN orders ON order_details.order_id = orders.order_id
GROUP BY category
ORDER BY total_sales DESC;

-- (5a)Lets see which individual store spent the most with us.
SELECT clients.client_id, company, SUM(quantity * price) AS total_sales
FROM clients INNER JOIN orders ON clients.client_id = orders.client_id
INNER JOIN order_details ON orders.order_id = order_details.order_id
INNER JOIN  products ON order_details.product_id = products.product_id
GROUP BY client_id
ORDER BY total_sales DESC;
/* (5b) This is nice... but I want to see our biggest accounts, because some companies have multiple stores with us.
For example we sell to multiple Chili's locations so lets GROUP BY company instead */
SELECT company, SUM(quantity * price) AS total_sales
FROM clients INNER JOIN orders ON clients.client_id = orders.client_id
INNER JOIN order_details ON orders.order_id = order_details.order_id
INNER JOIN  products ON order_details.product_id = products.product_id
GROUP BY company
ORDER BY total_sales DESC;

-- (6) Lets see which are our top 5 specific stores in terms of average order
SELECT company, city, ROUND(AVG(quantity * price),2) AS average_order
FROM clients INNER JOIN orders ON clients.client_id = orders.client_id
INNER JOIN order_details ON orders.order_id = order_details.order_id
INNER JOIN  products ON order_details.product_id = products.product_id
GROUP BY clients.client_id
ORDER BY average_order DESC
LIMIT 5;

-- (7) Our boss needs a count how many orders we've received and see how many orders we've shipped 
SELECT COUNT(*) AS orders_received, COUNT(shipped_date) AS orders_shipped
FROM orders;

-- (8) The pandemic has been tough... we need to make cuts to our sales department. Lets find out who our bottom 3 sales people are
SELECT sales_reps.employee_id, first_name, last_name, SUM(quantity * price) AS total_sales 
FROM sales_reps INNER JOIN clients ON sales_reps.employee_id = clients.employee_id
INNER JOIN orders ON clients.client_id = orders.client_id
INNER JOIN order_details ON orders.order_id = order_details.order_id
INNER JOIN  products ON order_details.product_id = products.product_id
GROUP BY sales_reps.employee_id
ORDER BY total_sales
LIMIT 3;

/* (9) So our sales reps get a commission of 5% on their sales... Lets see who the top earners were for the month (this dataset is only for the month of march
Not only do we wanna see how how much are sales reps are making... but maybe we can see if one of our bottom reps in terms of sales is making too much money for their
performance. Also wanted to use aliases for this join. */
SELECT sr.employee_id, first_name, last_name, ROUND(SUM(quantity * price) * .05,2) AS commission, ROUND(salary / 12, 2) AS monthly_salary, ROUND(SUM(quantity * price) * .05 + salary / 12,2) AS total_monthly_pay 
FROM sales_reps sr INNER JOIN clients c ON sr.employee_id = c.employee_id
INNER JOIN orders o ON c.client_id = o.client_id
INNER JOIN order_details od ON o.order_id = od.order_id
INNER JOIN  products p ON od.product_id = p.product_id
GROUP BY sr.employee_id
ORDER BY total_monthly_pay DESC;

/* (10) I made a mistake in my dataset, and my sales reps' salaries were all in the hundreds of thousands.... and needed to be decreased by .1
ex. a rep being paid 45,000 had a salary of 450,000 listed */
UPDATE sales_reps SET salary = salary * .1;

/* (11) The default decimal settings are 10,0.... which doesn't really make sense?  I mean that if you set up your schema and put in the datatype 
as DECIMAL with no space after... it reverts to DECIMAL(10,0). Now while this wasn't a problem for SALARY, this was a problem for my product prices.
It resulted in all my prices being rounded to the nearest dollar amount.  So this is a function that alters the product table to fix that. */

ALTER TABLE products MODIFY COLUMN price DECIMAL(10,2);