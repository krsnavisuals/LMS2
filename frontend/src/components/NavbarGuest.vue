<template>
  <nav class="navbar navbar-dark bg-dark">
    <div class="container-fluid d-flex justify-content-center align-items-center">
      <router-link
        class="navbar-brand fw-medium fs-3 d-flex justify-content-center align-items-center gap-2"
        to="/"
      >
        <v-icon name="io-library" scale="2.3"></v-icon>
        Library Management System
      </router-link>
      <ul class="navbar-nav me-auto mb-2 mb-lg-0 d-flex flex-row gap-3">
        <li class="nav-item">
          <router-link active-class="active" class="nav-link" to="/user-login"
            >User Login</router-link
          >
        </li>
        <li class="nav-item">
          <router-link active-class="active" class="nav-link" to="/librarian-login"
            >Librarian Login</router-link
          >
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup lang="ts"></script>
