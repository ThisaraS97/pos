# Day End Feature - Quick Start Guide

## Quick Access

### Frontend Access
- **URL**: http://localhost:5173
- **Menu Item**: "🔚 Day End" in sidebar
- **Login**: admin / admin123

### API Docs
- **Swagger UI**: http://localhost:8000/docs
- **Search for**: "Day End" endpoints

## Common Tasks

### Open Day End
1. Click "Day End" in sidebar
2. Click "Open New Day End"
3. Enter opening cash amount
4. Add optional notes
5. Submit

**API**: `POST /api/dayend/open`

### View Active Day End
Click "Day End" in sidebar to see:
- Active day-end status
- Sales count and total
- Payment method breakdown
- Cash reconciliation

**API**: `GET /api/dayend/active`

### Close Day End
1. Click "Close Day End" button
2. Count actual cash in register
3. Enter amount in form
4. System shows variance
5. Add notes if variance occurs
6. Submit

**API**: `POST /api/dayend/{dayend_id}/close`

### View Summary Report
1. Open active day-end
2. Click "View Full Summary"
3. See detailed breakdown:
   - Sales summary
   - Payment breakdown
   - Cash reconciliation

**API**: `GET /api/dayend/{dayend_id}/summary`

### View History
- Scroll to "Day End History" table
- See all past day-ends
- Shows date, sales, revenue, and variance
- Green variance = overage
- Red variance = shortage

## Key Metrics

### Sales Summary
- **Total Sales**: Number of transactions
- **Revenue**: Total from all payments
- **Discount**: Total discounts given
- **Tax**: Total tax collected

### Payment Breakdown
- **Cash**: Physical cash payments
- **Card**: Credit/debit card payments
- **Cheque**: Check payments
- **Online**: Online/electronic payments
- **Credit**: Customer credit payments

### Cash Reconciliation
- **Opening**: Starting balance at day open
- **Expected**: Should be this much in cash (from cash sales)
- **Actual**: What you physically counted
- **Variance**: Difference (positive = overage, negative = shortage)
- **Closing**: Final balance

## Common Scenarios

### Scenario 1: Perfect Cash Match
1. Open day-end with $500
2. Make $1,200 in cash sales
3. Expected cash = $1,700
4. Count $1,700
5. Variance = $0 ✓
6. Close day-end

### Scenario 2: Cash Overage (tips, found money)
1. Expected cash = $1,700
2. Count $1,750
3. Variance = +$50 (overage)
4. Add note: "Tips included"
5. Close day-end

### Scenario 3: Cash Shortage
1. Expected cash = $1,700
2. Count $1,650
3. Variance = -$50 (shortage)
4. Add note: "Short by $50 - investigating"
5. Close day-end
6. Manager reviews discrepancy

## Tips

- ✅ Always enter opening balance when opening day-end
- ✅ Notes are important for explaining variances
- ✅ Review payment breakdown to identify issues
- ✅ Check daily history to track trends
- ✅ Managers can view all day-ends for oversight
- ⚠️ Can't add sales after day-end is closed
- ⚠️ Closing is permanent - double-check amounts

## Troubleshooting

### "No active day-end found"
→ Click "Open New Day End" first

### Variance doesn't match
→ Check if cash sales were recorded correctly
→ Verify no pending transactions

### Can't close day-end
→ Make sure amount is entered
→ Check user role (must be cashier of that day-end or admin)

### Want to reopen?
→ Contact admin (currently not supported)
→ Each day gets fresh day-end

## Keyboard Shortcuts

- Tab: Move between form fields
- Enter: Submit form
- Escape: Close form

## Role-Based Access

### Cashier
- ✅ Open own day-end
- ✅ Close own day-end
- ✅ View own day-end summary
- ✅ View own history
- ❌ View other cashiers' day-ends
- ❌ View all day-ends

### Manager
- ✅ View all day-ends
- ✅ View all summaries
- ✅ View all cashier histories
- ✅ Monitor cash variances
- ❌ Modify day-ends

### Admin
- ✅ Full access to everything
- ✅ Can view and manage all day-ends
- ✅ Access to all reports

## Data Retention

- Day-ends are permanently recorded
- Can be viewed anytime via history
- Used for audit trail and reporting
- Linked to specific sales and cashier
- Timestamps recorded for accountability

---

Need more help? See `DAYEND_FEATURE.md` for complete documentation.
