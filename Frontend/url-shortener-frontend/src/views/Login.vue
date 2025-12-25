<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  
  try {
    const response = await api.post('/auth/login', { 
      email: email.value, 
      password: password.value 
    })
    
    // Response includes access_token and refresh_token
    const { access_token, refresh_token } = response.data
    if (access_token && refresh_token) {
      localStorage.setItem('token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      router.push('/')
    } else {
      error.value = "Token não recebido. Verifique o backend."
    }
  } catch (err) {
    if (err.response && err.response.status === 401) {
      error.value = 'Credenciais inválidas.'
    } else {
      error.value = 'Erro ao fazer login. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-container">
    <div class="glass-panel auth-card">
      <h1 class="auth-title">Bem vindo de volta</h1>
      <p class="auth-subtitle">Entre para gerenciar seus links</p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label" for="email">Email</label>
          <input 
            id="email" 
            v-model="email" 
            type="email" 
            placeholder="seu@email.com" 
            required 
          />
        </div>
        
        <div class="form-group">
          <label class="form-label" for="password">Senha</label>
          <input 
            id="password" 
            v-model="password" 
            type="password" 
            placeholder="••••••••" 
            required 
          />
        </div>
        
        <p v-if="error" class="error-message">{{ error }}</p>
        
        <button type="submit" :disabled="loading" style="margin-top: 1rem">
          {{ loading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
      
      <p style="text-align: center; margin-top: 1.5rem; color: var(--text-muted); font-size: 0.9rem">
        Não tem uma conta? 
        <router-link to="/register">Crie uma agora</router-link>
      </p>
    </div>
  </div>
</template>
