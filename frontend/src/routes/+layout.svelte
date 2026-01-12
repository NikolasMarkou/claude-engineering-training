<script lang="ts">
	import { page } from '$app/stores';
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let { children } = $props();

	const navItems = [
		{ href: '/', label: 'Dashboard' },
		{ href: '/transactions', label: 'Transactions' },
		{ href: '/banking', label: 'Banking' },
		{ href: '/budgets', label: 'Budgets' },
		{ href: '/recurring', label: 'Recurring' },
		{ href: '/goals', label: 'Goals' },
		{ href: '/reports', label: 'Reports' },
		{ href: '/settings', label: 'Settings' }
	];

	onMount(async () => {
		await auth.checkStatus();
	});

	function handleLogout() {
		auth.logout();
		goto('/login');
	}

	$effect(() => {
		const unsubscribe = auth.subscribe((state) => {
			if (!state.loading && !state.isAuthenticated && !$page.url.pathname.startsWith('/login')) {
				goto('/login');
			}
		});
		return unsubscribe;
	});
</script>

<svelte:head>
	<title>Budget App</title>
</svelte:head>

{#if $page.url.pathname.startsWith('/login')}
	{@render children()}
{:else if $auth.isAuthenticated}
	<div class="app-layout">
		<nav class="sidebar">
			<div class="logo">
				<h2>Budget</h2>
			</div>
			<ul class="nav-list">
				{#each navItems as item}
					<li>
						<a href={item.href} class:active={$page.url.pathname === item.href}>
							{item.label}
						</a>
					</li>
				{/each}
			</ul>
			<button class="logout-btn" onclick={handleLogout}>Logout</button>
		</nav>
		<main class="main-content">
			{@render children()}
		</main>
	</div>
{:else}
	<div class="loading">Loading...</div>
{/if}

<style>
	:global(body) {
		margin: 0;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
	}

	.app-layout {
		display: flex;
		min-height: 100vh;
	}

	.sidebar {
		width: 220px;
		background: #2c3e50;
		color: white;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		box-sizing: border-box;
	}

	.logo h2 {
		margin: 0 0 2rem;
		font-size: 1.5rem;
	}

	.nav-list {
		list-style: none;
		padding: 0;
		margin: 0;
		flex: 1;
	}

	.nav-list li {
		margin-bottom: 0.5rem;
	}

	.nav-list a {
		display: block;
		padding: 0.75rem 1rem;
		color: #ecf0f1;
		text-decoration: none;
		border-radius: 4px;
		transition: background 0.2s;
	}

	.nav-list a:hover {
		background: #34495e;
	}

	.nav-list a.active {
		background: #3498db;
	}

	.logout-btn {
		padding: 0.75rem 1rem;
		background: #e74c3c;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-size: 1rem;
	}

	.logout-btn:hover {
		background: #c0392b;
	}

	.main-content {
		flex: 1;
		padding: 2rem;
		background: #f5f5f5;
		overflow-y: auto;
	}

	.loading {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		font-size: 1.2rem;
		color: #666;
	}
</style>
