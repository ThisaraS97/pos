import React, { useState, useEffect } from 'react';
import { reportService } from '../services/api';

function Dashboard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchDashboardStats();
    }, []);

    const fetchDashboardStats = async () => {
        try {
            const data = await reportService.getDashboard();
            setStats(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div style={{ padding: '20px' }}>
            <h1>Dashboard - AnyPos</h1>
            {stats && (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
                    <div style={{ padding: '20px', background: '#f0f0f0', borderRadius: '5px' }}>
                        <h3>Today's Sales</h3>
                        <p style={{ fontSize: '24px' }}>${stats.today_revenue.toFixed(2)}</p>
                        <small>{stats.today_sales} transactions</small>
                    </div>
                    <div style={{ padding: '20px', background: '#f0f0f0', borderRadius: '5px' }}>
                        <h3>Month's Revenue</h3>
                        <p style={{ fontSize: '24px' }}>${stats.month_revenue.toFixed(2)}</p>
                        <small>{stats.month_sales} transactions</small>
                    </div>
                    <div style={{ padding: '20px', background: '#f0f0f0', borderRadius: '5px' }}>
                        <h3>Total Products</h3>
                        <p style={{ fontSize: '24px' }}>{stats.total_products}</p>
                        <small>{stats.total_customers} customers</small>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Dashboard;
