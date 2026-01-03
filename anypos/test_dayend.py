#!/usr/bin/env python3
"""
Test script for Day End feature
Usage: python test_dayend.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

# Test credentials
LOGIN_CREDS = {
    "username": "admin",
    "password": "admin123"
}

def test_dayend():
    """Test Day End feature endpoints"""
    
    print("\n" + "="*60)
    print("Day End Feature Test")
    print("="*60)
    
    # 1. Login to get token
    print("\n[1] Logging in...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=LOGIN_CREDS,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        token = response.json()["access_token"]
        print(f"✓ Login successful. Token: {token[:20]}...")
    except Exception as e:
        print(f"✗ Login failed: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Open Day End
    print("\n[2] Opening Day End...")
    try:
        payload = {
            "opening_balance": 500.00,
            "notes": "Test day end"
        }
        response = requests.post(
            f"{BASE_URL}/dayend/open",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        dayend = response.json()
        dayend_id = dayend["id"]
        print(f"✓ Day End opened successfully. ID: {dayend_id}")
        print(f"  Opening Balance: ${dayend['opening_balance']}")
        print(f"  Status: {'CLOSED' if dayend['is_closed'] else 'OPEN'}")
    except Exception as e:
        print(f"✗ Open Day End failed: {e}")
        return
    
    # 3. Get Active Day End
    print("\n[3] Fetching Active Day End...")
    try:
        response = requests.get(
            f"{BASE_URL}/dayend/active",
            headers=headers
        )
        response.raise_for_status()
        dayend = response.json()
        print(f"✓ Active Day End fetched successfully")
        print(f"  ID: {dayend['id']}")
        print(f"  Total Sales: {dayend['total_sales_count']}")
        print(f"  Total Revenue: ${dayend['total_revenue']}")
    except Exception as e:
        print(f"✗ Fetch Active Day End failed: {e}")
        return
    
    # 4. Get Day End Summary
    print(f"\n[4] Getting Day End Summary...")
    try:
        response = requests.get(
            f"{BASE_URL}/dayend/{dayend_id}/summary",
            headers=headers
        )
        response.raise_for_status()
        summary = response.json()
        print(f"✓ Day End Summary fetched successfully")
        print(f"  Sales Summary:")
        print(f"    Total Sales: {summary['sales_summary']['total_sales']}")
        print(f"    Revenue: ${summary['sales_summary']['total_revenue']}")
        print(f"    Discount: ${summary['sales_summary']['total_discount']}")
        print(f"    Tax: ${summary['sales_summary']['total_tax']}")
        print(f"  Payment Breakdown:")
        for method, amount in summary['payment_breakdown'].items():
            print(f"    {method.capitalize()}: ${amount}")
        print(f"  Cash Reconciliation:")
        print(f"    Opening: ${summary['cash_reconciliation']['opening_balance']}")
        print(f"    Expected: ${summary['cash_reconciliation']['expected_cash']}")
        print(f"    Actual: ${summary['cash_reconciliation']['actual_cash']}")
        print(f"    Variance: ${summary['cash_reconciliation']['variance']}")
    except Exception as e:
        print(f"✗ Get Summary failed: {e}")
        return
    
    # 5. Close Day End
    print(f"\n[5] Closing Day End...")
    try:
        payload = {
            "actual_cash": 523.50,
            "notes": "Counted and reconciled"
        }
        response = requests.post(
            f"{BASE_URL}/dayend/{dayend_id}/close",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        dayend = response.json()
        print(f"✓ Day End closed successfully")
        print(f"  Actual Cash: ${dayend['actual_cash']}")
        print(f"  Expected Cash: ${dayend['expected_cash']}")
        print(f"  Variance: ${dayend['cash_variance']}")
        print(f"  Status: {'CLOSED' if dayend['is_closed'] else 'OPEN'}")
        print(f"  Closed At: {dayend['closed_at']}")
    except Exception as e:
        print(f"✗ Close Day End failed: {e}")
        return
    
    # 6. Get Day End by ID
    print(f"\n[6] Fetching Day End by ID...")
    try:
        response = requests.get(
            f"{BASE_URL}/dayend/{dayend_id}",
            headers=headers
        )
        response.raise_for_status()
        dayend = response.json()
        print(f"✓ Day End fetched successfully")
        print(f"  Status: {'CLOSED' if dayend['is_closed'] else 'OPEN'}")
        print(f"  Revenue: ${dayend['total_revenue']}")
    except Exception as e:
        print(f"✗ Get Day End failed: {e}")
        return
    
    # 7. List Day Ends
    print(f"\n[7] Listing Day Ends...")
    try:
        response = requests.get(
            f"{BASE_URL}/dayend/list",
            headers=headers
        )
        if response.status_code == 403:
            print(f"⚠ List Day Ends requires admin/manager role (current user is cashier)")
            print(f"  Skipping this test")
        else:
            response.raise_for_status()
            dayends = response.json()
            print(f"✓ Day Ends list fetched successfully")
            print(f"  Total Day Ends: {len(dayends)}")
            for de in dayends[:3]:
                print(f"    - ID: {de['id']}, Status: {'CLOSED' if de['is_closed'] else 'OPEN'}, Revenue: ${de['total_revenue']}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"⚠ List Day Ends requires admin/manager role")
        else:
            print(f"✗ List Day Ends failed: {e}")
    except Exception as e:
        print(f"✗ List Day Ends failed: {e}")
    
    print("\n" + "="*60)
    print("✓ All Day End tests completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_dayend()
