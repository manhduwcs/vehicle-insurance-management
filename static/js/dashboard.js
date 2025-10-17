// Global variables for charts
var revenueLineChart, vehicleBarChart, expensePieChart, areaChart;
var allMonthlyRevenue, allVehicleData, allExpenseData, allContracts;
var currentExpensePieType = "donut";
var currentVehicleSort = "default";

document.addEventListener("DOMContentLoaded", function () {
  // Initialize sample data
  initializeData();

  // Initialize all components
  updateRevenueStats(allMonthlyRevenue);
  initializeRevenueChart(allMonthlyRevenue);
  initializeVehicleBarChart(allVehicleData);
  initializeExpensePieChart(allExpenseData);
  initializeAreaChart();
  populateContractsTable(allContracts);
  const searchInput = document.getElementById("contract-search");
  searchInput.addEventListener("keyup", searchContracts);
});

// ============================================
// DATA INITIALIZATION
// ============================================

function initializeData() {
  // Monthly revenue data for the year
  allMonthlyRevenue = [
    { month: "Jan", revenue: 45000 },
    { month: "Feb", revenue: 52000 },
    { month: "Mar", revenue: 48000 },
    { month: "Apr", revenue: 61000 },
    { month: "May", revenue: 55000 },
    { month: "Jun", revenue: 67000 },
    { month: "Jul", revenue: 72000 },
    { month: "Aug", revenue: 58000 },
    { month: "Sep", revenue: 63000 },
    { month: "Oct", revenue: 70000 },
    { month: "Nov", revenue: 68000 },
    { month: "Dec", revenue: 75000 },
  ];

  // Vehicle type revenue data
  allVehicleData = [
    { type: "Sedan", revenue: 125000, count: 450, icon: "🚗" },
    { type: "SUV", revenue: 185000, count: 320, icon: "🚙" },
    { type: "Truck", revenue: 95000, count: 180, icon: "🚚" },
    { type: "Van", revenue: 78000, count: 145, icon: "🚐" },
    { type: "Motorcycle", revenue: 45000, count: 280, icon: "🏍️" },
    { type: "Electric", revenue: 152000, count: 210, icon: "⚡" },
  ];

  // Expense data by category
  allExpenseData = window.expenseData;

  // Contract expiration data
  allContracts = [
    {
      contractNo: "CNT-2024-001",
      customerName: "John Smith",
      vehicleName: "Toyota Camry 2022",
      insuranceCategory: "Comprehensive",
      expirationDate: "2024-11-20",
      daysRemaining: -25,
    },
    {
      contractNo: "CNT-2024-002",
      customerName: "Sarah Johnson",
      vehicleName: "Honda CR-V 2023",
      insuranceCategory: "Third Party",
      expirationDate: "2024-12-05",
      daysRemaining: -10,
    },
    {
      contractNo: "CNT-2024-003",
      customerName: "Michael Brown",
      vehicleName: "Ford F-150 2021",
      insuranceCategory: "Comprehensive",
      expirationDate: "2024-12-18",
      daysRemaining: 3,
    },
    {
      contractNo: "CNT-2024-004",
      customerName: "Emily Davis",
      vehicleName: "Tesla Model 3 2024",
      insuranceCategory: "Premium",
      expirationDate: "2024-12-25",
      daysRemaining: 10,
    },
    {
      contractNo: "CNT-2024-005",
      customerName: "David Wilson",
      vehicleName: "BMW X5 2023",
      insuranceCategory: "Comprehensive",
      expirationDate: "2025-01-10",
      daysRemaining: 26,
    },
    {
      contractNo: "CNT-2024-006",
      customerName: "Lisa Anderson",
      vehicleName: "Mercedes C-Class 2022",
      insuranceCategory: "Premium",
      expirationDate: "2025-01-15",
      daysRemaining: 31,
    },
    {
      contractNo: "CNT-2024-007",
      customerName: "James Martinez",
      vehicleName: "Chevrolet Silverado 2023",
      insuranceCategory: "Third Party",
      expirationDate: "2025-02-20",
      daysRemaining: 67,
    },
    {
      contractNo: "CNT-2024-008",
      customerName: "Maria Garcia",
      vehicleName: "Nissan Altima 2021",
      insuranceCategory: "Comprehensive",
      expirationDate: "2025-03-05",
      daysRemaining: 80,
    },
    {
      contractNo: "CNT-2024-009",
      customerName: "Robert Taylor",
      vehicleName: "Audi A4 2024",
      insuranceCategory: "Premium",
      expirationDate: "2025-04-12",
      daysRemaining: 118,
    },
    {
      contractNo: "CNT-2024-010",
      customerName: "Jennifer Lee",
      vehicleName: "Hyundai Tucson 2023",
      insuranceCategory: "Third Party",
      expirationDate: "2025-05-01",
      daysRemaining: 137,
    },
  ];
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
  document.getElementById("total-revenue").textContent =
    "$" + totalRevenue.toLocaleString();
  document.getElementById("highest-month").textContent =
    data[maxIndex].month + " - $" + maxRevenue.toLocaleString();
  document.getElementById("lowest-month").textContent =
    data[minIndex].month + " - $" + minRevenue.toLocaleString();
  document.getElementById("avg-revenue-display").textContent =
    "$" + Math.round(avgRevenue).toLocaleString();
  document.getElementById("growth-rate").textContent =
    (growthRate > 0 ? "+" : "") + growthRate + "%";

  document.getElementById("total-users").textContent = "2,543";
  document.getElementById("total-contracts").textContent = "156";
  document.getElementById("total-claims").textContent = "89";
}

// ============================================
// REVENUE LINE CHART
// ============================================

function initializeRevenueChart(data) {
  var months = data.map((m) => m.month);
  var revenues = data.map((m) => m.revenue);
  var avgRevenue = revenues.reduce((a, b) => a + b, 0) / revenues.length;
  var avgRevenueArray = new Array(revenues.length).fill(avgRevenue);

  var revenueLineOptions = {
    chart: {
      id: "revenue-chart",
      type: "line",
      height: 400,
      toolbar: { show: false },
      animations: {
        enabled: true,
        speed: 800,
        animateGradually: { enabled: true, delay: 150 },
      },
      events: {
        dataPointSelection: function (event, chartContext, config) {
          var monthData = allMonthlyRevenue[config.dataPointIndex];
          alert(
            "Month: " +
              monthData.month +
              "\nRevenue: $" +
              monthData.revenue.toLocaleString()
          );
        },
      },
    },
    stroke: {
      curve: "smooth",
      width: [4, 2],
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
        formatter: function (val) {
          return "$" + (val / 1000).toFixed(0) + "K";
        },
      },
    },
    colors: ["#5e72e4", "#f5365c"],
    markers: {
      size: [6, 0],
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
        formatter: function (val) {
          return "$" + val.toLocaleString();
        },
      },
    },
    legend: { show: false },
  };

  revenueLineChart = new ApexCharts(
    document.querySelector("#revenue-line-chart"),
    revenueLineOptions
  );
  revenueLineChart.render();
}

function updateRevenueChart(period) {
  var data;
  if (period === "q1") data = allMonthlyRevenue.slice(0, 3);
  else if (period === "q2") data = allMonthlyRevenue.slice(3, 6);
  else if (period === "q3") data = allMonthlyRevenue.slice(6, 9);
  else if (period === "q4") data = allMonthlyRevenue.slice(9, 12);
  else data = allMonthlyRevenue;

  var months = data.map((m) => m.month);
  var revenues = data.map((m) => m.revenue);
  var avgRevenue = revenues.reduce((a, b) => a + b, 0) / revenues.length;
  var avgRevenueArray = new Array(revenues.length).fill(avgRevenue);

  revenueLineChart.updateOptions({
    xaxis: { categories: months },
  });

  revenueLineChart.updateSeries([
    { name: "Monthly Revenue", data: revenues },
    { name: "Average Revenue", data: avgRevenueArray },
  ]);

  updateRevenueStats(data);

  // Update button states
  document
    .querySelectorAll(".btn-group button")
    .forEach((btn) => btn.classList.remove("active"));
  event.target.classList.add("active");
}

// ============================================
// VEHICLE BAR CHART
// ============================================

function initializeVehicleBarChart(data) {
  var types = data.map((v) => v.type);
  var revenues = data.map((v) => v.revenue);

  // Update vehicle stats
  var topVehicle = data.reduce((max, v) => (v.revenue > max.revenue ? v : max));
  var totalVehicles = data.reduce((sum, v) => sum + v.count, 0);

  document.getElementById("top-vehicle").textContent =
    topVehicle.icon +
    " " +
    topVehicle.type +
    " - $" +
    topVehicle.revenue.toLocaleString();
  document.getElementById("total-vehicles").textContent =
    totalVehicles.toLocaleString();

  var vehicleBarOptions = {
    chart: {
      id: "vehicle-bar-chart",
      type: "bar",
      height: 350,
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
              "\nRevenue: $" +
              vehicle.revenue.toLocaleString() +
              "\nCount: " +
              vehicle.count
          );
        },
      },
    },
    plotOptions: {
      bar: {
        borderRadius: 10,
        dataLabels: { position: "top" },
        distributed: true,
        horizontal: false,
        columnWidth: "60%",
      },
    },
    dataLabels: {
      enabled: true,
      formatter: function (val) {
        return "$" + (val / 1000).toFixed(0) + "K";
      },
      offsetY: -25,
      style: {
        fontSize: "11px",
        colors: ["#304758"],
        fontWeight: 600,
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
          fontSize: "12px",
          fontWeight: 600,
        },
        rotate: -45,
        rotateAlways: false,
      },
    },
    yaxis: {
      labels: {
        formatter: function (val) {
          return "$" + (val / 1000).toFixed(0) + "K";
        },
        style: { fontSize: "11px" },
      },
      title: {
        text: "Revenue (USD)",
        style: { fontSize: "12px", fontWeight: 600 },
      },
    },
    colors: ["#5e72e4", "#2dce89", "#f5365c", "#fb6340", "#11cdef", "#ffd600"],
    tooltip: {
      y: {
        formatter: function (val, { seriesIndex, dataPointIndex, w }) {
          var vehicle = allVehicleData[dataPointIndex];
          return (
            "$" + val.toLocaleString() + " (" + vehicle.count + " vehicles)"
          );
        },
      },
    },
    grid: {
      borderColor: "#e7e7e7",
      strokeDashArray: 5,
      padding: {
        top: 0,
        right: 10,
        bottom: 0,
        left: 10,
      },
    },
    legend: { show: false },
  };

  vehicleBarChart = new ApexCharts(
    document.querySelector("#vehicle-bar-chart"),
    vehicleBarOptions
  );
  vehicleBarChart.render();
}

function sortVehicleChart(sortType) {
  currentVehicleSort = sortType;
  var sortedData;

  if (sortType === "desc") {
    sortedData = [...allVehicleData].sort((a, b) => b.revenue - a.revenue);
  } else if (sortType === "asc") {
    sortedData = [...allVehicleData].sort((a, b) => a.revenue - b.revenue);
  } else {
    sortedData = allVehicleData;
  }

  var types = sortedData.map((v) => v.type);
  var revenues = sortedData.map((v) => v.revenue);

  vehicleBarChart.updateOptions({
    xaxis: { categories: types },
  });
  vehicleBarChart.updateSeries([{ data: revenues }]);

  // Update button states
  event.target.parentElement
    .querySelectorAll("button")
    .forEach((btn) => btn.classList.remove("active"));
  event.target.classList.add("active");
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
    e.amount > max.amount ? e : max
  );

  document.getElementById("total-expenses").textContent =
    "$" + totalExpense.toLocaleString();
  document.getElementById("highest-expense").textContent =
    highestExpense.icon + " " + highestExpense.category;

  var expensePieOptions = {
    chart: {
      id: "expense-pie-chart",
      type: currentExpensePieType,
      height: 350,
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
              expense.amount.toLocaleString()
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
                    w.globals.seriesTotals.reduce((a, b) => a + b, 0) / 1000
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
    expensePieOptions
  );
  expensePieChart.render();
}

function changeExpensePieType(type) {
  currentExpensePieType = type;
  expensePieChart.destroy();
  initializeExpensePieChart(allExpenseData);

  // Update button states
  event.target.parentElement.querySelectorAll("button").forEach((btn, idx) => {
    btn.classList.remove("active");
    if ((type === "donut" && idx === 0) || (type === "pie" && idx === 1)) {
      btn.classList.add("active");
    }
  });
}

// ============================================
// AREA CHART
// ============================================

function initializeAreaChart() {
  var months = allMonthlyRevenue.map((m) => m.month);
  var revenues = allMonthlyRevenue.map((m) => m.revenue);

  var areaOptions = {
    chart: {
      id: "area-chart",
      type: "area",
      height: 350,
      toolbar: { show: false },
      animations: {
        enabled: true,
        speed: 800,
      },
      zoom: {
        enabled: true,
        type: "x",
        autoScaleYaxis: true,
      },
    },
    dataLabels: { enabled: false },
    stroke: {
      curve: "smooth",
      width: 2,
    },
    series: [
      {
        name: "Active Users",
        data: revenues.map((r) => Math.floor(r / 1000)),
      },
    ],
    xaxis: {
      categories: months,
      labels: { style: { fontSize: "12px" } },
    },
    yaxis: {
      labels: {
        formatter: function (val) {
          return val + " users";
        },
      },
    },
    fill: {
      type: "gradient",
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.3,
        stops: [0, 90, 100],
      },
    },
    colors: ["#2dce89"],
    tooltip: {
      y: {
        formatter: function (val) {
          return val + " users";
        },
      },
    },
    grid: {
      borderColor: "#e7e7e7",
    },
  };

  areaChart = new ApexCharts(
    document.querySelector("#area-chart"),
    areaOptions
  );
  areaChart.render();
}

function resetAreaZoom() {
  areaChart.resetSeries();
}

// ============================================
// CONTRACT TABLE WITH PAGINATION
// ============================================

var currentPage = 1;
var itemsPerPage = 5;
var filteredContracts = [];
var currentFilter = "all";

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
  var endIndex = Math.min(startIndex + itemsPerPage, filteredContracts.length);
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
      } else if (daysRemaining <= 15) {
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
                    0
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
        return daysRemaining >= 0 && daysRemaining <= 15;
      } else if (status === "active") {
        return daysRemaining > 15;
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
        return daysRemaining >= 0 && daysRemaining <= 15;
      } else if (currentFilter === "active") {
        return daysRemaining > 15;
      }
      return true;
    });
  }

  // Apply search filter
  filteredContracts = baseContracts.filter((contract) =>
    contract.contractNo.toLowerCase().includes(searchTerm)
  );

  renderContractsTable();
}
