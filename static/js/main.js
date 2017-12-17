$(document).ready(function() {
	$(chart_id).highcharts({
		chart: chart,
		title: title,
		subtitle: subtitle,
		xAxis: xAxis,
		yAxis: yAxis,
		series: series
	});
});