# Phase 2 – Step 2.2 Cleaning Log (Silver Layer)

## Rules applied
- Parsed date/datetime columns and created `order_date`.
- Removed duplicate primary keys (customers, products, orders) and exact duplicate order_item rows.
- Filled missing categorical fields with `Unknown`.
- Enforced numeric ranges: discount_rate ∈ [0,1], shipping_days ≥ 1, non-negative spend/sessions/orders/totals.
- Normalised `is_returned` to boolean.
- Created `line_total_gbp` in order_items.

## Referential integrity after cleaning
- Orders with customer_id not found in customers: **0**
- Order_items with order_id not found in orders: **0**
- Order_items with product_id not found in products: **0**
