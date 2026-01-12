<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import type { MonthlySummary, BudgetStatus, Goal } from '$lib/api/types';

	let summary: MonthlySummary | null = $state(null);
	let budgetStatus: BudgetStatus[] = $state([]);
	let goals: Goal[] = $state([]);
	let loading = $state(true);

	const currentMonth = new Date().toISOString().slice(0, 7);

	onMount(async () => {
		try {
			const [summaryData, budgetData, goalsData] = await Promise.all([
				api.getMonthlySummary(currentMonth),
				api.getBudgetStatus(currentMonth),
				api.getGoals()
			]);
			summary = summaryData;
			budgetStatus = budgetData;
			goals = goalsData;
		} catch (e) {
			console.error('Failed to load dashboard data:', e);
		} finally {
			loading = false;
		}
	});

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount);
	}
</script>

<svelte:head>
	<title>Dashboard | Budget App</title>
</svelte:head>

<div class="dashboard">
	<h1>Dashboard</h1>

	{#if loading}
		<p>Loading...</p>
	{:else}
		<div class="summary-cards">
			<div class="card income">
				<h3>Income</h3>
				<p class="amount">{formatCurrency(summary?.income ?? 0)}</p>
				<span class="period">{currentMonth}</span>
			</div>
			<div class="card expenses">
				<h3>Expenses</h3>
				<p class="amount">{formatCurrency(summary?.expenses ?? 0)}</p>
				<span class="period">{currentMonth}</span>
			</div>
			<div class="card net" class:positive={(summary?.net ?? 0) >= 0}>
				<h3>Net</h3>
				<p class="amount">{formatCurrency(summary?.net ?? 0)}</p>
				<span class="period">{currentMonth}</span>
			</div>
		</div>

		<div class="sections">
			<section class="budget-section">
				<h2>Budget Status</h2>
				{#if budgetStatus.length === 0}
					<p class="empty">No budgets set for this month. <a href="/budgets">Set up budgets</a></p>
				{:else}
					<div class="budget-list">
						{#each budgetStatus as budget}
							<div class="budget-item">
								<div class="budget-header">
									<span class="category-name">{budget.category_name}</span>
									<span class="budget-amounts">
										{formatCurrency(budget.spent)} / {formatCurrency(budget.budgeted)}
									</span>
								</div>
								<div class="progress-bar">
									<div
										class="progress-fill"
										class:over={budget.percentage_used > 100}
										style="width: {Math.min(budget.percentage_used, 100)}%"
									></div>
								</div>
								<span class="percentage">{budget.percentage_used}%</span>
							</div>
						{/each}
					</div>
				{/if}
			</section>

			<section class="goals-section">
				<h2>Savings Goals</h2>
				{#if goals.length === 0}
					<p class="empty">No savings goals. <a href="/goals">Create a goal</a></p>
				{:else}
					<div class="goals-list">
						{#each goals as goal}
							<div class="goal-item">
								<div class="goal-header">
									<span class="goal-name">{goal.name}</span>
									<span class="goal-amounts">
										{formatCurrency(goal.current_amount)} / {formatCurrency(goal.target_amount)}
									</span>
								</div>
								<div class="progress-bar">
									<div
										class="progress-fill goal-progress"
										style="width: {Math.min(goal.progress_percentage, 100)}%"
									></div>
								</div>
								<div class="goal-meta">
									<span>{goal.progress_percentage}%</span>
									<span>{goal.days_remaining} days left</span>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</section>
		</div>
	{/if}
</div>

<style>
	.dashboard {
		max-width: 1200px;
	}

	h1 {
		margin: 0 0 1.5rem;
	}

	.summary-cards {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1rem;
		margin-bottom: 2rem;
	}

	.card {
		background: white;
		padding: 1.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.card h3 {
		margin: 0 0 0.5rem;
		font-size: 0.9rem;
		color: #666;
		text-transform: uppercase;
	}

	.card .amount {
		margin: 0;
		font-size: 1.8rem;
		font-weight: bold;
	}

	.card .period {
		font-size: 0.85rem;
		color: #999;
	}

	.card.income .amount {
		color: #2ecc71;
	}

	.card.expenses .amount {
		color: #e74c3c;
	}

	.card.net .amount {
		color: #e74c3c;
	}

	.card.net.positive .amount {
		color: #2ecc71;
	}

	.sections {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
		gap: 1.5rem;
	}

	section {
		background: white;
		padding: 1.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	section h2 {
		margin: 0 0 1rem;
		font-size: 1.2rem;
	}

	.empty {
		color: #666;
	}

	.empty a {
		color: #3498db;
	}

	.budget-item,
	.goal-item {
		margin-bottom: 1rem;
	}

	.budget-header,
	.goal-header {
		display: flex;
		justify-content: space-between;
		margin-bottom: 0.5rem;
	}

	.category-name,
	.goal-name {
		font-weight: 500;
	}

	.budget-amounts,
	.goal-amounts {
		color: #666;
		font-size: 0.9rem;
	}

	.progress-bar {
		height: 8px;
		background: #eee;
		border-radius: 4px;
		overflow: hidden;
	}

	.progress-fill {
		height: 100%;
		background: #3498db;
		border-radius: 4px;
		transition: width 0.3s;
	}

	.progress-fill.over {
		background: #e74c3c;
	}

	.progress-fill.goal-progress {
		background: #2ecc71;
	}

	.percentage {
		font-size: 0.85rem;
		color: #666;
	}

	.goal-meta {
		display: flex;
		justify-content: space-between;
		font-size: 0.85rem;
		color: #666;
		margin-top: 0.25rem;
	}
</style>
