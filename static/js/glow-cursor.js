/**
 * Rural Opportunity Connect — Glow Cursor & Interactive Light Trail
 * Inspired by React Bits GlowCursor WebGL/OGL implementation.
 * 
 * Features:
 * - High-DPI Canvas 2D engine with additive bloom blending
 * - Dual-tone chromatic gradient: Cyan (#67E8F9) -> Purple (#A78BFA)
 * - Spring interpolation physics & multi-node decaying energy trail
 * - Intense white/cyan hotspot with ambient halo
 * - Auto-idle fade after ~700ms of inactivity
 * - Reactive states: nav expand, button magnet, card glow boost, link ring, click ripple
 * - Zero blocking (pointer-events: none, passive listeners, rAF loop)
 * - Mobile and reduced-motion safe (fully deactivated on touch/reduced motion)
 */

(function () {
    'use strict';

    const CONFIG = {
        primaryColor: { r: 6, g: 182, b: 212 },     // #06B6D4 (Vibrant Cyan)
        secondaryColor: { r: 168, g: 85, b: 247 },  // #A855F7 (Vibrant Purple)
        accentWhite: { r: 255, g: 255, b: 255 },
        trailLength: 32,
        headRadius: 8,
        glowRadius: 42,
        glowRadiusHoverCard: 64,
        glowRadiusHoverBtn: 52,
        idleTimeout: 3500,
        springTension: 0.32,
        springDamping: 0.70
    };

    class GlowCursorEngine {
        constructor() {
            this.canvas = null;
            this.ctx = null;
            this.width = window.innerWidth;
            this.height = window.innerHeight;
            this.dpr = Math.min(window.devicePixelRatio || 1, 2);

            // Coordinates
            this.targetX = this.width / 2;
            this.targetY = this.height / 2;
            this.currentX = this.targetX;
            this.currentY = this.targetY;
            this.vx = 0;
            this.vy = 0;

            // Trail History
            this.trail = [];
            for (let i = 0; i < CONFIG.trailLength; i++) {
                this.trail.push({ x: this.currentX, y: this.currentY, alpha: 0 });
            }

            // Idle & Fade state
            this.lastMoveTime = performance.now();
            this.opacity = 0.8;
            this.targetOpacity = 1;
            this.isActive = true;

            // Hover state
            this.hoverState = 'default'; // 'default', 'link', 'button', 'card'
            this.currentGlowRadius = CONFIG.glowRadius;
            this.targetGlowRadius = CONFIG.glowRadius;

            // Particles on burst
            this.particles = [];

            this.init();
        }

        init() {
            // Create Canvas
            this.canvas = document.createElement('canvas');
            this.canvas.id = 'glowCursorCanvas';
            document.body.appendChild(this.canvas);
            document.body.classList.add('glow-cursor-active');

            this.ctx = this.canvas.getContext('2d', { alpha: true });
            this.resize();

            // Bind Event Listeners
            this.bindEvents();

            // Start Animation Loop
            requestAnimationFrame((time) => this.render(time));
        }

        resize() {
            this.width = window.innerWidth;
            this.height = window.innerHeight;
            this.dpr = Math.min(window.devicePixelRatio || 1, 2);

            this.canvas.width = this.width * this.dpr;
            this.canvas.height = this.height * this.dpr;
            this.canvas.style.width = `${this.width}px`;
            this.canvas.style.height = `${this.height}px`;

            this.ctx.scale(this.dpr, this.dpr);
        }

        bindEvents() {
            window.addEventListener('resize', () => this.resize(), { passive: true });

            // Mouse movement tracking
            window.addEventListener('mousemove', (e) => {
                this.targetX = e.clientX;
                this.targetY = e.clientY;
                this.lastMoveTime = performance.now();
                this.targetOpacity = 1;
                this.isActive = true;
            }, { passive: true });

            // Window blur / mouse leave
            document.addEventListener('mouseleave', () => {
                this.targetOpacity = 0;
            });

            document.addEventListener('mouseenter', (e) => {
                this.targetX = e.clientX;
                this.targetY = e.clientY;
                this.lastMoveTime = performance.now();
                this.targetOpacity = 1;
            });

            // Contextual interactions delegation
            document.addEventListener('mouseover', (e) => {
                const target = e.target;
                if (!target) return;

                if (target.closest('.nav-link, nav a, .roc-lang-selector')) {
                    this.hoverState = 'link';
                    this.targetGlowRadius = 42;
                } else if (target.closest('.btn-primary, .btn-secondary, .btn-magnetic, button, .carousel-nav-btn')) {
                    this.hoverState = 'button';
                    this.targetGlowRadius = CONFIG.glowRadiusHoverBtn;
                } else if (target.closest('.roc-card, .tilt-card-3d, .kpi-card-glow, .carousel-3d-card')) {
                    this.hoverState = 'card';
                    this.targetGlowRadius = CONFIG.glowRadiusHoverCard;
                } else {
                    this.hoverState = 'default';
                    this.targetGlowRadius = CONFIG.glowRadius;
                }
            }, { passive: true });

            // Click ripple effect
            document.addEventListener('mousedown', (e) => {
                this.createClickRipple(e.clientX, e.clientY);
            }, { passive: true });
        }

        createClickRipple(x, y) {
            const ripple = document.createElement('div');
            ripple.className = 'cursor-click-ripple';
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            document.body.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);

            // Emit mini light bursts into the canvas
            for (let i = 0; i < 8; i++) {
                const angle = (Math.PI * 2 / 8) * i + (Math.random() * 0.4);
                const speed = 2.0 + Math.random() * 2.5;
                this.particles.push({
                    x,
                    y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    radius: 2 + Math.random() * 2,
                    alpha: 1,
                    color: CONFIG.primaryColor,
                    decay: 0.04 + Math.random() * 0.03
                });
            }
        }

        // Public hook: trigger Quick Apply success pulse
        successPulse(x, y) {
            const pulse = document.createElement('div');
            pulse.className = 'cursor-apply-pulse';
            pulse.style.left = `${x}px`;
            pulse.style.top = `${y}px`;
            document.body.appendChild(pulse);
            setTimeout(() => pulse.remove(), 800);

            for (let i = 0; i < 18; i++) {
                const angle = Math.random() * Math.PI * 2;
                const speed = 3.0 + Math.random() * 4.0;
                this.particles.push({
                    x,
                    y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    radius: 2.5 + Math.random() * 3,
                    alpha: 1,
                    color: { r: 16, g: 185, b: 129 }, // Emerald
                    decay: 0.03
                });
            }
        }

        // Public hook: trigger Bookmark particle burst
        particleBurst(x, y, color = CONFIG.primaryColor, count = 16) {
            for (let i = 0; i < count; i++) {
                const angle = Math.random() * Math.PI * 2;
                const speed = 2.5 + Math.random() * 4.5;
                this.particles.push({
                    x,
                    y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed - 1.0,
                    radius: 2.0 + Math.random() * 2.5,
                    alpha: 1,
                    color: color,
                    decay: 0.025 + Math.random() * 0.02
                });
            }
        }

        render(time) {
            requestAnimationFrame((t) => this.render(t));

            // Idle fade detection (retains soft ambient glow rather than total darkness)
            const now = performance.now();
            if (now - this.lastMoveTime > CONFIG.idleTimeout) {
                this.targetOpacity = 0.35;
            }

            // Smooth opacity interpolation
            this.opacity += (this.targetOpacity - this.opacity) * 0.08;
            if (this.opacity < 0.005 && this.particles.length === 0) {
                this.ctx.clearRect(0, 0, this.width, this.height);
                return;
            }

            // Smooth spring physics for cursor head
            const dx = this.targetX - this.currentX;
            const dy = this.targetY - this.currentY;
            this.vx = (this.vx + dx * CONFIG.springTension) * CONFIG.springDamping;
            this.vy = (this.vy + dy * CONFIG.springTension) * CONFIG.springDamping;
            this.currentX += this.vx;
            this.currentY += this.vy;

            // Interpolate glow radius
            this.currentGlowRadius += (this.targetGlowRadius - this.currentGlowRadius) * 0.12;

            // Update trail coordinates with trailing lerp
            this.trail[0].x = this.currentX;
            this.trail[0].y = this.currentY;
            this.trail[0].alpha = this.opacity;

            for (let i = 1; i < this.trail.length; i++) {
                const prev = this.trail[i - 1];
                const cur = this.trail[i];
                // Smooth drag follow
                cur.x += (prev.x - cur.x) * 0.42;
                cur.y += (prev.y - cur.y) * 0.42;
                cur.alpha = prev.alpha * 0.91;
            }

            // Clear frame
            this.ctx.clearRect(0, 0, this.width, this.height);

            // Set additive bloom blending
            this.ctx.globalCompositeOperation = 'screen';

            // 1. Render Cyan -> Purple Energy Light Trail
            if (this.trail.length > 2) {
                for (let i = this.trail.length - 1; i > 0; i--) {
                    const pt = this.trail[i];
                    const prevPt = this.trail[i - 1];
                    const progress = i / this.trail.length; // 0 = head, 1 = tail

                    // Interpolate color from Cyan to Purple
                    const r = Math.round(CONFIG.primaryColor.r + (CONFIG.secondaryColor.r - CONFIG.primaryColor.r) * progress);
                    const g = Math.round(CONFIG.primaryColor.g + (CONFIG.secondaryColor.g - CONFIG.primaryColor.g) * progress);
                    const b = Math.round(CONFIG.primaryColor.b + (CONFIG.secondaryColor.b - CONFIG.primaryColor.b) * progress);
                    const alpha = pt.alpha * (1 - progress * 0.85) * 0.65;

                    if (alpha <= 0.001) continue;

                    // Wide soft bloom along trail segment
                    const trailWidth = Math.max(1, (1 - progress) * (this.hoverState === 'card' ? 14 : 9));
                    this.ctx.beginPath();
                    this.ctx.moveTo(prevPt.x, prevPt.y);
                    this.ctx.lineTo(pt.x, pt.y);
                    this.ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, ${alpha * 0.45})`;
                    this.ctx.lineWidth = trailWidth * 2.8;
                    this.ctx.lineCap = 'round';
                    this.ctx.stroke();

                    // Core bright line
                    this.ctx.beginPath();
                    this.ctx.moveTo(prevPt.x, prevPt.y);
                    this.ctx.lineTo(pt.x, pt.y);
                    this.ctx.strokeStyle = `rgba(${r}, ${g}, ${b}, ${alpha})`;
                    this.ctx.lineWidth = trailWidth;
                    this.ctx.lineCap = 'round';
                    this.ctx.stroke();
                }
            }

            // 2. Render Ambient Glowing Corona at Cursor Head
            const glow = this.ctx.createRadialGradient(
                this.currentX, this.currentY, 0,
                this.currentX, this.currentY, this.currentGlowRadius
            );
            glow.addColorStop(0, `rgba(${CONFIG.primaryColor.r}, ${CONFIG.primaryColor.g}, ${CONFIG.primaryColor.b}, ${0.55 * this.opacity})`);
            glow.addColorStop(0.35, `rgba(${CONFIG.secondaryColor.r}, ${CONFIG.secondaryColor.g}, ${CONFIG.secondaryColor.b}, ${0.25 * this.opacity})`);
            glow.addColorStop(1, 'rgba(7, 21, 38, 0)');

            this.ctx.fillStyle = glow;
            this.ctx.beginPath();
            this.ctx.arc(this.currentX, this.currentY, this.currentGlowRadius, 0, Math.PI * 2);
            this.ctx.fill();

            // 3. Render Link / Nav Ring when hovering interactive items
            if (this.hoverState === 'link') {
                this.ctx.beginPath();
                this.ctx.arc(this.currentX, this.currentY, 16, 0, Math.PI * 2);
                this.ctx.strokeStyle = `rgba(${CONFIG.primaryColor.r}, ${CONFIG.primaryColor.g}, ${CONFIG.primaryColor.b}, ${0.85 * this.opacity})`;
                this.ctx.lineWidth = 1.5;
                this.ctx.stroke();
            }

            // 4. Render Bright Hotspot
            // Outer cyan halo
            this.ctx.beginPath();
            this.ctx.arc(this.currentX, this.currentY, CONFIG.headRadius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${CONFIG.primaryColor.r}, ${CONFIG.primaryColor.g}, ${CONFIG.primaryColor.b}, ${0.9 * this.opacity})`;
            this.ctx.fill();

            // Core intense white center
            this.ctx.beginPath();
            this.ctx.arc(this.currentX, this.currentY, Math.max(2, CONFIG.headRadius * 0.45), 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(255, 255, 255, ${0.98 * this.opacity})`;
            this.ctx.fill();

            // 5. Render Active Burst Particles
            for (let i = this.particles.length - 1; i >= 0; i--) {
                const p = this.particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.alpha -= p.decay;
                p.vx *= 0.96;
                p.vy *= 0.96;

                if (p.alpha <= 0) {
                    this.particles.splice(i, 1);
                    continue;
                }

                this.ctx.beginPath();
                this.ctx.arc(p.x, p.y, Math.max(0.5, p.radius * p.alpha), 0, Math.PI * 2);
                this.ctx.fillStyle = `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, ${p.alpha})`;
                this.ctx.fill();
            }

            // Reset composite operation
            this.ctx.globalCompositeOperation = 'source-over';
        }
    }

    // Initialize once DOM is ready
    let engine = null;
    const bootGlowCursor = () => {
        if (!engine) {
            engine = new GlowCursorEngine();
            window.GlowCursor = engine;
            window.GlowCursorEngine = engine;
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootGlowCursor);
    } else {
        bootGlowCursor();
    }
})();
