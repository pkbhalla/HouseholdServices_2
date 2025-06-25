<template>
    <div>
      <nav class="navbar navbar-expand-sm navbar-dark bg-danger">
        <a class="navbar-brand" href="#" @click.prevent="goToAdmin">Admin</a>
        <button
          class="navbar-toggler d-lg-none"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#collapsibleNavId"
          aria-controls="collapsibleNavId"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="collapsibleNavId">
          <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
            <li class="nav-item">
              <router-link class="nav-link active" to="/admin/summary">Summary</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </nav>
      
      <div class="container mt-3">
        <h1>Summary</h1>
        <div class="row">
          <div class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Pending Requests</h5>
                <p class="card-text">{{ summaryData.pending_requests }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Completed Requests</h5>
                <p class="card-text">{{ summaryData.completed_requests }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Active Requests</h5>
                <p class="card-text">{{ summaryData.active_requests }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Rejected Requests</h5>
                <p class="card-text">{{ summaryData.rejected_requests }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Professionals</h5>
                <p class="card-text">{{ summaryData.professionals_count }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Customers</h5>
                <p class="card-text">{{ summaryData.customers_count }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-6 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Number of Users by Role</h5>
                <canvas ref="userRoleChart"></canvas>
              </div>
            </div>
          </div>
          <div class="col-md-6 mb-3">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Request Status Distribution</h5>
                <canvas ref="requestStatusChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue';
  import { useRouter } from 'vue-router';
  import Chart from 'chart.js/auto';
  
  const router = useRouter();
  const summaryData = ref({
    pending_requests: 0,
    completed_requests: 0,
    active_requests: 0,
    rejected_requests: 0,
    professionals_count: 0,
    customers_count: 0,
    user_distribution: {
      roles: [],
      counts: []
    },
    request_distribution: {
      status: [],
      counts: []
    }
  });
  
  const userRoleChart = ref(null);
  const requestStatusChart = ref(null);
  let userRoleChartInstance = null;
  let requestStatusChartInstance = null;
  
  
  const fetchSummaryData = async () => {
    try {
      const token = localStorage.getItem('admin_token');
      if (!token) {
        router.push('/admin/login');
        return;
      }
  
      const response = await fetch('/api/admin/summary', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
  
      if (response.ok) {
        summaryData.value = await response.json();
        renderCharts();
      } else if (response.status === 401 || response.status === 403) {
        localStorage.removeItem('admin_token');
        router.push('/admin/login');
      }
    } catch (error) {
      console.error('Error fetching summary data:', error);
    }
  };
  

  const renderCharts = () => {
    if (userRoleChartInstance) {
      userRoleChartInstance.destroy();
    }
    if (requestStatusChartInstance) {
      requestStatusChartInstance.destroy();
    }
  
    if (userRoleChart.value) {
      userRoleChartInstance = new Chart(userRoleChart.value, {
        type: 'bar',
        data: {
          labels: summaryData.value.user_distribution.roles,
          datasets: [{
            label: 'Number of Users',
            data: summaryData.value.user_distribution.counts,
            backgroundColor: [
              'rgba(54, 162, 235, 0.6)',
              'rgba(255, 99, 132, 0.6)'
            ],
            borderColor: [
              'rgba(54, 162, 235, 1)',
              'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0
              }
            }
          }
        }
      });
    }
  
    if (requestStatusChart.value) {
      requestStatusChartInstance = new Chart(requestStatusChart.value, {
        type: 'pie',
        data: {
          labels: summaryData.value.request_distribution.status,
          datasets: [{
            data: summaryData.value.request_distribution.counts,
            backgroundColor: [
              'rgba(54, 162, 235, 0.6)',
              'rgba(255, 99, 132, 0.6)',
              'rgba(255, 206, 86, 0.6)',
              'rgba(75, 192, 192, 0.6)'
            ],
            borderColor: [
              'rgba(54, 162, 235, 1)',
              'rgba(255, 99, 132, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true
        }
      });
    }
  };
  
  const goToAdmin = () => {
    router.push('/admin/dashboard');
  };
  
  const logout = () => {
    localStorage.removeItem('admin_token');
    router.push('/');
  };
  
  watch(() => summaryData.value, () => {
    renderCharts();
  }, { deep: true });
  
  onMounted(() => {
    fetchSummaryData();
  });
  </script>
  