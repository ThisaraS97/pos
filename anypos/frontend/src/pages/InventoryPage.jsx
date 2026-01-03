import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function InventoryPage() {
  const [adjustments, setAdjustments] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    product_id: '',
    adjustment_type: 'stock_in',
    quantity: '',
    reason: ''
  });

  const token = localStorage.getItem('access_token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    fetchAdjustments();
    fetchProducts();
  }, []);

  const fetchAdjustments = async () => {
    try {
      const res = await axios.get(`${API_URL}/inventory`, { headers });
      setAdjustments(res.data);
    } catch (err) {
      console.error('Error fetching adjustments:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchProducts = async () => {
    try {
      const res = await axios.get(`${API_URL}/products`, { headers });
      setProducts(res.data);
    } catch (err) {
      console.error('Error fetching products:', err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/inventory`, formData, { headers });
      alert('Stock adjusted successfully!');
      setFormData({ product_id: '', adjustment_type: 'stock_in', quantity: '', reason: '' });
      setShowForm(false);
      fetchAdjustments();
    } catch (err) {
      alert('Error adjusting stock: ' + err.message);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="page">
      <h2 className="page-title">📚 Inventory Management</h2>

      <div style={{ marginBottom: '20px' }}>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '+ Adjust Stock'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3>Adjust Stock</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div className="form-group">
                <label>Product *</label>
                <select 
                  name="product_id"
                  value={formData.product_id}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select product</option>
                  {products.map(product => (
                    <option key={product.id} value={product.id}>
                      {product.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Adjustment Type *</label>
                <select 
                  name="adjustment_type"
                  value={formData.adjustment_type}
                  onChange={handleInputChange}
                  required
                >
                  <option value="stock_in">Stock In</option>
                  <option value="stock_out">Stock Out</option>
                  <option value="damaged">Damaged</option>
                  <option value="lost">Lost</option>
                  <option value="return">Return</option>
                </select>
              </div>
              <div className="form-group">
                <label>Quantity *</label>
                <input 
                  type="number" 
                  name="quantity"
                  value={formData.quantity}
                  onChange={handleInputChange}
                  placeholder="Quantity"
                  min="1"
                  required
                />
              </div>
              <div className="form-group">
                <label>Reason</label>
                <input 
                  type="text" 
                  name="reason"
                  value={formData.reason}
                  onChange={handleInputChange}
                  placeholder="e.g., Restock, Damage, Loss"
                />
              </div>
            </div>
            <button type="submit" className="btn btn-success">Adjust Stock</button>
          </form>
        </div>
      )}

      <div className="card">
        <h3>Stock Adjustments</h3>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Type</th>
                <th>Quantity</th>
                <th>Reason</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {adjustments.map(adj => (
                <tr key={adj.id}>
                  <td>{adj.product?.name || 'Unknown'}</td>
                  <td>{adj.adjustment_type}</td>
                  <td style={{ color: adj.adjustment_type === 'stock_in' ? '#48bb78' : '#f56565' }}>
                    {adj.adjustment_type === 'stock_in' ? '+' : '-'}{adj.quantity}
                  </td>
                  <td>{adj.reason || '-'}</td>
                  <td>{new Date(adj.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Low stock alert */}
      <div className="card" style={{ marginTop: '20px' }}>
        <h3>⚠️ Low Stock Products</h3>
        {products.filter(p => p.quantity && p.quantity < 10).length === 0 ? (
          <p style={{ color: '#999' }}>No low stock products</p>
        ) : (
          <ul style={{ listStyle: 'none' }}>
            {products.filter(p => p.quantity && p.quantity < 10).map(product => (
              <li key={product.id} style={{ padding: '10px', backgroundColor: '#feebc8', marginBottom: '10px', borderRadius: '5px' }}>
                <strong>{product.name}</strong> - Only {product.quantity} left in stock
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default InventoryPage;
