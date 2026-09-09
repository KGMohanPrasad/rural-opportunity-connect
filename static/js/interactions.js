/**
 * Rural Opportunity Connect — Interactive System Engine
 * Handles:
 * - 3D Card Tilt with Specular Glare Tracking
 * - Magnetic Buttons with Spring Physics
 * - KPI Animated Number Rollups (count up from 0 to real values)
 * - Circular SVG Progress Rings & Checkmark Drawing
 * - Quick Apply & Bookmark Celebration Particles
 * - Back to Top Smooth Navigation
 * - Navbar Scroll Glassmorphism & Sliding Pill
 */

(function () {
    'use strict';

    /* ==========================================================================
       1. 3D CARD TILT & SPECULAR GLARE
       ========================================================================== */
    const Card3DTilt = {
        init() {
            const cards = document.querySelectorAll('.tilt-card-3d, .hover-lift-3d, .roc-card, .kpi-card-glow');
            cards.forEach(card => {
                card.addEventListener('mousemove', (e) => {
                    // Hover stabilization: When cursor is over a button or link, pause dynamic tilt
                    if (e.target && e.target.closest('button, a, input, select, .save-btn')) {
                        card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(-5px) translateZ(4px)`;
                        return;
                    }

                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;

                    // Controlled 6 to 8 degree tilt
                    const rotateX = ((y - centerY) / centerY) * -7;
                    const rotateY = ((x - centerX) / centerX) * 7;

                    card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-5px) translateZ(8px)`;

                    // Specular light sheen
                    const sheenX = ((x / rect.width) * 100).toFixed(1);
                    const sheenY = ((y / rect.height) * 100).toFixed(1);
                    card.style.setProperty('--sheen-x', `${sheenX}%`);
                    card.style.setProperty('--sheen-y', `${sheenY}%`);
                });

                card.addEventListener('mouseleave', () => {
                    card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px) translateZ(0px)`;
                    card.style.removeProperty('--sheen-x');
                    card.style.removeProperty('--sheen-y');
                });
            });
        }
    };

    /* ==========================================================================
       2. MAGNETIC BUTTON ATTRACTION
       ========================================================================== */
    const MagneticButtons = {
        init() {
            const btns = document.querySelectorAll('.btn-magnetic, .btn-primary, #backToTopBtn');
            btns.forEach(btn => {
                btn.addEventListener('mousemove', (e) => {
                    const rect = btn.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    const deltaX = (e.clientX - centerX) * 0.32;
                    const deltaY = (e.clientY - centerY) * 0.32;

                    // Clamped to 12px for subtle, elegant control
                    const clampX = Math.max(-12, Math.min(12, deltaX));
                    const clampY = Math.max(-12, Math.min(12, deltaY));

                    btn.style.transform = `translate3d(${clampX}px, ${clampY}px, 0)`;
                });

                btn.addEventListener('mouseleave', () => {
                    btn.style.transform = 'translate3d(0, 0, 0)';
                });
            });
        }
    };

    /* ==========================================================================
       3. ANIMATED KPI NUMBER ROLLUPS
       ========================================================================== */
    const NumberRollup = {
        init() {
            const counters = document.querySelectorAll('.counter-value, [data-counter]');
            if (!counters.length) return;

            if (!('IntersectionObserver' in window)) {
                counters.forEach(c => this.setFinalValue(c));
                return;
            }

            const observer = new IntersectionObserver((entries, obs) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.animateCounter(entry.target);
                        obs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.15 });

            counters.forEach(c => observer.observe(c));
        },

        animateCounter(el) {
            const raw = el.dataset.counter || el.innerText.trim();
            const match = raw.match(/^([^\d]*)([\d,.]+)(.*)$/);
            if (!match) return;

            const prefix = match[1] || '';
            const numStr = match[2].replace(/,/g, '');
            const targetNum = parseFloat(numStr);
            const suffix = match[3] || '';

            if (isNaN(targetNum)) return;

            const hasDecimals = numStr.includes('.');
            const decimalPlaces = hasDecimals ? numStr.split('.')[1].length : 0;
            const hasComma = match[2].includes(',');

            const duration = 1400;
            const startTime = performance.now();
            const easeOutExpo = (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

            const update = (now) => {
                const elapsed = now - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = easeOutExpo(progress);
                const current = targetNum * eased;

                let formatted = hasDecimals ? current.toFixed(decimalPlaces) : Math.floor(current).toString();
                if (hasComma) {
                    const parts = formatted.split('.');
                    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                    formatted = parts.join('.');
                }

                el.innerText = `${prefix}${formatted}${suffix}`;

                if (progress < 1) {
                    requestAnimationFrame(update);
                } else {
                    this.setFinalValue(el, raw);
                }
            };

            requestAnimationFrame(update);
        },

        setFinalValue(el, text) {
            el.innerText = text || el.dataset.counter || el.innerText;
        }
    };

    /* ==========================================================================
       4. SVG PROGRESS RINGS & CHECKMARK ANIMATION
       ========================================================================== */
    const SvgInteractions = {
        init() {
            this.initRings();
            this.initChecklist();
        },

        initRings() {
            const rings = document.querySelectorAll('.circle-progress-bar');
            rings.forEach(ring => {
                const percent = parseFloat(ring.dataset.percent || 0);
                const r = ring.r && ring.r.baseVal ? ring.r.baseVal.value : 26;
                const circumference = 2 * Math.PI * r;

                ring.style.strokeDasharray = `${circumference} ${circumference}`;
                ring.style.strokeDashoffset = `${circumference}`;

                setTimeout(() => {
                    const offset = circumference - (percent / 100) * circumference;
                    ring.style.strokeDashoffset = `${offset}`;
                }, 180);
            });
        },

        initChecklist() {
            const items = document.querySelectorAll('.checklist-interactive-item');
            if (!items.length) return;

            items.forEach(item => {
                const checkbox = item.querySelector('input[type="checkbox"]');
                if (!checkbox) return;

                // Set initial visual state
                item.classList.toggle('checked', checkbox.checked);

                // Listen to native change to avoid click double-toggle cancellation
                checkbox.addEventListener('change', () => {
                    const isChecked = checkbox.checked;
                    item.classList.toggle('checked', isChecked);

                    if (isChecked && window.GlowCursor && typeof window.GlowCursor.particleBurst === 'function') {
                        const rect = item.getBoundingClientRect();
                        window.GlowCursor.particleBurst(rect.right - 40, rect.top + rect.height / 2, { r: 16, g: 185, b: 129 }, 14);
                    }

                    // Check if 100% reached
                    const allChecked = Array.from(items).every(it => {
                        const cb = it.querySelector('input[type="checkbox"]');
                        return cb ? cb.checked : it.classList.contains('checked');
                    });

                    if (allChecked && window.GlowCursor && typeof window.GlowCursor.particleBurst === 'function') {
                        window.GlowCursor.particleBurst(window.innerWidth * 0.3, window.innerHeight * 0.4, { r: 245, g: 158, b: 11 }, 25);
                        window.GlowCursor.particleBurst(window.innerWidth * 0.7, window.innerHeight * 0.4, { r: 6, g: 182, b: 212 }, 25);
                    }
                });
            });
        }
    };

    /* ==========================================================================
       5. NAVBAR SCROLL GLASS & ACTIVE PILL INDICATOR
       ========================================================================== */
    const NavEnhancements = {
        init() {
            const nav = document.querySelector('nav');
            const backToTopBtn = document.getElementById('backToTopBtn');

            // Scroll listener
            let ticking = false;
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    requestAnimationFrame(() => {
                        const scrollY = window.pageYOffset || document.documentElement.scrollTop;

                        if (nav) {
                            if (scrollY > 20) {
                                nav.classList.add('nav-glass-scrolled');
                            } else {
                                nav.classList.remove('nav-glass-scrolled');
                            }
                        }

                        if (backToTopBtn) {
                            if (scrollY > 300) {
                                backToTopBtn.classList.add('visible');
                            } else {
                                backToTopBtn.classList.remove('visible');
                            }
                        }

                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });

            // Back to top click
            if (backToTopBtn) {
                backToTopBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                });
            }

            // Sliding nav indicator pill
            this.initSlidingPill(nav);
        },

        initSlidingPill(nav) {
            if (!nav) return;
            const container = nav.querySelector('.hidden.lg\\:flex, [class*="lg:flex"]');
            if (!container) return;

            let pill = container.querySelector('.nav-sliding-pill');
            if (!pill) {
                pill = document.createElement('div');
                pill.className = 'nav-sliding-pill';
                container.style.position = 'relative';
                container.appendChild(pill);
            }

            const links = container.querySelectorAll('.nav-link');
            const activeLink = container.querySelector('.nav-link.active') || links[0];

            const movePill = (el) => {
                if (!el || !pill) return;
                const rect = el.getBoundingClientRect();
                const containerRect = container.getBoundingClientRect();
                pill.style.width = `${rect.width * 0.8}px`;
                pill.style.left = `${(rect.left - containerRect.left) + (rect.width * 0.1)}px`;
                pill.style.opacity = '1';
            };

            if (activeLink) movePill(activeLink);

            links.forEach(link => {
                link.addEventListener('mouseenter', () => movePill(link));
            });

            container.addEventListener('mouseleave', () => {
                if (activeLink) movePill(activeLink);
                else pill.style.opacity = '0';
            });
        }
    };

    /* ==========================================================================
       6. QUICK APPLY & BOOKMARK CELEBRATIONS
       ========================================================================== */
    const ActionCelebrations = {
        init() {
            // Global hook for Quick Apply completion
            window.celebrateQuickApply = (btn, name) => {
                if (btn) {
                    btn.classList.remove('btn-primary', 'btn-applying');
                    btn.classList.add('btn-applied');
                    btn.disabled = true;
                    btn.innerHTML = `<i class="fas fa-check-circle text-emerald-600"></i> Already Applied ✓`;

                    const rect = btn.getBoundingClientRect();
                    const x = rect.left + rect.width / 2;
                    const y = rect.top + rect.height / 2;

                    if (window.GlowCursor && typeof window.GlowCursor.successPulse === 'function') {
                        window.GlowCursor.successPulse(x, y);
                    }
                }
            };

            // Global hook for Wishlist Save
            document.addEventListener('click', (e) => {
                const btn = e.target.closest('.save-btn, .heart-pop');
                if (!btn) return;

                const rect = btn.getBoundingClientRect();
                const x = rect.left + rect.width / 2;
                const y = rect.top + rect.height / 2;
                const isSaved = btn.classList.contains('is-saved');

                if (!isSaved && window.GlowCursor && typeof window.GlowCursor.particleBurst === 'function') {
                    window.GlowCursor.particleBurst(x, y, { r: 239, g: 68, b: 68 }, 16);
                }
            });
        }
    };

    /* ==========================================================================
       7. INITIALIZE ALL ON DOM READY
       ========================================================================== */
    const bootInteractions = () => {
        Card3DTilt.init();
        MagneticButtons.init();
        NumberRollup.init();
        SvgInteractions.init();
        NavEnhancements.init();
        ActionCelebrations.init();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootInteractions);
    } else {
        bootInteractions();
    }

    window.Card3DTilt = Card3DTilt;
    window.MagneticButtons = MagneticButtons;
    window.NumberRollup = NumberRollup;
})();
