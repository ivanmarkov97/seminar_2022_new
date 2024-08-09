SELECT
    prod_id,
    prod_name,
    prod_measure,
    prod_price
FROM product
WHERE 1=1
    AND prod_name='$input_product'
