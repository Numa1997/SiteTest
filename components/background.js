/**
 * PhysicsParticleBackground
 *
 * A performance-optimized particle physics background system with:
 * - Realistic particle physics and collision detection
 * - Mouse interaction (attract/repel)
 * - Red glowing particles matching futuristic theme
 * - Mobile optimization and reduced motion support
 * - Page visibility API for performance
 */

class PhysicsParticleBackground {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d', { alpha: false });

    // Animation state
    this.isRunning = false;
    this.animationId = null;
    this.lastFrameTime = 0;

    // Mouse interaction
    this.mouse = {
      x: null,
      y: null,
      radius: 150
    };

    // Performance monitoring
    this.isMobile = this.detectMobile();
    this.isTabVisible = true;

    // Particle configuration
    this.particleCount = this.isMobile ? 30 : 80;
    this.particles = [];

    // Theme colors
    this.colors = {
      background: '#0a0a0a',
      particle: '#dc2626',
      glow: 'rgba(220, 38, 38, 0.4)',
      connection: 'rgba(220, 38, 38, 0.15)'
    };

    // Physics constants
    this.physics = {
      friction: 0.98,
      maxSpeed: 0.8,
      minSpeed: 0.1,
      collisionDamping: 0.9,
      mouseForce: 0.3,
      connectionDistance: 120
    };

    // Initialize
    this.setupCanvas();
    this.initParticles();
    this.setupEventListeners();
  }

  /**
   * Detect if device is mobile
   */
  detectMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
      || window.innerWidth < 768;
  }

  /**
   * Setup canvas dimensions
   */
  setupCanvas() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;

    // Set initial background
    this.ctx.fillStyle = this.colors.background;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
  }

  /**
   * Initialize particle array
   */
  initParticles() {
    this.particles = [];

    for (let i = 0; i < this.particleCount; i++) {
      this.particles.push(this.createParticle());
    }
  }

  /**
   * Create a single particle with random properties
   */
  createParticle() {
    const radius = Math.random() * 1.5 + 2; // 2-3.5px radius

    return {
      x: Math.random() * this.canvas.width,
      y: Math.random() * this.canvas.height,
      vx: (Math.random() - 0.5) * this.physics.maxSpeed,
      vy: (Math.random() - 0.5) * this.physics.maxSpeed,
      radius: radius,
      mass: radius, // Mass proportional to radius
      glow: Math.random() * 10 + 10 // 10-20px glow
    };
  }

  /**
   * Setup event listeners for interaction and optimization
   */
  setupEventListeners() {
    // Mouse movement for particle interaction
    this.canvas.addEventListener('mousemove', (e) => {
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;
    });

    this.canvas.addEventListener('mouseleave', () => {
      this.mouse.x = null;
      this.mouse.y = null;
    });

    // Touch support for mobile
    this.canvas.addEventListener('touchmove', (e) => {
      e.preventDefault();
      const touch = e.touches[0];
      this.mouse.x = touch.clientX;
      this.mouse.y = touch.clientY;
    }, { passive: false });

    this.canvas.addEventListener('touchend', () => {
      this.mouse.x = null;
      this.mouse.y = null;
    });

    // Window resize handler
    window.addEventListener('resize', () => this.resize());

    // Page visibility API for performance
    document.addEventListener('visibilitychange', () => {
      this.isTabVisible = !document.hidden;

      if (this.isTabVisible && this.isRunning) {
        this.lastFrameTime = performance.now();
      }
    });

    // Respect reduced motion preference
    const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (motionQuery.matches) {
      this.stop();
    }

    motionQuery.addEventListener('change', (e) => {
      if (e.matches) {
        this.stop();
      }
    });
  }

  /**
   * Start animation loop
   */
  start() {
    if (this.isRunning) return;

    this.isRunning = true;
    this.lastFrameTime = performance.now();
    this.animate();
  }

  /**
   * Stop animation loop
   */
  stop() {
    this.isRunning = false;

    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  /**
   * Handle window resize
   */
  resize() {
    this.setupCanvas();

    // Update mobile detection
    const wasMobile = this.isMobile;
    this.isMobile = this.detectMobile();

    // Reinitialize particles if mobile state changed
    if (wasMobile !== this.isMobile) {
      this.particleCount = this.isMobile ? 30 : 80;
      this.initParticles();
    }
  }

  /**
   * Main animation loop
   */
  animate() {
    if (!this.isRunning) return;

    const currentTime = performance.now();
    const deltaTime = Math.min((currentTime - this.lastFrameTime) / 16.67, 2); // Cap at 2x speed
    this.lastFrameTime = currentTime;

    // Only animate if tab is visible
    if (this.isTabVisible) {
      this.update(deltaTime);
      this.draw();
    }

    this.animationId = requestAnimationFrame(() => this.animate());
  }

  /**
   * Update particle positions and physics
   */
  update(deltaTime) {
    for (let i = 0; i < this.particles.length; i++) {
      const particle = this.particles[i];

      // Apply mouse interaction
      if (this.mouse.x !== null && this.mouse.y !== null) {
        const dx = this.mouse.x - particle.x;
        const dy = this.mouse.y - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < this.mouse.radius) {
          const force = (1 - distance / this.mouse.radius) * this.physics.mouseForce;
          const angle = Math.atan2(dy, dx);

          // Repel particles from mouse
          particle.vx -= Math.cos(angle) * force;
          particle.vy -= Math.sin(angle) * force;
        }
      }

      // Apply friction
      particle.vx *= this.physics.friction;
      particle.vy *= this.physics.friction;

      // Enforce speed limits
      const speed = Math.sqrt(particle.vx * particle.vx + particle.vy * particle.vy);
      if (speed > this.physics.maxSpeed) {
        particle.vx = (particle.vx / speed) * this.physics.maxSpeed;
        particle.vy = (particle.vy / speed) * this.physics.maxSpeed;
      } else if (speed < this.physics.minSpeed && speed > 0) {
        const boost = this.physics.minSpeed / speed;
        particle.vx *= boost;
        particle.vy *= boost;
      }

      // Update position
      particle.x += particle.vx * deltaTime;
      particle.y += particle.vy * deltaTime;

      // Bounce off edges
      if (particle.x - particle.radius < 0) {
        particle.x = particle.radius;
        particle.vx = Math.abs(particle.vx) * this.physics.collisionDamping;
      } else if (particle.x + particle.radius > this.canvas.width) {
        particle.x = this.canvas.width - particle.radius;
        particle.vx = -Math.abs(particle.vx) * this.physics.collisionDamping;
      }

      if (particle.y - particle.radius < 0) {
        particle.y = particle.radius;
        particle.vy = Math.abs(particle.vy) * this.physics.collisionDamping;
      } else if (particle.y + particle.radius > this.canvas.height) {
        particle.y = this.canvas.height - particle.radius;
        particle.vy = -Math.abs(particle.vy) * this.physics.collisionDamping;
      }

      // Check collisions with other particles
      for (let j = i + 1; j < this.particles.length; j++) {
        this.handleCollision(particle, this.particles[j]);
      }
    }
  }

  /**
   * Handle collision between two particles
   */
  handleCollision(p1, p2) {
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    const minDistance = p1.radius + p2.radius;

    if (distance < minDistance) {
      // Separate particles
      const angle = Math.atan2(dy, dx);
      const targetX = p1.x + Math.cos(angle) * minDistance;
      const targetY = p1.y + Math.sin(angle) * minDistance;

      const ax = (targetX - p2.x) * 0.5;
      const ay = (targetY - p2.y) * 0.5;

      p1.x -= ax;
      p1.y -= ay;
      p2.x += ax;
      p2.y += ay;

      // Calculate new velocities (elastic collision)
      const normalX = dx / distance;
      const normalY = dy / distance;

      const relativeVelocityX = p1.vx - p2.vx;
      const relativeVelocityY = p1.vy - p2.vy;

      const speed = relativeVelocityX * normalX + relativeVelocityY * normalY;

      if (speed < 0) return; // Particles moving apart

      const impulse = (2 * speed) / (p1.mass + p2.mass);

      p1.vx -= impulse * p2.mass * normalX * this.physics.collisionDamping;
      p1.vy -= impulse * p2.mass * normalY * this.physics.collisionDamping;
      p2.vx += impulse * p1.mass * normalX * this.physics.collisionDamping;
      p2.vy += impulse * p1.mass * normalY * this.physics.collisionDamping;
    }
  }

  /**
   * Draw particles and connections
   */
  draw() {
    // Clear canvas
    this.ctx.fillStyle = this.colors.background;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw connection lines between nearby particles (optional, subtle)
    if (!this.isMobile) {
      this.drawConnections();
    }

    // Draw particles
    for (const particle of this.particles) {
      this.drawParticle(particle);
    }
  }

  /**
   * Draw connection lines between nearby particles
   */
  drawConnections() {
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const p1 = this.particles[i];
        const p2 = this.particles[j];

        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < this.physics.connectionDistance) {
          const opacity = 1 - distance / this.physics.connectionDistance;

          this.ctx.beginPath();
          this.ctx.strokeStyle = `rgba(220, 38, 38, ${opacity * 0.15})`;
          this.ctx.lineWidth = 0.5;
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);
          this.ctx.stroke();
        }
      }
    }
  }

  /**
   * Draw a single particle with glow effect
   */
  drawParticle(particle) {
    // Draw glow
    const gradient = this.ctx.createRadialGradient(
      particle.x, particle.y, 0,
      particle.x, particle.y, particle.glow
    );
    gradient.addColorStop(0, this.colors.glow);
    gradient.addColorStop(1, 'rgba(220, 38, 38, 0)');

    this.ctx.fillStyle = gradient;
    this.ctx.fillRect(
      particle.x - particle.glow,
      particle.y - particle.glow,
      particle.glow * 2,
      particle.glow * 2
    );

    // Draw core particle
    this.ctx.beginPath();
    this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
    this.ctx.fillStyle = this.colors.particle;
    this.ctx.fill();
  }
}
