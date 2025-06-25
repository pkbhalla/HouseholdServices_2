<template>
    <div>
        <nav class="navbar navbar-expand-sm navbar-dark bg-danger">
            <a class="navbar-brand" href="#" @click.prevent="goToAdmin">Admin</a>
            <button class="navbar-toggler d-lg-none" type="button" data-bs-toggle="collapse"
                data-bs-target="#collapsibleNavId" aria-controls="collapsibleNavId" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="collapsibleNavId">
                <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/admin/summary">Summary</router-link>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" @click.prevent="exportCSV">Export CSV</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
                    </li>
                </ul>
            </div>
        </nav>
        <div v-if="showExportAlert" class="alert alert-success alert-dismissible fade show" role="alert">
            {{ exportMessage }}
            <button type="button" class="btn-close" @click="showExportAlert = false" aria-label="Close"></button>
        </div>
        <div class="container mt-3">
            <h1>Admin Dashboard</h1>

            <h2>All users</h2>
            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th>User ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Location</th>
                        <th>Pincode</th>
                        <th>Mobile Number</th>
                        <th>Approved</th>
                        <th>Experience</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in dashboardData.users" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.role }}</td>
                        <td>{{ user.location }}</td>
                        <td>{{ user.pincode }}</td>
                        <td>{{ user.mobile_number }}</td>
                        <td>{{ user.is_approved }}</td>
                        <td>{{ user.prof_experience }}</td>
                        <td v-if="user.role !== 'admin'">
                            <button v-if="user.is_flagged" @click="toggleUserFlag(user.id)" class="btn btn-danger">
                                Unflag User
                            </button>
                            <button v-else @click="toggleUserFlag(user.id)" class="btn btn-warning">
                                Flag User
                            </button>
                        </td>
                        <td v-else></td>
                    </tr>
                </tbody>
            </table>

            <h2>All Services</h2>
            <div v-if="dashboardData.services && dashboardData.services.length > 0">
                <table class="table table-striped table-bordered">
                    <thead>
                        <tr>
                            <th>Service ID</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Base Price</th>
                            <th>Time Required</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="service in dashboardData.services" :key="service.id">
                            <td>{{ service.id }}</td>
                            <td>{{ service.name }}</td>
                            <td>{{ service.description }}</td>
                            <td>{{ service.base_price }}</td>
                            <td>{{ service.time_required }}</td>
                            <td>
                                <button type="button" class="btn btn-warning" @click="openEditModal(service)">
                                    Edit
                                </button>
                                <button @click="deleteService(service.id)" class="btn btn-danger">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <button type="button" class="btn btn-primary" @click="showCreateModal = true">
                    Create New Service
                </button>
            </div>
            <div v-else>
                <p>No services found.</p>
                <button type="button" class="btn btn-primary" @click="showCreateModal = true">
                    Create Service
                </button>
            </div>

            <h2 class="mt-4">All Service Requests</h2>
            <div v-if="dashboardData.service_requests && dashboardData.service_requests.length > 0">
                <table class="table table-striped table-bordered">
                    <thead>
                        <tr>
                            <th>Service Request ID</th>
                            <th>Service ID</th>
                            <th>Customer ID</th>
                            <th>Professional ID</th>
                            <th>Description</th>
                            <th>Status</th>
                            <th>Date Created</th>
                            <th>Date Closed</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="request in dashboardData.service_requests" :key="request.id">
                            <td>{{ request.id }}</td>
                            <td>{{ request.service_id }}</td>
                            <td>{{ request.customer_id }}</td>
                            <td>{{ request.professional_id }}</td>
                            <td>{{ request.description }}</td>
                            <td>{{ request.status }}</td>
                            <td>{{ request.date_created }}</td>
                            <td>{{ request.date_closed }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <p>No service requests found.</p>
            </div>

            <h2 class="mt-4">Unapproved Professionals</h2>
            <div v-if="dashboardData.unapproved_professionals && dashboardData.unapproved_professionals.length > 0">
                <table class="table table-striped table-bordered">
                    <thead>
                        <tr>
                            <th>User ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Location</th>
                            <th>Pincode</th>
                            <th>Mobile Number</th>
                            <th>Experience</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="prof in dashboardData.unapproved_professionals" :key="prof.id">
                            <td>{{ prof.id }}</td>
                            <td>{{ prof.name }}</td>
                            <td>{{ prof.email }}</td>
                            <td>{{ prof.location }}</td>
                            <td>{{ prof.pincode }}</td>
                            <td>{{ prof.mobile_number }}</td>
                            <td>{{ prof.prof_experience }}</td>
                            <td>
                                <button type="button" class="btn btn-primary" @click="openPortfolioModal(prof)">
                                    View Portfolio
                                </button>
                                <button @click="approveProfessional(prof.id)" class="btn btn-success">
                                    Approve
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div v-else>
                <p>No unapproved professionals found.</p>
            </div>
        </div>

        <div v-if="showCreateModal" class="modal-backdrop show"></div>
        <div v-if="showCreateModal" class="modal d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Create Service</h5>
                        <button type="button" class="btn-close" @click="showCreateModal = false"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="createService">
                            <label for="create-name" class="form-label">Name:</label>
                            <input type="text" id="create-name" v-model="newService.name" required class="form-control">

                            <label for="create-description" class="form-label">Description:</label>
                            <input type="text" id="create-description" v-model="newService.description" required
                                class="form-control">

                            <label for="create-base_price" class="form-label">Base Price:</label>
                            <input type="number" id="create-base_price" v-model="newService.base_price" required
                                class="form-control">

                            <label for="create-time_required" class="form-label">Time Required:</label>
                            <input type="text" id="create-time_required" v-model="newService.time_required" required
                                class="form-control">

                            <div class="mt-3">
                                <button type="submit" class="btn btn-primary">Create</button>
                                <button type="button" class="btn btn-secondary ms-2"
                                    @click="showCreateModal = false">Cancel</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

      
        <div v-if="showEditModal" class="modal-backdrop show"></div>
        <div v-if="showEditModal" class="modal d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Edit Service</h5>
                        <button type="button" class="btn-close" @click="showEditModal = false"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="updateService">
                            <label for="edit-name" class="form-label">Name:</label>
                            <input type="text" id="edit-name" v-model="editingService.name" required
                                class="form-control">

                            <label for="edit-description" class="form-label">Description:</label>
                            <input type="text" id="edit-description" v-model="editingService.description" required
                                class="form-control">

                            <label for="edit-base_price" class="form-label">Base Price:</label>
                            <input type="number" id="edit-base_price" v-model="editingService.base_price" required
                                class="form-control">

                            <label for="edit-time_required" class="form-label">Time Required:</label>
                            <input type="text" id="edit-time_required" v-model="editingService.time_required" required
                                class="form-control">

                            <div class="mt-3">
                                <button type="submit" class="btn btn-primary">Update</button>
                                <button type="button" class="btn btn-secondary ms-2"
                                    @click="showEditModal = false">Cancel</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

       
        <div v-if="showPortfolioModal" class="modal-backdrop show"></div>
        <div v-if="showPortfolioModal" class="modal d-block" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{ selectedProfessional?.name }}'s Portfolio</h5>
                        <button type="button" class="btn-close" @click="showPortfolioModal = false"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <iframe v-if="selectedProfessional"
                            :src="`/api/static/pdf/${selectedProfessional.prof_profile}`" width="100%"
                            height="600"></iframe>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary"
                            @click="showPortfolioModal = false">Close</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const dashboardData = ref({
    users: [],
    services: [],
    service_requests: [],
    unapproved_professionals: []
});
const showExportAlert = ref(false);
const exportMessage = ref('');


const showCreateModal = ref(false);
const showEditModal = ref(false);
const showPortfolioModal = ref(false);

const newService = ref({
    name: '',
    description: '',
    base_price: 0,
    time_required: ''
});

const editingService = ref({
    id: null,
    name: '',
    description: '',
    base_price: 0,
    time_required: ''
});

const selectedProfessional = ref(null);


const fetchDashboardData = async () => {
    try {
        const token = localStorage.getItem('admin_token');
        if (!token) {
            router.push('/admin/login');
            return;
        }

        const response = await fetch('/api/admin/dashboard', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            dashboardData.value = await response.json();
        } else if (response.status === 401 || response.status === 403) {
            localStorage.removeItem('admin_token');
            router.push('/admin/login');
        }
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
    }
};


const toggleUserFlag = async (userId) => {
    try {
        const token = localStorage.getItem('admin_token');
        const response = await fetch(`/api/admin/flag-user/${userId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            await fetchDashboardData(); 
        }
    } catch (error) {
        console.error('Error toggling user flag:', error);
    }
};
const exportCSV = async () => {
  if (!confirm('Are you sure you want to export closed service requests as CSV? The file will be sent to your email.')) {
    return;
  }
  
  try {
    const token = localStorage.getItem('admin_token');
    const response = await fetch('/api/admin/export-csv', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const data = await response.json();
      exportMessage.value = data.message;
      showExportAlert.value = true;
      
      
      setTimeout(() => {
        showExportAlert.value = false;
      }, 5000);
    } else {
      console.error('Error exporting CSV');
    }
  } catch (error) {
    console.error('Error during CSV export:', error);
  }
};


const openEditModal = (service) => {
    editingService.value = { ...service };
    showEditModal.value = true;
};

const openPortfolioModal = (professional) => {
    selectedProfessional.value = professional;
    showPortfolioModal.value = true;
};


const createService = async () => {
    try {
        const token = localStorage.getItem('admin_token');
        const response = await fetch('/api/service', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newService.value)
        });

        if (response.ok) {
            newService.value = {
                name: '',
                description: '',
                base_price: 0,
                time_required: ''
            };
            showCreateModal.value = false;
            await fetchDashboardData();
        }
    } catch (error) {
        console.error('Error creating service:', error);
    }
};


const updateService = async () => {
    try {
        const token = localStorage.getItem('admin_token');
        const response = await fetch(`/api/service/${editingService.value.id}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(editingService.value)
        });

        if (response.ok) {
            showEditModal.value = false;
            await fetchDashboardData();
        }
    } catch (error) {
        console.error('Error updating service:', error);
    }
};


const deleteService = async (serviceId) => {
    if (!confirm('Are you sure you want to delete this service?')) {
        return;
    }

    try {
        const token = localStorage.getItem('admin_token');
        const response = await fetch(`/api/service/${serviceId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            await fetchDashboardData();
        }
    } catch (error) {
        console.error('Error deleting service:', error);
    }
};


const approveProfessional = async (userId) => {
    try {
        const token = localStorage.getItem('admin_token');
        const response = await fetch(`/api/admin/approve-professional/${userId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            await fetchDashboardData();
        }
    } catch (error) {
        console.error('Error approving professional:', error);
    }
};

const goToAdmin = () => {
    router.push('/admin/dashboard');
};

const logout = () => {
    localStorage.removeItem('admin_token');
    router.push('/');
};

onMounted(() => {
    fetchDashboardData();
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