<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { categories } from '$lib/stores/categories';
	import type { Transaction, Category, TransactionCreate } from '$lib/api/types';

	let transactions: Transaction[] = $state([]);
	let loading = $state(true);
	let showForm = $state(false);
	let editingId: number | null = $state(null);

	let formData: TransactionCreate = $state({
		amount: 0,
		type: 'expense',
		category_id: 0,
		description: '',
		date: new Date().toISOString().slice(0, 10)
	});

	let filterType = $state('');
	let filterCategory = $state(0);

	onMount(async () => {
		await Promise.all([loadTransactions(), categories.load()]);
	});

	async function loadTransactions() {
		loading = true;
		try {
			transactions = await api.getTransactions({
				type: filterType || undefined,
				category_id: filterCategory || undefined
			});
		} catch (e) {
			console.error('Failed to load transactions:', e);
		} finally {
			loading = false;
		}
	}

	function resetForm() {
		formData = {
			amount: 0,
			type: 'expense',
			category_id: 0,
			description: '',
			date: new Date().toISOString().slice(0, 10)
		};
		editingId = null;
		showForm = false;
	}

	async function handleSubmit() {
		try {
			if (editingId) {
				await api.updateTransaction(editingId, formData);
			} else {
				await api.createTransaction(formData);
			}
			resetForm();
			await loadTransactions();
		} catch (e) {
			console.error('Failed to save transaction:', e);
		}
	}

	function startEdit(transaction: Transaction) {
		formData = {
			amount: transaction.amount,
			type: transaction.type,
			category_id: transaction.category_id,
			description: transaction.description || '',
			date: transaction.date
		};
		editingId = transaction.id;
		showForm = true;
	}

	async function handleDelete(id: number) {
		if (confirm('Delete this transaction?')) {
			try {
				await api.deleteTransaction(id);
				await loadTransactions();
			} catch (e) {
				console.error('Failed to delete transaction:', e);
			}
		}
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	}

	function getCategoryColor(category: Category): string {
		return category.color || '#666';
	}

	$effect(() => {
		if (filterType !== undefined || filterCategory !== undefined) {
			loadTransactions();
		}
	});
</script>

<svelte:head>
	<title>Transactions | Budget App</title>
</svelte:head>

<div class="transactions-page">
	<div class="header">
		<h1>Transactions</h1>
		<button class="btn-primary" onclick={() => (showForm = true)}>Add Transaction</button>
	</div>

	<div class="filters">
		<select bind:value={filterType}>
			<option value="">All Types</option>
			<option value="income">Income</option>
			<option value="expense">Expense</option>
		</select>
		<select bind:value={filterCategory}>
			<option value={0}>All Categories</option>
			{#each $categories as category}
				<option value={category.id}>{category.name}</option>
			{/each}
		</select>
	</div>

	{#if showForm}
		<div class="modal-overlay" onclick={() => resetForm()}>
			<div class="modal" onclick={(e) => e.stopPropagation()}>
				<h2>{editingId ? 'Edit' : 'Add'} Transaction</h2>
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
							<input
								type="number"
								id="amount"
								bind:value={formData.amount}
								step="0.01"
								min="0"
								required
							/>
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

					<div class="form-group">
						<label for="date">Date</label>
						<input type="date" id="date" bind:value={formData.date} required />
					</div>

					<div class="form-group">
						<label for="description">Description</label>
						<input
							type="text"
							id="description"
							bind:value={formData.description}
							placeholder="Optional description"
						/>
					</div>

					<div class="form-actions">
						<button type="button" class="btn-secondary" onclick={() => resetForm()}>
							Cancel
						</button>
						<button type="submit" class="btn-primary">
							{editingId ? 'Update' : 'Add'}
						</button>
					</div>
				</form>
			</div>
		</div>
	{/if}

	{#if loading}
		<p>Loading...</p>
	{:else if transactions.length === 0}
		<p class="empty">No transactions found.</p>
	{:else}
		<div class="transactions-list">
			{#each transactions as transaction}
				<div class="transaction-item" class:income={transaction.type === 'income'}>
					<div class="transaction-main">
						<div
							class="category-badge"
							style="background-color: {getCategoryColor(transaction.category)}"
						>
							{transaction.category.name}
						</div>
						<div class="transaction-details">
							<span class="description">
								{transaction.description || transaction.category.name}
							</span>
							<span class="date">{transaction.date}</span>
						</div>
					</div>
					<div class="transaction-amount">
						<span class="amount" class:income={transaction.type === 'income'}>
							{transaction.type === 'income' ? '+' : '-'}{formatCurrency(transaction.amount)}
						</span>
						<div class="actions">
							<button class="btn-icon" onclick={() => startEdit(transaction)}>Edit</button>
							<button class="btn-icon danger" onclick={() => handleDelete(transaction.id)}>
								Delete
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.transactions-page {
		max-width: 900px;
	}

	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1.5rem;
	}

	h1 {
		margin: 0;
	}

	.filters {
		display: flex;
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.filters select {
		padding: 0.5rem 1rem;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 0.9rem;
	}

	.btn-primary {
		padding: 0.75rem 1.5rem;
		background: #3498db;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.9rem;
	}

	.btn-primary:hover {
		background: #2980b9;
	}

	.btn-secondary {
		padding: 0.75rem 1.5rem;
		background: #ecf0f1;
		color: #333;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.9rem;
	}

	.btn-secondary:hover {
		background: #bdc3c7;
	}

	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 100;
	}

	.modal {
		background: white;
		padding: 2rem;
		border-radius: 8px;
		width: 100%;
		max-width: 500px;
	}

	.modal h2 {
		margin: 0 0 1.5rem;
	}

	.form-row {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1rem;
	}

	.form-group {
		margin-bottom: 1rem;
	}

	.form-group label {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: 500;
	}

	.form-group input,
	.form-group select {
		width: 100%;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 1rem;
		box-sizing: border-box;
	}

	.form-actions {
		display: flex;
		justify-content: flex-end;
		gap: 1rem;
		margin-top: 1.5rem;
	}

	.transactions-list {
		background: white;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.transaction-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem 1.5rem;
		border-bottom: 1px solid #eee;
	}

	.transaction-item:last-child {
		border-bottom: none;
	}

	.transaction-main {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.category-badge {
		padding: 0.25rem 0.75rem;
		border-radius: 20px;
		color: white;
		font-size: 0.8rem;
	}

	.transaction-details {
		display: flex;
		flex-direction: column;
	}

	.description {
		font-weight: 500;
	}

	.date {
		font-size: 0.85rem;
		color: #666;
	}

	.transaction-amount {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.amount {
		font-size: 1.1rem;
		font-weight: 600;
		color: #e74c3c;
	}

	.amount.income {
		color: #2ecc71;
	}

	.actions {
		display: flex;
		gap: 0.5rem;
	}

	.btn-icon {
		padding: 0.25rem 0.5rem;
		background: none;
		border: 1px solid #ddd;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.8rem;
	}

	.btn-icon:hover {
		background: #f5f5f5;
	}

	.btn-icon.danger {
		color: #e74c3c;
		border-color: #e74c3c;
	}

	.btn-icon.danger:hover {
		background: #fde8e8;
	}

	.empty {
		text-align: center;
		color: #666;
		padding: 3rem;
		background: white;
		border-radius: 8px;
	}
</style>
