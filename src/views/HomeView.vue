<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Bienvenue sur <span class="highlight">FreelanceCAM</span></h1>
        <p class="hero-subtitle">
          La plateforme qui connecte les talents freelances avec les meilleures opportunités.
          Trouvez votre prochain projet ou découvrez des experts pour réaliser vos idées.
        </p>
        <div class="hero-actions" v-if="!currentUser">
          <router-link to="/register">
            <button class="btn btn-primary">Commencer gratuitement</button>
          </router-link>
          <router-link to="/login">
            <button class="btn btn-secondary">Se connecter</button>
          </router-link>
        </div>
        <div class="hero-actions" v-else>
          <router-link to="/dashboard">
            <button class="btn btn-primary">Accéder à mon espace</button>
          </router-link>
        </div>
      </div>
      <div class="hero-visual">
        <div class="visual-placeholder">
          <div class="floating-card card-1">
            <div class="card-icon">💼</div>
            <p>Projets</p>
          </div>
          <div class="floating-card card-2">
            <div class="card-icon">⭐</div>
            <p>Évaluations</p>
          </div>
          <div class="floating-card card-3">
            <div class="card-icon">🚀</div>
            <p>Croissance</p>
          </div>
          <div class="main-visual">
            <div class="visual-icon">👨‍💻👩‍💻</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title">Pourquoi choisir FreelanceHub ?</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Matching Intelligent</h3>
            <p>Notre algorithme vous connecte avec les projets qui correspondent parfaitement à vos compétences.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Processus Rapide</h3>
            <p>De la candidature au paiement, tout est optimisé pour gagner du temps.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <h3>Sécurisé</h3>
            <p>Paiements sécurisés et protection des deux parties pendant tout le projet.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Croissance</h3>
            <p>Développez votre réputation et accédez à des projets plus prestigieux.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- For Freelancers Section -->
    <section class="audience-section">
      <div class="container">
        <div class="audience-content">
          <div class="audience-text">
            <h2>Pour les <span class="highlight">Freelances</span></h2>
            <ul class="benefits-list">
              <li>✅ Trouvez des projets qui correspondent à vos compétences</li>
              <li>✅ Fixez vos propres tarifs et conditions</li>
              <li>✅ Développez votre portfolio et votre réputation</li>
              <li>✅ Recevez des paiements sécurisés</li>
              <li>✅ Travaillez avec des clients vérifiés</li>
            </ul>
            <div v-if="!currentUser">
              <router-link to="/register">
                <button class="btn btn-primary">Devenir Freelance</button>
              </router-link>
            </div>
          </div>
          <div class="audience-visual">
            <div class="visual-placeholder freelance">
              <div class="icon">👨‍💻</div>
              <p>Rejoignez notre communauté de talents</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- For Clients Section -->
    <section class="audience-section client-section">
      <div class="container">
        <div class="audience-content reverse">
          <div class="audience-text">
            <h2>Pour les <span class="highlight">Clients</span></h2>
            <ul class="benefits-list">
              <li>✅ Accédez à des milliers de freelances qualifiés</li>
              <li>✅ Trouvez le bon talent en quelques clics</li>
              <li>✅ Gérez vos projets simplement</li>
              <li>✅ Paiements sécurisés et satisfaction garantie</li>
              <li>✅ Support dédié pour vos projets</li>
            </ul>
            <div v-if="!currentUser">
              <router-link to="/register">
                <button class="btn btn-primary">Trouver un Freelance</button>
              </router-link>
            </div>
          </div>
          <div class="audience-visual">
            <div class="visual-placeholder client">
              <div class="icon">🏢</div>
              <p>Des experts pour chaque besoin</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">5000+</div>
            <div class="stat-label">Freelances actifs</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">12000+</div>
            <div class="stat-label">Projets réalisés</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">98%</div>
            <div class="stat-label">Taux de satisfaction</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">2M€+</div>
            <div class="stat-label">Volume de transactions</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section" v-if="!currentUser">
      <div class="container">
        <div class="cta-content">
          <h2>Prêt à commencer ?</h2>
          <p>Rejoignez des milliers de freelances et clients qui font grandir leurs projets.</p>
          <div class="cta-actions">
            <router-link to="/register">
              <button class="btn btn-large btn-primary">Créer un compte gratuit</button>
            </router-link>
            <router-link to="/login">
              <button class="btn btn-large btn-secondary">Se connecter</button>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="home-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <h3>FreelanceHub</h3>
            <p>Votre succès, notre mission.</p>
          </div>
          <div class="footer-links">
            <div class="link-group">
              <h4>Plateforme</h4>
              <a href="#">À propos</a>
              <a href="#">Fonctionnalités</a>
              <a href="#">Tarifs</a>
            </div>
            <div class="link-group">
              <h4>Support</h4>
              <a href="#">Centre d'aide</a>
              <a href="#">Contact</a>
              <a href="#">Mentions légales</a>
            </div>
            <div class="link-group">
              <h4>Communauté</h4>
              <a href="#">Blog</a>
              <a href="#">Témoignages</a>
              <a href="#">Événements</a>
            </div>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; 2024 FreelanceHub. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  props: ['currentUser']
};
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

/* Hero Section */
.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  min-height: 80vh;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.highlight {
  color: #4f46e5;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.875rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.btn-primary {
  background: #4f46e5;
  color: white;
}

.btn-primary:hover {
  background: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
}

.btn-secondary {
  background: transparent;
  color: #4f46e5;
  border: 2px solid #4f46e5;
}

.btn-secondary:hover {
  background: #4f46e5;
  color: white;
  transform: translateY(-2px);
}

.btn-large {
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
}

.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.visual-placeholder {
  position: relative;
  width: 400px;
  height: 300px;
}

.main-visual {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.visual-icon {
  font-size: 4rem;
}

.floating-card {
  position: absolute;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 120px;
  animation: float 3s ease-in-out infinite;
}

.card-1 {
  top: 10%;
  left: 0;
  animation-delay: 0s;
}

.card-2 {
  top: 20%;
  right: 0;
  animation-delay: 1s;
}

.card-3 {
  bottom: 20%;
  left: 10%;
  animation-delay: 2s;
}

.card-icon {
  font-size: 1.5rem;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Features Section */
.features-section {
  padding: 6rem 2rem;
  background: #f8fafc;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 4rem;
  color: #1f2937;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1f2937;
}

.feature-card p {
  color: #6b7280;
  line-height: 1.6;
}

/* Audience Sections */
.audience-section {
  padding: 6rem 2rem;
}

.audience-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.audience-content.reverse {
  direction: rtl;
}

.audience-content.reverse > * {
  direction: ltr;
}

.audience-text h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: #1f2937;
}

.benefits-list {
  list-style: none;
  padding: 0;
  margin-bottom: 2.5rem;
}

.benefits-list li {
  padding: 0.5rem 0;
  font-size: 1.125rem;
  color: #4b5563;
}

.audience-visual {
  display: flex;
  justify-content: center;
}

.visual-placeholder.freelance,
.visual-placeholder.client {
  width: 300px;
  height: 250px;
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.visual-placeholder.client {
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
}

.visual-placeholder .icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.client-section {
  background: #f8fafc;
}

/* Stats Section */
.stats-section {
  padding: 4rem 2rem;
  background: #1f2937;
  color: white;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  text-align: center;
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: #4f46e5;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.125rem;
  color: #d1d5db;
}

/* CTA Section */
.cta-section {
  padding: 6rem 2rem;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  text-align: center;
}

.cta-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.cta-content p {
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  opacity: 0.9;
}

.cta-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-section .btn-primary {
  background: white;
  color: #4f46e5;
}

.cta-section .btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.cta-section .btn-secondary:hover {
  background: white;
  color: #4f46e5;
}

/* Footer */
.home-footer {
  background: #111827;
  color: white;
  padding: 4rem 2rem 2rem;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 4rem;
  margin-bottom: 3rem;
}

.footer-brand h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #4f46e5;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.link-group h4 {
  margin-bottom: 1rem;
  color: #f3f4f6;
}

.link-group a {
  display: block;
  color: #d1d5db;
  text-decoration: none;
  margin-bottom: 0.5rem;
  transition: color 0.3s;
}

.link-group a:hover {
  color: #4f46e5;
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid #374151;
  color: #9ca3af;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 2rem 1rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-actions {
    justify-content: center;
  }

  .audience-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .footer-links {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .visual-placeholder {
    width: 100%;
    max-width: 300px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .cta-actions {
    flex-direction: column;
    align-items: center;
  }

  .btn {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .floating-card {
    position: relative;
    margin: 0.5rem;
    animation: none;
  }

  .visual-placeholder {
    height: auto;
    padding: 2rem 0;
  }
}
</style>