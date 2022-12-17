-- 1- (SELECT first_name FROM actor)
-- UNION
-- (SELECT first_name FROM customer);

-- 2- (SELECT first_name FROM actor)
-- INTERSECT
-- (SELECT first_name FROM customer);

-- 3- (SELECT first_name FROM actor)
-- EXCEPT
-- (SELECT first_name FROM customer);

-- 1.2- (SELECT first_name FROM actor)
-- UNION ALL
-- (SELECT first_name FROM customer);

-- 2.2- (SELECT first_name FROM actor)
-- INTERSECT ALL -- normal intersect ile hicbir farki yok
-- (SELECT first_name FROM customer);

-- 3.2- (SELECT first_name FROM actor)
-- EXCEPT ALL -- normal except ile hicbir farki yok
-- (SELECT first_name FROM customer);