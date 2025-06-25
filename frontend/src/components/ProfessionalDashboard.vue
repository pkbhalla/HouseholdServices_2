<template>
    <div>
      <nav class="navbar navbar-expand-sm navbar-dark bg-primary">
        <a class="navbar-brand" href="#" @click.prevent="goToProfessional">Professional</a>
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
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </nav>
      
      <div class="container">
        <h2>Pending Requests</h2>
        <div v-if="dashboardData.pending_requests && dashboardData.pending_requests.length > 0">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Customer Name</th>
                <th>Description</th>
                <th>Mobile Number</th>
                <th>Location</th>
                <th>Pincode</th>
                <th>Date Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in dashboardData.pending_requests" :key="request.id">
                <td>{{ request.customer?.name }}</td>
                <td>{{ request.description }}</td>
                <td>{{ request.customer?.mobile_number }}</td>
                <td>{{ request.customer?.location }}</td>
                <td>{{ request.customer?.pincode }}</td>
                <td>{{ request.date_created }}</td>
                <td>
                  <button @click="acceptRequest(request.id)" class="btn btn-success">Accept</button>
                  <button @click="rejectRequest(request.id)" class="btn btn-danger ms-2">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>No pending requests.</p>
        
        <h2>Accepted Requests</h2>
        <div v-if="dashboardData.active_requests && dashboardData.active_requests.length > 0">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Customer Name</th>
                <th>Description</th>
                <th>Mobile Number</th>
                <th>Location</th>
                <th>Pincode</th>
                <th>Date Created</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in dashboardData.active_requests" :key="request.id">
                <td>{{ request.customer?.name }}</td>
                <td>{{ request.description }}</td>
                <td>{{ request.customer?.mobile_number }}</td>
                <td>{{ request.customer?.location }}</td>
                <td>{{ request.customer?.pincode }}</td>
                <td>{{ request.date_created }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>No active requests.</p>
        
        <h2>Closed Requests</h2>
        <div v-if="dashboardData.completed_requests && dashboardData.completed_requests.length > 0">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Customer Name</th>
                <th>Description</th>
                <th>Mobile Number</th>
                <th>Location</th>
                <th>Pincode</th>
                <th>Date Created</th>
                <th>Date Closed</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in dashboardData.completed_requests" :key="request.id">
                <td>{{ request.customer?.name }}</td>
                <td>{{ request.description }}</td>
                <td>{{ request.customer?.mobile_number }}</td>
                <td>{{ request.customer?.location }}</td>
                <td>{{ request.customer?.pincode }}</td>
                <td>{{ request.date_created }}</td>
                <td>{{ request.date_closed }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>No completed requests.</p>
        
        <h2>Rejected Requests</h2>
        <div v-if="dashboardData.rejected_requests && dashboardData.rejected_requests.length > 0">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Customer Name</th>
                <th>Description</th>
                <th>Mobile Number</th>
                <th>Location</th>
                <th>Pincode</th>
                <th>Date Created</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in dashboardData.rejected_requests" :key="request.id">
                <td>{{ request.customer?.name }}</td>
                <td>{{ request.description }}</td>
                <td>{{ request.customer?.mobile_number }}</td>
                <td>{{ request.customer?.location }}</td>
                <td>{{ request.customer?.pincode }}</td>
                <td>{{ request.date_created }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>No rejected requests.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const dashboardData = ref({
    pending_requests: [],
    active_requests: [],
    completed_requests: [],
    rejected_requests: []
  });
  
  // Fetch dashboard data
  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('professional_token');
      if (!token) {
        router.push('/login');
        return;
      }
  
      const response = await fetch('/api/professional/dashboard', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
  
      if (response.ok) {
        dashboardData.value = await response.json();
      } else if (response.status === 401 || response.status === 403) {
        localStorage.removeItem('professional_token');
        router.push('/login');
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };
  
  // Accept service request
  const acceptRequest = async (requestId) => {
    try {
      const token = localStorage.getItem('professional_token');
      const response = await fetch(`/api/professional/service-request/${requestId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          status: 'Accepted'
        })
      });
  
      if (response.ok) {
        await fetchDashboardData();
      }
    } catch (error) {
      console.error('Error accepting request:', error);
    }
  };
  
  // Reject service request
  const rejectRequest = async (requestId) => {
    try {
      const token = localStorage.getItem('professional_token');
      const response = await fetch(`/api/professional/service-request/${requestId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          status: 'Rejected'
        })
      });
  
      if (response.ok) {
        await fetchDashboardData();
      }
    } catch (error) {
      console.error('Error rejecting request:', error);
    }
  };
  
  // Navigation functions
  const goToProfessional = () => {
    router.push('/professional/dashboard');
  };
  
  const logout = () => {
    localStorage.removeItem('professional_token');
    localStorage.removeItem('user_role');
    router.push('/');
  };
  
  onMounted(() => {
    fetchDashboardData();
  });
  </script>
  