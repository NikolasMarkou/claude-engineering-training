import { writable } from 'svelte/store';
import { api } from '$lib/api/client';
import type { Category } from '$lib/api/types';

function createCategoriesStore() {
	const { subscribe, set } = writable<Category[]>([]);

	return {
		subscribe,
		async load() {
			const categories = await api.getCategories();
			set(categories);
		},
		async create(data: Partial<Category>) {
			const category = await api.createCategory(data);
			await this.load();
			return category;
		},
		async delete(id: number) {
			await api.deleteCategory(id);
			await this.load();
		}
	};
}

export const categories = createCategoriesStore();
