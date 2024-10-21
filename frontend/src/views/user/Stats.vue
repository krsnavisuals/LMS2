<template>
  <div class="container mt-4">
    <h1 class="mb-4">User Dashboard</h1>
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
              <h5 class="card-title">Top Requested eBooks</h5>
              <canvas ref="topRequestedChart"></canvas>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Borrowing History</h5>
              <canvas ref="borrowingHistoryChart"></canvas>
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
                  v-for="(request, index) in stats.active_requests"
                  :key="index"
                  class="list-group-item"
                >
                  {{ request.name }} - Requested on
                  {{ new Date(request.request_date).toLocaleDateString() }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Overdue Books</h5>
              <ul class="list-group">
                <li
                  v-for="(book, index) in stats.overdue_books"
                  :key="index"
                  class="list-group-item text-danger"
                >
                  {{ book.name }} - Due on {{ new Date(book.return_date).toLocaleDateString() }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Recent Feedback</h5>
              <ul class="list-group">
                <li
                  v-for="(feedback, index) in stats.feedback_given.slice(0, 5)"
                  :key="index"
                  class="list-group-item"
                >
                  <strong>{{ feedback.name }}</strong
                  >: {{ feedback.feedback }}
                  <br />
                  <small class="text-muted">{{
                    new Date(feedback.feedback_date).toLocaleDateString()
                  }}</small>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Recently Added eBooks</h5>
              <ul class="list-group">
                <li
                  v-for="(book, index) in stats.recently_added_ebooks"
                  :key="index"
                  class="list-group-item"
                >
                  <strong>{{ book.name }}</strong> by {{ book.author }}
                  <br />
                  <small class="text-muted"
                    >Added on {{ new Date(book.date_issued).toLocaleDateString() }}</small
                  >
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
import { getUserStats, type UserStats } from '@/api/stats'
import Chart from 'chart.js/auto'

const stats = ref<UserStats | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const topRequestedChart = ref<HTMLCanvasElement | null>(null)
const borrowingHistoryChart = ref<HTMLCanvasElement | null>(null)

const fetchStats = async () => {
  try {
    stats.value = await getUserStats()
    loading.value = false
  } catch (err) {
    error.value = 'Failed to fetch user stats'
    loading.value = false
  }
}

const createCharts = () => {
  if (stats.value) {
    new Chart(topRequestedChart.value!, {
      type: 'bar',
      data: {
        labels: stats.value.top_requested_ebooks.map((item) => item.name),
        datasets: [
          {
            label: 'Request Count',
            data: stats.value.top_requested_ebooks.map((item) => item.request_count),
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

    new Chart(borrowingHistoryChart.value!, {
      type: 'line',
      data: {
        labels: stats.value.borrowing_history.map((item) =>
          new Date(item.request_date).toLocaleDateString()
        ),
        datasets: [
          {
            label: 'Borrowed Books',
            data: stats.value.borrowing_history.map((_, index) => index + 1),
            borderColor: 'rgba(255, 99, 132, 1)',
            tension: 0.1
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1
            }
          }
        }
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
