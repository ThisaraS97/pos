import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function ReportsPage() {
  const [stats, setStats] = useState(null);
  const [topProducts, setTopProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('access_token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const [dashRes, topRes] = await Promise.all([
        axios.get(`${API_URL}/reports/dashboard`, { headers }),
        axios.get(`${API_URL}/reports/products/top`, { headers })
      ]);
      
      setStats(dashRes.data);
      setTopProducts(topRes.data);
    } catch (err) {
      console.error('Error fetching reports:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!stats) return <div>No data available</div>;

  return (
    <div className="page">
      <h2 className="page-title">📊 Reports & Analytics</h2>

      {/* Key metrics */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Today's Sales</div>
          <div className="stat-value">${stats.today_revenue?.toFixed(2) || '0.00'}</div>
          <small>{stats.today_sales || 0} transactions</small>
        </div>
        <div className="stat-card success">
          <div className="stat-label">Month's Revenue</div>
          <div className="stat-value">${stats.month_revenue?.toFixed(2) || '0.00'}</div>
          <small>{stats.month_sales || 0} transactions</small>
        </div>
        <div className="stat-card warning">
          <div className="stat-label">Total Products</div>
          <div className="stat-value">{stats.total_products || 0}</div>
          <small>{stats.total_customers || 0} customers</small>
        </div>
        <div className="stat-card danger">
          <div className="stat-label">Year Revenue</div>
          <div className="stat-value">${stats.year_revenue?.toFixed(2) || '0.00'}</div>
          <small>Total all time</small>
        </div>
      </div>

      {/* Top products */}
      <div className="card">
        <h3>Top Selling Products</h3>
        {topProducts.length === 0 ? (
          <p style={{ color: '#999' }}>No sales data yet</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Product Name</th>
                  <th>Units Sold</th>
                  <th>Revenue</th>
                  <th>Avg Price</th>
                </tr>
              </thead>
              <tbody>
                {topProducts.map((product, idx) => (
                  <tr key={product.id}>
                    <td>
                      <span style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '30px',
                        height: '30px',
                        borderRadius: '50%',
                        background: idx === 0 ? '#ffd700' : idx === 1 ? '#c0c0c0' : '#cd7f32',
                        color: 'white',
                        fontWeight: 'bold'
                      }}>
                        {idx + 1}
                      </span>
                    </td>
                    <td>{product.name}</td>
                    <td>{product.total_quantity}</td>
                    <td>${product.total_revenue?.toFixed(2) || '0.00'}</td>
                    <td>${(product.total_revenue / product.total_quantity)?.toFixed(2) || '0.00'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Sales trend info */}
      <div className="card" style={{ marginTop: '20px' }}>
        <h3>Sales Summary</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div>
            <h4>Daily Average</h4>
            <p style={{ fontSize: '1.5em', color: '#667eea' }}>
              ${(stats.today_revenue / (stats.today_sales || 1))?.toFixed(2) || '0.00'}
            </p>
            <small>Per transaction</small>
          </div>
          <div>
            <h4>Monthly Average</h4>
            <p style={{ fontSize: '1.5em', color: '#667eea' }}>
              ${(stats.month_revenue / 30)?.toFixed(2) || '0.00'}
            </p>
            <small>Per day</small>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ReportsPage;
