<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, getUserIdFromToken } from '../services/api'

const router = useRouter()
const longUrl = ref('')
const urls = ref([])
const loading = ref(false)
const createLoading = ref(false)
const error = ref('')
const userId = ref(null)

// Fetch URLs on mount
const fetchUrls = async () => {
  if (!userId.value) return
  
  loading.value = true
  try {
    const response = await api.get(`/urls/${userId.value}`)
    urls.value = response.data
  } catch (err) {
    console.error("Erro ao buscar URLs", err)
  } finally {
    loading.value = false
  }
}

const shortenUrl = async () => {
  error.value = ""
  if (!longUrl.value) {
    error.value = "Informe uma URL"
    return
  }
  
  if (!userId.value) {
    error.value = "Usuário não autenticado"
    return
  }

  try {
    createLoading.value = true
    const response = await api.post(`/urls/${userId.value}`, {
      long_url: longUrl.value,
    })
    
    // Refresh list
    await fetchUrls()
    longUrl.value = ''
  } catch (err) {
    console.error("Erro ao criar URL", err)
    error.value = "Erro ao encurtar. Tente novamente."
  } finally {
    createLoading.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}

// Helper to format/construct URL if needed
// If backend doesn't return full short_url, construct it.
// Based on previous App.vue, it seemed to return an ID.
const getShortUrl = (urlObj) => {
    if (urlObj.short_url) return urlObj.short_url
    // Fallback based on App.vue logic
    return `http://127.0.0.1:8000/${urlObj.short_code || urlObj.id}`
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text)
  // Could add a toast notification here
}

onMounted(() => {
  userId.value = getUserIdFromToken()
  if (userId.value) {
    fetchUrls()
  } else {
    router.push('/login')
  }
})
</script>

<template>
  <div class="dashboard">
    <!-- Header -->
    <header class="header glass-panel">
      <div class="logo">
        <span class="icon">🔗</span>
        <span class="text">Encurtador</span>
      </div>
      <button @click="logout" class="logout-btn">Sair</button>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      
      <!-- Creation Section -->
      <section class="create-section">
        <div class="glass-panel create-card">
          <h2>Nova URL Curta</h2>
          <div class="input-group">
            <input 
              v-model="longUrl" 
              type="url" 
              placeholder="Cole sua URL longa aqui (https://...)" 
            />
            <button @click="shortenUrl" :disabled="createLoading">
              {{ createLoading ? '...' : 'Encurtar' }}
            </button>
          </div>
          <p v-if="error" class="error-message">{{ error }}</p>
        </div>
      </section>

      <!-- List Section -->
      <section class="list-section">
        <h3>Suas URLs</h3>
        
        <div v-if="loading" class="loading">Carregando...</div>
        
        <div v-else-if="urls.length === 0" class="empty-state">
          Nenhuma URL criada ainda.
        </div>
        
        <div v-else class="url-grid">
            <div v-for="url in urls" :key="url.id" class="glass-panel url-card">
              <div class="card-header">
                <a :href="getShortUrl(url)" target="_blank" class="short-link">
                    {{ getShortUrl(url) }}
                </a>
                <button class="copy-btn" @click="copyToClipboard(getShortUrl(url))" title="Copiar">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                  </svg>
                </button>
              </div>
              <div class="long-link" :title="url.long_url">
                {{ url.long_url }}
              </div>
              <div class="card-footer">
                <span class="views">{{ url.clicks || 0 }} cliques</span>
                <span class="date">{{ new Date(url.created_at).toLocaleDateString() }}</span>
              </div>
            </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding: 15px 30px;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logout-btn {
  width: auto;
  background: transparent;
  border: 1px solid var(--border-color);
}

.logout-btn:hover {
  background: rgba(255,255,255,0.1);
}

.create-section {
  max-width: 800px;
  margin: 0 auto 60px;
}

.create-card {
  text-align: center;
}

.create-card h2 {
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  gap: 10px;
}

.input-group input {
  flex: 1;
}

.input-group button {
  width: auto;
  min-width: 120px;
}

.list-section h3 {
  margin-bottom: 20px;
  font-size: 1.5rem;
}

.url-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.url-card {
  padding: 20px;
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.url-card:hover {
  transform: translateY(-5px);
  border-color: var(--primary-color);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.short-link {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--success-color); /* Greenish for active link */
}

.copy-btn {
  background: transparent;
  width: auto;
  padding: 5px;
  font-size: 1.2rem;
}

.copy-btn:hover {
  background: rgba(255,255,255,0.1);
  transform: none;
}

.long-link {
  color: var(--text-muted);
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--text-muted);
  padding-top: 10px;
  border-top: 1px solid var(--border-color);
}

.empty-state {
    text-align: center;
    color: var(--text-muted);
    padding: 40px;
}
</style>
