# Day End Database Schema

## Database Diagram

```
┌─────────────────────────────────────────────────────┐
│                    DAYENDS TABLE                     │
├─────────────────────────────────────────────────────┤
│ id (PK, Integer)                                     │
│ cashier_id (FK → users.id)                          │
│                                                     │
│ SALES SUMMARY                                       │
│ total_sales_count (Integer)                         │
│ total_revenue (Float)                               │
│ total_discount (Float)                              │
│ total_tax (Float)                                   │
│                                                     │
│ PAYMENT METHOD BREAKDOWN                            │
│ cash_sales (Float)                                  │
│ card_sales (Float)                                  │
│ cheque_sales (Float)                                │
│ online_sales (Float)                                │
│ credit_sales (Float)                                │
│                                                     │
│ CASH RECONCILIATION                                 │
│ opening_balance (Float)                             │
│ closing_balance (Float)                             │
│ expected_cash (Float)                               │
│ actual_cash (Float)                                 │
│ cash_variance (Float)                               │
│                                                     │
│ METADATA                                            │
│ is_closed (Boolean)                                 │
│ notes (String, nullable)                            │
│ opened_at (DateTime)                                │
│ closed_at (DateTime, nullable)                      │
│ created_at (DateTime)                               │
│ updated_at (DateTime)                               │
└─────────────────────────────────────────────────────┘
         │
         │ 1:N relationship
         │
         ▼
┌─────────────────────────────────────────────────────┐
│              DAYEND_TRANSACTIONS TABLE               │
├─────────────────────────────────────────────────────┤
│ id (PK, Integer)                                     │
│ dayend_id (FK → dayends.id)                         │
│ sale_id (FK → sales.id)                             │
│ created_at (DateTime)                               │
└─────────────────────────────────────────────────────┘
         │
         │ Links to
         │
         ▼
┌─────────────────────────────────────────────────────┐
│                    SALES TABLE                       │
├─────────────────────────────────────────────────────┤
│ id (PK, Integer)                                     │
│ reference_number (String, unique)                   │
│ customer_id (FK → customers.id)                     │
│ cashier_id (FK → users.id)                          │
│ subtotal, discount, tax, total (Float)              │
│ amount_paid, change (Float)                         │
│ payment_method (Enum)                               │
│ status (Enum)                                       │
│ created_at, updated_at (DateTime)                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                    USERS TABLE                       │
├─────────────────────────────────────────────────────┤
│ id (PK, Integer)                                     │
│ username, email (String, unique)                    │
│ hashed_password (String)                            │
│ role (String: admin, manager, cashier, staff)       │
│ is_active (Boolean)                                 │
│ created_at, updated_at (DateTime)                   │
└─────────────────────────────────────────────────────┘
```

## Table Relationships

### DAYENDS
```
┌─ Relations ─────────────────────┐
│ cashier_id → users.id          │
│ is_closed: Boolean              │
│ is_deleted: Boolean (inherited) │
└────────────────────────────────┘
```

### DAYEND_TRANSACTIONS
```
┌─ Relations ─────────────────────┐
│ dayend_id → dayends.id          │
│ sale_id → sales.id              │
└────────────────────────────────┘
```

## Key Columns Explained

### Revenue Tracking
- **total_sales_count**: Count of transactions
- **total_revenue**: Sum of all (subtotal - discount + tax)
- **total_discount**: Sum of discounts applied
- **total_tax**: Sum of taxes collected

### Payment Reconciliation
- **cash_sales**: Sum of sales where payment_method='cash'
- **card_sales**: Sum of sales where payment_method='card'
- **cheque_sales**: Sum of sales where payment_method='cheque'
- **online_sales**: Sum of sales where payment_method='online'
- **credit_sales**: Sum of sales where payment_method='credit'

### Cash Accounting
- **opening_balance**: Starting cash count (entered by user)
- **expected_cash**: cash_sales + opening_balance
- **actual_cash**: Physical count done by cashier
- **cash_variance**: actual_cash - expected_cash
  - Positive = overage (good)
  - Negative = shortage (investigate)
- **closing_balance**: opening_balance + total_revenue

### Timestamps
- **opened_at**: When day-end session was started
- **closed_at**: When day-end was finalized (NULL while open)
- **created_at**: DB record creation time
- **updated_at**: Last DB modification time

### Status
- **is_closed**: 
  - false = active, can add sales
  - true = finalized, read-only
- **notes**: Comments from cashier about variances

## Data Flow

```
1. Cashier opens day-end
   └─ Create new DAYENDS record
      ├─ cashier_id = current user
      ├─ opening_balance = entered amount
      ├─ is_closed = false
      └─ opened_at = now()

2. Sales happen throughout day
   └─ Each SALES record created
      ├─ Links to active day-end via DAYEND_TRANSACTIONS
      ├─ Records cashier_id
      └─ Records payment_method

3. Cashier closes day-end
   └─ Calculate totals from linked DAYEND_TRANSACTIONS
      ├─ Sum sales by payment method
      ├─ Calculate expected_cash = cash_sales + opening_balance
      ├─ Compare to actual_cash (entered by cashier)
      ├─ Calculate variance
      ├─ Update DAYENDS record
      └─ Set is_closed = true, closed_at = now()

4. Reports generated
   └─ Query DAYENDS + linked DAYEND_TRANSACTIONS
      ├─ Show payment breakdown
      ├─ Show variance analysis
      ├─ Show history per cashier
      └─ Generate audit trail
```

## Example Queries

### Get Today's Day End
```sql
SELECT * FROM dayends
WHERE cashier_id = ? 
  AND is_closed = false
  AND DATE(opened_at) = CURDATE()
LIMIT 1;
```

### Get Sales for Day End
```sql
SELECT s.* FROM sales s
JOIN dayend_transactions dt ON s.id = dt.sale_id
WHERE dt.dayend_id = ?
ORDER BY s.created_at;
```

### Cash Variance Report
```sql
SELECT 
  cashier_id,
  DATE(opened_at) as day,
  total_sales_count,
  total_revenue,
  expected_cash,
  actual_cash,
  cash_variance
FROM dayends
WHERE DATE(opened_at) BETWEEN ? AND ?
ORDER BY opened_at DESC;
```

### Discrepancy Report
```sql
SELECT 
  id,
  cashier_id,
  opened_at,
  cash_variance,
  notes
FROM dayends
WHERE ABS(cash_variance) > 0
ORDER BY ABS(cash_variance) DESC;
```

### Cashier Performance
```sql
SELECT 
  u.username,
  COUNT(*) as total_dayends,
  AVG(ABS(d.cash_variance)) as avg_variance,
  SUM(d.total_revenue) as total_revenue
FROM dayends d
JOIN users u ON d.cashier_id = u.id
GROUP BY d.cashier_id
ORDER BY avg_variance ASC;
```

## Indexes (Recommended)

For optimal query performance:

```sql
CREATE INDEX idx_dayends_cashier_id ON dayends(cashier_id);
CREATE INDEX idx_dayends_opened_at ON dayends(opened_at);
CREATE INDEX idx_dayends_is_closed ON dayends(is_closed);
CREATE INDEX idx_dayend_trans_dayend_id ON dayend_transactions(dayend_id);
CREATE INDEX idx_dayend_trans_sale_id ON dayend_transactions(sale_id);
```

## Constraints

```sql
-- Foreign Keys
FOREIGN KEY (cashier_id) REFERENCES users(id)
FOREIGN KEY (dayend_id) REFERENCES dayends(id)
FOREIGN KEY (sale_id) REFERENCES sales(id)

-- Data Integrity
CHECK (opening_balance >= 0)
CHECK (total_revenue >= 0)
CHECK (expected_cash >= 0)
CHECK (actual_cash >= 0)
```

## Migration Script (if needed)

```python
# If using Alembic for migrations
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'dayends',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cashier_id', sa.Integer(), nullable=False),
        sa.Column('total_sales_count', sa.Integer(), nullable=True),
        # ... all columns ...
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['cashier_id'], ['users.id'])
    )
    
    op.create_table(
        'dayend_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dayend_id', sa.Integer(), nullable=False),
        sa.Column('sale_id', sa.Integer(), nullable=False),
        # ... timestamps ...
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['dayend_id'], ['dayends.id']),
        sa.ForeignKeyConstraint(['sale_id'], ['sales.id'])
    )
```

---

For more information, see `DAYEND_FEATURE.md`
