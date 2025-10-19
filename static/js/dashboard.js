// ============================================
// GLOBAL VARIABLES
// ============================================
var revenueLineChart, vehicleBarChart, expensePieChart, areaChart;
var allMonthlyRevenue, allVehicleData, allExpenseData, allContracts;
var currentExpensePieType = "donut";
var currentVehicleSort = "default";
var currentPage = 1;
var itemsPerPage = 5;
var filteredContracts = [];
var currentFilter = "all";

// ============================================
// CONFIGURATION CONSTANTS
// ============================================
const CHART_CONFIG = {
    height: 400,
    animationSpeed: 800,
    strokeWidth: [4, 2],
    markerSize: [6, 0],
    colors: ["#5e72e4", "#f5365c"],
};

const QUARTER_MONTHS = {
    q1: ["Jan", "Feb", "Mar"],
    q2: ["Apr", "May", "Jun"],
    q3: ["Jul", "Aug", "Sep"],
    q4: ["Oct", "Nov", "Dec"],
};

// ============================================
// UTILITY FUNCTIONS
// ============================================
function formatVND(amount) {
    if (amount == null || isNaN(amount)) return "0 ₫";
    return amount.toLocaleString("vi-VN", {
        style: "currency",
        currency: "VND",
    });
}

function formatVNDShort(val) {
    if (val == null || isNaN(val)) return "0 ₫";

    if (val >= 1_000_000_000) {
        return (val / 1_000_000_000).toFixed(1) + "B ₫"; // Billion
    } else if (val >= 1_000_000) {
        return (val / 1_000_000).toFixed(1) + "M ₫"; // Million
    } else if (val >= 1_000) {
        return (val / 1_000).toFixed(1) + "K ₫"; // Thousand
    }
    return val.toLocaleString("vi-VN") + " ₫";
}

function calculateAverage(revenues) {
    return revenues.reduce((a, b) => a + b, 0) / revenues.length;
}

function updateActiveButton(targetButton, parentSelector) {
    const parent = parentSelector
        ? document.querySelector(parentSelector)
        : targetButton?.parentElement;

    if (parent) {
        parent.querySelectorAll("button").forEach((btn) => {
            btn.classList.remove("active");
        });
        if (targetButton && targetButton.tagName === "BUTTON") {
            targetButton.classList.add("active");
        }
    }
}

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener("DOMContentLoaded", function () {
    initializeData();
    populateYearFilter();

    const filteredData = getDataByYearAndQuarter("all");
    updateRevenueStats(filteredData);
    initializeRevenueChart(filteredData);

    initializeVehicleBarChart(allVehicleData);
    initializeExpensePieChart(allExpenseData);
    initializeClaimsChart();
    populateContractsTable(allContracts);

    const searchInput = document.getElementById("contract-search");
    if (searchInput) {
        searchInput.addEventListener("keyup", searchContracts);
    }
});

// ============================================
// DATA INITIALIZATION
// ============================================

function initializeData() {
    // Monthly revenue data for the year
    allMonthlyRevenue = window.allMonthlyRevenue;
    // Vehicle type revenue data
    allVehicleData = window.allVehicleData;

    // Expense data by category
    allExpenseData = window.expenseData;

    // Contract expiration data
    allContracts = window.contractList;
}

// ============================================
// STATS CARD FUNCTIONS
// ============================================

function updateRevenueStats(data) {
    var revenues = data.map((m) => m.revenue);
    var totalRevenue = revenues.reduce((a, b) => a + b, 0);
    var avgRevenue = totalRevenue / revenues.length;

    // Find highest and lowest
    var maxRevenue = Math.max(...revenues);
    var minRevenue = Math.min(...revenues);
    var maxIndex = revenues.indexOf(maxRevenue);
    var minIndex = revenues.indexOf(minRevenue);

    // Calculate growth rate
    var firstMonth = revenues[0];
    var lastMonth = revenues[revenues.length - 1];
    var growthRate = (((lastMonth - firstMonth) / firstMonth) * 100).toFixed(1);

    // Update displays

    document.getElementById("highest-month").textContent =
        data[maxIndex].month + " - $" + maxRevenue.toLocaleString();
    document.getElementById("lowest-month").textContent =
        data[minIndex].month + " - $" + minRevenue.toLocaleString();
    document.getElementById("avg-revenue-display").textContent =
        "$" + Math.round(avgRevenue).toLocaleString();
    document.getElementById("growth-rate").textContent =
        (growthRate > 0 ? "+" : "") + growthRate + "%";
}

// ============================================
// YEAR FILTER FUNCTIONS
// ============================================
function populateYearFilter() {
    const yearFilter = document.getElementById("year-filter");
    if (!yearFilter) return;

    yearFilter.innerHTML = "";

    const years = [...new Set(allMonthlyRevenue.map((item) => item.year))].sort(
        (a, b) => b - a,
    );
    const currentYear = new Date().getFullYear();

    years.forEach((year) => {
        const option = document.createElement("option");
        option.value = year;
        option.textContent = year;
        yearFilter.appendChild(option);
    });

    if (years.includes(currentYear)) {
        yearFilter.value = currentYear;
    } else if (years.length > 0) {
        yearFilter.value = years[0];
    }
}

function getDataByYearAndQuarter(quarter) {
    const selectedYear = document.getElementById("year-filter")?.value;

    let filteredData = allMonthlyRevenue.filter(
        (item) => item.year == selectedYear,
    );

    if (quarter !== "all" && QUARTER_MONTHS[quarter]) {
        const quarterMonthsList = QUARTER_MONTHS[quarter];
        filteredData = filteredData.filter((item) =>
            quarterMonthsList.includes(item.month),
        );
    }

    return filteredData;
}

// ============================================
// REVENUE STATS FUNCTIONS
// ============================================
function updateRevenueStats(data) {
    if (!data || data.length === 0) {
        clearStatsDisplay();
        return;
    }

    var revenues = data.map((m) => m.revenue);
    var avgRevenue = calculateAverage(revenues);

    var maxRevenue = Math.max(...revenues);
    var minRevenue = Math.min(...revenues);
    var maxIndex = revenues.indexOf(maxRevenue);
    var minIndex = revenues.indexOf(minRevenue);

    var firstMonth = revenues[0];
    var lastMonth = revenues[revenues.length - 1];
    var growthRate = (((lastMonth - firstMonth) / firstMonth) * 100).toFixed(1);

    document.getElementById("highest-month").textContent =
        data[maxIndex].month + " - " + formatVNDShort(maxRevenue);
    document.getElementById("lowest-month").textContent =
        data[minIndex].month + " - " + formatVNDShort(minRevenue);
    document.getElementById("avg-revenue-display").textContent = formatVNDShort(
        Math.round(avgRevenue),
    );
    document.getElementById("growth-rate").textContent =
        (growthRate > 0 ? "+" : "") + growthRate + "%";
}

function clearStatsDisplay() {
    const ids = [
        "highest-month",
        "lowest-month",
        "avg-revenue-display",
        "growth-rate",
    ];
    ids.forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.textContent = "-";
    });
}

// ============================================
// REVENUE LINE CHART
// ============================================
function initializeRevenueChart(data) {
    if (!data || data.length === 0) {
        showNoDataMessage("#revenue-line-chart");
        return;
    }

    var months = data.map((m) => m.month);
    var revenues = data.map((m) => m.revenue);
    var avgRevenue = calculateAverage(revenues);
    var avgRevenueArray = new Array(revenues.length).fill(avgRevenue);

    var revenueLineOptions = {
        chart: {
            id: "revenue-chart",
            type: "line",
            height: CHART_CONFIG.height,
            toolbar: { show: false },
            animations: {
                enabled: true,
                speed: CHART_CONFIG.animationSpeed,
                animateGradually: { enabled: true, delay: 150 },
            },
            events: {
                dataPointSelection: function (event, chartContext, config) {
                    var monthData = data[config.dataPointIndex];
                    if (monthData) {
                        alert(
                            "Month: " +
                                monthData.month +
                                " " +
                                monthData.year +
                                "\nRevenue: " +
                                formatVNDShort(monthData.revenue),
                        );
                    }
                },
            },
        },
        stroke: {
            curve: "smooth",
            width: CHART_CONFIG.strokeWidth,
            dashArray: [0, 5],
        },
        series: [
            {
                name: "Monthly Revenue",
                data: revenues,
                type: "line",
            },
            {
                name: "Average Revenue",
                data: avgRevenueArray,
                type: "line",
            },
        ],
        xaxis: {
            categories: months,
            labels: {
                style: {
                    fontSize: "12px",
                    fontWeight: 600,
                },
            },
        },
        yaxis: {
            labels: {
                formatter: formatVNDShort,
            },
        },
        colors: CHART_CONFIG.colors,
        markers: {
            size: CHART_CONFIG.markerSize,
            strokeWidth: 2,
            hover: { size: 9, sizeOffset: 3 },
        },
        grid: {
            borderColor: "#e7e7e7",
            strokeDashArray: 5,
        },
        tooltip: {
            shared: true,
            intersect: false,
            y: {
                formatter: formatVNDShort,
            },
        },
        legend: { show: false },
    };

    if (revenueLineChart) {
        revenueLineChart.destroy();
    }

    revenueLineChart = new ApexCharts(
        document.querySelector("#revenue-line-chart"),
        revenueLineOptions,
    );
    revenueLineChart.render();
}

function updateRevenueChart(period) {
    var data = getDataByYearAndQuarter(period);

    if (data.length === 0) {
        showNoDataMessage("#revenue-line-chart");
        clearStatsDisplay();
        return;
    }

    var months = data.map((m) => m.month);
    var revenues = data.map((m) => m.revenue);
    var avgRevenue = calculateAverage(revenues);
    var avgRevenueArray = new Array(revenues.length).fill(avgRevenue);

    revenueLineChart.updateOptions({
        xaxis: { categories: months },
    });

    revenueLineChart.updateSeries([
        { name: "Monthly Revenue", data: revenues },
        { name: "Average Revenue", data: avgRevenueArray },
    ]);

    updateRevenueStats(data);

    if (event && event.target) {
        updateActiveButton(event.target);
    }
}

function showNoDataMessage(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.innerHTML =
            '<p class="text-center text-muted py-5">No data available for selected period</p>';
    }
}

// ============================================
// VEHICLE BAR CHART
// ============================================

function initializeVehicleBarChart(data) {
    var types = data.map((v) => v.type);
    var revenues = data.map((v) => v.revenue);

    // Update vehicle stats
    var topVehicle = data.reduce((max, v) =>
        v.revenue > max.revenue ? v : max,
    );
    var totalVehicles = data.reduce((sum, v) => sum + v.count, 0);

    document.getElementById("top-vehicle").textContent =
        topVehicle.icon +
        " " +
        topVehicle.type +
        " - " +
        formatVND(topVehicle.revenue);
    document.getElementById("total-vehicles").textContent =
        totalVehicles.toLocaleString();

    // --- Dynamic column width ---
    var count = types.length;
    let columnWidth;
    if (count <= 5) columnWidth = "70%";
    else if (count <= 10) columnWidth = "55%";
    else if (count <= 20) columnWidth = "40%";
    else if (count <= 30) columnWidth = "30%";
    else columnWidth = "20%";

    // --- Dynamic chart height ---
    // Minimum 350px, then add 10px per bar (max around 700px)
    let chartHeight = Math.min(700, 350 + count * 10);

    var vehicleBarOptions = {
        chart: {
            id: "vehicle-bar-chart",
            type: "bar",
            height: chartHeight, // Increased height for better visibility
            toolbar: { show: false },
            animations: {
                enabled: true,
                speed: 800,
                animateGradually: { enabled: true, delay: 150 },
            },
            events: {
                dataPointSelection: function (event, chartContext, config) {
                    var vehicle = allVehicleData[config.dataPointIndex];
                    alert(
                        "Vehicle Type: " +
                            vehicle.type +
                            "\nRevenue: " +
                            formatVND(vehicle.revenue) +
                            "\nCount: " +
                            vehicle.count,
                    );
                },
            },
        },
        plotOptions: {
            bar: {
                borderRadius: 8,
                dataLabels: { position: "top" },
                distributed: true,
                horizontal: false,
                columnWidth: columnWidth, // Wider bars
            },
        },
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                return formatVNDShort(val);
            },
            offsetY: -25,
            style: {
                fontSize: "12px",
                colors: ["#344767"],
                fontWeight: 700,
            },
            background: {
                enabled: false,
            },
        },
        series: [
            {
                name: "Revenue",
                data: revenues,
            },
        ],
        xaxis: {
            categories: types,
            labels: {
                style: {
                    fontSize: "13px",
                    fontWeight: 600,
                    colors: "#344767",
                },
                rotate: 0, // No rotation for better readability
                trim: true,
                hideOverlappingLabels: false,
            },
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false,
            },
        },
        yaxis: {
            labels: {
                formatter: function (val) {
                    return formatVNDShort(val);
                },
                style: {
                    fontSize: "12px",
                    colors: "#8392ab",
                },
            },
            title: {
                text: "Revenue",
                style: {
                    fontSize: "13px",
                    fontWeight: 600,
                    color: "#344767",
                },
            },
        },
        colors: [
            "#5e72e4",
            "#2dce89",
            "#f5365c",
            "#fb6340",
            "#11cdef",
            "#ffd600",
        ],
        tooltip: {
            theme: "light",
            style: {
                fontSize: "13px",
            },
            y: {
                formatter: function (val, { seriesIndex, dataPointIndex, w }) {
                    var vehicle = allVehicleData[dataPointIndex];
                    return formatVND(val) + " (" + vehicle.count + " vehicles)";
                },
            },
            marker: {
                show: true,
            },
        },
        grid: {
            show: true,
            borderColor: "#e9ecef",
            strokeDashArray: 3,
            padding: {
                top: 10,
                right: 20,
                bottom: 10,
                left: 20,
            },
            xaxis: {
                lines: {
                    show: false,
                },
            },
            yaxis: {
                lines: {
                    show: true,
                },
            },
        },
        legend: { show: false },
        states: {
            hover: {
                filter: {
                    type: "darken",
                    value: 0.85,
                },
            },
            active: {
                filter: {
                    type: "darken",
                    value: 0.75,
                },
            },
        },
    };

    if (vehicleBarChart) {
        vehicleBarChart.destroy();
    }

    vehicleBarChart = new ApexCharts(
        document.querySelector("#vehicle-bar-chart"),
        vehicleBarOptions,
    );
    vehicleBarChart.render();
}

function sortVehicleChart(sortType) {
    currentVehicleSort = sortType;
    var sortedData;
    console.log(`allVehicleData: ${JSON.stringify(allVehicleData, null, 4)}`);

    if (sortType === "desc") {
        sortedData = [...allVehicleData].sort((a, b) => b.revenue - a.revenue);
    } else if (sortType === "asc") {
        sortedData = [...allVehicleData].sort((a, b) => a.revenue - b.revenue);
    } else {
        sortedData = allVehicleData;
    }

    var types = sortedData.map((v) => v.type);
    var revenues = sortedData.map((v) => v.revenue);

    // Store the sorted data reference
    window.currentSortedVehicleData = sortedData;

    vehicleBarChart.updateOptions({
        xaxis: { categories: types },
    });

    vehicleBarChart.updateSeries([
        {
            name: "Revenue",
            data: revenues,
        },
    ]);

    // Update button states
    if (event && event.target) {
        event.target.parentElement
            .querySelectorAll("button")
            .forEach((btn) => btn.classList.remove("active"));
        event.target.classList.add("active");
    }
}
// ============================================
// EXPENSE PIE/DONUT CHART
// ============================================

function initializeExpensePieChart(data) {
    var categories = data.map((e) => e.category);
    var amounts = data.map((e) => e.amount);

    // Update expense stats
    var totalExpense = amounts.reduce((a, b) => a + b, 0);
    var highestExpense = data.reduce((max, e) =>
        e.amount > max.amount ? e : max,
    );

    document.getElementById("total-expenses").textContent =
        "$" + totalExpense.toLocaleString();
    document.getElementById("highest-expense").textContent =
        highestExpense.icon + " " + highestExpense.category;

    var expensePieOptions = {
        chart: {
            id: "expense-pie-chart",
            type: currentExpensePieType,
            height: 450,
            toolbar: { show: false },
            animations: {
                enabled: true,
                speed: 800,
                dynamicAnimation: {
                    enabled: true,
                    speed: 350,
                },
            },
            events: {
                dataPointSelection: function (event, chartContext, config) {
                    var expense = allExpenseData[config.dataPointIndex];
                    alert(
                        "Category: " +
                            expense.category +
                            "\nAmount: $" +
                            expense.amount.toLocaleString(),
                    );
                },
            },
        },
        series: amounts,
        labels: categories,
        colors: [
            "#f5365c",
            "#fb6340",
            "#ffd600",
            "#2dce89",
            "#11cdef",
            "#5e72e4",
            "#8965e0",
        ],
        legend: {
            position: "bottom",
            fontSize: "12px",
            fontWeight: 500,
            offsetY: 0,
            markers: {
                width: 12,
                height: 12,
                radius: 12,
            },
            itemMargin: {
                horizontal: 8,
                vertical: 4,
            },
        },
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                return val.toFixed(1) + "%";
            },
            style: {
                fontSize: "11px",
                fontWeight: 600,
                colors: ["#fff"],
            },
            dropShadow: {
                enabled: false,
            },
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return "$" + val.toLocaleString();
                },
            },
        },
        plotOptions: {
            pie: {
                donut: {
                    size: "65%",
                    labels: {
                        show: true,
                        name: {
                            show: true,
                            fontSize: "14px",
                            fontWeight: 600,
                            offsetY: -10,
                        },
                        value: {
                            show: true,
                            fontSize: "20px",
                            fontWeight: 700,
                            offsetY: 5,
                            formatter: function (val) {
                                return "$" + (val / 1000).toFixed(0) + "K";
                            },
                        },
                        total: {
                            show: true,
                            label: "Total Expenses",
                            fontSize: "14px",
                            fontWeight: 600,
                            color: "#373d3f",
                            formatter: function (w) {
                                return (
                                    "$" +
                                    (
                                        w.globals.seriesTotals.reduce(
                                            (a, b) => a + b,
                                            0,
                                        ) / 1000
                                    ).toFixed(0) +
                                    "K"
                                );
                            },
                        },
                    },
                },
                expandOnClick: true,
            },
        },
        stroke: {
            width: 2,
            colors: ["#fff"],
        },
        responsive: [
            {
                breakpoint: 480,
                options: {
                    chart: {
                        height: 300,
                    },
                    legend: {
                        position: "bottom",
                        fontSize: "10px",
                    },
                },
            },
        ],
    };

    expensePieChart = new ApexCharts(
        document.querySelector("#expense-pie-chart"),
        expensePieOptions,
    );
    expensePieChart.render();
}

function changeExpensePieType(type) {
    currentExpensePieType = type;
    expensePieChart.destroy();
    initializeExpensePieChart(allExpenseData);

    // Update button states
    event.target.parentElement
        .querySelectorAll("button")
        .forEach((btn, idx) => {
            btn.classList.remove("active");
            if (
                (type === "donut" && idx === 0) ||
                (type === "pie" && idx === 1)
            ) {
                btn.classList.add("active");
            }
        });
}

// ============================================
// CLAIMS DUAL LINE CHART
// ============================================

function populateClaimsYearFilter() {
    const select = document.getElementById("claims-year-filter");
    if (!select) return;

    select.innerHTML = "";

    const years = [
        ...new Set(window.allClaimsData.map((item) => item.year)),
    ].sort((a, b) => b - a);

    if (years.length === 0) {
        const currentYear = new Date().getFullYear();
        select.innerHTML = `<option value="${currentYear}">${currentYear}</option>`;
    } else {
        years.forEach((year) => {
            const opt = document.createElement("option");
            opt.value = year;
            opt.textContent = year;
            select.appendChild(opt);
        });
    }

    select.addEventListener("change", function () {
        updateClaimsChartByYear(this.value);
    });
}

function initializeClaimsChart() {
    populateClaimsYearFilter();
}

function updateClaimsChartByYear(year) {
    if (!window.allClaimsData || window.allClaimsData.length === 0) {
        showNoDataMessage("#area-chart");
        return;
    }

    // Filter claims data by selected year
    const yearData = window.allClaimsData.filter((item) => item.year == year);

    if (yearData.length === 0) {
        showNoDataMessage("#area-chart");
        clearClaimsStats();
        return;
    }

    var months = yearData.map((m) => m.month);
    var personalCompensation = yearData.map(
        (m) => m.personal_compensation || 0,
    );
    var propertyCompensation = yearData.map(
        (m) => m.property_compensation || 0,
    );

    // Calculate averages
    var avgPersonal = calculateAverage(personalCompensation);
    var avgProperty = calculateAverage(propertyCompensation);
    var avgPersonalArray = new Array(personalCompensation.length).fill(
        avgPersonal,
    );
    var avgPropertyArray = new Array(propertyCompensation.length).fill(
        avgProperty,
    );

    var claimsOptions = {
        chart: {
            id: "claims-chart",
            type: "line",
            height: 350,
            toolbar: { show: false },
            animations: {
                enabled: true,
                speed: 800,
                animateGradually: { enabled: true, delay: 150 },
            },
            zoom: {
                enabled: true,
                type: "x",
                autoScaleYaxis: true,
            },
            events: {
                dataPointSelection: function (event, chartContext, config) {
                    var claimData = yearData[config.dataPointIndex];
                    if (claimData) {
                        const seriesName =
                            config.w.config.series[config.seriesIndex].name;
                        const value =
                            config.w.config.series[config.seriesIndex].data[
                                config.dataPointIndex
                            ];
                        alert(
                            "Month: " +
                                claimData.month +
                                " " +
                                claimData.year +
                                "\n" +
                                seriesName +
                                ": " +
                                formatVND(value),
                        );
                    }
                },
            },
        },
        stroke: {
            curve: "smooth",
            width: [3, 3, 2, 2],
            dashArray: [0, 0, 5, 5],
        },
        series: [
            {
                name: "Personal Compensation",
                data: personalCompensation,
                color: "#f5365c",
            },
            {
                name: "Property Compensation",
                data: propertyCompensation,
                color: "#11cdef",
            },
            {
                name: "Avg Personal",
                data: avgPersonalArray,
                color: "#f5365c",
            },
            {
                name: "Avg Property",
                data: avgPropertyArray,
                color: "#11cdef",
            },
        ],
        xaxis: {
            categories: months,
            labels: {
                style: {
                    fontSize: "12px",
                    fontWeight: 600,
                    colors: "#344767",
                },
            },
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false,
            },
        },
        yaxis: {
            labels: {
                formatter: formatVNDShort,
                style: {
                    fontSize: "12px",
                    colors: "#8392ab",
                },
            },
            title: {
                text: "Compensation Amount",
                style: {
                    fontSize: "13px",
                    fontWeight: 600,
                    color: "#344767",
                },
            },
        },
        markers: {
            size: [5, 5, 0, 0],
            strokeWidth: 2,
            hover: {
                size: 7,
                sizeOffset: 3,
            },
        },
        tooltip: {
            shared: true,
            intersect: false,
            y: {
                formatter: formatVND,
            },
        },
        legend: {
            show: true,
            position: "top",
            horizontalAlign: "right",
            fontSize: "13px",
            fontWeight: 600,
            markers: {
                width: 12,
                height: 12,
                radius: 12,
            },
            itemMargin: {
                horizontal: 10,
                vertical: 5,
            },
        },
        grid: {
            show: true,
            borderColor: "#e9ecef",
            strokeDashArray: 3,
            xaxis: {
                lines: {
                    show: false,
                },
            },
            yaxis: {
                lines: {
                    show: true,
                },
            },
        },
        dataLabels: {
            enabled: false,
        },
    };

    if (areaChart) {
        areaChart.destroy();
    }

    areaChart = new ApexCharts(
        document.querySelector("#area-chart"),
        claimsOptions,
    );
    areaChart.render();

    // Update claims stats
    updateClaimsStats(personalCompensation, propertyCompensation);
}

function updateClaimsStats(personalComp, propertyComp) {
    const totalPersonal = personalComp.reduce((a, b) => a + b, 0);
    const totalProperty = propertyComp.reduce((a, b) => a + b, 0);
    const totalClaims = totalPersonal + totalProperty;

    const personalPercentage =
        totalClaims > 0 ? ((totalPersonal / totalClaims) * 100).toFixed(1) : 0;
    const propertyPercentage =
        totalClaims > 0 ? ((totalProperty / totalClaims) * 100).toFixed(1) : 0;

    const totalClaimsEl = document.getElementById("total-claims-amount");
    const personalEl = document.getElementById("personal-claims");
    const propertyEl = document.getElementById("property-claims");

    if (totalClaimsEl) {
        totalClaimsEl.textContent = formatVNDShort(totalClaims);
    }

    if (personalEl) {
        personalEl.textContent =
            formatVNDShort(totalPersonal) + ` (${personalPercentage}%)`;
    }

    if (propertyEl) {
        propertyEl.textContent =
            formatVNDShort(totalProperty) + ` (${propertyPercentage}%)`;
    }
}

function clearClaimsStats() {
    const ids = ["total-claims-amount", "personal-claims", "property-claims"];
    ids.forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.textContent = "-";
    });
}

function resetAreaZoom() {
    if (areaChart) {
        areaChart.resetSeries();
    }
}

// ============================================
// CONTRACT TABLE WITH PAGINATION
// ============================================

var currentPage = 1;
var itemsPerPage = 10;
var filteredContracts = [];
var currentFilter = "all";
var expiredSoonDay = 45;

function populateContractsTable(contracts) {
    filteredContracts = contracts;
    currentPage = 1;
    renderContractsTable();
}

function renderContractsTable() {
    var tableBody = document.querySelector("#contracts-list");
    tableBody.innerHTML = "";

    // Calculate pagination
    var totalPages = Math.ceil(filteredContracts.length / itemsPerPage);
    var startIndex = (currentPage - 1) * itemsPerPage;
    var endIndex = Math.min(
        startIndex + itemsPerPage,
        filteredContracts.length,
    );
    var paginatedContracts = filteredContracts.slice(startIndex, endIndex);

    // Update showing text
    document.getElementById("showing-start").textContent =
        filteredContracts.length > 0 ? startIndex + 1 : 0;
    document.getElementById("showing-end").textContent = endIndex;
    document.getElementById("total-contracts").textContent =
        filteredContracts.length;

    // Render rows
    if (paginatedContracts.length === 0) {
        tableBody.innerHTML = `
      <tr>
        <td colspan="7" class="text-center py-4">
          <div class="text-secondary">
            <i class="fa fa-inbox fa-3x mb-3 opacity-3"></i>
            <p class="mb-0">No contracts found</p>
          </div>
        </td>
      </tr>
    `;
    } else {
        paginatedContracts.forEach(function (contract) {
            var daysRemaining = contract.daysRemaining;
            var statusBadge = "";
            var statusClass = "";
            var daysText = "";

            // Determine status based on days remaining
            if (daysRemaining < 0) {
                statusBadge =
                    '<span class="badge badge-sm bg-gradient-danger">Expired</span>';
                statusClass = "expired";
                daysText =
                    '<span class="text-danger text-xs font-weight-bold">' +
                    Math.abs(daysRemaining) +
                    " days ago</span>";
            } else if (daysRemaining <= expiredSoonDay) {
                statusBadge =
                    '<span class="badge badge-sm bg-gradient-warning">Expiring Soon</span>';
                statusClass = "expiring";
                daysText =
                    '<span class="text-warning text-xs font-weight-bold">' +
                    daysRemaining +
                    " days</span>";
            } else {
                statusBadge =
                    '<span class="badge badge-sm bg-gradient-success">Active</span>';
                statusClass = "active";
                daysText =
                    '<span class="text-success text-xs font-weight-bold">' +
                    daysRemaining +
                    " days</span>";
            }

            // Format expiration date
            var expDate = new Date(contract.expirationDate);
            var formattedDate = expDate.toLocaleDateString("en-US", {
                year: "numeric",
                month: "short",
                day: "numeric",
            });

            var row = `
        <tr data-status="${statusClass}" class="contract-row">
          <td>
            <div class="d-flex px-3 py-1">
              <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-xs font-weight-bold">${
                    contract.contractNo
                }</h6>
              </div>
            </div>
          </td>
          <td>
            <div class="d-flex px-2 py-1">
              <div>
                <div class="avatar avatar-sm me-3 bg-gradient-primary">
                  <span class="text-white text-xs">${contract.customerName.charAt(
                      0,
                  )}</span>
                </div>
              </div>
              <div class="d-flex flex-column justify-content-center">
                <h6 class="mb-0 text-sm">${contract.customerName}</h6>
              </div>
            </div>
          </td>
          <td>
            <p class="text-xs font-weight-bold mb-0">${contract.vehicleName}</p>
          </td>
          <td>
            <p class="text-xs font-weight-bold mb-0">${
                contract.insuranceCategory
            }</p>
          </td>
          <td class="align-middle text-center">
            <span class="text-secondary text-xs font-weight-bold">${formattedDate}</span>
          </td>
          <td class="align-middle text-center">
            ${daysText}
          </td>
          <td class="align-middle text-center">
            ${statusBadge}
          </td>
        </tr>
      `;
            tableBody.innerHTML += row;
        });
    }

    // Render pagination
    renderPagination(totalPages);
}

function renderPagination(totalPages) {
    var paginationControls = document.getElementById("pagination-controls");
    paginationControls.innerHTML = "";

    if (totalPages <= 1) {
        return;
    }

    // Previous button
    var prevDisabled = currentPage === 1 ? "disabled" : "";
    paginationControls.innerHTML += `
    <li class="page-item ${prevDisabled}">
      <a class="page-link" href="javascript:;" onclick="changePage(${
          currentPage - 1
      })" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
  `;

    // Page numbers
    var startPage = Math.max(1, currentPage - 2);
    var endPage = Math.min(totalPages, currentPage + 2);

    // First page
    if (startPage > 1) {
        paginationControls.innerHTML += `
      <li class="page-item">
        <a class="page-link" href="javascript:;" onclick="changePage(1)">1</a>
      </li>
    `;
        if (startPage > 2) {
            paginationControls.innerHTML += `
        <li class="page-item disabled">
          <a class="page-link" href="javascript:;">...</a>
        </li>
      `;
        }
    }

    // Page numbers in range
    for (var i = startPage; i <= endPage; i++) {
        var activeClass = i === currentPage ? "active" : "";
        paginationControls.innerHTML += `
      <li class="page-item ${activeClass}">
        <a class="page-link" href="javascript:;" onclick="changePage(${i})">${i}</a>
      </li>
    `;
    }

    // Last page
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            paginationControls.innerHTML += `
        <li class="page-item disabled">
          <a class="page-link" href="javascript:;">...</a>
        </li>
      `;
        }
        paginationControls.innerHTML += `
      <li class="page-item">
        <a class="page-link" href="javascript:;" onclick="changePage(${totalPages})">${totalPages}</a>
      </li>
    `;
    }

    // Next button
    var nextDisabled = currentPage === totalPages ? "disabled" : "";
    paginationControls.innerHTML += `
    <li class="page-item ${nextDisabled}">
      <a class="page-link" href="javascript:;" onclick="changePage(${
          currentPage + 1
      })" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  `;
}

function changePage(page) {
    var totalPages = Math.ceil(filteredContracts.length / itemsPerPage);
    if (page < 1 || page > totalPages) {
        return;
    }
    currentPage = page;
    renderContractsTable();
}

function filterContracts(status) {
    currentFilter = status;
    currentPage = 1;

    if (status === "all") {
        filteredContracts = allContracts;
    } else {
        filteredContracts = allContracts.filter((contract) => {
            var daysRemaining = contract.daysRemaining;
            if (status === "expired") {
                return daysRemaining < 0;
            } else if (status === "expiring") {
                return daysRemaining >= 0 && daysRemaining <= expiredSoonDay;
            } else if (status === "active") {
                return daysRemaining > expiredSoonDay;
            }
            return true;
        });
    }

    // Apply search if there's a search term
    var searchTerm = document.getElementById("contract-search").value;
    if (searchTerm) {
        applySearch(searchTerm);
    } else {
        renderContractsTable();
    }

    // Update button states
    event.target.parentElement
        .querySelectorAll("button")
        .forEach((btn) => btn.classList.remove("active"));
    event.target.classList.add("active");
}

function searchContracts() {
    var searchTerm = document
        .getElementById("contract-search")
        .value.toLowerCase()
        .trim();
    currentPage = 1;
    console.log("Searching for:", searchTerm);

    if (searchTerm === "") {
        // Reset to current filter
        filterContracts(currentFilter);
        // Restore active button state
        var buttons = document.querySelectorAll(".btn-group button");
        buttons.forEach((btn, idx) => {
            btn.classList.remove("active");
            if (
                (currentFilter === "all" && idx === 0) ||
                (currentFilter === "expired" && idx === 1) ||
                (currentFilter === "expiring" && idx === 2) ||
                (currentFilter === "active" && idx === 3)
            ) {
                btn.classList.add("active");
            }
        });
        return;
    }

    applySearch(searchTerm);
}

function applySearch(searchTerm) {
    // Get base filtered contracts based on current filter
    var baseContracts;
    if (currentFilter === "all") {
        baseContracts = allContracts;
    } else {
        baseContracts = allContracts.filter((contract) => {
            var daysRemaining = contract.daysRemaining;
            if (currentFilter === "expired") {
                return daysRemaining < 0;
            } else if (currentFilter === "expiring") {
                return daysRemaining >= 0 && daysRemaining <= expiredSoonDay;
            } else if (currentFilter === "active") {
                return daysRemaining > expiredSoonDay;
            }
            return true;
        });
    }

    // Apply search filter
    filteredContracts = baseContracts.filter((contract) =>
        contract.contractNo.toLowerCase().includes(searchTerm),
    );

    renderContractsTable();
}
