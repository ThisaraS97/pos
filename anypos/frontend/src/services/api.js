// API Base URL Configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// API Client with authentication
class APIClient {
    constructor() {
        this.baseURL = API_BASE_URL;
        this.token = localStorage.getItem('access_token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('access_token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('access_token');
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const response = await fetch(url, {
            ...options,
            headers: this.getHeaders(),
        });

        if (response.status === 401) {
            this.clearToken();
            window.location.href = '/login';
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API Error');
        }

        return response.json();
    }

    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

export default new APIClient();

// API Service Methods
export const authService = {
    login: (username, password) => APIClient.post('/auth/login', { username, password }),
    register: (userData) => APIClient.post('/auth/register', userData),
};

export const productService = {
    getProducts: (skip = 0, limit = 100) => APIClient.get(`/products?skip=${skip}&limit=${limit}`),
    getProduct: (id) => APIClient.get(`/products/${id}`),
    searchProducts: (q) => APIClient.get(`/products/search?q=${q}`),
    createProduct: (data) => APIClient.post('/products', data),
    updateProduct: (id, data) => APIClient.put(`/products/${id}`, data),
    deleteProduct: (id) => APIClient.delete(`/products/${id}`),
    getCategories: () => APIClient.get('/products/categories'),
    createCategory: (data) => APIClient.post('/products/categories', data),
};

export const saleService = {
    getSales: (skip = 0, limit = 100) => APIClient.get(`/sales?skip=${skip}&limit=${limit}`),
    getSale: (id) => APIClient.get(`/sales/${id}`),
    createSale: (data) => APIClient.post('/sales', data),
    updateSale: (id, data) => APIClient.put(`/sales/${id}`, data),
    cancelSale: (id) => APIClient.delete(`/sales/${id}`),
};

export const customerService = {
    getCustomers: (skip = 0, limit = 100) => APIClient.get(`/customers?skip=${skip}&limit=${limit}`),
    getCustomer: (id) => APIClient.get(`/customers/${id}`),
    searchCustomers: (q) => APIClient.get(`/customers/search?q=${q}`),
    createCustomer: (data) => APIClient.post('/customers', data),
    updateCustomer: (id, data) => APIClient.put(`/customers/${id}`, data),
    deleteCustomer: (id) => APIClient.delete(`/customers/${id}`),
};

export const reportService = {
    getDashboard: () => APIClient.get('/reports/dashboard'),
    getSalesReport: (startDate, endDate) => APIClient.get(`/reports/sales?start_date=${startDate}&end_date=${endDate}`),
};
