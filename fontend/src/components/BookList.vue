<script setup>
import { ref, onMounted } from 'vue'

const books = ref([])
const chargement = ref(true)
const erreur = ref(null)

const recupererLivres = async () => {
  try {
    const response = await fetch('http://localhost:5000/books/')
    if (!response.ok) throw new Error('Erreur serveur')
    books.value = await response.json()
  } catch (e) {
    erreur.value = "Impossible de charger les livres."
  } finally {
    chargement.value = false
  }
}

onMounted(() => {
  recupererLivres()
})
</script>

<template>
  <div class="container">
    <h1 class="page-title">Tous les livres</h1>

    <div v-if="chargement" class="msg">Chargement...</div>
    <div v-else-if="erreur" class="msg error">{{ erreur }}</div>

    <div v-else class="gallery-grid">
      
      <div v-for="book in books" :key="book.id" class="book-item">
        
        <img 
          v-if="book.cover_url" 
          :src="book.cover_url" 
          :alt="book.title" 
          class="cover-img"
        />
        
        <div v-else class="no-cover">
            <span>{{ book.title }}</span>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'Inter', sans-serif;
}

.page-title {
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin-bottom: 50px;
  color: #333;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

.book-item {
  border-radius: 8px;
  overflow: hidden; 
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
  
  aspect-ratio: 2 / 3;
}

.book-item:hover {
  transform: scale(1.03); 
  box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

/* 4. L'IMAGE */
.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* L'image remplit tout l'espace sans être déformée */
  display: block;
}

/* 5. LE BACKUP (Si pas d'image) */
.no-cover {
  width: 100%;
  height: 100%;
  background-color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 10px;
  color: #555;
  font-weight: bold;
}

.msg { text-align: center; color: #888; margin-top: 50px; }
.error { color: red; }
</style>