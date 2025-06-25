<template>
    <section class="h-100 gradient-background d-flex justify-content-center align-items-center">
      <div class="card" style="width: 50rem;">
        <div class="card-body">
          <h5 class="card-title">Register as a Professional</h5>
          <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
            <div class="mb-3">
              <label for="name" class="form-label">Name:</label>
              <input type="text" class="form-control" id="name" v-model="formData.name" required>
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email:</label>
              <input type="email" class="form-control" id="email" v-model="formData.email" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password:</label>
              <input type="password" class="form-control" id="password" v-model="formData.password" required>
            </div>
            <div class="mb-3">
              <label for="location" class="form-label">Location:</label>
              <input type="text" class="form-control" id="location" v-model="formData.location" required>
            </div>
            <div class="mb-3">
              <label for="pincode" class="form-label">Pincode:</label>
              <input type="number" class="form-control" id="pincode" v-model="formData.pincode" required>
            </div>
            <div class="mb-3">
              <label for="mobile_number" class="form-label">Mobile Number:</label>
              <input type="number" class="form-control" id="mobile_number" v-model="formData.mobile_number" required>
            </div>
            <div class="mb-3">
              <label for="service" class="form-label">Service:</label>
              <select class="form-select" id="service" v-model="formData.service" required>
                <option v-for="service in services" :key="service.name" :value="service.name">
                  {{ service.name }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="prof_profile" class="form-label">Profile:</label>
              <input type="file" class="form-control" id="prof_profile" @change="handleFileUpload" required>
            </div>
            <div class="mb-3">
              <label for="prof_experience" class="form-label">Experience:</label>
              <input type="text" class="form-control" id="prof_experience" v-model="formData.prof_experience" required>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
          </form>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const services = ref([]);
  const formData = ref({
    name: '',
    email: '',
    password: '',
    location: '',
    pincode: '',
    mobile_number: '',
    service: '',
    prof_experience: '',
    prof_profile: null
  });
  
  const fetchServices = async () => {
    try {
      const response = await fetch('/api/service');
      if (response.ok) {
        services.value = await response.json();
      }
    } catch (error) {
      console.error('Error fetching services:', error);
    }
  };
  
  const handleFileUpload = (event) => {
    formData.value.prof_profile = event.target.files[0];
  };
  
  const handleSubmit = async () => {
    try {
      const form = new FormData();
      for (const key in formData.value) {
        form.append(key, formData.value[key]);
      }
  
      const response = await fetch('/api/register/professional', {
        method: 'POST',
        body: form
      });
  
      if (response.ok) {
        alert('Registration successful! Please wait for admin approval.');
        router.push('/login');
      } else {
        const errorData = await response.json();
        alert(`Registration failed: ${errorData.message}`);
      }
    } catch (error) {
      console.error('Error during registration:', error);
      alert('An error occurred during registration. Please try again.');
    }
  };
  
  onMounted(() => {
    fetchServices();
  });
  </script>
  
  <style scoped>
  .gradient-background {
    background: linear-gradient(to bottom right, #ff0066, #ff6600);
    min-height: 100vh;
  }
  </style>
  