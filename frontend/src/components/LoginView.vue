<template>
    <section class="d-flex vh-100">
      <img :src="backgroundImage" alt="Background" class="flex-grow-1 h-100 object-fit-cover">
      <div class="card" style="width: 30rem;">
        <div class="card-body">
          <h1 class="card-title text-center">Login</h1>
          <form @submit.prevent="handleLogin" class="form-group">
            <label for="email" class="form-label">Email:</label>
            <input type="email" id="email" v-model="email" required class="form-control mb-3">
            <label for="password" class="form-label">Password:</label>
            <input type="password" id="password" v-model="password" required class="form-control mb-3">
            <button type="submit" class="btn btn-primary w-100">Login</button>
          </form>
          <p class="mt-3">Don't have an account? <router-link to="/register/customer">Register as Customer</router-link></p>
          <p>Are you a service professional? <router-link to="/register/professional">Register as Professional</router-link></p>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const email = ref('');
  const password = ref('');
  const backgroundImage = '../src/assets/img_4.jpg'; 
  
  const handleLogin = async () => {
    try {
      const response = await fetch('/api/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email.value,
          password: password.value,
        }),
      });
  
      if (response.ok) {
        const data = await response.json();
        if (data.role === 'customer') {
          localStorage.setItem('customer_token', data.access_token);
        } else if (data.role === 'professional') {
          localStorage.setItem('professional_token', data.access_token);
        }
        localStorage.setItem('user_role', data.role);
        
        // Redirect based on user role
        if (data.role === 'customer') {
          router.push('/customer/dashboard');
        } else if (data.role === 'professional') {
          router.push('/professional/dashboard');
        }
      } else {
        const errorData = await response.json();
        alert(`Login failed: ${errorData.message}`);
      }
    } catch (error) {
      console.error('Error during login:', error);
      alert('An error occurred during login. Please try again.');
    }
  };
  </script>
  
  <style scoped>
  .object-fit-cover {
    object-fit: cover;
  }
  </style>
  