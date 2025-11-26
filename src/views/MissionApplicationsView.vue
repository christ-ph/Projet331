<template>
  <div class="mission-applications-view">

    <div class="applications-container" v-if="showDetails">

      <h2 class="title">📨 Candidatures reçues pour la mission sélectionnée</h2>

      <button @click="hideDetails" class="btn btn-secondary btn-small back-button">
        Retour à la liste des missions
      </button>

      <div v-if="applications.length === 0" class="empty">
        Aucune candidature pour le moment.
      </div>

      <div v-else class="applications-list">
        <div 
          v-for="app in applications" 
          :key="app.id" 
          class="application-card"
        >
          <div class="application-header">
            <h3>{{ app.freelance_name }}</h3>
            <p class="email">{{ app.freelance_email }}</p>
          </div>
          <div class="application-body">
            <p><strong>💬 Proposition :</strong> {{ app.proposal }}</p>
            <p><strong>💰 Budget proposé :</strong> 
              {{ formatBudget(app.proposed_budget) }}
            </p>
            <p><strong>📅 Date :</strong> 
              {{ formatDate(app.created_at) }}
            </p>
            <p><strong>📌 Statut :</strong>
              <span class="status">{{ app.status }}</span>
            </p>
            <p><strong>⭐ Note freelance :</strong>
              {{ app.freelancer_rating ?? "—" }}
            </p>
            <p><strong>📝 Avis :</strong>
              {{ app.freelancer_reviews_count }} avis
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="missions-container" v-else>

      <h2 class="title">📌 Missions & Candidatures reçues</h2>

      <div v-if="missions.length === 0 " class="empty">
        Aucune mission n'a encore reçu de candidatures.
      </div>

      <div v-else class="missions-list">

        <div 
          v-for="mission in missions" 
          :key="mission.id" 
          class="mission-card"
        >
          <h3>{{ mission.title }}</h3>
          <p>{{ mission.description }}</p>
          <p><strong>Statut :</strong> {{ mission.status }}</p>
          <p><strong>📅 Créée le :</strong> {{ formatDate(mission.created_at) }}</p>

          <h4>📨 Candidatures reçues ({{ mission.applications_count }})</h4>

          <div v-if="mission.applications.length === 0" class="empty-app">
            Aucune candidature pour cette mission.
          </div>

          <div v-else class="applications-list">
            <div 
              v-for="app in mission.applications" 
              :key="app.id" 
              class="application-card"
            >
              <p><strong>👤 Freelance :</strong> {{ app.freelance_name }}</p>
              <p><strong>💬 Proposition :</strong> {{ app.proposal }}</p>
              <p><strong>💰 Budget proposé :</strong> {{ formatBudget(app.proposed_budget) }}</p>
              <p><strong>📌 Statut :</strong> {{ app.status }}</p>
              <p><strong>📅 Date :</strong> {{ formatDate(app.created_at) }}</p>

              <div class="application-actions">
                <button @click="acceptApplication(mission.id, app.id)" class="btn btn-success btn-small">
                  ✅ Accepter
                </button>
                <button @click="rejectApplication(mission.id, app.id)" class="btn btn-danger btn-small">
                  ❌ Refuser
                </button>
                <button @click="openDiscussion(app.freelance_id)" class="btn btn-primary btn-small">
                  💬 Discussion
                </button>
                <button @click="viewMission(mission.id)" class="btn btn-info btn-small">
                  🔍 Voir Détails
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { 
  getMissions, 
  getMissionApplications,
  getClientMissionsAppliedByFreelance,
  updateApplicationStatus 
} from '@/services/api';

export default {
  name: 'MissionsApplicationsView',
  props: ['currentUser'],

  data() {
    return {
      showDetails: false,
      successMessage: "",
      errorMessage: "",
      latestOffers: [],
      applications: [],
      missions: [] 
    };
  },

  methods: {
    // -----------------------
    // ✔ Récupère les dernières missions
    // -----------------------
    async fetchLatestOffers() {
      try {
        const response = await getMissions();
        this.latestOffers = response.data;
      } catch (error) {
        console.error('Error fetching latest offers:', error);
      }
    },

    // -----------------------
    // ✔ Récupère missions + candidatures du client
    // -----------------------
    async fetchClientMissions() {
      try {
        const clientId =
          this.currentUser?.id || localStorage.getItem("user_id");

        const response =
          await getClientMissionsAppliedByFreelance(clientId);

        this.missions = response.data.missions_with_applications || [];
      } catch (error) {
        console.error("Erreur chargement missions :", error);
        this.errorMessage = "Impossible de charger les missions.";
      }
    },

    // -----------------------
    // ✔ Voir les candidatures d'une mission
    // -----------------------
    async viewMission(missionId) {
      this.showDetails = true;
      try {
        const response = await getMissionApplications(missionId);
        console.log("Applications reçues :", response.data);
        this.applications = response.data.applications;
        
        // Debug: Vérifier les budgets
        this.applications.forEach((app, index) => {
          console.log(`App ${index} - proposed_budget:`, app.proposed_budget, "Type:", typeof app.proposed_budget);
        });
      } catch (error) {
        console.error("Error fetching mission applications:", error);
      }
    },

    // -----------------------
    // ✔ Formater date
    // -----------------------
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    // -----------------------
    // ✔ NOUVELLE MÉTHODE : Formater le budget
    // -----------------------
    formatBudget(budget) {
      if (budget === null || budget === undefined || budget === '') {
        return "Non spécifié";
      }
      
      // Convertir en nombre si c'est une chaîne
      const budgetNumber = Number(budget);
      
      if (isNaN(budgetNumber)) {
        return "Montant invalide";
      }
      
      // Formater avec 2 décimales
      return `${budgetNumber.toFixed(2)} €`;
    },

    // -----------------------
    // ✔ Accepter une candidature
    // -----------------------
    async acceptApplication(missionId, appId) {
      try {
        console.log(`[DEBUG] Acceptation appId ${appId}`);

        const response = await updateApplicationStatus(appId, { 
          status: "ACCEPTED" 
        });

        this.successMessage = response.data.message;
        alert(this.successMessage);

        await this.fetchClientMissions();

      } catch (error) {
        console.error("Erreur acceptation :", error.response || error);
        this.errorMessage = "Impossible d'accepter la candidature.";
      }
    },

    // -----------------------
    // ✔ Refuser une candidature
    // -----------------------
    async rejectApplication(missionId, appId) {
      try {
        console.log(`[DEBUG] Rejet appId ${appId}`);

        const response = await updateApplicationStatus(appId, { 
          status: "REJECTED" 
        });

        this.successMessage = response.data.message;
        alert(this.successMessage);

        await this.fetchClientMissions();

      } catch (error) {
        console.error("Erreur refus :", error.response || error);
        this.errorMessage = "Impossible de refuser la candidature.";
      }
    },

    hideDetails() {
      this.showDetails = false;
      this.applications = []; // Vider les données détaillées
      this.fetchClientMissions();
    },

    // -----------------------
    // ✔ Discussion avec un freelance
    // -----------------------
    openDiscussion(freelanceId) {
      this.$router.push(`/messages/${freelanceId}`);
    },

  },

  mounted() {
    this.fetchClientMissions();
    this.fetchLatestOffers();
  }
};
</script>


<style scoped>
/* ----------------------------------- */
/* 1. LAYOUT GÉNÉRAL ET CONTENEURS */
/* ----------------------------------- */
.mission-applications-view {
  padding: 30px;
  background-color: #f8f9fa; /* Arrière-plan léger */
  min-height: 85vh; /* Assure que le conteneur couvre la page */
}

.title {
  font-size: 1.8em;
  color: #343a40;
  margin-bottom: 25px;
  border-bottom: 3px solid #007bff; /* Soulignement bleu */
  padding-bottom: 10px;
  display: inline-block;
}

.back-button {
  margin-bottom: 20px;
  background-color: #6c757d;
  color: white;
  border: none;
}

.empty {
  padding: 40px;
  text-align: center;
  font-size: 1.2em;
  color: #6c757d;
  border: 1px dashed #ced4da;
  border-radius: 8px;
  margin-top: 20px;
}

/* ----------------------------------- */
/* 2. LISTE DES MISSIONS (Vue Principale) */
/* ----------------------------------- */
.missions-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); /* 2 ou 3 colonnes flexibles */
  gap: 30px;
}

.mission-card {
  background-color: white;
  border: 1px solid #e9ecef;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s;
}

.mission-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.mission-card h3 {
  color: #007bff;
  margin-top: 0;
  margin-bottom: 10px;
}

.mission-card h4 {
  color: #495057;
  border-top: 1px solid #e9ecef;
  padding-top: 15px;
  margin-top: 20px;
  margin-bottom: 15px;
  font-size: 1.1em;
}

.empty-app {
  font-style: italic;
  color: #adb5bd;
  padding: 10px 0;
}

/* ----------------------------------- */
/* 3. LISTE ET CARTE DES CANDIDATURES */
/* ----------------------------------- */
.applications-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.application-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  background-color: #f1f3f5;
}

/* Styles spécifiques pour la vue détaillée (applications-container) */
.applications-container .application-card {
    background-color: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.application-header h3 {
  color: #212529;
  margin: 0 0 5px 0;
}

.application-header .email {
  font-size: 0.9em;
  color: #6c757d;
  margin-bottom: 10px;
}

.application-body strong {
    color: #495057;
}

.status {
  font-weight: bold;
  padding: 2px 8px;
  border-radius: 4px;
  display: inline-block;
  margin-left: 5px;
}

.status[v-text="ACCEPTED"] { /* Cible le statut ACCEPTED (si possible) */
  background-color: #d4edda;
  color: #155724;
}

.status[v-text="REJECTED"] { /* Cible le statut REJECTED (si possible) */
  background-color: #f8d7da;
  color: #721c24;
}

/* ----------------------------------- */
/* 4. ACTIONS ET BOUTONS */
/* ----------------------------------- */
.application-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px dashed #ced4da;
}

button {
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.2s, transform 0.1s;
}

.btn-small {
  padding: 7px 12px;
  font-size: 0.85em;
  font-weight: 500;
}

.btn-success {
  background-color: #28a745;
  color: white;
}
.btn-success:hover {
  background-color: #218838;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}
.btn-danger:hover {
  background-color: #c82333;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}
.btn-primary:hover {
  background-color: #0056b3;
}

.btn-info {
  background-color: #17a2b8;
  color: white;
}
.btn-info:hover {
  background-color: #138496;
}
</style>