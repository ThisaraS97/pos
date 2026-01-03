import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    selling_price: '',
    cost_price: '',
    category_id: '',
    code: ''
  });
  const [categories, setCategories] = useState([]);

  const token = localStorage.getItem('access_token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await axios.get(`${API_URL}/products`, { headers });
      setProducts(res.data);
    } catch (err) {
      console.error('Error fetching products:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const res = await axios.get(`${API_URL}/products/categories`, { headers });
      setCategories(res.data);
    } catch (err) {
      console.error('Error fetching categories:', err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/products`, formData, { headers });
      alert('Product added successfully!');
      setFormData({
        name: '',
        description: '',
        selling_price: '',
        cost_price: '',
        category_id: '',
        code: ''
      });
      setShowForm(false);
      fetchProducts();
    } catch (err) {
      alert('Error adding product: ' + err.message);
    }
  };

  const deleteProduct = async (productId) => {
    if (!confirm('Are you sure?')) return;
    try {
      await axios.delete(`${API_URL}/products/${productId}`, { headers });
      fetchProducts();
    } catch (err) {
      alert('Error deleting product');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="page">
      <h2 className="page-title">📦 Products</h2>

      <div style={{ marginBottom: '20px' }}>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '+ Add Product'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3>Add New Product</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div className="form-group">
                <label>Product Name *</label>
                <input 
                  type="text" 
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>SKU *</label>
                <input 
                  type="text" 
                  name="code"
                  value={formData.code}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Category</label>
                <select 
                  name="category_id"
                  value={formData.category_id}
                  onChange={handleInputChange}
                >
                  <option value="">Select category</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Selling Price *</label>
                <input 
                  type="number" 
                  name="selling_price"
                  value={formData.selling_price}
                  onChange={handleInputChange}
                  step="0.01"
                  required
                />
              </div>
              <div className="form-group">
                <label>Cost Price</label>
                <input 
                  type="number" 
                  name="cost_price"
                  value={formData.cost_price}
                  onChange={handleInputChange}
                  step="0.01"
                />
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea 
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  rows="2"
                />
              </div>
            </div>
            <button type="submit" className="btn btn-success">Add Product</button>
          </form>
        </div>
      )}

      <div className="card">
        <h3>Products List</h3>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>SKU</th>
                <th>Price</th>
                <th>Cost</th>
                <th>Margin</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {products.map(product => {
                const margin = product.cost_price ? ((product.selling_price - product.cost_price) / product.selling_price * 100).toFixed(1) : '-';
                return (
                  <tr key={product.id}>
                    <td>{product.name}</td>
                    <td>{product.code || '-'}</td>
                    <td>${product.selling_price.toFixed(2)}</td>
                    <td>${product.cost_price ? product.cost_price.toFixed(2) : '-'}</td>
                    <td>{margin}%</td>
                    <td>
                      <button 
                        className="btn btn-danger btn-small"
                        onClick={() => deleteProduct(product.id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default ProductsPage;
