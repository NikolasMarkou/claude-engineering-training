import { writable, get } from 'svelte/store';
import { api } from '$lib/api/client';
import type { SupportedCurrency, ExchangeRates } from '$lib/api/types';
import { CURRENCY_CONFIG } from '$lib/api/types';

interface CurrencyState {
	current: SupportedCurrency;
	available: SupportedCurrency[];
	rates: ExchangeRates | null;
	loading: boolean;
}

function createCurrencyStore() {
	const { subscribe, set, update } = writable<CurrencyState>({
		current: 'USD',
		available: ['USD', 'EUR', 'GBP'],
		rates: null,
		loading: false
	});

	return {
		subscribe,

		/**
		 * Load currency preference from auth status
		 */
		async load() {
			update((s) => ({ ...s, loading: true }));
			try {
				const status = await api.getAuthStatus();
				update((s) => ({
					...s,
					current: status.currency as SupportedCurrency,
					available: (status.available_currencies || ['USD', 'EUR', 'GBP']) as SupportedCurrency[],
					loading: false
				}));
			} catch {
				update((s) => ({ ...s, loading: false }));
			}
		},

		/**
		 * Update user's currency preference
		 */
		async setCurrency(currency: SupportedCurrency) {
			try {
				await api.updateCurrency(currency);
				update((s) => ({ ...s, current: currency }));
			} catch (e) {
				console.error('Failed to update currency:', e);
				throw e;
			}
		},

		/**
		 * Load exchange rates
		 */
		async loadRates() {
			try {
				const rates = await api.getExchangeRates();
				update((s) => ({ ...s, rates }));
			} catch (e) {
				console.error('Failed to load exchange rates:', e);
			}
		},

		/**
		 * Refresh exchange rates from provider
		 */
		async refreshRates() {
			try {
				await api.refreshExchangeRates();
				await this.loadRates();
			} catch (e) {
				console.error('Failed to refresh exchange rates:', e);
				throw e;
			}
		},

		/**
		 * Format amount in current currency
		 */
		format(amount: number, currencyOverride?: SupportedCurrency): string {
			const state = get({ subscribe });
			const curr = currencyOverride || state.current;
			const config = CURRENCY_CONFIG[curr];

			return new Intl.NumberFormat(config.locale, {
				style: 'currency',
				currency: curr
			}).format(amount);
		},

		/**
		 * Get current currency
		 */
		getCurrent(): SupportedCurrency {
			return get({ subscribe }).current;
		}
	};
}

export const currency = createCurrencyStore();

/**
 * Utility function for formatting currency without store subscription
 * Can be imported and used directly in components
 */
export function formatCurrency(amount: number, curr: SupportedCurrency = 'USD'): string {
	const config = CURRENCY_CONFIG[curr];
	return new Intl.NumberFormat(config.locale, {
		style: 'currency',
		currency: curr
	}).format(amount);
}
