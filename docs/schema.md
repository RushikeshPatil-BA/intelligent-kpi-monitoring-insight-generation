# Phase 2 – Step 2.3 Data Model (Star Schema)

## Dimensions
### DimDate (generated; also provided as `data_silver/dim_date.csv`)
- Grain: 1 row per day
- Key: `date`
- Attributes: year, quarter, month, month_name, week_start, day_of_week, is_weekend

### DimCustomer (`customers_silver.csv`)
- Key: `customer_id`
- Attributes: signup_date, country, segment

### DimProduct (`products_silver.csv`)
- Key: `product_id`
- Attributes: category, base_unit_price_gbp

## Facts
### FactOrders (`orders_silver.csv`)
- Grain: 1 row per order
- PK: `order_id`
- FKs: `customer_id` → DimCustomer, `order_date` → DimDate
- Attributes: channel, discount_rate, shipping_days, is_returned
- Measures: order_total_gbp

### FactOrderItems (`order_items_silver.csv`)
- Grain: 1 row per order line
- PK: `order_item_id`
- FKs: `order_id` → FactOrders, `product_id` → DimProduct
- Measures: quantity, unit_price_gbp, line_total_gbp

### FactMarketingDaily (`marketing_spend_daily_silver.csv`)
- Grain: 1 row per day
- FK: `date` → DimDate
- Measures: total_spend_gbp and spend-by-channel columns

### FactWebDaily (`web_sessions_daily_silver.csv`)
- Grain: 1 row per day
- FK: `date` → DimDate
- Measures: sessions, orders, conversion_rate_calc, avg_order_value_gbp (if present)

## Relationships (Power BI)
- DimCustomer[customer_id] 1—* FactOrders[customer_id]
- FactOrders[order_id] 1—* FactOrderItems[order_id]
- DimProduct[product_id] 1—* FactOrderItems[product_id]
- DimDate[date] 1—* FactOrders[order_date]
- DimDate[date] 1—* FactMarketingDaily[date]
- DimDate[date] 1—* FactWebDaily[date]
