import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function ExpensesPage() {
  const [expenses, setExpenses] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    description: '',
    amount: '',
    category_id: '',
    expense_date: new Date().toISOString().split('T')[0]
  });

  const token = localStorage.getItem('access_token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    fetchExpenses();
    fetchCategories();
  }, []);

  const fetchExpenses = async () => {
    try {
      const res = await axios.get(`${API_URL}/expenses`, { headers });
      setExpenses(res.data);
    } catch (err) {
      console.error('Error fetching expenses:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const res = await axios.get(`${API_URL}/expenses/categories`, { headers });
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
      await axios.post(`${API_URL}/expenses`, formData, { headers });
      alert('Expense recorded successfully!');
      setFormData({
        description: '',
        amount: '',
        category_id: '',
        expense_date: new Date().toISOString().split('T')[0]
      });
      setShowForm(false);
      fetchExpenses();
    } catch (err) {
      alert('Error recording expense: ' + err.message);
    }
  };

  if (loading) return <div>Loading...</div>;

  const totalExpenses = expenses.reduce((sum, exp) => sum + (exp.amount || 0), 0);

  return (
    <div className="page">
      <h2 className="page-title">💰 Expenses</h2>

      {/* Summary */}
      <div className="stats-grid">
        <div className="stat-card danger">
          <div className="stat-label">Total Expenses</div>
          <div className="stat-value">${totalExpenses.toFixed(2)}</div>
          <small>{expenses.length} records</small>
        </div>
        <div className="stat-card warning">
          <div className="stat-label">This Month</div>
          <div className="stat-value">
            ${expenses
              .filter(e => {
                const date = new Date(e.expense_date);
                const now = new Date();
                return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear();
              })
              .reduce((sum, e) => sum + (e.amount || 0), 0)
              .toFixed(2)}
          </div>
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '+ Record Expense'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h3>Record New Expense</h3>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div className="form-group">
                <label>Description *</label>
                <input 
                  type="text" 
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Amount *</label>
                <input 
                  type="number" 
                  name="amount"
                  value={formData.amount}
                  onChange={handleInputChange}
                  step="0.01"
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
                <label>Date *</label>
                <input 
                  type="date" 
                  name="expense_date"
                  value={formData.expense_date}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>
            <button type="submit" className="btn btn-success">Record Expense</button>
          </form>
        </div>
      )}

      <div className="card">
        <h3>Expense Records</h3>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Description</th>
                <th>Category</th>
                <th>Amount</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {expenses.map(expense => (
                <tr key={expense.id}>
                  <td>{expense.description}</td>
                  <td>{expense.category?.name || '-'}</td>
                  <td style={{ color: '#f56565' }}>-${expense.amount.toFixed(2)}</td>
                  <td>{new Date(expense.expense_date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default ExpensesPage;
