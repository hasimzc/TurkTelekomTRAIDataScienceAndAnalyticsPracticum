-- 1- SELECT city.city, country.country FROM CITY
-- LEFT JOIN country ON city.country_id = country.country_id;

-- 2- SELECT payment.payment_id, customer.first_name, customer.last_name FROM customer
-- RIGHT JOIN payment ON customer.customer_id = payment.customer_id

-- 3- SELECT rental.rental_id, customer.first_name, customer.last_name FROM rental
-- FULL JOIN customer ON customer.customer_id = rental.customer_id