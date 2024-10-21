<template>
  <div class="container mt-4">
    <h1 class="mb-4">Stats</h1>
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    <div v-else>
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Total eBooks</h5>
              <p class="card-text display-4">{{ stats.total_ebooks }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Total Sections</h5>
              <p class="card-text display-4">{{ stats.total_sections }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">eBook Activity</h5>
              <canvas ref="ebookActivityChart"></canvas>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Top Borrowed eBooks</h5>
              <canvas ref="topBorrowedChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">User Activity</h5>
              <canvas ref="userActivityChart"></canvas>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">eBooks by Section</h5>
              <canvas ref="ebooksBySectionChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Active Requests</h5>
              <ul class="list-group">
                <li
                  v-for="request in stats.active_requests"
                  :key="request.id"
                  class="list-group-item"
                >
                  {{ request.ebook_id }} - Requested on
                  {{ new Date(request.request_date).toLocaleDateString() }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Overdue Requests</h5>
              <ul class="list-group">
                <li
                  v-for="request in stats.overdue_requests"
                  :key="request.id"
                  class="list-group-item"
                >
                  {{ request.ebook_id }} - Due on
                  {{ new Date(request.return_date).toLocaleDateString() }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getLibrarianStats, type LibrarianStats } from '@/api/stats'
import { Chart } from 'chart.js/auto'

const stats = ref<LibrarianStats | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const ebookActivityChart = ref<HTMLCanvasElement | null>(null)
const topBorrowedChart = ref<HTMLCanvasElement | null>(null)
const userActivityChart = ref<HTMLCanvasElement | null>(null)
const ebooksBySectionChart = ref<HTMLCanvasElement | null>(null)

const fetchStats = async () => {
  try {
    stats.value = await getLibrarianStats()
    loading.value = false
  } catch (err) {
    error.value = 'Failed to fetch librarian stats'
    loading.value = false
  }
}

const createCharts = () => {
  if (stats.value) {
    new Chart(ebookActivityChart.value!, {
      type: 'bar',
      data: {
        labels: stats.value.ebook_activity.map((item) => item.name),
        datasets: [
          {
            label: 'Request Count',
            data: stats.value.ebook_activity.map((item) => item.request_count),
            backgroundColor: 'rgba(75, 192, 192, 0.6)'
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })

    new Chart(topBorrowedChart.value!, {
      type: 'pie',
      data: {
        labels: stats.value.top_borrowed_ebooks.map((item) => item.name),
        datasets: [
          {
            data: stats.value.top_borrowed_ebooks.map((item) => item.borrow_count),
            backgroundColor: [
              'rgba(255, 99, 132, 0.6)',
              'rgba(54, 162, 235, 0.6)',
              'rgba(255, 206, 86, 0.6)',
              'rgba(75, 192, 192, 0.6)',
              'rgba(153, 102, 255, 0.6)'
            ]
          }
        ]
      },
      options: {
        responsive: true
      }
    })

    new Chart(userActivityChart.value!, {
      type: 'bar',
      data: {
        labels: stats.value.user_activity.map((item) => item.username),
        datasets: [
          {
            label: 'Total Requests',
            data: stats.value.user_activity.map((item) => item.total_requests),
            backgroundColor: 'rgba(255, 99, 132, 0.6)'
          },
          {
            label: 'Granted Requests',
            data: stats.value.user_activity.map((item) => item.granted_requests),
            backgroundColor: 'rgba(75, 192, 192, 0.6)'
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })

    new Chart(ebooksBySectionChart.value!, {
      type: 'doughnut',
      data: {
        labels: stats.value.ebooks_by_section.map((item) => item.section_name),
        datasets: [
          {
            data: stats.value.ebooks_by_section.map((item) => item.ebook_count),
            backgroundColor: [
              'rgba(255, 99, 132, 0.6)',
              'rgba(54, 162, 235, 0.6)',
              'rgba(255, 206, 86, 0.6)',
              'rgba(75, 192, 192, 0.6)',
              'rgba(153, 102, 255, 0.6)'
            ]
          }
        ]
      },
      options: {
        responsive: true
      }
    })
  }
}

onMounted(() => {
  fetchStats().then(() => {
    if (stats.value) {
      createCharts()
    }
  })
})
</script>
