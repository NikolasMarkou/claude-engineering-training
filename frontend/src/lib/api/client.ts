import type {
	Category,
	Transaction,
	TransactionCreate,
	Budget,
	BudgetStatus,
	RecurringTransaction,
	Goal,
	MonthlySummary,
	CategoryBreakdown,
	AuthStatus,
	Token,
	BankInfo,
	BankConnection,
	PendingTransaction,
	BankBalance,
	ExchangeRates,
	SupportedCurrency
} from './types';

const API_BASE = 'http://localhost:8000/api';

class ApiClient {
	private token: string | null = null;

	constructor() {
		if (typeof window !== 'undefined') {
			this.token = localStorage.getItem('token');
		}
	}

	private async request<T>(
		endpoint: string,
		options: RequestInit = {}
	): Promise<T> {
		const headers: Record<string, string> = {
			'Content-Type': 'application/json',
			...(options.headers as Record<string, string>)
		};

		if (this.token) {
			headers['Authorization'] = `Bearer ${this.token}`;
		}

		const response = await fetch(`${API_BASE}${endpoint}`, {
			...options,
			headers
		});

		if (!response.ok) {
			const error = await response.json().catch(() => ({ detail: 'Request failed' }));
			throw new Error(error.detail || 'Request failed');
		}

		if (response.status === 204) {
			return undefined as T;
		}

		return response.json();
	}

	setToken(token: string) {
		this.token = token;
		if (typeof window !== 'undefined') {
			localStorage.setItem('token', token);
		}
	}

	clearToken() {
		this.token = null;
		if (typeof window !== 'undefined') {
			localStorage.removeItem('token');
		}
	}

	isAuthenticated(): boolean {
		return !!this.token;
	}

	// Auth
	async getAuthStatus(): Promise<AuthStatus> {
		return this.request('/auth/status');
	}

	async setupPin(pin: string): Promise<Token> {
		const result = await this.request<Token>('/auth/setup', {
			method: 'POST',
			body: JSON.stringify({ pin })
		});
		this.setToken(result.access_token);
		return result;
	}

	async login(pin: string): Promise<Token> {
		const result = await this.request<Token>('/auth/login', {
			method: 'POST',
			body: JSON.stringify({ pin })
		});
		this.setToken(result.access_token);
		return result;
	}

	async changePin(currentPin: string, newPin: string): Promise<void> {
		await this.request('/auth/change-pin', {
			method: 'POST',
			body: JSON.stringify({ current_pin: currentPin, new_pin: newPin })
		});
	}

	// Currency
	async updateCurrency(currency: SupportedCurrency): Promise<{ message: string; currency: string }> {
		return this.request('/auth/currency', {
			method: 'PUT',
			body: JSON.stringify({ currency })
		});
	}

	async getExchangeRates(): Promise<ExchangeRates> {
		return this.request('/auth/exchange-rates');
	}

	async refreshExchangeRates(): Promise<{ message: string; provider: string; cached_at: string | null }> {
		return this.request('/auth/exchange-rates/refresh', { method: 'POST' });
	}

	// Categories
	async getCategories(): Promise<Category[]> {
		return this.request('/categories');
	}

	async createCategory(data: Partial<Category>): Promise<Category> {
		return this.request('/categories', {
			method: 'POST',
			body: JSON.stringify(data)
		});
	}

	async deleteCategory(id: number): Promise<void> {
		await this.request(`/categories/${id}`, { method: 'DELETE' });
	}

	// Transactions
	async getTransactions(params?: {
		start_date?: string;
		end_date?: string;
		category_id?: number;
		type?: string;
	}): Promise<Transaction[]> {
		const searchParams = new URLSearchParams();
		if (params?.start_date) searchParams.set('start_date', params.start_date);
		if (params?.end_date) searchParams.set('end_date', params.end_date);
		if (params?.category_id) searchParams.set('category_id', String(params.category_id));
		if (params?.type) searchParams.set('type', params.type);

		const query = searchParams.toString();
		return this.request(`/transactions${query ? `?${query}` : ''}`);
	}

	async createTransaction(data: TransactionCreate): Promise<Transaction> {
		return this.request('/transactions', {
			method: 'POST',
			body: JSON.stringify(data)
		});
	}

	async updateTransaction(id: number, data: Partial<TransactionCreate>): Promise<Transaction> {
		return this.request(`/transactions/${id}`, {
			method: 'PUT',
			body: JSON.stringify(data)
		});
	}

	async deleteTransaction(id: number): Promise<void> {
		await this.request(`/transactions/${id}`, { method: 'DELETE' });
	}

	// Budgets
	async getBudgets(month: string): Promise<Budget[]> {
		return this.request(`/budgets?month=${month}`);
	}

	async getBudgetStatus(month: string): Promise<BudgetStatus[]> {
		return this.request(`/budgets/status?month=${month}`);
	}

	async createBudget(data: { category_id: number; amount: number; month: string }): Promise<Budget> {
		return this.request('/budgets', {
			method: 'POST',
			body: JSON.stringify(data)
		});
	}

	async deleteBudget(id: number): Promise<void> {
		await this.request(`/budgets/${id}`, { method: 'DELETE' });
	}

	// Recurring
	async getRecurring(): Promise<RecurringTransaction[]> {
		return this.request('/recurring');
	}

	async createRecurring(data: Partial<RecurringTransaction>): Promise<RecurringTransaction> {
		return this.request('/recurring', {
			method: 'POST',
			body: JSON.stringify(data)
		});
	}

	async updateRecurring(id: number, data: Partial<RecurringTransaction>): Promise<RecurringTransaction> {
		return this.request(`/recurring/${id}`, {
			method: 'PUT',
			body: JSON.stringify(data)
		});
	}

	async deleteRecurring(id: number): Promise<void> {
		await this.request(`/recurring/${id}`, { method: 'DELETE' });
	}

	async processRecurring(): Promise<{ processed: number }> {
		return this.request('/recurring/process', { method: 'POST' });
	}

	// Goals
	async getGoals(): Promise<Goal[]> {
		return this.request('/goals');
	}

	async createGoal(data: { name: string; target_amount: number; deadline: string }): Promise<Goal> {
		return this.request('/goals', {
			method: 'POST',
			body: JSON.stringify(data)
		});
	}

	async updateGoal(id: number, data: Partial<Goal>): Promise<Goal> {
		return this.request(`/goals/${id}`, {
			method: 'PUT',
			body: JSON.stringify(data)
		});
	}

	async contributeToGoal(id: number, amount: number): Promise<Goal> {
		return this.request(`/goals/${id}/contribute`, {
			method: 'POST',
			body: JSON.stringify({ amount })
		});
	}

	async deleteGoal(id: number): Promise<void> {
		await this.request(`/goals/${id}`, { method: 'DELETE' });
	}

	// Reports
	async getMonthlySummary(month: string): Promise<MonthlySummary> {
		return this.request(`/reports/monthly-summary?month=${month}`);
	}

	async getCategoryBreakdown(month: string): Promise<CategoryBreakdown[]> {
		return this.request(`/reports/category-breakdown?month=${month}`);
	}

	async getTrends(months: number = 6): Promise<MonthlySummary[]> {
		return this.request(`/reports/trends?months=${months}`);
	}

	// Import
	async uploadCSV(file: File): Promise<{ rows: unknown[]; errors: string[] }> {
		const formData = new FormData();
		formData.append('file', file);

		const response = await fetch(`${API_BASE}/import/csv`, {
			method: 'POST',
			headers: this.token ? { Authorization: `Bearer ${this.token}` } : {},
			body: formData
		});

		if (!response.ok) {
			const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
			throw new Error(error.detail || 'Upload failed');
		}

		return response.json();
	}

	async confirmImport(rows: unknown[]): Promise<{ created: number; errors: string[] }> {
		return this.request('/import/confirm', {
			method: 'POST',
			body: JSON.stringify({ rows })
		});
	}

	// Banking
	async getAvailableBanks(): Promise<BankInfo[]> {
		return this.request('/banking/banks');
	}

	async getBankConnections(): Promise<BankConnection[]> {
		return this.request('/banking/connections');
	}

	async createBankConnection(data: { bank_name: string; account_name: string; account_type: string }): Promise<BankConnection> {
		return this.request('/banking/connections', {
			method: 'POST',
			body: JSON.stringify(data)
		});
	}

	async deleteBankConnection(id: number): Promise<void> {
		await this.request(`/banking/connections/${id}`, { method: 'DELETE' });
	}

	async syncBankConnection(id: number): Promise<{ synced: number; balance: number }> {
		return this.request(`/banking/connections/${id}/sync`, { method: 'POST' });
	}

	async getPendingTransactions(): Promise<PendingTransaction[]> {
		return this.request('/banking/pending');
	}

	async importPendingTransaction(id: number, categoryId: number): Promise<{ message: string; transaction_id: number }> {
		return this.request(`/banking/pending/${id}/import`, {
			method: 'POST',
			body: JSON.stringify({ category_id: categoryId })
		});
	}

	async dismissPendingTransaction(id: number): Promise<void> {
		await this.request(`/banking/pending/${id}/dismiss`, { method: 'POST' });
	}

	async importAllPending(): Promise<{ imported: number }> {
		return this.request('/banking/pending/import-all', { method: 'POST' });
	}

	async getBankBalances(): Promise<BankBalance[]> {
		return this.request('/banking/balances');
	}
}

export const api = new ApiClient();
