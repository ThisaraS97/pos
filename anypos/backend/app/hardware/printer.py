"""
Modern POS Printer Module
Supports ESC/POS commands for thermal printers
"""
import os
import serial
import serial.tools.list_ports
from typing import Optional, List, Dict, Any
from datetime import datetime
from config import settings


class PrinterError(Exception):
    """Custom printer exception"""
    pass


class ThermalPrinter:
    """
    ESC/POS Thermal Printer Controller
    Supports USB, Serial, and Network printers
    """
    
    def __init__(self, port: Optional[str] = None, baudrate: int = 9600, timeout: int = 1):
        """
        Initialize printer connection
        
        Args:
            port: Serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate: Serial baud rate (default: 9600)
            timeout: Serial timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection: Optional[serial.Serial] = None
        self.is_connected = False
        
    def connect(self) -> bool:
        """Establish connection to printer"""
        if self.port is None:
            # Try to auto-detect printer
            available_ports = self.list_available_ports()
            if available_ports:
                self.port = available_ports[0]['port']
            else:
                raise PrinterError("No printer port found. Please specify a port.")
        
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            self.is_connected = True
            # Initialize printer
            self._initialize()
            return True
        except serial.SerialException as e:
            self.is_connected = False
            raise PrinterError(f"Failed to connect to printer: {str(e)}")
    
    def disconnect(self):
        """Close printer connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.is_connected = False
    
    def _initialize(self):
        """Initialize printer with default settings"""
        if not self.is_connected:
            return
        
        # Reset printer
        self._send_command(b'\x1B\x40')  # ESC @
        # Set encoding to UTF-8
        self._send_command(b'\x1B\x74\x00')  # ESC t 0
    
    def _send_command(self, command: bytes):
        """Send raw command to printer"""
        if not self.is_connected or not self.serial_connection:
            raise PrinterError("Printer not connected")
        self.serial_connection.write(command)
    
    def _send_text(self, text: str, encoding: str = 'utf-8'):
        """Send text to printer"""
        if not self.is_connected or not self.serial_connection:
            raise PrinterError("Printer not connected")
        self.serial_connection.write(text.encode(encoding, errors='ignore'))
    
    @staticmethod
    def list_available_ports() -> List[Dict[str, Any]]:
        """List all available serial ports"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'port': port.device,
                'description': port.description,
                'manufacturer': port.manufacturer,
                'hwid': port.hwid
            })
        return ports
    
    def print_receipt(self, receipt_data: Dict[str, Any]) -> bool:
        """
        Print a receipt
        
        Args:
            receipt_data: Dictionary containing receipt information:
                - company_name: str
                - company_address: str
                - company_phone: str
                - receipt_number: str
                - date: str
                - items: List[Dict] with keys: name, quantity, unit_price, total
                - subtotal: float
                - discount: float
                - tax: float
                - total: float
                - amount_paid: float
                - change: float
                - payment_method: str
                - cashier: str
                - customer: Optional[str]
        
        Returns:
            bool: True if successful
        """
        if not self.is_connected:
            self.connect()
        
        try:
            # Header
            self._send_command(b'\x1B\x61\x01')  # Center align
            self._send_command(b'\x1B\x21\x30')  # Double height and width
            company_name = receipt_data.get('company_name', settings.COMPANY_NAME or 'ANYPOS')
            self._send_text(f"{company_name}\n")
            
            self._send_command(b'\x1B\x21\x00')  # Normal text
            self._send_command(b'\x1B\x61\x01')  # Center align
            
            if receipt_data.get('company_address'):
                self._send_text(f"{receipt_data['company_address']}\n")
            if receipt_data.get('company_phone'):
                self._send_text(f"Tel: {receipt_data['company_phone']}\n")
            if receipt_data.get('company_email'):
                self._send_text(f"{receipt_data['company_email']}\n")
            
            self._send_text("-" * 32 + "\n")
            
            # Receipt info
            self._send_command(b'\x1B\x61\x00')  # Left align
            self._send_text(f"Receipt: {receipt_data.get('receipt_number', 'N/A')}\n")
            self._send_text(f"Date: {receipt_data.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n")
            if receipt_data.get('customer'):
                self._send_text(f"Customer: {receipt_data['customer']}\n")
            self._send_text("-" * 32 + "\n")
            
            # Items
            self._send_text("ITEM              QTY  PRICE   TOTAL\n")
            self._send_text("-" * 32 + "\n")
            
            items = receipt_data.get('items', [])
            for item in items:
                name = item.get('name', '')[:16]  # Limit width
                qty = item.get('quantity', 0)
                unit_price = item.get('unit_price', 0.0)
                total = item.get('total', 0.0)
                
                # Format item line
                line = f"{name:<16} {qty:>3}  {unit_price:>6.2f} {total:>7.2f}\n"
                self._send_text(line)
            
            self._send_text("-" * 32 + "\n")
            
            # Totals
            self._send_command(b'\x1B\x61\x02')  # Right align
            subtotal = receipt_data.get('subtotal', 0.0)
            discount = receipt_data.get('discount', 0.0)
            tax = receipt_data.get('tax', 0.0)
            total = receipt_data.get('total', 0.0)
            
            self._send_text(f"Subtotal:  {subtotal:>10.2f}\n")
            if discount > 0:
                self._send_text(f"Discount:  {discount:>10.2f}\n")
            if tax > 0:
                self._send_text(f"Tax:       {tax:>10.2f}\n")
            
            self._send_command(b'\x1B\x21\x08')  # Bold
            self._send_text(f"TOTAL:     {total:>10.2f}\n")
            self._send_command(b'\x1B\x21\x00')  # Normal
            
            # Payment
            self._send_text("-" * 32 + "\n")
            amount_paid = receipt_data.get('amount_paid', 0.0)
            change = receipt_data.get('change', 0.0)
            payment_method = receipt_data.get('payment_method', 'Cash')
            
            self._send_text(f"Payment:   {amount_paid:>10.2f}\n")
            if payment_method.lower() == 'cash' and change > 0:
                self._send_text(f"Change:    {change:>10.2f}\n")
            self._send_text(f"Method:    {payment_method.upper():>10}\n")
            
            # Footer
            self._send_text("-" * 32 + "\n")
            self._send_command(b'\x1B\x61\x01')  # Center align
            if receipt_data.get('cashier'):
                self._send_text(f"Cashier: {receipt_data['cashier']}\n")
            self._send_text("Thank you for your business!\n")
            self._send_text("\n" * 2)  # Extra blank lines
            
            # Cut paper
            self._send_command(b'\x1D\x56\x41\x03')  # Partial cut
            
            return True
            
        except Exception as e:
            raise PrinterError(f"Failed to print receipt: {str(e)}")
    
    def open_cash_drawer(self, pin: int = 0, on_time: int = 255, off_time: int = 255) -> bool:
        """
        Open cash drawer using ESC/POS command
        
        Args:
            pin: Drawer pin number (0 or 1, default: 0)
            on_time: Pulse ON time in 2ms units (0-255, default: 255 = 510ms)
            off_time: Pulse OFF time in 2ms units (0-255, default: 255 = 510ms)
        
        Returns:
            bool: True if successful
        """
        if not self.is_connected:
            try:
                self.connect()
            except PrinterError:
                raise PrinterError("Cannot open cash drawer: Printer not connected")
        
        try:
            # ESC p command: ESC p m t1 t2
            # m = pin number (0 or 1)
            # t1 = ON time in 2ms units (0-255)
            # t2 = OFF time in 2ms units (0-255)
            command = bytes([0x1B, 0x70, pin, on_time, off_time])
            self._send_command(command)
            return True
        except Exception as e:
            raise PrinterError(f"Failed to open cash drawer: {str(e)}")
    
    def test_print(self) -> bool:
        """Print a test page"""
        test_data = {
            'company_name': 'TEST PRINT',
            'receipt_number': 'TEST-001',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'items': [
                {'name': 'Test Item 1', 'quantity': 2, 'unit_price': 10.00, 'total': 20.00},
                {'name': 'Test Item 2', 'quantity': 1, 'unit_price': 15.50, 'total': 15.50},
            ],
            'subtotal': 35.50,
            'discount': 0.0,
            'tax': 3.55,
            'total': 39.05,
            'amount_paid': 50.00,
            'change': 10.95,
            'payment_method': 'Cash',
            'cashier': 'Test Cashier'
        }
        return self.print_receipt(test_data)
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()


# Global printer instance
_default_printer: Optional[ThermalPrinter] = None


def get_printer(port: Optional[str] = None) -> ThermalPrinter:
    """Get or create default printer instance"""
    global _default_printer
    if _default_printer is None:
        _default_printer = ThermalPrinter(port=port)
    return _default_printer

