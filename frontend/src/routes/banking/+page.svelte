<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import { categories } from '$lib/stores/categories';
	import { currency } from '$lib/stores/currency';
	import type { BankConnection, BankInfo, PendingTransaction } from '$lib/api/types';

	let connections: BankConnection[] = $state([]);
	let pendingTransactions: PendingTransaction[] = $state([]);
	let availableBanks: BankInfo[] = $state([]);
	let loading = $state(true);
	let syncing = $state<number | null>(null);

	let showAddBank = $state(false);
	let selectedBank = $state('');
	let selectedAccount = $state('');

	onMount(async () => {
		await Promise.all([categories.load(), currency.load()]);
		await loadData();
	});

	async function loadData() {
		loading = true;
		try {
			const [conns, pending, banks] = await Promise.all([
				api.getBankConnections(),
				api.getPendingTransactions(),
				api.getAvailableBanks()
			]);
			connections = conns;
			pendingTransactions = pending;
			availableBanks = banks;
		} catch (e) {
			console.error('Failed to load banking data:', e);
		} finally {
			loading = false;
		}
	}

	async function addConnection() {
		if (!selectedBank || !selectedAccount) return;

		const bank = availableBanks.find((b) => b.name === selectedBank);
		if (!bank) return;

		const accountType = selectedAccount.toLowerCase().includes('credit')
			? 'credit'
			: selectedAccount.toLowerCase().includes('savings')
				? 'savings'
				: 'checking';

		try {
			await api.createBankConnection({
				bank_name: selectedBank,
				account_name: selectedAccount,
				account_type: accountType
			});
			showAddBank = false;
			selectedBank = '';
			selectedAccount = '';
			await loadData();
		} catch (e) {
			console.error('Failed to add connection:', e);
		}
	}

	async function syncConnection(id: number) {
		syncing = id;
		try {
			const result = await api.syncBankConnection(id);
			alert(`Synced ${result.synced} new transactions`);
			await loadData();
		} catch (e) {
			console.error('Failed to sync:', e);
		} finally {
			syncing = null;
		}
	}

	async function disconnectBank(id: number) {
		if (confirm('Disconnect this bank account?')) {
			try {
				await api.deleteBankConnection(id);
				await loadData();
			} catch (e) {
				console.error('Failed to disconnect:', e);
			}
		}
	}

	async function importTransaction(pending: PendingTransaction) {
		const categoryId = pending.suggested_category_id;
		if (!categoryId) {
			alert('Please select a category');
			return;
		}
		try {
			await api.importPendingTransaction(pending.id, categoryId);
			await loadData();
		} catch (e) {
			console.error('Failed to import:', e);
		}
	}

	async function dismissTransaction(id: number) {
		try {
			await api.dismissPendingTransaction(id);
			await loadData();
		} catch (e) {
			console.error('Failed to dismiss:', e);
		}
	}

	async function importAll() {
		try {
			const result = await api.importAllPending();
			alert(`Imported ${result.imported} transactions`);
			await loadData();
		} catch (e) {
			console.error('Failed to import all:', e);
		}
	}

	function updateCategory(pending: PendingTransaction, categoryId: number) {
		pending.suggested_category_id = categoryId;
	}

	function formatCurrency(amount: number): string {
		return currency.format(amount);
	}

	function formatDate(dateStr: string | null): string {
		if (!dateStr) return 'Never';
		return new Date(dateStr).toLocaleString();
	}

	$effect(() => {
		if (selectedBank) {
			const bank = availableBanks.find((b) => b.name === selectedBank);
			if (bank && bank.accounts.length > 0) {
				selectedAccount = bank.accounts[0];
			}
		}
	});
</script>

<svelte:head>
	<title>Banking | Budget App</title>
</svelte:head>

<div class="banking-page">
	<div class="header">
		<h1>Open Banking</h1>
		<button class="btn-primary" onclick={() => (showAddBank = true)}>Connect Bank</button>
	</div>

	{#if showAddBank}
		<div class="modal-overlay" onclick={() => (showAddBank = false)}>
			<div class="modal" onclick={(e) => e.stopPropagation()}>
				<h2>Connect Bank Account</h2>
				<div class="form-group">
					<label for="bank">Select Bank</label>
					<select id="bank" bind:value={selectedBank}>
						<option value="">Choose a bank...</option>
						{#each availableBanks as bank}
							<option value={bank.name}>{bank.name}</option>
						{/each}
					</select>
				</div>
				{#if selectedBank}
					<div class="form-group">
						<label for="account">Select Account</label>
						<select id="account" bind:value={selectedAccount}>
							{#each availableBanks.find((b) => b.name === selectedBank)?.accounts || [] as account}
								<option value={account}>{account}</option>
							{/each}
						</select>
					</div>
				{/if}
				<div class="form-actions">
					<button class="btn-secondary" onclick={() => (showAddBank = false)}>Cancel</button>
					<button class="btn-primary" onclick={addConnection} disabled={!selectedBank || !selectedAccount}>
						Connect
					</button>
				</div>
			</div>
		</div>
	{/if}

	{#if loading}
		<p>Loading...</p>
	{:else}
		<section class="accounts-section">
			<h2>Connected Accounts</h2>
			{#if connections.length === 0}
				<p class="empty">No bank accounts connected. Click "Connect Bank" to get started.</p>
			{:else}
				<div class="accounts-grid">
					{#each connections as conn}
						<div class="account-card">
							<div class="account-header">
								<h3>{conn.bank_name}</h3>
								<span class="account-type">{conn.account_type}</span>
							</div>
							<p class="account-name">{conn.account_name}</p>
							<p class="balance" class:negative={conn.balance < 0}>
								{formatCurrency(conn.balance)}
							</p>
							<p class="last-synced">Last synced: {formatDate(conn.last_synced)}</p>
							<div class="account-actions">
								<button
									class="btn-secondary"
									onclick={() => syncConnection(conn.id)}
									disabled={syncing === conn.id}
								>
									{syncing === conn.id ? 'Syncing...' : 'Sync'}
								</button>
								<button class="btn-danger" onclick={() => disconnectBank(conn.id)}>Disconnect</button>
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</section>

		<section class="pending-section">
			<div class="pending-header">
				<h2>Pending Transactions ({pendingTransactions.length})</h2>
				{#if pendingTransactions.length > 0}
					<button class="btn-primary" onclick={importAll}>Import All</button>
				{/if}
			</div>

			{#if pendingTransactions.length === 0}
				<p class="empty">No pending transactions. Sync a bank account to fetch new transactions.</p>
			{:else}
				<div class="pending-list">
					{#each pendingTransactions as pending}
						<div class="pending-item">
							<div class="pending-info">
								<span class="merchant">{pending.merchant_name}</span>
								<span class="date">{pending.date}</span>
							</div>
							<div class="pending-amount">
								{formatCurrency(pending.amount)}
							</div>
							<div class="pending-category">
								<select
									value={pending.suggested_category_id || 0}
									onchange={(e) => updateCategory(pending, parseInt((e.target as HTMLSelectElement).value))}
								>
									<option value={0} disabled>Select category</option>
									{#each $categories as cat}
										<option value={cat.id}>{cat.name}</option>
									{/each}
								</select>
							</div>
							<div class="pending-actions">
								<button class="btn-small btn-primary" onclick={() => importTransaction(pending)}>
									Import
								</button>
								<button class="btn-small btn-secondary" onclick={() => dismissTransaction(pending.id)}>
									Dismiss
								</button>
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</section>
	{/if}
</div>

<style>
	.banking-page {
		max-width: 1000px;
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

	.btn-primary {
		padding: 0.75rem 1.5rem;
		background: #3498db;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	.btn-primary:hover {
		background: #2980b9;
	}

	.btn-primary:disabled {
		background: #bdc3c7;
		cursor: not-allowed;
	}

	.btn-secondary {
		padding: 0.75rem 1.5rem;
		background: #ecf0f1;
		color: #333;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	.btn-danger {
		padding: 0.75rem 1.5rem;
		background: #e74c3c;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	.btn-small {
		padding: 0.4rem 0.8rem;
		font-size: 0.85rem;
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
		max-width: 400px;
	}

	.modal h2 {
		margin: 0 0 1.5rem;
	}

	.form-group {
		margin-bottom: 1rem;
	}

	.form-group label {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: 500;
	}

	.form-group select {
		width: 100%;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 1rem;
	}

	.form-actions {
		display: flex;
		justify-content: flex-end;
		gap: 1rem;
		margin-top: 1.5rem;
	}

	section {
		background: white;
		padding: 1.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		margin-bottom: 1.5rem;
	}

	section h2 {
		margin: 0 0 1rem;
		font-size: 1.2rem;
	}

	.empty {
		color: #666;
		text-align: center;
		padding: 2rem;
	}

	.accounts-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: 1rem;
	}

	.account-card {
		border: 1px solid #eee;
		border-radius: 8px;
		padding: 1.25rem;
	}

	.account-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.5rem;
	}

	.account-header h3 {
		margin: 0;
		font-size: 1.1rem;
	}

	.account-type {
		font-size: 0.8rem;
		background: #ecf0f1;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		text-transform: capitalize;
	}

	.account-name {
		color: #666;
		margin: 0 0 0.5rem;
	}

	.balance {
		font-size: 1.5rem;
		font-weight: bold;
		margin: 0 0 0.5rem;
		color: #2ecc71;
	}

	.balance.negative {
		color: #e74c3c;
	}

	.last-synced {
		font-size: 0.85rem;
		color: #999;
		margin: 0 0 1rem;
	}

	.account-actions {
		display: flex;
		gap: 0.5rem;
	}

	.pending-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
	}

	.pending-header h2 {
		margin: 0;
	}

	.pending-list {
		border: 1px solid #eee;
		border-radius: 8px;
	}

	.pending-item {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		border-bottom: 1px solid #eee;
	}

	.pending-item:last-child {
		border-bottom: none;
	}

	.pending-info {
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	.merchant {
		font-weight: 500;
	}

	.date {
		font-size: 0.85rem;
		color: #666;
	}

	.pending-amount {
		font-weight: 600;
		min-width: 100px;
		text-align: right;
	}

	.pending-category select {
		padding: 0.5rem;
		border: 1px solid #ddd;
		border-radius: 4px;
		min-width: 150px;
	}

	.pending-actions {
		display: flex;
		gap: 0.5rem;
	}
</style>
