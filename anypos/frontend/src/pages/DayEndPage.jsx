import { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/DayEnd.css';

const API_URL = 'http://localhost:8000/api';

export default function DayEndPage() {
  const [activeDayEnd, setActiveDayEnd] = useState(null);
  const [dayEndList, setDayEndList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [mode, setMode] = useState('view'); // 'view', 'open', 'close'
  const [formData, setFormData] = useState({
    opening_balance: '',
    actual_cash: '',
    notes: ''
  });

  const token = localStorage.getItem('token');

  // Fetch active day-end
  const fetchActiveDayEnd = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/dayend/active`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setActiveDayEnd(response.data);
      setError('');
    } catch (err) {
      if (err.response?.status === 404) {
        setActiveDayEnd(null);
      } else {
        setError(err.response?.data?.detail || 'Failed to fetch day-end');
      }
    } finally {
      setLoading(false);
    }
  };

  // Fetch day-end history
  const fetchDayEndHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/dayend/list`, {
        headers: { Authorization: `Bearer ${token}` },
        params: { skip: 0, limit: 20 }
      });
      setDayEndList(response.data);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    }
  };

  useEffect(() => {
    fetchActiveDayEnd();
    fetchDayEndHistory();
  }, []);

  // Open new day-end
  const handleOpenDayEnd = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError('');
      const response = await axios.post(
        `${API_URL}/dayend/open`,
        {
          opening_balance: parseFloat(formData.opening_balance) || 0,
          notes: formData.notes
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setActiveDayEnd(response.data);
      setSuccess('Day-end opened successfully!');
      setFormData({ opening_balance: '', actual_cash: '', notes: '' });
      setMode('view');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to open day-end');
    } finally {
      setLoading(false);
    }
  };

  // Close day-end
  const handleCloseDayEnd = async (e) => {
    e.preventDefault();
    if (!activeDayEnd) return;

    try {
      setLoading(true);
      setError('');
      const response = await axios.post(
        `${API_URL}/dayend/${activeDayEnd.id}/close`,
        {
          actual_cash: parseFloat(formData.actual_cash),
          notes: formData.notes
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setActiveDayEnd(response.data);
      setSuccess('Day-end closed successfully!');
      setFormData({ opening_balance: '', actual_cash: '', notes: '' });
      setMode('view');
      fetchDayEndHistory();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to close day-end');
    } finally {
      setLoading(false);
    }
  };

  // Get day-end summary
  const handleViewSummary = async () => {
    if (!activeDayEnd) return;
    
    try {
      setLoading(true);
      const response = await axios.get(
        `${API_URL}/dayend/${activeDayEnd.id}/summary`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      // You could open this in a modal or navigate to a detailed view
      console.log('Summary:', response.data);
      alert('Summary loaded - check console for details');
    } catch (err) {
      setError('Failed to fetch summary');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="dayend-container">
      <h1>Day End Management</h1>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      {/* Active Day End Status */}
      {activeDayEnd ? (
        <div className="dayend-active">
          <h2>Active Day End</h2>
          <div className="dayend-info">
            <div className="info-row">
              <span className="label">Status:</span>
              <span className="value">
                {activeDayEnd.is_closed ? 'CLOSED' : 'OPEN'}
              </span>
            </div>
            <div className="info-row">
              <span className="label">Opened at:</span>
              <span className="value">{formatDate(activeDayEnd.opened_at)}</span>
            </div>
            <div className="info-row">
              <span className="label">Sales Count:</span>
              <span className="value">{activeDayEnd.total_sales_count}</span>
            </div>
            <div className="info-row">
              <span className="label">Total Revenue:</span>
              <span className="value">{formatCurrency(activeDayEnd.total_revenue)}</span>
            </div>
            <div className="info-row">
              <span className="label">Opening Balance:</span>
              <span className="value">{formatCurrency(activeDayEnd.opening_balance)}</span>
            </div>
          </div>

          {/* Payment Breakdown */}
          <div className="dayend-breakdown">
            <h3>Payment Method Breakdown</h3>
            <div className="breakdown-grid">
              <div className="breakdown-item">
                <span>Cash Sales:</span>
                <span>{formatCurrency(activeDayEnd.cash_sales)}</span>
              </div>
              <div className="breakdown-item">
                <span>Card Sales:</span>
                <span>{formatCurrency(activeDayEnd.card_sales)}</span>
              </div>
              <div className="breakdown-item">
                <span>Cheque Sales:</span>
                <span>{formatCurrency(activeDayEnd.cheque_sales)}</span>
              </div>
              <div className="breakdown-item">
                <span>Online Sales:</span>
                <span>{formatCurrency(activeDayEnd.online_sales)}</span>
              </div>
              <div className="breakdown-item">
                <span>Credit Sales:</span>
                <span>{formatCurrency(activeDayEnd.credit_sales)}</span>
              </div>
            </div>
          </div>

          {/* Cash Reconciliation */}
          <div className="dayend-reconciliation">
            <h3>Cash Reconciliation</h3>
            <div className="reconciliation-grid">
              <div className="reconciliation-item">
                <span>Expected Cash:</span>
                <span>{formatCurrency(activeDayEnd.expected_cash)}</span>
              </div>
              <div className="reconciliation-item">
                <span>Actual Cash:</span>
                <span>{formatCurrency(activeDayEnd.actual_cash)}</span>
              </div>
              <div className={`reconciliation-item ${activeDayEnd.cash_variance >= 0 ? 'positive' : 'negative'}`}>
                <span>Variance:</span>
                <span>{formatCurrency(activeDayEnd.cash_variance)}</span>
              </div>
              <div className="reconciliation-item">
                <span>Closing Balance:</span>
                <span>{formatCurrency(activeDayEnd.closing_balance)}</span>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="dayend-actions">
            <button 
              className="btn btn-primary"
              onClick={handleViewSummary}
              disabled={loading}
            >
              View Full Summary
            </button>
            {!activeDayEnd.is_closed && (
              <button 
                className="btn btn-danger"
                onClick={() => setMode('close')}
              >
                Close Day End
              </button>
            )}
          </div>
        </div>
      ) : (
        <div className="dayend-empty">
          <p>No active day-end. Please open one to begin.</p>
        </div>
      )}

      {/* Forms */}
      {mode === 'open' && (
        <div className="dayend-form">
          <h2>Open New Day End</h2>
          <form onSubmit={handleOpenDayEnd}>
            <div className="form-group">
              <label>Opening Balance ($)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={formData.opening_balance}
                onChange={(e) => setFormData({ ...formData, opening_balance: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Notes (Optional)</label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                rows="3"
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-success" disabled={loading}>
                {loading ? 'Opening...' : 'Open Day End'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => setMode('view')}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {mode === 'close' && activeDayEnd && (
        <div className="dayend-form">
          <h2>Close Day End</h2>
          <form onSubmit={handleCloseDayEnd}>
            <div className="form-group">
              <label>Expected Cash: {formatCurrency(activeDayEnd.expected_cash)}</label>
              <p style={{ marginTop: '5px', fontSize: '0.9em', color: '#666' }}>
                Based on cash sales recorded
              </p>
            </div>
            <div className="form-group">
              <label>Actual Cash Counted ($)</label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={formData.actual_cash}
                onChange={(e) => setFormData({ ...formData, actual_cash: e.target.value })}
                required
                autoFocus
              />
            </div>
            <div className="form-group">
              <label>Variance: {formatCurrency((parseFloat(formData.actual_cash) || 0) - activeDayEnd.expected_cash)}</label>
              <p style={{ marginTop: '5px', fontSize: '0.9em', color: '#666' }}>
                Difference between actual and expected
              </p>
            </div>
            <div className="form-group">
              <label>Notes/Comments (Optional)</label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                rows="3"
                placeholder="Note any discrepancies or observations"
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-success" disabled={loading}>
                {loading ? 'Closing...' : 'Close Day End'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => setMode('view')}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {!activeDayEnd && mode === 'view' && (
        <div className="dayend-form">
          <button 
            className="btn btn-primary btn-lg"
            onClick={() => setMode('open')}
          >
            Open New Day End
          </button>
        </div>
      )}

      {/* History */}
      <div className="dayend-history">
        <h2>Day End History</h2>
        {dayEndList.length > 0 ? (
          <table className="history-table">
            <thead>
              <tr>
                <th>Date Opened</th>
                <th>Sales</th>
                <th>Revenue</th>
                <th>Variance</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {dayEndList.map((dayend) => (
                <tr key={dayend.id}>
                  <td>{formatDate(dayend.opened_at)}</td>
                  <td>{dayend.total_sales_count}</td>
                  <td>{formatCurrency(dayend.total_revenue)}</td>
                  <td className={dayend.cash_variance >= 0 ? 'positive' : 'negative'}>
                    {formatCurrency(dayend.cash_variance)}
                  </td>
                  <td>
                    <span className={`status ${dayend.is_closed ? 'closed' : 'open'}`}>
                      {dayend.is_closed ? 'Closed' : 'Open'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No day-end history found.</p>
        )}
      </div>
    </div>
  );
}
