"""
Hardware package for POS system
"""
from app.hardware.printer import ThermalPrinter, PrinterError, get_printer

__all__ = ['ThermalPrinter', 'PrinterError', 'get_printer']


