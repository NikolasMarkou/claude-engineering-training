<script lang="ts">
	import { goto } from '$app/navigation';
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';

	let pin = '';
	let confirmPin = '';
	let error = '';
	let isSetup = false;
	let loading = true;

	onMount(async () => {
		await auth.checkStatus();
		auth.subscribe((state) => {
			isSetup = state.isSetup;
			loading = state.loading;
			if (state.isAuthenticated) {
				goto('/');
			}
		});
	});

	async function handleSubmit() {
		error = '';

		if (!isSetup) {
			if (pin.length < 4) {
				error = 'PIN must be at least 4 characters';
				return;
			}
			if (pin !== confirmPin) {
				error = 'PINs do not match';
				return;
			}
			try {
				await auth.setup(pin);
				goto('/');
			} catch (e) {
				error = e instanceof Error ? e.message : 'Setup failed';
			}
		} else {
			try {
				await auth.login(pin);
				goto('/');
			} catch (e) {
				error = e instanceof Error ? e.message : 'Login failed';
			}
		}
	}
</script>

<svelte:head>
	<title>{isSetup ? 'Login' : 'Setup'} | Budget App</title>
</svelte:head>

<div class="login-container">
	<div class="login-box">
		<h1>{isSetup ? 'Enter PIN' : 'Create PIN'}</h1>
		<p class="subtitle">
			{isSetup ? 'Enter your PIN to access your budget' : 'Create a PIN to protect your budget data'}
		</p>

		{#if loading}
			<p>Loading...</p>
		{:else}
			<form on:submit|preventDefault={handleSubmit}>
				<div class="form-group">
					<label for="pin">PIN</label>
					<input
						type="password"
						id="pin"
						bind:value={pin}
						placeholder="Enter PIN"
						autocomplete="current-password"
					/>
				</div>

				{#if !isSetup}
					<div class="form-group">
						<label for="confirmPin">Confirm PIN</label>
						<input
							type="password"
							id="confirmPin"
							bind:value={confirmPin}
							placeholder="Confirm PIN"
							autocomplete="new-password"
						/>
					</div>
				{/if}

				{#if error}
					<p class="error">{error}</p>
				{/if}

				<button type="submit" class="btn-primary">
					{isSetup ? 'Login' : 'Create PIN'}
				</button>
			</form>
		{/if}
	</div>
</div>

<style>
	.login-container {
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #f5f5f5;
	}

	.login-box {
		background: white;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
		width: 100%;
		max-width: 400px;
	}

	h1 {
		margin: 0 0 0.5rem;
		font-size: 1.5rem;
	}

	.subtitle {
		color: #666;
		margin: 0 0 1.5rem;
	}

	.form-group {
		margin-bottom: 1rem;
	}

	label {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: 500;
	}

	input {
		width: 100%;
		padding: 0.75rem;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 1rem;
		box-sizing: border-box;
	}

	input:focus {
		outline: none;
		border-color: #3498db;
	}

	.error {
		color: #e74c3c;
		margin: 0.5rem 0;
	}

	.btn-primary {
		width: 100%;
		padding: 0.75rem;
		background: #3498db;
		color: white;
		border: none;
		border-radius: 4px;
		font-size: 1rem;
		cursor: pointer;
		margin-top: 1rem;
	}

	.btn-primary:hover {
		background: #2980b9;
	}
</style>
