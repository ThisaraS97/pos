import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function LoginPage({ onLogin }) {
    const [username, setUsername] = useState('admin');
    const [password, setPassword] = useState('admin123');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showOpeningCash, setShowOpeningCash] = useState(false);
    const [openingCash, setOpeningCash] = useState('');
    const [token, setToken] = useState(null);
    const [userData, setUserData] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await axios.post(`${API_URL}/auth/login`, {
                username,
                password
            });

            const loginToken = response.data.access_token;
            const loginUserData = {
                username,
                full_name: username.charAt(0).toUpperCase() + username.slice(1)
            };

            setToken(loginToken);
            setUserData(loginUserData);

            // Check dayend status
            try {
                const dayendStatus = await axios.get(`${API_URL}/dayend/check-status`, {
                    headers: { Authorization: `Bearer ${loginToken}` }
                });

                if (!dayendStatus.data.has_active_dayend || dayendStatus.data.needs_opening_cash) {
                    // Show opening cash modal
                    setShowOpeningCash(true);
                    setLoading(false);
                } else {
                    // Already has active dayend with opening cash, proceed to login
                    onLogin(loginToken, loginUserData);
                }
            } catch (err) {
                // If check fails, assume we need opening cash
                setShowOpeningCash(true);
                setLoading(false);
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
            setLoading(false);
        }
    };

    const handleOpeningCashSubmit = async (e) => {
        e.preventDefault();
        if (!openingCash || parseFloat(openingCash) < 0) {
            setError('Please enter a valid opening cash amount');
            return;
        }

        setLoading(true);
        setError('');

        try {
            // Open dayend with opening cash
            await axios.post(
                `${API_URL}/dayend/open`,
                {
                    opening_balance: parseFloat(openingCash),
                    notes: 'Opening cash entered on login'
                },
                {
                    headers: { Authorization: `Bearer ${token}` }
                }
            );

            // Proceed to login
            onLogin(token, userData);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to set opening cash');
            setLoading(false);
        }
    };

    const handleSkipOpeningCash = () => {
        // Skip opening cash and proceed (will default to 0)
        onLogin(token, userData);
    };

    return (
        <div style={{
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px'
        }}>
            <div style={{
                background: 'white',
                borderRadius: '10px',
                padding: '40px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
                maxWidth: '400px',
                width: '100%'
            }}>
                <div style={{ textAlign: 'center', marginBottom: '30px' }}>
                    <div style={{ fontSize: '3em', marginBottom: '10px' }}>📊</div>
                    <h1 style={{ color: '#333', fontSize: '2em', margin: 0 }}>AnyPos</h1>
                    <p style={{ color: '#666', margin: '5px 0 0 0' }}>Modern Point of Sale System</p>
                </div>

                {error && (
                    <div style={{
                        background: '#fed7d7',
                        color: '#742a2a',
                        padding: '10px 15px',
                        borderRadius: '5px',
                        marginBottom: '20px',
                        borderLeft: '4px solid #f56565'
                    }}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '20px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: '#333' }}>
                            Username
                        </label>
                        <input
                            type="text"
                            placeholder="Enter username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            style={{
                                width: '100%',
                                padding: '12px',
                                border: '1px solid #ddd',
                                borderRadius: '5px',
                                fontSize: '1em',
                                transition: 'all 0.3s ease',
                                boxSizing: 'border-box'
                            }}
                            disabled={loading}
                        />
                    </div>

                    <div style={{ marginBottom: '25px' }}>
                        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600', color: '#333' }}>
                            Password
                        </label>
                        <input
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            style={{
                                width: '100%',
                                padding: '12px',
                                border: '1px solid #ddd',
                                borderRadius: '5px',
                                fontSize: '1em',
                                transition: 'all 0.3s ease',
                                boxSizing: 'border-box'
                            }}
                            disabled={loading}
                        />
                    </div>

                    <button
                        type="submit"
                        style={{
                            width: '100%',
                            padding: '12px',
                            background: '#667eea',
                            color: 'white',
                            border: 'none',
                            borderRadius: '5px',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            fontWeight: '600',
                            fontSize: '1em',
                            transition: 'all 0.3s ease',
                            opacity: loading ? 0.7 : 1
                        }}
                        disabled={loading}
                        onMouseOver={(e) => !loading && (e.target.style.background = '#5568d3')}
                        onMouseOut={(e) => (e.target.style.background = '#667eea')}
                    >
                        {loading ? 'Logging in...' : 'Login'}
                    </button>
                </form>

                <div style={{ marginTop: '20px', textAlign: 'center', color: '#999', fontSize: '0.9em' }}>
                    <p>Demo Credentials:</p>
                    <p>admin / admin123</p>
                    <p>manager / manager123</p>
                    <p>cashier / cashier123</p>
                </div>
            </div>

            {/* Opening Cash Modal */}
            {showOpeningCash && (
                <div style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'rgba(0, 0, 0, 0.7)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 1000,
                    padding: '20px'
                }}>
                    <div style={{
                        background: 'white',
                        borderRadius: '15px',
                        padding: '40px',
                        boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5)',
                        maxWidth: '500px',
                        width: '100%',
                        animation: 'fadeIn 0.3s ease'
                    }}>
                        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
                            <div style={{ fontSize: '4em', marginBottom: '10px' }}>💰</div>
                            <h2 style={{ color: '#333', margin: 0, fontSize: '1.8em' }}>Opening Cash</h2>
                            <p style={{ color: '#666', marginTop: '10px' }}>
                                Enter the starting cash amount for today
                            </p>
                        </div>

                        {error && (
                            <div style={{
                                background: '#fed7d7',
                                color: '#742a2a',
                                padding: '10px 15px',
                                borderRadius: '5px',
                                marginBottom: '20px',
                                borderLeft: '4px solid #f56565'
                            }}>
                                {error}
                            </div>
                        )}

                        <form onSubmit={handleOpeningCashSubmit}>
                            <div style={{ marginBottom: '25px' }}>
                                <label style={{ 
                                    display: 'block', 
                                    marginBottom: '10px', 
                                    fontWeight: '600', 
                                    color: '#333',
                                    fontSize: '1.1em'
                                }}>
                                    Opening Cash Amount ($)
                                </label>
                                <input
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    placeholder="0.00"
                                    value={openingCash}
                                    onChange={(e) => setOpeningCash(e.target.value)}
                                    style={{
                                        width: '100%',
                                        padding: '15px',
                                        border: '2px solid #667eea',
                                        borderRadius: '8px',
                                        fontSize: '1.2em',
                                        fontWeight: '600',
                                        textAlign: 'center',
                                        boxSizing: 'border-box',
                                        transition: 'all 0.3s ease'
                                    }}
                                    autoFocus
                                    disabled={loading}
                                />
                            </div>

                            <div style={{ display: 'flex', gap: '10px' }}>
                                <button
                                    type="submit"
                                    style={{
                                        flex: 1,
                                        padding: '15px',
                                        background: '#667eea',
                                        color: 'white',
                                        border: 'none',
                                        borderRadius: '8px',
                                        cursor: loading ? 'not-allowed' : 'pointer',
                                        fontWeight: '600',
                                        fontSize: '1.1em',
                                        transition: 'all 0.3s ease',
                                        opacity: loading ? 0.7 : 1
                                    }}
                                    disabled={loading}
                                >
                                    {loading ? 'Setting...' : 'Continue'}
                                </button>
                                <button
                                    type="button"
                                    onClick={handleSkipOpeningCash}
                                    style={{
                                        padding: '15px 20px',
                                        background: '#e2e8f0',
                                        color: '#4a5568',
                                        border: 'none',
                                        borderRadius: '8px',
                                        cursor: 'pointer',
                                        fontWeight: '600',
                                        fontSize: '1em',
                                        transition: 'all 0.3s ease'
                                    }}
                                    disabled={loading}
                                >
                                    Skip
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default LoginPage;
