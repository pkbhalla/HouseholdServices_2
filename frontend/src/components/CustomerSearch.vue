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
              <router-link class="nav-link active" to="/customer/search">Search</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </nav>
      <div class="container">
        <h2>Search for service providers</h2>
        <form @submit.prevent="performSearch" class="form-inline mb-3">
          <div class="form-group">
            <input
              type="text"
              class="form-control"
              v-model="searchQuery"
              placeholder="Search by service name, location or pincode"
            >
          </div>
          <button type="submit" class="btn btn-primary ms-2">Search</button>
          <button @click="resetSearch" class="btn btn-outline-success ms-2">Reset</button>
        </form>
        <table v-if="filteredServices.length" class="table table-striped">
          <thead>
            <tr>
              <th>Service Name</th>
              <th>Professional Name</th>
              <th>Location</th>
              <th>Pincode</th>
              <th>View Details</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in filteredServices" :key="service.id">
              <td>{{ service.name }}</td>
              <td>
                <div v-for="professional in service.professionals" :key="professional.id">
                  {{ professional.name }}<br><br>
                </div>
              </td>
              <td>
                <div v-for="professional in service.professionals" :key="professional.id">
                  {{ professional.location }}<br><br>
                </div>
              </td>
              <td>
                <div v-for="professional in service.professionals" :key="professional.id">
                  {{ professional.pincode }}<br><br>
                </div>
              </td>
              <td>
                <div v-for="professional in service.professionals" :key="professional.id">
                  <button
                    type="button"
                    class="btn btn-primary mb-2"
                    @click="openModal(professional, service)"
                  >
                    View Details
                  </button>
                  <br><br>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Modal -->
      <div v-if="showModal" class="modal-backdrop show"></div>
      <div v-if="showModal" class="modal d-block" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Professional Details</h5>
              <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <p>Name: {{ selectedProfessional.name }}</p>
              <p>Location: {{ selectedProfessional.location }}</p>
              <p>Pincode: {{ selectedProfessional.pincode }}</p>
              <p>Mobile Number: {{ selectedProfessional.mobile_number }}</p>
              <p>Service: {{ selectedService.name }}</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-primary" @click="closeModal">Close</button>
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
  const services = ref([]);
  const searchQuery = ref('');
  const showModal = ref(false);
  const selectedProfessional = ref({});
  const selectedService = ref({});
  
  const fetchServices = async () => {
    try {
      const token = localStorage.getItem('customer_token');
      const response = await fetch('/api/customer/search', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        services.value = await response.json();
      } else {
        console.error('Failed to fetch services');
      }
    } catch (error) {
      console.error('Error fetching services:', error);
    }
  };
  
  const filteredServices = computed(() => {
    if (!searchQuery.value) return services.value;
    const query = searchQuery.value.toLowerCase();
    return services.value.filter(service => 
      service.name.toLowerCase().includes(query) ||
      service.professionals.some(prof => 
        prof.location.toLowerCase().includes(query) ||
        prof.pincode.toString().includes(query)
      )
    );
  });
  
  const performSearch = () => {
    // The computed property will handle the filtering
  };
  
  const resetSearch = () => {
    searchQuery.value = '';
  };
  
  const openModal = (professional, service) => {
    selectedProfessional.value = professional;
    selectedService.value = service;
    showModal.value = true;
  };
  
  const closeModal = () => {
    showModal.value = false;
  };
  
  const goToCustomer = () => {
    router.push('/customer/dashboard');
  };
  
  const logout = () => {
    localStorage.removeItem('customer_token');
    localStorage.removeItem('user_role');
    router.push('/');
  };
  
  onMounted(() => {
    fetchServices();
  });
  </script>
  
  <style scoped>
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
  