<template>
    <section class="d-flex justify-content-center align-items-center grad1" style="height: 100vh;">
      <div class="card" style="width: 30rem;">
        <div class="card-body">
          <h5 class="card-title">Welcome to NestCare</h5>
          <p class="card-text">
            Are you an admin?
            <router-link to="/admin/login" class="btn btn-primary">Login Here</router-link>
          </p>
          <p class="card-text">
            Looking for services?
            <router-link to="/login" class="btn btn-primary">Click here</router-link>
          </p>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  // No additional logic needed for this component
  </script>
  
  <style scoped>
  .grad1 {
    background: linear-gradient(to right, #74ebd5, #acb6e5);
  }
  </style>
  