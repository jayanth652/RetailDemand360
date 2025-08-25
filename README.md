Superset setup (dev):
1. Start docker compose and ensure PostgreSQL reachable.
2. In Superset UI, add a database connection to Postgres (retail DB).
3. Register tables from ./lake/gold and features via external engine or import a sample CSV for KPIs.
4. Build dashboards:
   - Daily Revenue & Units by Store/Product
   - Promotions vs Revenue Uplift
   - Forecast vs Actuals (upload actuals from gold)
