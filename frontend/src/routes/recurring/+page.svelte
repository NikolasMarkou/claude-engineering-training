<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { categories } from '$lib/stores/categories';
	import type { RecurringTransaction } from '$lib/api/types';

	let recurring: RecurringTransaction[] = $state([]);
	let loading = $state(true);
	let showForm = $state(false);

	let formData = $state({
		amount: 0,
		type: 'expense' as 'income' | 'expense',
		category_id: 0,
		description: '',
		frequency: 'monthly',
		next_run_date: new Date().toISOString().slice(0, 10)
	});

	onMount(async () => {
		await categories.load();
		await loadRecurring();
	});

	async function loadRecurring() {
		loading = true;
		try {
			recurring = await api.getRecurring();
		} catch (e) {
			console.error('Failed to load recurring:', e);
		} finally {
			loading = false;
		}
	}

	async function handleSubmit() {
		try {
			await api.createRecurring(formData);
			showForm = false;
			formData = { amount: 0, type: 'expense', category_id: 0, description: '', frequency: 'monthly', next_run_date: new Date().toISOString().slice(0, 10) };
			await loadRecurring();
		} catch (e) {
			console.error('Failed to create recurring:', e);
		}
	}

	async function toggleActive(item: RecurringTransaction) {
		try {
			await api.updateRecurring(item.id, { is_active: !item.is_active });
			await loadRecurring();
		} catch (e) {
			console.error('Failed to update:', e);
		}
	}

	async function handleDelete(id: number) {
		if (confirm('Delete this recurring transaction?')) {
			try {
				await api.deleteRecurring(id);
				await loadRecurring();
			} catch (e) {
				console.error('Failed to delete:', e);
			}
		}
	}

	async function processNow() {
		try {
			const result = await api.processRecurring();
			alert(`Processed ${result.processed} recurring transactions`);
			await loadRecurring();
		} catch (e) {
			console.error('Failed to process:', e);
		}
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
	}
</script>

<svelte:head>
	<title>Recurring | Budget App</title>
</svelte:head>

<div class="recurring-page">
	<div class="header">
		<h1>Recurring Transactions</h1>
		<div class="header-actions">
			<button class="btn-secondary" onclick={processNow}>Process Due</button>
			<button class="btn-primary" onclick={() => (showForm = true)}>Add Recurring</button>
		</div>
	</div>

	{#if showForm}
		<div class="modal-overlay" onclick={() => (showForm = false)}>
			<div class="modal" onclick={(e) => e.stopPropagation()}>
				<h2>New Recurring Transaction</h2>
				<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
					<div class="form-row">
						<div class="form-group">
							<label for="type">Type</label>
							<select id="type" bind:value={formData.type}>
								<option value="expense">Expense</option>
								<option value="income">Income</option>
							</select>
						</div>
						<div class="form-group">
							<label for="amount">Amount</label>
							<input type="number" id="amount" bind:value={formData.amount} step="0.01" min="0" required />
						</div>
					</div>
					<div class="form-group">
						<label for="category">Category</label>
						<select id="category" bind:value={formData.category_id} required>
							<option value={0} disabled>Select category</option>
							{#each $categories.filter((c) => c.type === formData.type) as category}
								<option value={category.id}>{category.name}</option>
							{/each}
						</select>
					</div>
					<div class="form-row">
						<div class="form-group">
							<label for="frequency">Frequency</label>
							<select id="frequency" bind:value={formData.frequency}>
								<option value="daily">Daily</option>
								<option value="weekly">Weekly</option>
								<option value="monthly">Monthly</option>
							</select>
						</div>
						<div class="form-group">
							<label for="next">Next Run Date</label>
							<input type="date" id="next" bind:value={formData.next_run_date} required />
						</div>
					</div>
					<div class="form-group">
						<label for="description">Description</label>
						<input type="text" id="description" bind:value={formData.description} placeholder="Optional" />
					</div>
					<div class="form-actions">
						<button type="button" class="btn-secondary" onclick={() => (showForm = false)}>Cancel</button>
						<button type="submit" class="btn-primary">Create</button>
					</div>
				</form>
			</div>
		</div>
	{/if}

	{#if loading}
		<p>Loading...</p>
	{:else if recurring.length === 0}
		<p class="empty">No recurring transactions. Add one for regular expenses or income.</p>
	{:else}
		<div class="recurring-list">
			{#each recurring as item}
				<div class="recurring-item" class:inactive={!item.is_active}>
					<div class="item-main">
						<div class="item-info">
							<span class="description">{item.description || item.category.name}</span>
							<span class="meta">{item.frequency} • Next: {item.next_run_date}</span>
						</div>
						<span class="amount" class:income={item.type === 'income'}>
							{item.type === 'income' ? '+' : '-'}{formatCurrency(item.amount)}
						</span>
					</div>
					<div class="item-actions">
						<label class="toggle">
							<input type="checkbox" checked={item.is_active} onchange={() => toggleActive(item)} />
							<span>Active</span>
						</label>
						<button class="btn-icon danger" onclick={() => handleDelete(item.id)}>Delete</button>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.recurring-page { max-width: 800px; }
	.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
	h1 { margin: 0; }
	.header-actions { display: flex; gap: 1rem; }
	.btn-primary { padding: 0.75rem 1.5rem; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
	.btn-secondary { padding: 0.75rem 1.5rem; background: #ecf0f1; color: #333; border: none; border-radius: 4px; cursor: pointer; }
	.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
	.modal { background: white; padding: 2rem; border-radius: 8px; width: 100%; max-width: 500px; }
	.modal h2 { margin: 0 0 1.5rem; }
	.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
	.form-group { margin-bottom: 1rem; }
	.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
	.form-group input, .form-group select { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; box-sizing: border-box; }
	.form-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; }
	.recurring-list { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
	.recurring-item { padding: 1rem 1.5rem; border-bottom: 1px solid #eee; }
	.recurring-item:last-child { border-bottom: none; }
	.recurring-item.inactive { opacity: 0.5; }
	.item-main { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
	.item-info { display: flex; flex-direction: column; }
	.description { font-weight: 500; }
	.meta { font-size: 0.85rem; color: #666; }
	.amount { font-size: 1.1rem; font-weight: 600; color: #e74c3c; }
	.amount.income { color: #2ecc71; }
	.item-actions { display: flex; gap: 1rem; align-items: center; }
	.toggle { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
	.toggle input { width: auto; }
	.btn-icon { padding: 0.25rem 0.5rem; background: none; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; font-size: 0.8rem; }
	.btn-icon.danger { color: #e74c3c; border-color: #e74c3c; }
	.empty { text-align: center; color: #666; padding: 3rem; background: white; border-radius: 8px; }
</style>
