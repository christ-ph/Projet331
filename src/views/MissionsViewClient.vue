<template>
  <div class="mission-client">
    <div class="profile-header">
      <div class="header-content">
        <h1>🧾 Créer une mission</h1>
        <p>Décrivez votre mission pour trouver le freelance parfait.</p>
      </div>
      <div class="completion-badge" v-if="completionPercentage < 100">
        <div class="progress-circle">
          <span class="percentage">{{ completionPercentage }}%</span>
        </div>
        <p>Formulaire complété à {{ completionPercentage }}%</p>
      </div>
    </div>

    <div class="profile-container">
      <!-- Formulaire de création de mission -->
      <form @submit.prevent="submitMission" class="profile-form">
        
        <!-- Informations générales -->
        <div class="form-section">
          <div class="section-header">
            <h2>📋 Informations de la mission</h2>
            <span class="section-badge" v-if="mission.title && mission.description">✅</span>
          </div>
          <div class="form-group">
            <label for="title">Titre de la mission *</label>
            <input 
              v-model="mission.title" 
              id="title" 
              placeholder="Ex: Développement d'une API Flask"
              required
            />
          </div>
          <div class="form-group">
            <label for="description">Description *</label>
            <textarea
              v-model="mission.description"
              id="description"
              placeholder="Décrivez les objectifs, les livrables et les attentes..."
              rows="5"
              required
            ></textarea>
            <small>{{ mission.description.length }}/500 caractères</small>
          </div>
        </div>

        <!-- Budget et Deadline -->
        <div class="form-section">
          <div class="section-header">
            <h2>💰 Budget et échéance</h2>
            <span class="section-badge" v-if="mission.budget && mission.deadline">✅</span>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label for="budget">Budget (€) *</label>
              <div class="input-with-icon">
                <span class="input-icon">€</span>
                <input
                  v-model.number="mission.budget"
                  id="budget"
                  type="number"
                  min="0"
                  placeholder="2500"
                  required
                />
              </div>
              <small>Indiquez le budget total ou horaire prévu</small>
            </div>
            <div class="form-group">
              <label for="budget_type">Type de budget *</label>
              <select v-model="mission.budget_type" id="budget_type" required>
                <option value="FIXED">💼 Fixe</option>
                <option value="HOURLY">⏱ Horaire</option>
              </select>
            </div>
            <div class="form-group">
              <label for="deadline">Date limite *</label>
              <input v-model="mission.deadline" id="deadline" type="date" required />
            </div>
          </div>
        </div>

        <!-- Compétences requises -->
        <div class="form-section">
          <div class="section-header">
            <h2>🛠️ Compétences requises</h2>
            <span class="section-badge" v-if="mission.required_skills.length >= 1">✅</span>
          </div>
          <div class="form-group">
            <label>Ajouter des compétences *</label>
            <div class="skills-input-container">
              <input 
                v-model="newSkill" 
                @keydown.enter.prevent="addSkill"
                placeholder="Ex: Python, Flask, PostgreSQL..." 
                class="skills-input"
              />
              <button type="button" @click="addSkill" class="btn-add-skill" :disabled="!newSkill.trim()">+</button>
            </div>
            <small>Appuyez sur Entrée ou cliquez sur + pour ajouter</small>
          </div>
          <div v-if="mission.required_skills.length > 0" class="skills-list">
            <div v-for="(skill, index) in mission.required_skills" :key="index" class="skill-tag">
              <span>{{ skill }}</span>
              <button type="button" @click="removeSkill(index)" class="btn-remove-skill">×</button>
            </div>
          </div>
          <div v-else class="empty-state">
            <p>🚫 Aucune compétence ajoutée. Ajoutez-en au moins une.</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="form-actions">
          <button type="button" @click="resetForm" class="btn btn-secondary" :disabled="loading">
            Annuler
          </button>
          <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
            <span v-if="loading">
              <div class="spinner"></div>
              Publication...
            </span>
            <span v-else>
              🚀 Publier la mission
            </span>
          </button>
        </div>
      </form>

      <!-- Aperçu de la mission -->
      <div class="profile-preview">
        <div class="preview-card">
          <h3>Aperçu de la mission</h3>
          <div class="preview-content">
            <div class="preview-section">
              <h5>Titre</h5>
              <p>{{ mission.title || 'Titre de la mission' }}</p>
            </div>
            <div class="preview-section">
              <h5>Description</h5>
              <p class="preview-description">
                {{ mission.description || 'La description de votre mission apparaîtra ici...' }}
              </p>
            </div>
            <div class="preview-section">
              <h5>Budget</h5>
              <p class="preview-rate">{{ mission.budget || '---' }} € ({{ mission.budget_type }})</p>
            </div>
            <div class="preview-section">
              <h5>Échéance</h5>
              <p>{{ mission.deadline || 'Non définie' }}</p>
            </div>
            <div class="preview-section" v-if="mission.required_skills.length > 0">
              <h5>Compétences requises</h5>
              <div class="preview-skills">
                <span v-for="skill in mission.required_skills" :key="skill" class="preview-skill">
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateMissionClient',
  props: ['currentUser'],
  data() {
    return {
      mission: {
        title: '',
        description: '',
        budget: null,
        budget_type: 'FIXED',
        deadline: '',
        required_skills: []
      },
      newSkill: '',
      loading: false
    };
  },
  computed: {
    completionPercentage() {
      let completed = 0;
      const totalFields = 4;
      if (this.mission.title) completed++;
      if (this.mission.description) completed++;
      if (this.mission.budget && this.mission.deadline) completed++;
      if (this.mission.required_skills.length > 0) completed++;
      return Math.round((completed / totalFields) * 100);
    },
    isFormValid() {
      return (
        this.mission.title &&
        this.mission.description &&
        this.mission.budget &&
        this.mission.deadline &&
        this.mission.required_skills.length > 0
      );
    }
  },
  methods: {
    addSkill() {
      const skill = this.newSkill.trim();
      if (skill && !this.mission.required_skills.includes(skill)) {
        this.mission.required_skills.push(skill);
        this.newSkill = '';
      }
    },
    removeSkill(index) {
      this.mission.required_skills.splice(index, 1);
    },
    resetForm() {
      if (confirm('Voulez-vous vraiment réinitialiser ce formulaire ?')) {
        this.mission = {
          title: '',
          description: '',
          budget: null,
          budget_type: 'FIXED',
          deadline: '',
          required_skills: []
        };
      }
    },
    async submitMission() {
      if (!this.isFormValid) {
        alert('Veuillez compléter tous les champs obligatoires');
        return;
      }
      this.loading = true;
      try {
        const response = await axios.post('http://localhost:8000/missions', {
          ...this.mission,
          client_id: this.currentUser?.id || null
        });
        alert('✅ Mission publiée avec succès !');
        console.log('Mission créée:', response.data);
        this.$router.push('/dashboard-client');
      } catch (error) {
        console.error('Erreur création mission:', error);
        alert('❌ Erreur lors de la publication de la mission.');
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.mission-client {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* --- Styles identiques à ton FreelanceProfileView --- */
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.header-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.header-content p {
  color: #6b7280;
  font-size: 1.125rem;
  max-width: 600px;
}

.completion-badge {
  text-align: center;
}

.progress-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: conic-gradient(#10b981 0% v-bind('completionPercentage')0%, #e5e7eb 0% 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
  position: relative;
}

.progress-circle::before {
  content: '';
  position: absolute;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
}

.percentage {
  position: relative;
  font-weight: 700;
  color: #1f2937;
  font-size: 1.125rem;
}

/* Formulaire */
.profile-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  border: 1px solid #f3f4f6;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f8fafc;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.section-badge {
  background: #10b981;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  background: #fafafa;
  transition: all 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4f46e5;
  background: white;
  box-shadow: 0 0 0 3px rgba(79,70,229,0.1);
}

/* Skills */
.skills-input-container {
  display: flex;
  gap: 0.5rem;
}

.skills-input {
  flex: 1;
}

.btn-add-skill {
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  width: 48px;
  height: 48px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-add-skill:hover:not(:disabled) {
  background: #059669;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.skill-tag {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-remove-skill {
  background: none;
  border: none;
  color: #4f46e5;
  cursor: pointer;
  font-size: 1rem;
}

/* Aperçu */
.profile-preview {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.preview-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  padding: 2rem;
  border: 1px solid #e5e7eb;
}

.preview-card h3 {
  text-align: center;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.preview-section {
  margin-bottom: 1.5rem;
}

.preview-skill {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
}

/* Actions */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 1024px) {
  .profile-container {
    grid-template-columns: 1fr;
  }
}
</style>

