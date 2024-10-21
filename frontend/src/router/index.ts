import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LibrarianLogin from '@/views/librarian/Login.vue'
import LibrarianDashboard from '@/views/librarian/Dashboard.vue'
import LibrarianEbookDashboard from '@/views/librarian/EbookDashboard.vue'
import LibrarianRequest from '@/views/librarian/Request.vue'
import LibrarianStats from '@/views/librarian/Stats.vue'
import LibrarianSectionForm from '@/views/librarian/forms/Section.vue'
import LibrarianEbookForm from '@/views/librarian/forms/Ebook.vue'
import LibrarianSectionDetail from '@/views/librarian/SectionDetail.vue'
import LibrarianEbookDetail from '@/views/librarian/EbookDetail.vue'

import UserLogin from '@/views/user/Login.vue'
import UserCatalog from '@/views/user/EbookCatalog.vue'
import UserRequest from '@/views/user/EbookRequest.vue'
import UserMyEbooks from '@/views/user/MyEbooks.vue'
import UserEbookDetail from '@/views/user/EbookDetail.vue'
import UserStats from '@/views/user/Stats.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/user-login'
    },
    {
      path: '/user-login',
      name: 'UserLogin',
      component: UserLogin
    },
    {
      path: '/librarian-login',
      name: 'LibrarianLogin',
      component: LibrarianLogin
    },
    {
      path: '/user',
      meta: { role: 'user' },
      children: [
        {
          path: '',
          redirect: { name: 'UserCatalog' }
        },
        {
          path: 'catalog',
          name: 'UserCatalog',
          component: UserCatalog
        },
        {
          path: 'request/:ebookId',
          name: 'UserRequest',
          component: UserRequest
        },
        {
          path: 'my-ebooks',
          name: 'UserMyEbooks',
          component: UserMyEbooks
        },
        {
          path: 'section/:sectionId/ebook/:ebookId',
          name: 'UserEbookDetail',
          component: UserEbookDetail,
          props: true
        },
        {
          path: 'stats',
          name: 'UserStats',
          component: UserStats
        }
      ]
    },
    {
      path: '/librarian',
      meta: { role: 'librarian' },
      children: [
        {
          path: '',
          redirect: { name: 'LibrarianDashboard' }
        },
        {
          path: 'dashboard',
          name: 'LibrarianDashboard',
          component: LibrarianDashboard
        },
        {
          path: 'ebook-dashboard',
          name: 'LibrarianEbookDashboard',
          component: LibrarianEbookDashboard
        },
        {
          path: 'request',
          name: 'LibrarianRequest',
          component: LibrarianRequest
        },
        {
          path: 'stats',
          name: 'LibrarianStats',
          component: LibrarianStats
        },
        {
          path: 'section',
          children: [
            {
              path: 'create',
              name: 'LibrarianSectionCreate',
              component: LibrarianSectionForm
            },
            {
              path: ':sectionId',
              name: 'LibrarianSectionDetail',
              component: LibrarianSectionDetail,
              props: true
            },
            {
              path: 'update/:sectionId',
              name: 'LibrarianSectionUpdate',
              component: LibrarianSectionForm,
              props: true
            }
          ]
        },
        {
          path: 'section/:sectionId/ebook',
          children: [
            {
              path: 'create',
              name: 'LibrarianEbookCreate',
              component: LibrarianEbookForm,
              props: true
            },
            {
              path: 'update/:ebookId',
              name: 'LibrarianEbookUpdate',
              component: LibrarianEbookForm,
              props: true
            },
            {
              path: ':ebookId',
              name: 'LibrarianEbookDetail',
              component: LibrarianEbookDetail,
              props: true
            }
          ]
        }
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  console.log('authStore.user:', authStore.user)
  console.log('to.meta.role:', to.meta.role)

  // Check if the route requires a specific role
  if (to.meta.role) {
    const userRole = authStore.user?.role // Ensure user and role are defined

    if (userRole === to.meta.role) {
      next() // User has the required role, proceed
    } else if (to.meta.role === 'librarian') {
      next({ name: 'LibrarianLogin' }) // Redirect to the librarian login page
    } else if (to.meta.role === 'user') {
      next({ name: 'UserLogin' }) // Redirect to the user login page
    }

    if (userRole === 'user' && (!to.meta.role || to.meta.role != 'user')) {
      next({ name: 'UserCatalog' })
    }

    if (userRole === 'librarian' && (!to.meta.role || to.meta.role != 'librarian')) {
      next({ name: 'LibrarianDashboard' })
    }
  } else {
    next() // Proceed if no role is required
  }
})

export default router
