# PostgreSQL Integration

## Database

Database name:

`churn_clv_db`

Primary analytics table:

`customer_intelligence`

## Purpose

PostgreSQL is used as the persistence and analytics layer for the final customer intelligence outputs.

The table contains customer-level information including:

- churn probability
- customer lifetime value
- expected customer lifetime
- customer segment
- retention strategy
- billing and contract information

## Technology

Python communicates with PostgreSQL using:

- SQLAlchemy
- psycopg2

Architecture:

Python / Jupyter
→ SQLAlchemy
→ psycopg2
→ PostgreSQL
→ customer_intelligence table

## Validation

The final database validation returned:

| Metric | Result |
|---|---:|
| Total customers | 7,043 |
| Average churn probability | 0.4123 |
| Average discounted CLV | 658.96 |

## Example Query

```sql
SELECT
    "customerID",
    "ChurnProbability",
    "DiscountedCLV"
FROM customer_intelligence
WHERE "ChurnProbability" >= 0.50
ORDER BY "DiscountedCLV" DESC
LIMIT 20;