<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { categories } from '$lib/stores/categories';
	import { currency } from '$lib/stores/currency';
	import type { Budget, BudgetStatus } from '$lib/api/types';

	let budgets: Budget[] = $state([]);
	let budgetStatus: BudgetStatus[] = $state([]);
	let loading = $state(true);
	let showForm = $state(false);

	let currentMonth = $state(new Date().toISOString().slice(0, 7));
	let formData = $state({ category_id: 0, amount: 0 });

	onMount(async () => {
		await Promise.all([categories.load(), currency.load()]);
		await loadBudgets();
	});

	async function loadBudgets() {
		loading = true;
		try {
			const [budgetsData, statusData] = await Promise.all([
				api.getBudgets(currentMonth),
				api.getBudgetStatus(currentMonth)
			]);
			budgets = budgetsData;
			budgetStatus = statusData;
		} catch (e) {
			console.error('Failed to load budgets:', e);
		} finally {
			loading = false;
		}
	}

	async function handleSubmit() {
		try {
			await api.createBudget({ ...formData, month: currentMonth });
			showForm = false;
			formData = { category_id: 0, amount: 0 };
			await loadBudgets();
		} catch (e) {
			console.error('Failed to create budget:', e);
		}
	}

	async function handleDelete(id: number) {
		if (confirm('Delete this budget?')) {
			try {
				await api.deleteBudget(id);
				await loadBudgets();
			} catch (e) {
				console.error('Failed to delete budget:', e);
			}
		}
	}

	function formatCurrency(amount: number): string {
		return currency.format(amount);
	}

	$effect(() => {
		if (currentMonth) {
			loadBudgets();
		}
	});
</script>

<svelte:head>
	<title>Budgets | Budget App</title>
</svelte:head>

<div class="budgets-page">
	<div class="header">
		<h1>Monthly Budgets</h1>
		<div class="header-actions">
			<input type="month" bind:value={currentMonth} />
			<button class="btn-primary" onclick={() => (showForm = true)}>Add Budget</button>
		</div>
	</div>

	{#if showForm}
		<div class="modal-overlay" onclick={() => (showForm = false)}>
			<div class="modal" onclick={(e) => e.stopPropagation()}>
				<h2>Set Budget</h2>
				<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
					<div class="form-group">
						<label for="category">Category</label>
						<select id="category" bind:value={formData.category_id} required>
							<option value={0} disabled>Select category</option>
							{#each $categories.filter((c) => c.type === 'expense') as category}
								<option value={category.id}>{category.name}</option>
							{/each}
						</select>
					</div>
					<div class="form-group">
						<label for="amount">Budget Amount</label>
						<input type="number" id="amount" bind:value={formData.amount} step="0.01" min="0" required />
					</div>
					<div class="form-actions">
						<button type="button" class="btn-secondary" onclick={() => (showForm = false)}>Cancel</button>
						<button type="submit" class="btn-primary">Save Budget</button>
					</div>
				</form>
			</div>
		</div>
	{/if}

	{#if loading}
		<p>Loading...</p>
	{:else if budgetStatus.length === 0}
		<p class="empty">No budgets set for {currentMonth}. Click "Add Budget" to get started.</p>
	{:else}
		<div class="budget-list">
			{#each budgetStatus as status}
				<div class="budget-card">
					<div class="budget-header">
						<h3>{status.category_name}</h3>
						<button class="btn-icon danger" onclick={() => {
							const budget = budgets.find(b => b.category_id === status.category_id);
							if (budget) handleDelete(budget.id);
						}}>Delete</button>
					</div>
					<div class="budget-amounts">
						<span class="spent">{formatCurrency(status.spent)}</span>
						<span class="separator">/</span>
						<span class="budgeted">{formatCurrency(status.budgeted)}</span>
					</div>
					<div class="progress-bar">
						<div
							class="progress-fill"
							class:over={status.percentage_used > 100}
							class:warning={status.percentage_used > 75 && status.percentage_used <= 100}
							style="width: {Math.min(status.percentage_used, 100)}%"
						></div>
					</div>
					<div class="budget-footer">
						<span class="percentage">{status.percentage_used}% used</span>
						<span class="remaining" class:negative={status.remaining < 0}>
							{status.remaining >= 0 ? formatCurrency(status.remaining) + ' left' : formatCurrency(Math.abs(status.remaining)) + ' over'}
						</span>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.budgets-page { max-width: 900px; }
	.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
	h1 { margin: 0; }
	.header-actions { display: flex; gap: 1rem; align-items: center; }
	.header-actions input { padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; }
	.btn-primary { padding: 0.75rem 1.5rem; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
	.btn-primary:hover { background: #2980b9; }
	.btn-secondary { padding: 0.75rem 1.5rem; background: #ecf0f1; color: #333; border: none; border-radius: 4px; cursor: pointer; }
	.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
	.modal { background: white; padding: 2rem; border-radius: 8px; width: 100%; max-width: 400px; }
	.modal h2 { margin: 0 0 1.5rem; }
	.form-group { margin-bottom: 1rem; }
	.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
	.form-group input, .form-group select { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; box-sizing: border-box; }
	.form-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; }
	.budget-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
	.budget-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
	.budget-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
	.budget-header h3 { margin: 0; font-size: 1.1rem; }
	.budget-amounts { font-size: 1.5rem; margin-bottom: 0.75rem; }
	.spent { font-weight: bold; }
	.separator { color: #999; margin: 0 0.25rem; }
	.budgeted { color: #666; }
	.progress-bar { height: 10px; background: #eee; border-radius: 5px; overflow: hidden; margin-bottom: 0.75rem; }
	.progress-fill { height: 100%; background: #2ecc71; border-radius: 5px; transition: width 0.3s; }
	.progress-fill.warning { background: #f39c12; }
	.progress-fill.over { background: #e74c3c; }
	.budget-footer { display: flex; justify-content: space-between; font-size: 0.9rem; color: #666; }
	.remaining.negative { color: #e74c3c; }
	.btn-icon { padding: 0.25rem 0.5rem; background: none; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; font-size: 0.8rem; }
	.btn-icon.danger { color: #e74c3c; border-color: #e74c3c; }
	.empty { text-align: center; color: #666; padding: 3rem; background: white; border-radius: 8px; }
</style>
