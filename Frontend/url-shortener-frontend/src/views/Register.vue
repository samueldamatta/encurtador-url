<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

const handleRegister = async () => {
  error.value = ''
  
  if (password.value !== confirmPassword.value) {
    error.value = 'As senhas não coincidem.'
    return
  }
  
  loading.value = true
  
  try {
    await api.post('/auth/register', {
      email: email.value,
      password: password.value
    })
    
    // Redirect to login after successful registration
    router.push('/login')
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Erro ao criar conta.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-container">
    <div class="glass-panel auth-card">
      <h1 class="auth-title">Crie sua conta</h1>
      <p class="auth-subtitle">Comece a encurtar URLs gratuitamente</p>
      
      <form @submit.prevent="handleRegister">
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
        
        <div class="form-group">
          <label class="form-label" for="confirmPassword">Confirmar Senha</label>
          <input 
            id="confirmPassword" 
            v-model="confirmPassword" 
            type="password" 
            placeholder="••••••••" 
            required 
          />
        </div>
        
        <p v-if="error" class="error-message">{{ error }}</p>
        
        <button type="submit" :disabled="loading" style="margin-top: 1rem">
          {{ loading ? 'Criando conta...' : 'Cadastrar' }}
        </button>
      </form>
      
      <p style="text-align: center; margin-top: 1.5rem; color: var(--text-muted); font-size: 0.9rem">
        Já tem uma conta? 
        <router-link to="/login">Entrar</router-link>
      </p>
    </div>
  </div>
</template>
