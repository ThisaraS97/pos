import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function CustomersPage() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: ''
  });

  const token = localStorage.getItem('access_token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const res = await axios.get(`${API_URL}/customers`, { headers });
      setCustomers(res.data);
    } catch (err) {
      console.error('Error fetching customers:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/customers`, formData, { headers });
      alert('Customer added successfully!');
      setFormData({ name: '', email: '', phone: '', address: '' });
      setShowForm(false);
      fetchCustomers();
    } catch (err) {
      alert('Error adding customer: ' + err.message);
    }
  };

  const deleteCustomer = async (customerId) => {
    if (!confirm('Are you sure?')) return;
    try {
      await axios.delete(`${API_URL}/customers/${customerId}`, { headers });
      fetchCustomers();
    } catch (err) {
      alert('Error deleting customer');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="page">
      <h2 className="page-title">👥 Customers</h2>

      <div style={{ marginBottom: '20px' }}>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '+ Add Customer'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3>Add New Customer</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div className="form-group">
                <label>Name *</label>
                <input 
                  type="text" 
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input 
                  type="email" 
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                />
              </div>
              <div className="form-group">
                <label>Phone</label>
                <input 
                  type="text" 
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                />
              </div>
              <div className="form-group">
                <label>Address</label>
                <input 
                  type="text" 
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                />
              </div>
            </div>
            <button type="submit" className="btn btn-success">Add Customer</button>
          </form>
        </div>
      )}

      <div className="card">
        <h3>Customers List</h3>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Address</th>
                <th>Joined</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {customers.map(customer => (
                <tr key={customer.id}>
                  <td>{customer.name}</td>
                  <td>{customer.email || '-'}</td>
                  <td>{customer.phone || '-'}</td>
                  <td>{customer.address || '-'}</td>
                  <td>{new Date(customer.created_at).toLocaleDateString()}</td>
                  <td>
                    <button 
                      className="btn btn-danger btn-small"
                      onClick={() => deleteCustomer(customer.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default CustomersPage;
