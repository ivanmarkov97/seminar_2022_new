select
    item_id,
    name,
    price
from market_items
where 1
    and category="$category"
order by name;
