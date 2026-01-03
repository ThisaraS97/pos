import React, { useState, useEffect } from 'react';
import './App.css';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import SalesPage from './pages/SalesPage';
import InventoryPage from './pages/InventoryPage';
import CustomersPage from './pages/CustomersPage';
import ReportsPage from './pages/ReportsPage';
import ProductsPage from './pages/ProductsPage';
import ExpensesPage from './pages/ExpensesPage';
import DayEndPage from './pages/DayEndPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      setIsLoggedIn(true);
      setUser(JSON.parse(userData));
    }
    
    setLoading(false);
  }, []);

  const handleLogin = (token, userData) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setIsLoggedIn(true);
    setUser(userData);
    setCurrentPage('dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setIsLoggedIn(false);
    setUser(null);
    setCurrentPage('dashboard');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">📊</span>
            <h1>AnyPos</h1>
          </div>
          <div className="user-info">
            <span className="user-name">{user?.full_name || 'User'}</span>
            <button onClick={handleLogout} className="btn-logout">Logout</button>
          </div>
        </div>
      </header>

      <div className="app-container">
        <nav className="sidebar">
          <ul className="nav-menu">
            <li>
              <button
                className={`nav-btn ${currentPage === 'dashboard' ? 'active' : ''}`}
                onClick={() => setCurrentPage('dashboard')}
              >
                📈 Dashboard
              </button>
            </li>
            <li>
              <button
                className={`nav-btn ${currentPage === 'sales' ? 'active' : ''}`}
                onClick={() => setCurrentPage('sales')}
              >
                💳 Sales
              </button>
            </li>
            <li>
              <button
                className={`nav-btn ${currentPage === 'products' ? 'active' : ''}`}
                onClick={() => setCurrentPage('products')}
              >
                📦 Products
              </button>
            </li>
            <li>
              <button
                className={`nav-btn ${currentPage === 'inventory' ? 'active' : ''}`}
                onClick={() => setCurrentPage('inventory')}
              >
                📚 Inventory
              </button>
            </li>
            <li>
              <button
                className={`nav-btn ${currentPage === 'customers' ? 'active' : ''}`}
                onClick={() => setCurrentPage('customers')}
              >
                👥 Customers
              </button>
            </li>
            <li>
              <button
                className={`nav-btn ${currentPage === 'expenses' ? 'active' : ''}`}
                onClick={() => setCurrentPage('expenses')}
              >
                💰 Expenses
              </button>
            </li>
            <li>
              <button
                className={`nav-btn ${currentPage === 'reports' ? 'active' : ''}`}
                onClick={() => setCurrentPage('reports')}
              >
                📊 Reports
              </button>
            </li>
            <li>
              <button
                className={`nav-btn ${currentPage === 'dayend' ? 'active' : ''}`}
                onClick={() => setCurrentPage('dayend')}
              >
                🔚 Day End
              </button>
            </li>
          </ul>
        </nav>

        <main className="main-content">
          {currentPage === 'dashboard' && <Dashboard />}
          {currentPage === 'sales' && <SalesPage />}
          {currentPage === 'products' && <ProductsPage />}
          {currentPage === 'inventory' && <InventoryPage />}
          {currentPage === 'customers' && <CustomersPage />}
          {currentPage === 'expenses' && <ExpensesPage />}
          {currentPage === 'reports' && <ReportsPage />}
          {currentPage === 'dayend' && <DayEndPage />}
        </main>
      </div>
    </div>
  );
}

export default App;
