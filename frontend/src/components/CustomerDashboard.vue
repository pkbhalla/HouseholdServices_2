<template>
    <div>
      <nav class="navbar navbar-expand-sm navbar-dark bg-black">
        <a class="navbar-brand" href="#" @click.prevent="goToCustomer">Customer</a>
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
              <router-link class="nav-link" to="/customer/search">Search</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </nav>
      
      <div class="container-fluid">
        <div class="row">
          <div class="col">
            <h1>Services</h1>
            <div class="row row-cols-1 row-cols-md-3 g-4">
              <div v-for="service in dashboardData.services" :key="service.id" class="col">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title">{{ service.name }}</h5>
                    <p class="card-text">{{ service.description }}</p>
                    <p class="card-text">Base Price: {{ service.base_price }}</p>
                    <p class="card-text">Time Required: {{ service.time_required }}</p>
                    <button 
                      type="button" 
                      class="btn btn-primary" 
                      @click="openCreateRequestModal(service.id)"
                    >
                      Create Service Request
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="row mt-4">
          <div class="col">
            <h1>My Service Requests</h1>
            <table v-if="dashboardData.service_requests && dashboardData.service_requests.length > 0" class="table table-striped">
              <thead>
                <tr>
                  <th>Service Name</th>
                  <th>Description</th>
                  <th>Professional</th>
                  <th>Date Created</th>
                  <th>Date Closed</th>
                  <th>Status</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in dashboardData.service_requests" :key="request.id">
                  <td>{{ request.service?.name }}</td>
                  <td>{{ request.description }}</td>
                  <td>{{ request.professional?.name }}</td>
                  <td>{{ request.date_created }}</td>
                  <td>
                    {{ request.status === "Closed" ? request.date_closed : "-" }}
                  </td>
                  <td>{{ request.status }}</td>
                  <td>
                    <button 
                      v-if="request.status === 'Accepted'" 
                      @click="closeServiceRequest(request.id)" 
                      class="btn btn-primary"
                    >
                      Close Service Request
                    </button>
                    <template v-if="request.status === 'Pending'">
                      <button 
                        type="button" 
                        class="btn btn-warning" 
                        @click="openEditModal(request)"
                      >
                        Edit
                      </button>
                      <button 
                        @click="deleteServiceRequest(request.id)" 
                        class="btn btn-danger ms-2"
                      >
                        Delete
                      </button>
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
            <p v-else>No service requests found. Create a new service request.</p>
          </div>
        </div>
      </div>
  
      <!-- Create Service Request Modal -->
      <div v-if="showCreateModal" class="modal-backdrop show"></div>
      <div v-if="showCreateModal" class="modal d-block" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Create Service Request</h5>
              <button type="button" class="btn-close" @click="showCreateModal = false" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="createServiceRequest">
                <div class="mb-3">
                  <label for="description" class="form-label">Description</label>
                  <input type="text" class="form-control" id="description" v-model="newRequest.description" required>
                </div>
                <div class="mb-3">
                  <label for="professional_name" class="form-label">Professional</label>
                  <select class="form-select" id="professional_name" v-model="newRequest.professional_id" required>
                    <option v-for="professional in professionalsForSelectedService" 
                            :key="professional.id" 
                            :value="professional.id">
                      {{ professional.name }}
                    </option>
                  </select>
                </div>
                <button type="submit" class="btn btn-primary">Create</button>
                <button type="button" class="btn btn-secondary ms-2" @click="showCreateModal = false">Cancel</button>
              </form>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Edit Service Request Modal -->
      <div v-if="showEditModal" class="modal-backdrop show"></div>
      <div v-if="showEditModal" class="modal d-block" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Description</h5>
              <button type="button" class="btn-close" @click="showEditModal = false" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="updateServiceRequest">
                <div class="mb-3">
                  <label for="edit-description" class="form-label">Description</label>
                  <textarea class="form-control" id="edit-description" v-model="editingRequest.description"></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Save changes</button>
                <button type="button" class="btn btn-secondary ms-2" @click="showEditModal = false">Cancel</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const dashboardData = ref({
    services: [],
    service_requests: [],
    professionals_by_service: {}
  });
  

  const showCreateModal = ref(false);
  const showEditModal = ref(false);
  const selectedServiceId = ref(null);
  
 
  const newRequest = ref({
    description: '',
    professional_id: null,
    service_id: null
  });
  
  const editingRequest = ref({
    id: null,
    description: ''
  });
  

  const professionalsForSelectedService = computed(() => {
    if (!selectedServiceId.value || !dashboardData.value.professionals_by_service) {
      return [];
    }
    return dashboardData.value.professionals_by_service[selectedServiceId.value] || [];
  });
  

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('customer_token');
      if (!token) {
        router.push('/login');
        return;
      }
  
      const response = await fetch('/api/customer/dashboard', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
  
      if (response.ok) {
        dashboardData.value = await response.json();
      } else if (response.status === 401 || response.status === 403) {
        localStorage.removeItem('user_token');
        router.push('/login');
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };
  
  const openCreateRequestModal = (serviceId) => {
    selectedServiceId.value = serviceId;
    newRequest.value.service_id = serviceId;
    newRequest.value.description = '';
    
    if (professionalsForSelectedService.value.length > 0) {
      newRequest.value.professional_id = professionalsForSelectedService.value[0].id;
    } else {
      newRequest.value.professional_id = null;
    }
    
    showCreateModal.value = true;
  };
  
  const openEditModal = (request) => {
    editingRequest.value = {
      id: request.id,
      description: request.description
    };
    showEditModal.value = true;
  };
  
  // Create service request
  const createServiceRequest = async () => {
    try {
      const token = localStorage.getItem('customer_token');
      const response = await fetch('/api/service-request', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newRequest.value)
      });
  
      if (response.ok) {
        showCreateModal.value = false;
        await fetchDashboardData();
      }
    } catch (error) {
      console.error('Error creating service request:', error);
    }
  };
  
  // Update service request
  const updateServiceRequest = async () => {
    try {
      const token = localStorage.getItem('customer_token');
      const response = await fetch(`/api/service-request/${editingRequest.value.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          description: editingRequest.value.description
        })
      });
  
      if (response.ok) {
        showEditModal.value = false;
        await fetchDashboardData();
      }
    } catch (error) {
      console.error('Error updating service request:', error);
    }
  };
  
  // Close service request
  const closeServiceRequest = async (requestId) => {
    try {
      const token = localStorage.getItem('customer_token');
      const response = await fetch(`/api/customer/service-request/close/${requestId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
  
      if (response.ok) {
        await fetchDashboardData();
      }
    } catch (error) {
      console.error('Error closing service request:', error);
    }
  };
  
  // Delete service request
  const deleteServiceRequest = async (requestId) => {
    if (!confirm('Are you sure you want to delete this service request?')) {
      return;
    }
    
    try {
      const token = localStorage.getItem('customer_token');
      const response = await fetch(`/api/service-request/${requestId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
  
      if (response.ok) {
        await fetchDashboardData();
      }
    } catch (error) {
      console.error('Error deleting service request:', error);
    }
  };
  
  // Navigation functions
  const goToCustomer = () => {
    router.push('/customer/dashboard');
  };
  
  const logout = () => {
    localStorage.removeItem('customer_token');
    localStorage.removeItem('user_role');
    router.push('/');
  };
  
  onMounted(() => {
    fetchDashboardData();
  });
  </script>
  
  <style scoped>
  /* Modal styles */
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1040;
  }
  
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1050;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    outline: 0;
  }
  
  .d-block {
    display: block !important;
  }
  </style>
  