SELECT
    prod_id,
    prod_name AS name,
    CAST(prod_price AS FLOAT) AS price
FROM product
ORDER BY prod_name;
