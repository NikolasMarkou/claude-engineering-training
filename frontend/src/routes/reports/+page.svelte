<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/api/client';
	import type { MonthlySummary, CategoryBreakdown } from '$lib/api/types';
	import { Chart, registerables } from 'chart.js';

	Chart.register(...registerables);

	let trends: MonthlySummary[] = $state([]);
	let breakdown: CategoryBreakdown[] = $state([]);
	let loading = $state(true);
	let currentMonth = $state(new Date().toISOString().slice(0, 7));

	let trendChart: Chart | null = null;
	let breakdownChart: Chart | null = null;
	let trendCanvas: HTMLCanvasElement;
	let breakdownCanvas: HTMLCanvasElement;

	onMount(async () => {
		await loadData();
	});

	async function loadData() {
		loading = true;
		try {
			const [trendsData, breakdownData] = await Promise.all([
				api.getTrends(6),
				api.getCategoryBreakdown(currentMonth)
			]);
			trends = trendsData;
			breakdown = breakdownData;
			renderCharts();
		} catch (e) {
			console.error('Failed to load reports:', e);
		} finally {
			loading = false;
		}
	}

	function renderCharts() {
		// Trend chart
		if (trendChart) trendChart.destroy();
		if (trendCanvas) {
			trendChart = new Chart(trendCanvas, {
				type: 'bar',
				data: {
					labels: trends.map((t) => t.month),
					datasets: [
						{
							label: 'Income',
							data: trends.map((t) => t.income),
							backgroundColor: '#2ecc71'
						},
						{
							label: 'Expenses',
							data: trends.map((t) => t.expenses),
							backgroundColor: '#e74c3c'
						}
					]
				},
				options: {
					responsive: true,
					plugins: {
						legend: { position: 'top' }
					}
				}
			});
		}

		// Breakdown chart
		if (breakdownChart) breakdownChart.destroy();
		const expenseBreakdown = breakdown.filter((b) => b.type === 'expense');
		if (breakdownCanvas && expenseBreakdown.length > 0) {
			breakdownChart = new Chart(breakdownCanvas, {
				type: 'doughnut',
				data: {
					labels: expenseBreakdown.map((b) => b.category_name),
					datasets: [
						{
							data: expenseBreakdown.map((b) => b.total),
							backgroundColor: [
								'#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FF8B94',
								'#9B59B6', '#F39C12', '#E74C3C', '#3498DB', '#95A5A6'
							]
						}
					]
				},
				options: {
					responsive: true,
					plugins: {
						legend: { position: 'right' }
					}
				}
			});
		}
	}

	function formatCurrency(amount: number): string {
		return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
	}

	$effect(() => {
		if (currentMonth && !loading) {
			loadData();
		}
	});
</script>

<svelte:head>
	<title>Reports | Budget App</title>
</svelte:head>

<div class="reports-page">
	<div class="header">
		<h1>Reports</h1>
		<input type="month" bind:value={currentMonth} />
	</div>

	{#if loading}
		<p>Loading...</p>
	{:else}
		<div class="charts-grid">
			<section class="chart-section">
				<h2>Income vs Expenses (6 months)</h2>
				<div class="chart-container">
					<canvas bind:this={trendCanvas}></canvas>
				</div>
			</section>

			<section class="chart-section">
				<h2>Expense Breakdown ({currentMonth})</h2>
				<div class="chart-container">
					{#if breakdown.filter((b) => b.type === 'expense').length === 0}
						<p class="empty">No expenses this month</p>
					{:else}
						<canvas bind:this={breakdownCanvas}></canvas>
					{/if}
				</div>
			</section>
		</div>

		<section class="summary-section">
			<h2>Monthly Summary</h2>
			<table class="summary-table">
				<thead>
					<tr>
						<th>Month</th>
						<th>Income</th>
						<th>Expenses</th>
						<th>Net</th>
					</tr>
				</thead>
				<tbody>
					{#each trends as month}
						<tr>
							<td>{month.month}</td>
							<td class="income">{formatCurrency(month.income)}</td>
							<td class="expense">{formatCurrency(month.expenses)}</td>
							<td class:positive={month.net >= 0} class:negative={month.net < 0}>
								{formatCurrency(month.net)}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</section>
	{/if}
</div>

<style>
	.reports-page { max-width: 1000px; }
	.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
	h1 { margin: 0; }
	.header input { padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; }
	.charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem; }
	.chart-section { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
	.chart-section h2 { margin: 0 0 1rem; font-size: 1.1rem; }
	.chart-container { height: 300px; display: flex; align-items: center; justify-content: center; }
	.summary-section { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
	.summary-section h2 { margin: 0 0 1rem; font-size: 1.1rem; }
	.summary-table { width: 100%; border-collapse: collapse; }
	.summary-table th, .summary-table td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #eee; }
	.summary-table th { font-weight: 600; color: #666; }
	.income { color: #2ecc71; }
	.expense { color: #e74c3c; }
	.positive { color: #2ecc71; font-weight: 600; }
	.negative { color: #e74c3c; font-weight: 600; }
	.empty { color: #666; text-align: center; }
</style>
