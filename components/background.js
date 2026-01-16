/**
 * Physics-Based Particle Network Background Animation
 *
 * High-performance particle system with realistic physics simulation
 * Optimized for 60fps with spatial grid collision detection
 *
 * Features:
 * - Realistic particle physics (velocity, acceleration, collisions)
 * - Mouse interaction (repulsion/attraction)
 * - Proximity-based connections (network visualization)
 * - Dynamic coloring based on velocity
 * - Adaptive performance scaling
 * - Pause when tab hidden
 * - Mobile optimization
 */

class PhysicsParticleBackground {
  constructor(canvas, config = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d', {
      alpha: true,
      desynchronized: true // Better performance on some browsers
    });

    this.particles = [];
    this.mouse = { x: null, y: null, radius: 150 };

    // Default configuration
    this.config = {
      particleCount: 250,
      connectionDistance: 120,
      maxSpeed: 0.8,
      bounceEnergy: 0.95,        // Energy retained on wall bounce (0-1)
      mouseRepulsion: true,      // true = repel, false = attract
      mouseForce: 0.5,
      particleRadius: 2,
      colors: {
        slow: '#737373',         // Gray for slow particles
        medium: '#ef4444',       // Red for medium speed
        fast: '#dc2626',         // Deep red for fast particles
        connection: 'rgba(220, 38, 38, 0.15)'
      },
      ...config
    };

    this.running = false;
    this.resizeObserver = null;
    this.lastFrameTime = performance.now();
    this.frameCount = 0;
    this.fps = 60;

    // Performance monitoring
    this.performanceMode = 'high'; // high, medium, low
    this.performanceCheckInterval = 60; // Check every 60 frames

    // Debug mode
    this.debug = config.debug || false;
    if (this.debug) {
      this.stats = {
        fps: 0,
        frameTime: 0,
        particles: 0,
        connections: 0,
        updateTime: 0,
        renderTime: 0
      };
    }

    this.init();
  }

  init() {
    this.setupCanvas();
    this.createParticles();
    this.setupEventListeners();

    if (this.debug) {
      this.setupDebugPanel();
    }

    // Detect mobile and adjust settings
    this.optimizeForDevice();
  }

  setupCanvas() {
    const resize = () => {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;

      // Recreate particles on significant resize
      if (this.particles.length > 0) {
        const wasRunning = this.running;
        if (wasRunning) this.stop();
        this.createParticles();
        if (wasRunning) this.start();
      }
    };

    resize();

    // Use ResizeObserver for better performance than window.resize
    this.resizeObserver = new ResizeObserver(resize);
    this.resizeObserver.observe(document.body);
  }

  optimizeForDevice() {
    const isMobile = window.innerWidth < 768;
    const isTablet = window.innerWidth >= 768 && window.innerWidth < 1024;
    const isLowEnd = navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4;

    if (isMobile) {
      this.config.particleCount = 80;
      this.config.connectionDistance = 100;
      this.config.mouseForce = 0;  // Disable mouse interaction on mobile
      this.performanceMode = 'low';
    } else if (isTablet || isLowEnd) {
      this.config.particleCount = 150;
      this.config.connectionDistance = 110;
      this.performanceMode = 'medium';
    }

    // Respect user preferences
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      this.config.maxSpeed = 0.3;
      this.config.particleCount = 50;
    }
  }

  createParticles() {
    this.particles = [];
    for (let i = 0; i < this.config.particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: (Math.random() - 0.5) * this.config.maxSpeed,
        vy: (Math.random() - 0.5) * this.config.maxSpeed,
        radius: this.config.particleRadius,
        connections: 0,
        speed: 0
      });
    }
  }

  updateParticle(particle, deltaTime) {
    // Mouse interaction (repulsion or attraction)
    if (this.mouse.x !== null && this.mouse.y !== null && this.config.mouseForce > 0) {
      const dx = particle.x - this.mouse.x;
      const dy = particle.y - this.mouse.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < this.mouse.radius && distance > 0) {
        const force = (this.mouse.radius - distance) / this.mouse.radius;
        const angle = Math.atan2(dy, dx);
        const direction = this.config.mouseRepulsion ? 1 : -1;

        particle.vx += Math.cos(angle) * force * this.config.mouseForce * direction * deltaTime;
        particle.vy += Math.sin(angle) * force * this.config.mouseForce * direction * deltaTime;
      }
    }

    // Apply velocity with deltaTime for frame-rate independence
    particle.x += particle.vx * deltaTime;
    particle.y += particle.vy * deltaTime;

    // Boundary collision with realistic bounce (energy loss)
    if (particle.x <= 0 || particle.x >= this.canvas.width) {
      particle.vx *= -this.config.bounceEnergy;
      particle.x = Math.max(0, Math.min(this.canvas.width, particle.x));
    }
    if (particle.y <= 0 || particle.y >= this.canvas.height) {
      particle.vy *= -this.config.bounceEnergy;
      particle.y = Math.max(0, Math.min(this.canvas.height, particle.y));
    }

    // Speed limit to prevent runaway velocities
    const speed = Math.sqrt(particle.vx ** 2 + particle.vy ** 2);
    particle.speed = speed;

    if (speed > this.config.maxSpeed * 2) {
      const factor = (this.config.maxSpeed * 2) / speed;
      particle.vx *= factor;
      particle.vy *= factor;
    }

    // Add slight friction to create more interesting dynamics
    particle.vx *= 0.999;
    particle.vy *= 0.999;
  }

  drawConnections() {
    // Optimization: Spatial grid for O(n) collision detection instead of O(n²)
    const grid = new Map();
    const cellSize = this.config.connectionDistance;
    let connectionCount = 0;

    // Populate spatial grid
    this.particles.forEach(particle => {
      const cellX = Math.floor(particle.x / cellSize);
      const cellY = Math.floor(particle.y / cellSize);
      const key = `${cellX},${cellY}`;
      if (!grid.has(key)) grid.set(key, []);
      grid.get(key).push(particle);
      particle.connections = 0;
    });

    // Check only nearby cells (9 cells: current + 8 neighbors)
    this.particles.forEach(p1 => {
      const cellX = Math.floor(p1.x / cellSize);
      const cellY = Math.floor(p1.y / cellSize);

      for (let dx = -1; dx <= 1; dx++) {
        for (let dy = -1; dy <= 1; dy++) {
          const key = `${cellX + dx},${cellY + dy}`;
          const cellParticles = grid.get(key);
          if (!cellParticles) continue;

          cellParticles.forEach(p2 => {
            if (p1 === p2) return;

            const dx = p2.x - p1.x;
            const dy = p2.y - p1.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < this.config.connectionDistance) {
              const opacity = 1 - (distance / this.config.connectionDistance);

              // Draw connection line
              this.ctx.strokeStyle = this.config.colors.connection.replace('0.15', (opacity * 0.15).toFixed(2));
              this.ctx.lineWidth = 0.5;
              this.ctx.beginPath();
              this.ctx.moveTo(p1.x, p1.y);
              this.ctx.lineTo(p2.x, p2.y);
              this.ctx.stroke();

              p1.connections++;
              connectionCount++;
            }
          });
        }
      }
    });

    if (this.debug) {
      this.stats.connections = Math.floor(connectionCount / 2);
    }
  }

  drawParticles() {
    this.particles.forEach(particle => {
      // Color based on speed (physics-accurate velocity mapping)
      const speedRatio = particle.speed / (this.config.maxSpeed * 2);

      let color;
      if (speedRatio < 0.3) {
        color = this.config.colors.slow;
      } else if (speedRatio < 0.7) {
        color = this.config.colors.medium;
      } else {
        color = this.config.colors.fast;
      }

      // Brightness based on connection count (more connected = more visible)
      const alpha = Math.min(1, 0.3 + (particle.connections * 0.1));

      this.ctx.fillStyle = color;
      this.ctx.globalAlpha = alpha;
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.globalAlpha = 1;
    });
  }

  animate(currentTime) {
    if (!this.running) return;

    const deltaTime = Math.min((currentTime - this.lastFrameTime) / 16.67, 2); // Cap deltaTime
    this.lastFrameTime = currentTime;

    // FPS calculation
    this.frameCount++;
    if (this.frameCount >= this.performanceCheckInterval) {
      this.fps = Math.round(1000 / ((currentTime - this.fpsCheckTime) / this.performanceCheckInterval));
      this.fpsCheckTime = currentTime;
      this.frameCount = 0;

      // Adaptive performance scaling
      this.adaptPerformance();
    } else if (this.frameCount === 1) {
      this.fpsCheckTime = currentTime;
    }

    // Clear canvas with transparency
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Update physics
    const updateStart = this.debug ? performance.now() : 0;
    this.particles.forEach(particle => this.updateParticle(particle, deltaTime));
    if (this.debug) this.stats.updateTime = performance.now() - updateStart;

    // Render
    const renderStart = this.debug ? performance.now() : 0;
    this.drawConnections();
    this.drawParticles();
    if (this.debug) this.stats.renderTime = performance.now() - renderStart;

    // Debug overlay
    if (this.debug) {
      this.stats.fps = this.fps;
      this.stats.frameTime = deltaTime * 16.67;
      this.stats.particles = this.particles.length;
      this.updateDebugPanel();
    }

    requestAnimationFrame((time) => this.animate(time));
  }

  adaptPerformance() {
    // Adaptive performance: reduce particle count if FPS drops below 30
    if (this.fps < 30 && this.particles.length > 50) {
      const reduction = Math.floor(this.particles.length * 0.1);
      this.particles.splice(0, reduction);
      console.log(`Performance: Reduced particles to ${this.particles.length}`);
    }

    // Increase particle count if FPS is consistently high and below max
    if (this.fps > 55 && this.particles.length < this.config.particleCount) {
      const increase = Math.min(10, this.config.particleCount - this.particles.length);
      for (let i = 0; i < increase; i++) {
        this.particles.push({
          x: Math.random() * this.canvas.width,
          y: Math.random() * this.canvas.height,
          vx: (Math.random() - 0.5) * this.config.maxSpeed,
          vy: (Math.random() - 0.5) * this.config.maxSpeed,
          radius: this.config.particleRadius,
          connections: 0,
          speed: 0
        });
      }
    }
  }

  setupEventListeners() {
    // Mouse tracking for interaction
    const handleMouseMove = (e) => {
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;
    };

    const handleMouseLeave = () => {
      this.mouse.x = null;
      this.mouse.y = null;
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseleave', handleMouseLeave);

    // Touch support for mobile
    document.addEventListener('touchmove', (e) => {
      if (e.touches.length > 0) {
        this.mouse.x = e.touches[0].clientX;
        this.mouse.y = e.touches[0].clientY;
      }
    });

    document.addEventListener('touchend', handleMouseLeave);

    // Pause when tab hidden (performance optimization)
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.stop();
      } else {
        this.start();
      }
    });

    // Store handlers for cleanup
    this._eventHandlers = {
      mousemove: handleMouseMove,
      mouseleave: handleMouseLeave
    };
  }

  setupDebugPanel() {
    const panel = document.createElement('div');
    panel.id = 'physics-debug-panel';
    panel.style.cssText = `
      position: fixed;
      top: 10px;
      left: 10px;
      background: rgba(0, 0, 0, 0.85);
      color: #0f0;
      padding: 15px;
      font-family: 'Courier New', monospace;
      font-size: 12px;
      z-index: 9999;
      border: 1px solid #0f0;
      border-radius: 4px;
      min-width: 200px;
      line-height: 1.6;
    `;
    document.body.appendChild(panel);
  }

  updateDebugPanel() {
    const panel = document.getElementById('physics-debug-panel');
    if (panel) {
      panel.innerHTML = `
        <strong style="color: #f00;">PHYSICS DEBUG</strong><br>
        FPS: ${this.stats.fps.toFixed(0)}<br>
        Frame Time: ${this.stats.frameTime.toFixed(2)}ms<br>
        Particles: ${this.stats.particles}<br>
        Connections: ${this.stats.connections}<br>
        Update: ${this.stats.updateTime.toFixed(2)}ms<br>
        Render: ${this.stats.renderTime.toFixed(2)}ms<br>
        Mode: ${this.performanceMode}<br>
        Mouse: ${this.mouse.x ? `(${Math.round(this.mouse.x)}, ${Math.round(this.mouse.y)})` : 'None'}
      `;
    }
  }

  start() {
    if (this.running) return;
    this.running = true;
    this.lastFrameTime = performance.now();
    this.frameCount = 0;
    this.animate(this.lastFrameTime);
  }

  stop() {
    this.running = false;
  }

  destroy() {
    this.stop();

    // Clean up event listeners
    if (this._eventHandlers) {
      document.removeEventListener('mousemove', this._eventHandlers.mousemove);
      document.removeEventListener('mouseleave', this._eventHandlers.mouseleave);
    }

    // Clean up resize observer
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
    }

    // Clean up debug panel
    if (this.debug) {
      const panel = document.getElementById('physics-debug-panel');
      if (panel) panel.remove();
    }

    // Clear references
    this.canvas = null;
    this.ctx = null;
    this.particles = [];
  }

  // Public API for runtime configuration
  updateConfig(newConfig) {
    this.config = { ...this.config, ...newConfig };
    const wasRunning = this.running;
    if (wasRunning) this.stop();
    this.createParticles();
    if (wasRunning) this.start();
  }

  getConfig() {
    return { ...this.config };
  }

  getStats() {
    return {
      fps: this.fps,
      particleCount: this.particles.length,
      performanceMode: this.performanceMode,
      running: this.running
    };
  }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PhysicsParticleBackground;
}
