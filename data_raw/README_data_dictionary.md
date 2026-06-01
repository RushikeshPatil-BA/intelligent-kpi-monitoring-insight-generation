# MSc Business Analytics Demo Dataset (Synthetic but Realistic)

This package is designed for Option E (Agentic "Insight-to-Action" analytics assistant).
It mimics an e-commerce / retail business with marketing + web analytics signals.

## Files
- customers.csv (customer master)
- products.csv (product master)
- orders.csv (order header / transactions)
- order_items.csv (line items)
- marketing_spend_daily.csv (daily spend by channel)
- web_sessions_daily.csv (daily sessions + orders + conversion rate)

## Keys / joins
- customers.customer_id  = orders.customer_id
- products.product_id    = order_items.product_id
- orders.order_id        = order_items.order_id

## Notes
- Currency: GBP
- Date range: 2024-01-01 to 2025-12-31
- Includes seasonality (Oct–Dec peaks), discounts, returns, shipping delays, and channel mix.

## Suggested KPIs to power your agent
- Revenue, AOV, conversion rate, CAC proxy (spend / orders), repeat purchase rate
- Top products/categories, country mix, return rate
- Anomaly detection on revenue/orders/sessions, sudden return spikes, discount spikes
