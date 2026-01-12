<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import type { Goal } from '$lib/api/types';

	let goals: Goal[] = $state([]);
	let loading = $state(true);
	let showForm = $state(false);
	let showContribute = $state<number | null>(null);

	let formData = $state({ name: '', target_amount: 0, deadline: '' });
	let contributeAmount = $state(0);

	onMount(loadGoals);

	async function loadGoals() {
		loading = true;
		try {
			goals = await api.getGoals();
		} catch (e) {
			console.error('Failed to load goals:', e);
		} finally {
			loading = false;
		}
	}

	async function handleSubmit() {
		try {
			await api.createGoal(formData);
			showForm = false;
			formData = { name: '', target_amount: 0, deadline: '' };
			await loadGoals();
		} catch (e) {
			console.error('Failed to create goal:', e);
		}
	}

	async function handleContribute(goalId: number) {
		try {
			await api.contributeToGoal(goalId, contributeAmount);
			showContribute = null;
			contributeAmount = 0;
			await loadGoals();
		} catch (e) {
			console.error('Failed to contribute:', e);
		}
	}

	async function handleDelete(id: number) {
		if (confirm('Delete this goal?')) {
			try {
				await api.deleteGoal(id);
				await loadGoals();
			} catch (e) {
				console.error('Failed to delete goal:', e);
			}
		}
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
	}
</script>

<svelte:head>
	<title>Goals | Budget App</title>
</svelte:head>

<div class="goals-page">
	<div class="header">
		<h1>Savings Goals</h1>
		<button class="btn-primary" onclick={() => (showForm = true)}>New Goal</button>
	</div>

	{#if showForm}
		<div class="modal-overlay" onclick={() => (showForm = false)}>
			<div class="modal" onclick={(e) => e.stopPropagation()}>
				<h2>Create Goal</h2>
				<form onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
					<div class="form-group">
						<label for="name">Goal Name</label>
						<input type="text" id="name" bind:value={formData.name} required placeholder="e.g., Emergency Fund" />
					</div>
					<div class="form-group">
						<label for="target">Target Amount</label>
						<input type="number" id="target" bind:value={formData.target_amount} step="0.01" min="0" required />
					</div>
					<div class="form-group">
						<label for="deadline">Deadline</label>
						<input type="date" id="deadline" bind:value={formData.deadline} required />
					</div>
					<div class="form-actions">
						<button type="button" class="btn-secondary" onclick={() => (showForm = false)}>Cancel</button>
						<button type="submit" class="btn-primary">Create Goal</button>
					</div>
				</form>
			</div>
		</div>
	{/if}

	{#if showContribute !== null}
		<div class="modal-overlay" onclick={() => (showContribute = null)}>
			<div class="modal" onclick={(e) => e.stopPropagation()}>
				<h2>Add to Goal</h2>
				<form onsubmit={(e) => { e.preventDefault(); handleContribute(showContribute!); }}>
					<div class="form-group">
						<label for="contribute">Amount to Add</label>
						<input type="number" id="contribute" bind:value={contributeAmount} step="0.01" min="0" required />
					</div>
					<div class="form-actions">
						<button type="button" class="btn-secondary" onclick={() => (showContribute = null)}>Cancel</button>
						<button type="submit" class="btn-primary">Add</button>
					</div>
				</form>
			</div>
		</div>
	{/if}

	{#if loading}
		<p>Loading...</p>
	{:else if goals.length === 0}
		<p class="empty">No savings goals yet. Create one to start tracking!</p>
	{:else}
		<div class="goals-list">
			{#each goals as goal}
				<div class="goal-card">
					<div class="goal-header">
						<h3>{goal.name}</h3>
						<button class="btn-icon danger" onclick={() => handleDelete(goal.id)}>Delete</button>
					</div>
					<div class="goal-amounts">
						<span class="current">{formatCurrency(goal.current_amount)}</span>
						<span class="separator">/</span>
						<span class="target">{formatCurrency(goal.target_amount)}</span>
					</div>
					<div class="progress-bar">
						<div class="progress-fill" style="width: {Math.min(goal.progress_percentage, 100)}%"></div>
					</div>
					<div class="goal-footer">
						<span class="percentage">{goal.progress_percentage}%</span>
						<span class="days">{goal.days_remaining} days left</span>
					</div>
					<button class="btn-contribute" onclick={() => (showContribute = goal.id)}>+ Add Money</button>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.goals-page { max-width: 900px; }
	.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
	h1 { margin: 0; }
	.btn-primary { padding: 0.75rem 1.5rem; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
	.btn-primary:hover { background: #2980b9; }
	.btn-secondary { padding: 0.75rem 1.5rem; background: #ecf0f1; color: #333; border: none; border-radius: 4px; cursor: pointer; }
	.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
	.modal { background: white; padding: 2rem; border-radius: 8px; width: 100%; max-width: 400px; }
	.modal h2 { margin: 0 0 1.5rem; }
	.form-group { margin-bottom: 1rem; }
	.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
	.form-group input { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; box-sizing: border-box; }
	.form-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; }
	.goals-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
	.goal-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
	.goal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
	.goal-header h3 { margin: 0; font-size: 1.1rem; }
	.goal-amounts { font-size: 1.5rem; margin-bottom: 0.75rem; }
	.current { font-weight: bold; color: #2ecc71; }
	.separator { color: #999; margin: 0 0.25rem; }
	.target { color: #666; }
	.progress-bar { height: 10px; background: #eee; border-radius: 5px; overflow: hidden; margin-bottom: 0.75rem; }
	.progress-fill { height: 100%; background: #2ecc71; border-radius: 5px; transition: width 0.3s; }
	.goal-footer { display: flex; justify-content: space-between; font-size: 0.9rem; color: #666; margin-bottom: 1rem; }
	.btn-contribute { width: 100%; padding: 0.75rem; background: #2ecc71; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }
	.btn-contribute:hover { background: #27ae60; }
	.btn-icon { padding: 0.25rem 0.5rem; background: none; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; font-size: 0.8rem; }
	.btn-icon.danger { color: #e74c3c; border-color: #e74c3c; }
	.empty { text-align: center; color: #666; padding: 3rem; background: white; border-radius: 8px; }
</style>
