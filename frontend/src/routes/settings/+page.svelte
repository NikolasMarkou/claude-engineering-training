<script lang="ts">
	import { api } from '$lib/api/client';
	import { categories } from '$lib/stores/categories';
	import { currency } from '$lib/stores/currency';
	import { onMount } from 'svelte';
	import type { Category, SupportedCurrency, ExchangeRates } from '$lib/api/types';
	import { CURRENCY_CONFIG } from '$lib/api/types';

	// Currency state
	let selectedCurrency = $state<SupportedCurrency>('USD');
	let currencySuccess = $state('');
	let currencyError = $state('');
	let exchangeRates = $state<ExchangeRates | null>(null);
	let refreshingRates = $state(false);

	let currentPin = $state('');
	let newPin = $state('');
	let confirmPin = $state('');
	let pinError = $state('');
	let pinSuccess = $state('');

	let newCategory = $state({ name: '', type: 'expense' as 'income' | 'expense', color: '#3498db' });
	let categoryError = $state('');

	let csvFile: FileList | null = $state(null);
	let csvPreview: { rows: unknown[]; errors: string[] } | null = $state(null);
	let importError = $state('');
	let importSuccess = $state('');

	onMount(async () => {
		categories.load();
		await currency.load();
		selectedCurrency = currency.getCurrent();
		loadExchangeRates();
	});

	async function loadExchangeRates() {
		try {
			exchangeRates = await api.getExchangeRates();
		} catch (e) {
			console.error('Failed to load exchange rates:', e);
		}
	}

	async function updateCurrency() {
		currencyError = '';
		currencySuccess = '';
		try {
			await currency.setCurrency(selectedCurrency);
			currencySuccess = 'Currency preference saved';
			setTimeout(() => (currencySuccess = ''), 3000);
		} catch (e) {
			currencyError = e instanceof Error ? e.message : 'Failed to update currency';
		}
	}

	async function refreshRates() {
		refreshingRates = true;
		try {
			await currency.refreshRates();
			await loadExchangeRates();
		} catch (e) {
			console.error('Failed to refresh rates:', e);
		}
		refreshingRates = false;
	}

	async function changePin() {
		pinError = '';
		pinSuccess = '';

		if (newPin.length < 4) {
			pinError = 'PIN must be at least 4 characters';
			return;
		}
		if (newPin !== confirmPin) {
			pinError = 'PINs do not match';
			return;
		}

		try {
			await api.changePin(currentPin, newPin);
			pinSuccess = 'PIN changed successfully';
			currentPin = '';
			newPin = '';
			confirmPin = '';
		} catch (e) {
			pinError = e instanceof Error ? e.message : 'Failed to change PIN';
		}
	}

	async function addCategory() {
		categoryError = '';
		if (!newCategory.name.trim()) {
			categoryError = 'Name is required';
			return;
		}
		try {
			await categories.create(newCategory);
			newCategory = { name: '', type: 'expense', color: '#3498db' };
		} catch (e) {
			categoryError = e instanceof Error ? e.message : 'Failed to create category';
		}
	}

	async function deleteCategory(id: number) {
		if (confirm('Delete this category?')) {
			try {
				await categories.delete(id);
			} catch (e) {
				alert(e instanceof Error ? e.message : 'Failed to delete');
			}
		}
	}

	async function handleCSVUpload() {
		importError = '';
		importSuccess = '';
		if (!csvFile || csvFile.length === 0) return;

		try {
			csvPreview = await api.uploadCSV(csvFile[0]);
		} catch (e) {
			importError = e instanceof Error ? e.message : 'Failed to parse CSV';
		}
	}

	async function confirmImport() {
		if (!csvPreview) return;
		try {
			const result = await api.confirmImport(csvPreview.rows);
			importSuccess = `Imported ${result.created} transactions`;
			if (result.errors.length > 0) {
				importError = result.errors.join(', ');
			}
			csvPreview = null;
			csvFile = null;
		} catch (e) {
			importError = e instanceof Error ? e.message : 'Import failed';
		}
	}
</script>

<svelte:head>
	<title>Settings | Budget App</title>
</svelte:head>

<div class="settings-page">
	<h1>Settings</h1>

	<section class="settings-section">
		<h2>Display Currency</h2>
		<div class="currency-form">
			<div class="form-group">
				<label for="currency">Preferred Currency</label>
				<select id="currency" bind:value={selectedCurrency} onchange={updateCurrency}>
					{#each $currency.available as curr}
						<option value={curr}>{CURRENCY_CONFIG[curr].symbol} {CURRENCY_CONFIG[curr].name} ({curr})</option>
					{/each}
				</select>
			</div>
			{#if currencyError}<p class="error">{currencyError}</p>{/if}
			{#if currencySuccess}<p class="success">{currencySuccess}</p>{/if}
		</div>

		{#if exchangeRates}
			<div class="exchange-rates">
				<h3>Exchange Rates</h3>
				<p class="help-text">
					Provider: {exchangeRates.provider}
					{#if exchangeRates.cached_at}
						| Last updated: {new Date(exchangeRates.cached_at).toLocaleString()}
					{/if}
				</p>
				<div class="rates-grid">
					{#each Object.entries(exchangeRates.rates) as [pair, rate]}
						<div class="rate-item">
							<span class="pair">{pair.replace('_', ' → ')}</span>
							<span class="rate">{rate.toFixed(4)}</span>
						</div>
					{/each}
				</div>
				<button class="btn-secondary" onclick={refreshRates} disabled={refreshingRates}>
					{refreshingRates ? 'Refreshing...' : 'Refresh Rates'}
				</button>
			</div>
		{/if}
	</section>

	<section class="settings-section">
		<h2>Change PIN</h2>
		<form onsubmit={(e) => { e.preventDefault(); changePin(); }}>
			<div class="form-group">
				<label for="currentPin">Current PIN</label>
				<input type="password" id="currentPin" bind:value={currentPin} />
			</div>
			<div class="form-group">
				<label for="newPin">New PIN</label>
				<input type="password" id="newPin" bind:value={newPin} />
			</div>
			<div class="form-group">
				<label for="confirmPin">Confirm New PIN</label>
				<input type="password" id="confirmPin" bind:value={confirmPin} />
			</div>
			{#if pinError}<p class="error">{pinError}</p>{/if}
			{#if pinSuccess}<p class="success">{pinSuccess}</p>{/if}
			<button type="submit" class="btn-primary">Change PIN</button>
		</form>
	</section>

	<section class="settings-section">
		<h2>Custom Categories</h2>
		<div class="category-form">
			<input type="text" bind:value={newCategory.name} placeholder="Category name" />
			<select bind:value={newCategory.type}>
				<option value="expense">Expense</option>
				<option value="income">Income</option>
			</select>
			<input type="color" bind:value={newCategory.color} />
			<button class="btn-primary" onclick={addCategory}>Add</button>
		</div>
		{#if categoryError}<p class="error">{categoryError}</p>{/if}

		<div class="categories-list">
			<h3>Expense Categories</h3>
			{#each $categories.filter((c) => c.type === 'expense') as cat}
				<div class="category-item">
					<span class="color-dot" style="background: {cat.color}"></span>
					<span class="name">{cat.name}</span>
					{#if cat.is_default}
						<span class="badge">Default</span>
					{:else}
						<button class="btn-icon danger" onclick={() => deleteCategory(cat.id)}>Delete</button>
					{/if}
				</div>
			{/each}

			<h3>Income Categories</h3>
			{#each $categories.filter((c) => c.type === 'income') as cat}
				<div class="category-item">
					<span class="color-dot" style="background: {cat.color}"></span>
					<span class="name">{cat.name}</span>
					{#if cat.is_default}
						<span class="badge">Default</span>
					{:else}
						<button class="btn-icon danger" onclick={() => deleteCategory(cat.id)}>Delete</button>
					{/if}
				</div>
			{/each}
		</div>
	</section>

	<section class="settings-section">
		<h2>Import Transactions (CSV)</h2>
		<p class="help-text">CSV must have columns: date, amount, type, category, description (optional)</p>
		<div class="import-form">
			<input type="file" accept=".csv" bind:files={csvFile} />
			<button class="btn-secondary" onclick={handleCSVUpload} disabled={!csvFile}>Preview</button>
		</div>
		{#if importError}<p class="error">{importError}</p>{/if}
		{#if importSuccess}<p class="success">{importSuccess}</p>{/if}

		{#if csvPreview}
			<div class="preview">
				<h3>Preview ({csvPreview.rows.length} rows)</h3>
				{#if csvPreview.errors.length > 0}
					<div class="preview-errors">
						{#each csvPreview.errors as err}
							<p class="error">{err}</p>
						{/each}
					</div>
				{/if}
				<div class="preview-actions">
					<button class="btn-secondary" onclick={() => (csvPreview = null)}>Cancel</button>
					<button class="btn-primary" onclick={confirmImport}>Import {csvPreview.rows.length} Transactions</button>
				</div>
			</div>
		{/if}
	</section>
</div>

<style>
	.settings-page { max-width: 700px; }
	h1 { margin: 0 0 1.5rem; }
	.settings-section { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
	.settings-section h2 { margin: 0 0 1rem; font-size: 1.1rem; }
	.form-group { margin-bottom: 1rem; }
	.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
	.form-group input { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; box-sizing: border-box; }
	.btn-primary { padding: 0.75rem 1.5rem; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
	.btn-secondary { padding: 0.75rem 1.5rem; background: #ecf0f1; color: #333; border: none; border-radius: 4px; cursor: pointer; }
	.error { color: #e74c3c; margin: 0.5rem 0; }
	.success { color: #2ecc71; margin: 0.5rem 0; }
	.category-form { display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap; }
	.category-form input[type="text"] { flex: 1; min-width: 150px; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; }
	.category-form select { padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; }
	.category-form input[type="color"] { width: 40px; height: 38px; padding: 0; border: 1px solid #ddd; border-radius: 4px; }
	.categories-list h3 { font-size: 0.9rem; color: #666; margin: 1rem 0 0.5rem; }
	.category-item { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0; border-bottom: 1px solid #eee; }
	.color-dot { width: 12px; height: 12px; border-radius: 50%; }
	.name { flex: 1; }
	.badge { font-size: 0.75rem; background: #eee; padding: 0.2rem 0.5rem; border-radius: 4px; color: #666; }
	.btn-icon { padding: 0.25rem 0.5rem; background: none; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; font-size: 0.8rem; }
	.btn-icon.danger { color: #e74c3c; border-color: #e74c3c; }
	.help-text { font-size: 0.9rem; color: #666; margin-bottom: 1rem; }
	.import-form { display: flex; gap: 1rem; align-items: center; }
	.preview { margin-top: 1rem; padding: 1rem; background: #f9f9f9; border-radius: 4px; }
	.preview h3 { margin: 0 0 0.5rem; font-size: 1rem; }
	.preview-actions { display: flex; gap: 1rem; margin-top: 1rem; }
	.currency-form select { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; }
	.exchange-rates { margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #eee; }
	.exchange-rates h3 { margin: 0 0 0.5rem; font-size: 1rem; }
	.rates-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.5rem; margin: 1rem 0; }
	.rate-item { display: flex; justify-content: space-between; padding: 0.5rem; background: #f9f9f9; border-radius: 4px; font-size: 0.9rem; }
	.rate-item .pair { color: #666; }
	.rate-item .rate { font-weight: 500; }
</style>
