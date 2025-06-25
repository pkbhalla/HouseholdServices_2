<template>
    <section class="vh-100 customer-gradient">
      <div class="container">
        <div class="card" style="width: 40rem; margin: auto;">
          <div class="card-body">
            <h1 class="card-title text-center">Register as a Customer</h1>
            <form @submit.prevent="handleSubmit">
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
              <button type="submit" class="btn btn-primary w-100">Register</button>
            </form>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const formData = ref({
    name: '',
    email: '',
    password: '',
    location: '',
    pincode: '',
    mobile_number: ''
  });
  
  const handleSubmit = async () => {
    try {
      const response = await fetch('/api/register/customer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData.value)
      });
  
      if (response.ok) {
        alert('Registration successful! You can now log in.');
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
  </script>
  
  <style scoped>
  .customer-gradient {
    background: linear-gradient(to right, #ff7e5f, #feb47b);
    padding: 20px;
  }
  </style>
  