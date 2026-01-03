import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function SalesPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cart, setCart] = useState([]);
  const [selectedPaymentMethod, setSelectedPaymentMethod] = useState('cash');
  const [amountPaid, setAmountPaid] = useState('');
  const [discount, setDiscount] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [completingSale, setCompletingSale] = useState(false);
  const [saleComplete, setSaleComplete] = useState(false);
  const [lastSaleRef, setLastSaleRef] = useState('');

  const token = localStorage.getItem('access_token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await axios.get(`${API_URL}/products`, { headers });
      setProducts(res.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching products:', err);
      setLoading(false);
    }
  };

  const addProductToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    if (existingItem) {
      existingItem.quantity += 1;
      setCart([...cart]);
    } else {
      setCart([...cart, {
        id: product.id,
        name: product.name,
        price: product.selling_price,
        cost: product.cost_price,
        quantity: 1
      }]);
    }
  };

  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(productId);
    } else {
      const item = cart.find(item => item.id === productId);
      if (item) {
        item.quantity = newQuantity;
        setCart([...cart]);
      }
    }
  };

  const removeFromCart = (productId) => {
    setCart(cart.filter(item => item.id !== productId));
  };

  const calculateSubtotal = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const subtotal = calculateSubtotal();
  const discountAmount = (subtotal * discount) / 100;
  const tax = (subtotal - discountAmount) * 0.1; // 10% tax
  const total = subtotal - discountAmount + tax;
  const change = amountPaid ? parseFloat(amountPaid) - total : 0;

  const completeSale = async () => {
    if (cart.length === 0) {
      alert('❌ Cart is empty. Please add items.');
      return;
    }

    if (!amountPaid || parseFloat(amountPaid) < total) {
      alert('❌ Insufficient payment amount');
      return;
    }

    setCompletingSale(true);
    try {
      const saleData = {
        payment_method: selectedPaymentMethod,
        discount: discountAmount,
        tax: tax,
        amount_paid: parseFloat(amountPaid),
        items: cart.map(item => ({
          product_id: item.id,
          quantity: item.quantity,
          unit_price: item.price
        }))
      };

      const response = await axios.post(`${API_URL}/sales`, saleData, { headers });
      
      setLastSaleRef(response.data.reference_number);
      setSaleComplete(true);
      setCart([]);
      setAmountPaid('');
      setDiscount(0);
      setSelectedPaymentMethod('cash');

      // Reset after 3 seconds
      setTimeout(() => {
        setSaleComplete(false);
      }, 3000);
    } catch (err) {
      alert('❌ Error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setCompletingSale(false);
    }
  };

  const filteredProducts = products.filter(p => 
    p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) return <div style={{ padding: '40px', textAlign: 'center' }}>Loading products...</div>;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '20px', height: '100%' }}>
      
      {/* LEFT SIDE - PRODUCTS */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {/* Search Products */}
        <div style={{
          background: '#fff',
          padding: '20px',
          borderRadius: '10px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ margin: '0 0 15px 0', color: '#333' }}>🛍️ Products</h2>
          <input
            type="text"
            placeholder="🔍 Search by name or code..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              padding: '12px 15px',
              border: '2px solid #ddd',
              borderRadius: '8px',
              fontSize: '1em',
              boxSizing: 'border-box'
            }}
          />
        </div>

        {/* Products Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '15px',
          overflow: 'auto',
          maxHeight: 'calc(100vh - 300px)',
          padding: '5px'
        }}>
          {filteredProducts.length === 0 ? (
            <div style={{ gridColumn: '1/-1', textAlign: 'center', color: '#999', padding: '40px' }}>
              No products found
            </div>
          ) : (
            filteredProducts.map(product => (
              <div
                key={product.id}
                onClick={() => addProductToCart(product)}
                style={{
                  background: '#fff',
                  padding: '15px',
                  borderRadius: '10px',
                  cursor: 'pointer',
                  border: '2px solid #e0e0e0',
                  transition: 'all 0.3s ease',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-5px)';
                  e.currentTarget.style.boxShadow = '0 5px 15px rgba(102, 126, 234, 0.3)';
                  e.currentTarget.style.borderColor = '#667eea';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
                  e.currentTarget.style.borderColor = '#e0e0e0';
                }}
              >
                <div style={{ fontSize: '2em', marginBottom: '8px', textAlign: 'center' }}>
                  {product.name[0].toUpperCase() === 'L' ? '💻' : 
                   product.name[0].toUpperCase() === 'M' ? '🖱️' : 
                   product.name[0].toUpperCase() === 'K' ? '⌨️' : 
                   product.name[0].toUpperCase() === 'T' ? '👕' : 
                   product.name[0].toUpperCase() === 'J' ? '👖' : 
                   product.name[0].toUpperCase() === 'C' ? '☕' : 
                   product.name[0].toUpperCase() === 'B' ? '📚' : '📦'}
                </div>
                <h4 style={{ margin: '0 0 5px 0', fontSize: '0.9em', color: '#333' }}>
                  {product.name}
                </h4>
                <p style={{ margin: '0 0 8px 0', fontSize: '0.85em', color: '#999' }}>
                  Code: {product.code}
                </p>
                <div style={{
                  background: '#f5f5f5',
                  padding: '8px',
                  borderRadius: '5px',
                  textAlign: 'center'
                }}>
                  <span style={{ fontSize: '1.3em', fontWeight: 'bold', color: '#667eea' }}>
                    ${product.selling_price.toFixed(2)}
                  </span>
                </div>
                <div style={{ fontSize: '0.8em', color: '#999', marginTop: '5px' }}>
                  Stock: {product.quantity_in_stock}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* RIGHT SIDE - CART & CHECKOUT */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        
        {/* CART ITEMS */}
        <div style={{
          background: '#fff',
          borderRadius: '10px',
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
          padding: '20px',
          flex: '1',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden'
        }}>
          <h3 style={{ margin: '0 0 15px 0', color: '#333' }}>🛒 Cart ({cart.length})</h3>
          
          <div style={{ 
            flex: '1', 
            overflowY: 'auto',
            marginBottom: '15px',
            paddingRight: '10px'
          }}>
            {cart.length === 0 ? (
              <div style={{ textAlign: 'center', color: '#999', padding: '40px 0' }}>
                <p style={{ fontSize: '3em' }}>📭</p>
                <p>Cart is empty</p>
              </div>
            ) : (
              <div>
                {cart.map(item => (
                  <div
                    key={item.id}
                    style={{
                      background: '#f9f9f9',
                      padding: '12px',
                      marginBottom: '10px',
                      borderRadius: '8px',
                      border: '1px solid #e0e0e0'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <span style={{ fontWeight: '600', color: '#333' }}>{item.name}</span>
                      <button
                        onClick={() => removeFromCart(item.id)}
                        style={{
                          background: '#ff4444',
                          color: 'white',
                          border: 'none',
                          borderRadius: '4px',
                          padding: '2px 8px',
                          cursor: 'pointer',
                          fontSize: '0.8em'
                        }}
                      >
                        ✕ Remove
                      </button>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px', fontSize: '0.9em' }}>
                      <div>
                        <label style={{ fontSize: '0.8em', color: '#999' }}>Qty:</label>
                        <input
                          type="number"
                          min="1"
                          value={item.quantity}
                          onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
                          style={{
                            width: '100%',
                            padding: '5px',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            textAlign: 'center'
                          }}
                        />
                      </div>
                      <div>
                        <label style={{ fontSize: '0.8em', color: '#999' }}>Price:</label>
                        <div style={{ fontWeight: '600', color: '#667eea' }}>
                          ${item.price.toFixed(2)}
                        </div>
                      </div>
                      <div>
                        <label style={{ fontSize: '0.8em', color: '#999' }}>Total:</label>
                        <div style={{ fontWeight: '700', color: '#333', fontSize: '1.1em' }}>
                          ${(item.price * item.quantity).toFixed(2)}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* PAYMENT & TOTALS */}
        {cart.length > 0 && (
          <div style={{
            background: '#fff',
            borderRadius: '10px',
            boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
            padding: '20px'
          }}>
            {/* Discount */}
            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: '#333' }}>
                Discount (%)
              </label>
              <input
                type="number"
                min="0"
                max="100"
                value={discount}
                onChange={(e) => setDiscount(parseFloat(e.target.value) || 0)}
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '5px',
                  fontSize: '1em',
                  boxSizing: 'border-box'
                }}
              />
            </div>

            {/* Payment Method */}
            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: '#333' }}>
                Payment Method
              </label>
              <select
                value={selectedPaymentMethod}
                onChange={(e) => setSelectedPaymentMethod(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '5px',
                  fontSize: '1em',
                  boxSizing: 'border-box'
                }}
              >
                <option value="cash">💵 Cash</option>
                <option value="card">💳 Card</option>
                <option value="cheque">📝 Cheque</option>
                <option value="online">🌐 Online Transfer</option>
              </select>
            </div>

            {/* Amount Paid */}
            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: '#333' }}>
                Amount Paid
              </label>
              <input
                type="number"
                min="0"
                step="0.01"
                value={amountPaid}
                onChange={(e) => setAmountPaid(e.target.value)}
                placeholder="Enter amount"
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '2px solid #ddd',
                  borderRadius: '5px',
                  fontSize: '1.1em',
                  boxSizing: 'border-box'
                }}
              />
            </div>

            {/* Totals Summary */}
            <div style={{
              background: '#f5f5f5',
              padding: '15px',
              borderRadius: '8px',
              marginBottom: '15px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.95em' }}>
                <span>Subtotal:</span>
                <span style={{ fontWeight: '600' }}>${subtotal.toFixed(2)}</span>
              </div>
              {discount > 0 && (
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.95em', color: '#00aa00' }}>
                  <span>Discount ({discount}%):</span>
                  <span style={{ fontWeight: '600' }}>-${discountAmount.toFixed(2)}</span>
                </div>
              )}
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px', fontSize: '0.95em' }}>
                <span>Tax (10%):</span>
                <span style={{ fontWeight: '600' }}>${tax.toFixed(2)}</span>
              </div>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: '1.3em',
                fontWeight: '700',
                color: '#667eea',
                borderTop: '2px solid #ddd',
                paddingTop: '10px'
              }}>
                <span>Total:</span>
                <span>${total.toFixed(2)}</span>
              </div>
              {change > 0 && (
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  fontSize: '1.1em',
                  fontWeight: '700',
                  color: '#00aa00',
                  marginTop: '10px',
                  padding: '10px',
                  background: '#f0f8f0',
                  borderRadius: '5px'
                }}>
                  <span>Change:</span>
                  <span>${change.toFixed(2)}</span>
                </div>
              )}
            </div>

            {/* Complete Sale Button */}
            <button
              onClick={completeSale}
              disabled={completingSale || cart.length === 0}
              style={{
                width: '100%',
                padding: '15px',
                background: saleComplete ? '#00aa00' : '#667eea',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '1.2em',
                fontWeight: '700',
                cursor: completingSale ? 'not-allowed' : 'pointer',
                transition: 'all 0.3s ease',
                opacity: completingSale ? 0.7 : 1
              }}
              onMouseEnter={(e) => {
                if (!completingSale) {
                  e.target.style.background = '#5568d3';
                  e.target.style.transform = 'scale(1.02)';
                }
              }}
              onMouseLeave={(e) => {
                if (!completingSale) {
                  e.target.style.background = '#667eea';
                  e.target.style.transform = 'scale(1)';
                }
              }}
            >
              {completingSale ? '⏳ Processing...' : saleComplete ? '✅ Sale Complete!' : '✓ Complete Sale'}
            </button>

            {saleComplete && (
              <div style={{
                background: '#e8f5e9',
                color: '#2e7d32',
                padding: '15px',
                borderRadius: '8px',
                marginTop: '10px',
                textAlign: 'center',
                fontWeight: '600'
              }}>
                ✓ Sale #{lastSaleRef} completed successfully!
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default SalesPage;
