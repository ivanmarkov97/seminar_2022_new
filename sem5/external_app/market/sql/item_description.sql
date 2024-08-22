SELECT
    prod_id,
    prod_name AS name,
    prod_price AS price
FROM product
WHERE 1=1
    AND prod_id='$product_id'
