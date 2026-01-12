export interface Category {
	id: number;
	name: string;
	type: 'income' | 'expense';
	is_default: boolean;
	icon: string | null;
	color: string | null;
	created_at: string;
}

export interface Transaction {
	id: number;
	amount: number;
	type: 'income' | 'expense';
	category_id: number;
	description: string | null;
	date: string;
	created_at: string;
	category: Category;
}

export interface TransactionCreate {
	amount: number;
	type: 'income' | 'expense';
	category_id: number;
	description?: string;
	date: string;
}

export interface Budget {
	id: number;
	category_id: number;
	amount: number;
	month: string;
	created_at: string;
	category: Category;
}

export interface BudgetStatus {
	category_id: number;
	category_name: string;
	budgeted: number;
	spent: number;
	remaining: number;
	percentage_used: number;
}

export interface RecurringTransaction {
	id: number;
	amount: number;
	type: 'income' | 'expense';
	category_id: number;
	description: string | null;
	frequency: 'daily' | 'weekly' | 'monthly';
	next_run_date: string;
	is_active: boolean;
	created_at: string;
	category: Category;
}

export interface Goal {
	id: number;
	name: string;
	target_amount: number;
	current_amount: number;
	deadline: string;
	created_at: string;
	progress_percentage: number;
	days_remaining: number;
}

export interface MonthlySummary {
	month: string;
	income: number;
	expenses: number;
	net: number;
}

export interface CategoryBreakdown {
	category_id: number;
	category_name: string;
	type: string;
	total: number;
}

export interface AuthStatus {
	currency: string;
	is_setup: boolean;
	available_currencies: string[];
}

export type SupportedCurrency = 'USD' | 'EUR' | 'GBP';

export const CURRENCY_CONFIG: Record<SupportedCurrency, { locale: string; symbol: string; name: string }> = {
	USD: { locale: 'en-US', symbol: '$', name: 'US Dollar' },
	EUR: { locale: 'de-DE', symbol: '€', name: 'Euro' },
	GBP: { locale: 'en-GB', symbol: '£', name: 'British Pound' }
};

export interface ExchangeRates {
	provider: string;
	rates: Record<string, number>;
	cached_at: string | null;
}

export interface Token {
	access_token: string;
	token_type: string;
}

// Banking types
export interface BankInfo {
	name: string;
	accounts: string[];
}

export interface BankConnection {
	id: number;
	bank_name: string;
	account_name: string;
	account_type: string;
	balance: number;
	last_synced: string | null;
	is_active: boolean;
	created_at: string;
}

export interface PendingTransaction {
	id: number;
	bank_connection_id: number;
	external_id: string;
	amount: number;
	merchant_name: string;
	date: string;
	suggested_category_id: number | null;
	suggested_category: Category | null;
	status: string;
	created_at: string;
}

export interface BankBalance {
	bank_connection_id: number;
	bank_name: string;
	account_name: string;
	account_type: string;
	balance: number;
}
