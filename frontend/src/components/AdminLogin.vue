<template>
    <section class="vh-100" :style="{ backgroundImage: `url(${backgroundImage})`, backgroundSize: 'cover' }">
      <div class="container py-5 h-100">
        <div class="row justify-content-center align-items-center h-100">
          <div class="col-md-5 mt-5">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Admin Login</h5>
                <form @submit.prevent="handleLogin">
                  <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" class="form-control" id="email" v-model="email" required>
                  </div>
                  <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" class="form-control" id="password" v-model="password" required>
                  </div>
                  <button type="submit" class="btn btn-primary">Login</button>
                </form>
              </div>
            </div>
          </div>
          <div class="col-md-4 mt-5">
            <div class="card">
              <img :src="cardImage" class="card-img-top" alt="...">
            </div>
          </div>
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
  const backgroundImage = '../src/assets/img_5.jpg';
  const cardImage = '../src/assets/img_4.jpg';
  
  const handleLogin = async () => {
    try {
      const response = await fetch('/api/admin/auth', {
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
        localStorage.setItem('admin_token', data.access_token);
        router.push('/admin/dashboard');
      } else {
        console.error('Login failed');
      }
    } catch (error) {
      console.error('Error during login:', error);
    }
  };
  </script>
  