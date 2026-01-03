"""
Hardware Routes - Printer Management
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.hardware.printer import ThermalPrinter, PrinterError, get_printer
from app.security import get_current_active_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.sale import Sale
from app.models.user import User
from config import settings

router = APIRouter(prefix="/api/hardware", tags=["Hardware"])


class PrinterPort(BaseModel):
    port: str
    description: str
    manufacturer: Optional[str] = None
    hwid: Optional[str] = None


class PrinterConnection(BaseModel):
    port: Optional[str] = None
    baudrate: int = 9600


class ReceiptData(BaseModel):
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    company_phone: Optional[str] = None
    company_email: Optional[str] = None
    receipt_number: str
    date: Optional[str] = None
    customer: Optional[str] = None
    items: List[Dict[str, Any]]
    subtotal: float
    discount: float = 0.0
    tax: float = 0.0
    total: float
    amount_paid: float
    change: float = 0.0
    payment_method: str = "cash"
    cashier: Optional[str] = None


@router.get("/printers/ports", response_model=List[PrinterPort])
def list_printer_ports():
    """List all available serial ports for printers"""
    try:
        ports = ThermalPrinter.list_available_ports()
        return [PrinterPort(**port) for port in ports]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list ports: {str(e)}")


@router.post("/printers/connect")
def connect_printer(connection: PrinterConnection):
    """Connect to a printer"""
    try:
        printer = get_printer(port=connection.port)
        printer.baudrate = connection.baudrate
        success = printer.connect()
        return {
            "success": success,
            "message": "Printer connected successfully",
            "port": printer.port,
            "is_connected": printer.is_connected
        }
    except PrinterError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect: {str(e)}")


@router.post("/printers/disconnect")
def disconnect_printer():
    """Disconnect from printer"""
    try:
        printer = get_printer()
        printer.disconnect()
        return {
            "success": True,
            "message": "Printer disconnected successfully",
            "is_connected": False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to disconnect: {str(e)}")


@router.get("/printers/status")
def get_printer_status():
    """Get current printer connection status"""
    try:
        printer = get_printer()
        return {
            "is_connected": printer.is_connected,
            "port": printer.port,
            "baudrate": printer.baudrate
        }
    except Exception as e:
        return {
            "is_connected": False,
            "port": None,
            "error": str(e)
        }


@router.post("/printers/test")
def test_print(current_user: User = Depends(get_current_active_user)):
    """Print a test page"""
    try:
        printer = get_printer()
        if not printer.is_connected:
            printer.connect()
        
        success = printer.test_print()
        return {
            "success": success,
            "message": "Test print sent successfully"
        }
    except PrinterError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test print failed: {str(e)}")


@router.post("/printers/receipt")
def print_receipt(
    receipt_data: ReceiptData,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Print a receipt"""
    try:
        printer = get_printer()
        if not printer.is_connected:
            printer.connect()
        
        # Convert receipt data to dict
        receipt_dict = receipt_data.model_dump()
        
        # Set cashier name if not provided
        if not receipt_dict.get('cashier'):
            receipt_dict['cashier'] = current_user.full_name or current_user.username
        
        success = printer.print_receipt(receipt_dict)
        return {
            "success": success,
            "message": "Receipt printed successfully"
        }
    except PrinterError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to print receipt: {str(e)}")


@router.post("/printers/receipt/{sale_id}")
def print_receipt_from_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Print receipt from an existing sale"""
    try:
        sale = db.query(Sale).filter(Sale.id == sale_id, Sale.is_deleted == False).first()
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        
        # Get sale items
        items = []
        for item in sale.items:
            items.append({
                'name': item.product_name,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'total': item.subtotal
            })
        
        # Build receipt data
        receipt_data = {
            'company_name': settings.COMPANY_NAME,
            'company_address': settings.COMPANY_ADDRESS,
            'company_phone': settings.COMPANY_PHONE,
            'company_email': settings.COMPANY_EMAIL,
            'receipt_number': sale.reference_number,
            'date': sale.created_at.strftime('%Y-%m-%d %H:%M:%S') if sale.created_at else None,
            'items': items,
            'subtotal': sale.subtotal,
            'discount': sale.discount,
            'tax': sale.tax,
            'total': sale.total,
            'amount_paid': sale.amount_paid,
            'change': sale.change,
            'payment_method': sale.payment_method.value if hasattr(sale.payment_method, 'value') else str(sale.payment_method),
            'cashier': current_user.full_name or current_user.username
        }
        
        # Print receipt
        printer = get_printer()
        if not printer.is_connected:
            printer.connect()
        
        success = printer.print_receipt(receipt_data)
        return {
            "success": success,
            "message": "Receipt printed successfully",
            "sale_id": sale_id
        }
    except HTTPException:
        raise
    except PrinterError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to print receipt: {str(e)}")


@router.post("/cash-drawer/open")
def open_cash_drawer(
    pin: int = 0,
    current_user: User = Depends(get_current_active_user)
):
    """Manually open the cash drawer"""
    try:
        printer = get_printer()
        if not printer.is_connected:
            printer.connect()
        
        success = printer.open_cash_drawer(pin=pin)
        return {
            "success": success,
            "message": "Cash drawer opened successfully"
        }
    except PrinterError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open cash drawer: {str(e)}")

