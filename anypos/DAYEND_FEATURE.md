# Day End Feature Documentation

## Overview

The Day End feature is a standard POS operation that allows cashiers to close out their register/till at the end of their shift. It provides a complete accounting mechanism including sales summary, payment reconciliation, and cash variance tracking.

## Features

### 1. Day End Session Management
- **Open Day End**: Start a new day-end session for a cashier
- **Get Active Day End**: Retrieve the currently open day-end
- **Close Day End**: Finalize the day-end with actual cash count

### 2. Sales Tracking
- Automatically tracks all sales during the day-end period
- Calculates total sales count and revenue
- Records discount and tax totals

### 3. Payment Method Breakdown
- Cash sales total
- Card sales total
- Cheque sales total
- Online payment sales total
- Credit sales total

### 4. Cash Reconciliation
- **Opening Balance**: Starting cash amount
- **Expected Cash**: Calculated from cash sales
- **Actual Cash**: Physically counted at day-end
- **Variance**: Difference between expected and actual (overage/shortage)
- **Closing Balance**: Opening balance + Total revenue

### 5. Audit Trail
- Timestamps for opening and closing
- Cashier identification
- All sales linked to day-end
- Optional notes for discrepancies

## API Endpoints

### Open Day End
```
POST /api/dayend/open
Content-Type: application/json

{
  "opening_balance": 100.00,
  "notes": "Starting with $100 float"
}

Response: DayEndResponse
```

### Get Active Day End
```
GET /api/dayend/active

Response: DayEndResponse with current active day-end
```

### Get Day End by ID
```
GET /api/dayend/{dayend_id}

Response: DayEndResponse
```

### Get Day End Summary Report
```
GET /api/dayend/{dayend_id}/summary

Response: DayEndSummary with formatted report
```

### Add Sale to Day End
```
POST /api/dayend/{dayend_id}/add-sale/{sale_id}

Response: Updated dayend data
```

### Close Day End
```
POST /api/dayend/{dayend_id}/close
Content-Type: application/json

{
  "actual_cash": 1250.50,
  "notes": "All matched, slight overage"
}

Response: DayEndResponse with closed status
```

### List All Day Ends
```
GET /api/dayend/list?skip=0&limit=100

Response: Array of DayEndList items
Note: Requires admin or manager role
```

### Get Cashier History
```
GET /api/dayend/cashier/{cashier_id}/history?skip=0&limit=50

Response: Array of day-end records for the cashier
```

## Data Models

### DayEnd Table
- `id`: Unique identifier
- `cashier_id`: User who opened the day-end
- `total_sales_count`: Number of sales
- `total_revenue`: Total amount from all sales
- `total_discount`: Total discounts applied
- `total_tax`: Total tax collected
- `cash_sales`: Revenue from cash payments
- `card_sales`: Revenue from card payments
- `cheque_sales`: Revenue from cheque payments
- `online_sales`: Revenue from online payments
- `credit_sales`: Revenue from credit payments
- `opening_balance`: Starting cash
- `closing_balance`: Ending cash
- `expected_cash`: Theoretical cash from sales
- `actual_cash`: Physically counted cash
- `cash_variance`: Difference (actual - expected)
- `is_closed`: Status flag
- `opened_at`: When day-end was created
- `closed_at`: When day-end was closed
- `notes`: Optional comments

### DayEndTransaction Table
- `id`: Unique identifier
- `dayend_id`: Reference to DayEnd
- `sale_id`: Reference to Sale
- Links sales to specific day-end sessions

## Workflow

### Typical Daily Workflow

1. **Morning**: Cashier opens day-end
   ```bash
   POST /api/dayend/open
   {
     "opening_balance": 500.00,
     "notes": "Starting float"
   }
   ```

2. **During Day**: Sales are automatically tracked
   - Each sale is created normally
   - Can optionally be added to active day-end

3. **End of Shift**: Cashier counts cash and closes
   ```bash
   POST /api/dayend/{dayend_id}/close
   {
     "actual_cash": 2350.75,
     "notes": "Cash counted: $2350.75"
   }
   ```

4. **Manager Review**: View summary report
   ```bash
   GET /api/dayend/{dayend_id}/summary
   ```

## Example Response: Day End Summary

```json
{
  "id": 1,
  "cashier_id": 2,
  "opened_at": "2026-01-03T08:00:00",
  "closed_at": "2026-01-03T17:30:00",
  "is_closed": true,
  "sales_summary": {
    "total_sales": 45,
    "total_revenue": 2250.00,
    "total_discount": 150.00,
    "total_tax": 225.00
  },
  "payment_breakdown": {
    "cash": 1500.00,
    "card": 650.00,
    "cheque": 0.00,
    "online": 100.00,
    "credit": 0.00
  },
  "cash_reconciliation": {
    "opening_balance": 500.00,
    "expected_cash": 1500.00,
    "actual_cash": 1520.00,
    "variance": 20.00,
    "closing_balance": 2750.00
  },
  "notes": "Overage due to tips"
}
```

## Security & Authorization

- **Cashiers**: Can only open/close their own day-ends
- **Managers**: Can view all day-ends
- **Admins**: Full access to all day-ends
- Role-based access control enforced on all endpoints

## Database Tables

The feature creates two new tables:

1. **dayends**: Main day-end records
2. **dayend_transactions**: Links between sales and day-ends

All tables include:
- Timestamps (created_at, updated_at)
- Proper foreign key relationships
- Indexing for performance

## Integration with Existing Features

### Sales Management
- Day-ends automatically reference sales
- Sales can be added to day-ends
- Payment method totals calculated from sales

### User Management
- Ties to user/cashier records
- Maintains audit trail with user IDs

### Reporting
- Can create day-end reports
- Provides variance analysis
- Supports management reviews

## Standard POS Features Implemented

✅ Day-end opening and closing
✅ Sales tracking and reconciliation
✅ Payment method breakdown
✅ Cash variance reporting
✅ Audit trail with timestamps
✅ Role-based access control
✅ Manager review capabilities
✅ Cashier history tracking
✅ Multiple day-end support
✅ Soft close capability with variance tracking

## Database Query

To verify the tables were created:

```sql
-- Check dayends table
SELECT * FROM dayends;

-- Check dayend_transactions
SELECT * FROM dayend_transactions;

-- Get cash variance report
SELECT 
  cashier_id, 
  opened_at, 
  total_revenue, 
  cash_variance, 
  is_closed 
FROM dayends 
ORDER BY opened_at DESC;
```

## Next Steps (Optional Enhancements)

1. **PDF Reports**: Generate day-end reports as PDFs
2. **Email Notifications**: Send summaries to managers
3. **Discrepancy Alerts**: Flag unusual variances
4. **Multi-register Support**: Handle multiple registers per day
5. **Weekly/Monthly Roll-up**: Aggregate day-end data
6. **Variance Approval**: Manager approval workflow for variances
7. **Auto-settlement**: Automatically close based on time
8. **Mobile Friendly UI**: Day-end form on mobile device

## Testing

To test the day-end feature:

```python
# Use the test endpoints in the API documentation
# Navigate to: http://localhost:8000/docs
# Try the /api/dayend/ endpoints

# Or use curl:
curl -X POST "http://localhost:8000/api/dayend/open" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"opening_balance": 100}'
```

---

**Day End Feature v1.0.0**
Complete POS day-end management with cash reconciliation and audit trail.
