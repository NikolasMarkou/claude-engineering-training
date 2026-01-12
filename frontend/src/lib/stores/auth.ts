import { writable } from 'svelte/store';
import { api } from '$lib/api/client';

interface AuthState {
	isAuthenticated: boolean;
	isSetup: boolean;
	loading: boolean;
}

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>({
		isAuthenticated: false,
		isSetup: false,
		loading: true
	});

	return {
		subscribe,
		async checkStatus() {
			update((s) => ({ ...s, loading: true }));
			try {
				const status = await api.getAuthStatus();
				const isAuthenticated = api.isAuthenticated();
				set({
					isAuthenticated,
					isSetup: status.is_setup,
					loading: false
				});
			} catch {
				set({ isAuthenticated: false, isSetup: false, loading: false });
			}
		},
		async login(pin: string) {
			await api.login(pin);
			update((s) => ({ ...s, isAuthenticated: true }));
		},
		async setup(pin: string) {
			await api.setupPin(pin);
			update((s) => ({ ...s, isAuthenticated: true, isSetup: true }));
		},
		logout() {
			api.clearToken();
			set({ isAuthenticated: false, isSetup: true, loading: false });
		}
	};
}

export const auth = createAuthStore();
