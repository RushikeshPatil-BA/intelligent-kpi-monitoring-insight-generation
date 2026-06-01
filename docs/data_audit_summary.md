# Phase 2 – Step 2.1 Data Audit Summary

## Raw file overview

A CSV version of this overview is saved as `docs/data_audit_overview.csv`.

## customers.csv
- Rows: **8,000**, Columns: **4**
- Duplicate customer_id: **0**
- Unique customer_id: **8,000**

## products.csv
- Rows: **500**, Columns: **3**
- Duplicate product_id: **0**
- Unique product_id: **500**

## orders.csv
- Rows: **141,085**, Columns: **8**
- Duplicate order_id: **0**
- Unique order_id: **141,085**

## order_items.csv
- Rows: **369,536**, Columns: **5**
- Duplicate order_item_id: **0**
- Unique order_item_id: **369,536**

## marketing_spend_daily.csv
- Rows: **731**, Columns: **7**
- Duplicate date: **0**
- Unique date: **731**

## web_sessions_daily.csv
- Rows: **731**, Columns: **5**
- Duplicate date: **0**
- Unique date: **731**

## Date ranges

- orders.order_datetime: **2024-01-01 00:00:00 → 2025-12-31 00:00:00**
- marketing_spend_daily.date: **2024-01-01 00:00:00 → 2025-12-31 00:00:00**
- web_sessions_daily.date: **2024-01-01 00:00:00 → 2025-12-31 00:00:00**

## Referential integrity checks (raw)

- Orders with customer_id not found in customers: **0**
- Order_items with order_id not found in orders: **0**
- Order_items with product_id not found in products: **0**
