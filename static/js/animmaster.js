/**
 * Animmaster Pro Animation Engine — Rural Opportunity Connect (Pass 2.1)
 * High-Visibility, Visibly Noticeable, Enterprise-Grade Interactive System.
 * GPU-Accelerated (transform & opacity only), 60-120 FPS, Zero Layout Shifts.
 */

(function () {
    'use strict';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isTouchDevice = window.matchMedia('(hover: none) and (pointer: coarse)').matches || ('ontouchstart' in window);

    /* ==========================================================================
       1. FLOATING INTERACTIVE TOAST
       ========================================================================== */
    const Toast = {
        el: null,
        timeout: null,
        init() {
            this.el = document.getElementById('rocToast');
            if (!this.el) {
                this.el = document.createElement('div');
                this.el.id = 'rocToast';
                document.body.appendChild(this.el);
            }
        },
        show(message, icon = 'fa-check-circle', color = '#00f2fe') {
            if (!this.el) this.init();
            clearTimeout(this.timeout);
            this.el.innerHTML = `<i class="fas ${icon}" style="color: ${color}; font-size: 16px;"></i> <span>${message}</span>`;
            this.el.classList.add('show');
            this.timeout = setTimeout(() => {
                if (this.el) this.el.classList.remove('show');
            }, 3200);
        }
    };

    /* ==========================================================================
       2. PAGE TRANSITIONS & BRANDED LOADER
       ========================================================================== */
    const PageTransitions = {
        bar: null,
        loaderOverlay: null,
        pageOverlay: null,

        init() {
            this.bar = document.getElementById('pageTransitionBar');
            if (!this.bar) {
                this.bar = document.createElement('div');
                this.bar.id = 'pageTransitionBar';
                document.body.appendChild(this.bar);
            }

            this.loaderOverlay = document.getElementById('pageLoadingOverlay');
            this.pageOverlay = document.getElementById('pageTransitionOverlay');
            this.finish();

            document.addEventListener('click', (e) => {
                const link = e.target.closest('a');
                if (!link) return;

                const href = link.getAttribute('href');
                const target = link.getAttribute('target');

                if (!href || href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
                if (target === '_blank' || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
                if (link.dataset.noTransition !== undefined) return;

                try {
                    const url = new URL(link.href, window.location.origin);
                    if (url.origin !== window.location.origin) return;

                    this.start();
                } catch (err) {}
            });

            window.addEventListener('pageshow', (event) => {
                if (event.persisted) {
                    this.finish();
                }
            });
        },

        start() {
            if (prefersReducedMotion) return;
            if (this.pageOverlay) {
                this.pageOverlay.classList.add('active');
            }
            if (this.bar) {
                this.bar.classList.add('active');
                this.bar.style.width = '45%';
                setTimeout(() => {
                    if (this.bar) this.bar.style.width = '85%';
                }, 120);
            }
        },

        finish() {
            if (this.pageOverlay) {
                this.pageOverlay.classList.remove('active');
            }
            if (this.bar) {
                this.bar.style.width = '100%';
                setTimeout(() => {
                    if (this.bar) {
                        this.bar.classList.remove('active');
                        this.bar.style.width = '0%';
                    }
                }, 280);
            }

            if (this.loaderOverlay) {
                this.loaderOverlay.classList.remove('active');
            }
        }
    };

    /* ==========================================================================
       3. SCROLL PROGRESS, PARALLAX & NAVBAR BLUR
       ========================================================================== */
    const ScrollAnimations = {
        progressBar: null,
        nav: null,
        backToTopBtn: null,

        init() {
            this.progressBar = document.getElementById('scrollProgressBar');
            this.nav = document.querySelector('nav');
            this.backToTopBtn = document.getElementById('backToTopBtn');

            this.initScrollObservers();
            this.initScrollListener();
            this.initBackToTop();
        },

        initScrollListener() {
            let ticking = false;

            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(() => {
                        const currentScrollY = window.pageYOffset || document.documentElement.scrollTop;
                        const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                        
                        if (this.progressBar && docHeight > 0) {
                            const scrollPercent = (currentScrollY / docHeight) * 100;
                            this.progressBar.style.width = `${Math.min(100, Math.max(0, scrollPercent))}%`;
                        }

                        if (this.nav) {
                            if (currentScrollY > 25) {
                                this.nav.classList.add('nav-glass-scrolled');
                            } else {
                                this.nav.classList.remove('nav-glass-scrolled');
                            }
                        }

                        if (this.backToTopBtn) {
                            if (currentScrollY > 320) {
                                this.backToTopBtn.classList.add('visible');
                            } else {
                                this.backToTopBtn.classList.remove('visible');
                            }
                        }

                        if (!prefersReducedMotion && !isTouchDevice) {
                            const parallaxElements = document.querySelectorAll('[data-parallax]');
                            parallaxElements.forEach(el => {
                                const factor = parseFloat(el.dataset.parallax || 0.12);
                                const rect = el.getBoundingClientRect();
                                if (rect.top < window.innerHeight && rect.bottom > 0) {
                                    const yOffset = (rect.top - window.innerHeight / 2) * factor;
                                    el.style.transform = `translate3d(0, ${yOffset.toFixed(1)}px, 0)`;
                                }
                            });
                        }

                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });
        },

        initScrollObservers() {
            const elements = document.querySelectorAll('[data-anim], .anim-reveal, .anim-grid-stagger, .chart-bar-grow');
            if (!elements.length) return;

            if (prefersReducedMotion || !('IntersectionObserver' in window)) {
                elements.forEach(el => el.classList.add('anim-in'));
                return;
            }

            const reveal = (el, extraDelay = 0) => {
                if (el.classList.contains('anim-in')) return;
                const delay = parseFloat(el.dataset.animDelay || 0) * 1000 + extraDelay;
                if (delay > 0) {
                    setTimeout(() => el.classList.add('anim-in'), delay);
                } else {
                    el.classList.add('anim-in');
                }
            };

            // Positive rootMargin so elements animate smoothly before user reaches them
            const observer = new IntersectionObserver((entries, obs) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        reveal(entry.target);
                        obs.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.05,
                rootMargin: '0px 0px 100px 0px'
            });

            elements.forEach(el => observer.observe(el));

            // Instant above-fold reveal without waiting for 2s external assets
            const revealAboveFold = () => {
                let aboveFoldIndex = 0;
                elements.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.top < (window.innerHeight * 1.15) && rect.bottom > 0) {
                        reveal(el, aboveFoldIndex * 60);
                        aboveFoldIndex++;
                    }
                });
            };

            // Run immediately
            requestAnimationFrame(revealAboveFold);
            if (document.readyState === 'complete') {
                setTimeout(revealAboveFold, 100);
            } else {
                window.addEventListener('load', revealAboveFold, { once: true });
                setTimeout(revealAboveFold, 400);
            }
        },


        initBackToTop() {
            if (!this.backToTopBtn) return;
            this.backToTopBtn.addEventListener('click', (e) => {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    };

    /* ==========================================================================
       4. KINETIC TYPOGRAPHY WORD REVEAL
       ========================================================================== */
    const KineticTypography = {
        init() {
            if (prefersReducedMotion) return;

            const headlines = document.querySelectorAll('.kinetic-headline');
            headlines.forEach(headline => {
                if (headline.dataset.kineticSplit) return;
                headline.dataset.kineticSplit = 'true';

                const words = headline.innerText.trim().split(/\s+/);
                headline.innerHTML = '';

                words.forEach((word, index) => {
                    const spanOuter = document.createElement('span');
                    spanOuter.className = 'word-reveal';
                    const spanInner = document.createElement('span');
                    spanInner.className = 'word-reveal-inner';
                    spanInner.innerText = word;
                    spanOuter.appendChild(spanInner);
                    headline.appendChild(spanOuter);

                    setTimeout(() => {
                        spanInner.classList.add('revealed');
                    }, 80 + index * 60);
                });
            });
        }
    };

    /* ==========================================================================
       5. NOTICEABLE 3D TILT, SPECULAR GLARE & MAGNETIC BUTTONS
       ========================================================================== */
    const MouseEffects = {
        spotlight: null,
        targetX: 0,
        targetY: 0,
        currentX: 0,
        currentY: 0,

        init() {
            this.spotlight = document.getElementById('cursorSpotlight');
            if (this.spotlight) {
                this.initSpotlight();
            }

            this.init3DTilt();
            this.initSpecularGlare();
            this.initMagneticElements();
        },

        initSpotlight() {
            let hasMoved = false;
            window.addEventListener('mousemove', (e) => {
                this.targetX = e.clientX;
                this.targetY = e.clientY;
                if (!hasMoved) {
                    hasMoved = true;
                    if (this.spotlight) this.spotlight.style.opacity = '1';
                }
            }, { passive: true });

            const updateSpotlight = () => {
                this.currentX += (this.targetX - this.currentX) * 0.12;
                this.currentY += (this.targetY - this.currentY) * 0.12;
                if (this.spotlight) {
                    // Use translate so the radial gradient is centered on cursor
                    this.spotlight.style.left = `${this.currentX}px`;
                    this.spotlight.style.top = `${this.currentY}px`;
                }
                requestAnimationFrame(updateSpotlight);
            };
            requestAnimationFrame(updateSpotlight);
        },

        init3DTilt() {
            // Use a Set to avoid duplicate listeners on elements with multiple matching classes
            const tiltCardSet = new Set();
            document.querySelectorAll('.tilt-card-3d, .kpi-card-glow').forEach(el => tiltCardSet.add(el));
            // Also add .hover-lift-3d that aren't already .tilt-card-3d
            document.querySelectorAll('.hover-lift-3d').forEach(el => {
                if (!el.classList.contains('tilt-card-3d')) tiltCardSet.add(el);
            });

            tiltCardSet.forEach(card => {
                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;

                    // Visible but elegant 3D tilt — 7deg for professional feel
                    const rotateX = ((y - centerY) / centerY) * -7;
                    const rotateY = ((x - centerX) / centerX) * 7;

                    card.style.transition = 'transform 0.12s cubic-bezier(0.16, 1, 0.3, 1)';
                    card.style.transform = `perspective(900px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-6px) translateZ(8px)`;

                    // Update glare position for tilt-glare element
                    card.style.setProperty('--mouse-x', `${x}px`);
                    card.style.setProperty('--mouse-y', `${y}px`);
                    const glare = card.querySelector('.tilt-glare');
                    if (glare) glare.style.opacity = '1';
                });

                card.addEventListener('mouseleave', () => {
                    card.style.transition = 'transform 0.45s cubic-bezier(0.16, 1, 0.3, 1)';
                    card.style.transform = '';
                    const glare = card.querySelector('.tilt-glare');
                    if (glare) glare.style.opacity = '0';
                });
            });
        },


        initSpecularGlare() {
            const glareCards = document.querySelectorAll('.card-specular-glare, .tilt-card-3d, .roc-card');
            glareCards.forEach(card => {
                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    card.style.setProperty('--mouse-x', `${x}px`);
                    card.style.setProperty('--mouse-y', `${y}px`);
                });
            });
        },

        initMagneticElements() {
            const magneticElements = document.querySelectorAll('.btn-magnetic, .btn-primary, .btn-secondary');
            magneticElements.forEach(el => {
                el.addEventListener('mousemove', (e) => {
                    const rect = el.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    const deltaX = (e.clientX - centerX) * 0.35;
                    const deltaY = (e.clientY - centerY) * 0.35;
                    // Cap translation to 14px for crisp control
                    const clampX = Math.max(-14, Math.min(14, deltaX));
                    const clampY = Math.max(-14, Math.min(14, deltaY));
                    el.style.transform = `translate3d(${clampX}px, ${clampY}px, 0)`;
                });

                el.addEventListener('mouseleave', () => {
                    el.style.transform = 'translate3d(0, 0, 0)';
                });
            });
        }
    };

    /* ==========================================================================
       6. BUTTON RIPPLE WAVE
       ========================================================================== */
    const ButtonInteractions = {
        init() {
            document.addEventListener('click', (e) => {
                const btn = e.target.closest('.btn-magnetic, .btn-primary, .btn-secondary, .btn-bookmark, .save-btn, .btn-sheen');
                if (!btn) return;

                const rect = btn.getBoundingClientRect();
                const wave = document.createElement('span');
                wave.className = 'ripple-wave';
                const size = Math.max(rect.width, rect.height) * 1.5;
                wave.style.width = wave.style.height = `${size}px`;
                wave.style.left = `${e.clientX - rect.left - size / 2}px`;
                wave.style.top = `${e.clientY - rect.top - size / 2}px`;

                btn.appendChild(wave);
                setTimeout(() => wave.remove(), 600);
            });
        }
    };

    /* ==========================================================================
       7. PARTICLE BURSTS & CONFETTI CELEBRATION
       ========================================================================== */
    const ParticleSystem = {
        burst(x, y, count = 16, colors = ['#00f2fe', '#06b6d4', '#38bdf8', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6']) {
            if (prefersReducedMotion) return;

            for (let i = 0; i < count; i++) {
                const particle = document.createElement('div');
                particle.className = 'confetti-particle';
                const size = Math.floor(Math.random() * 6) + 5;
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                particle.style.boxShadow = `0 0 10px ${particle.style.background}`;
                particle.style.left = `${x}px`;
                particle.style.top = `${y}px`;
                document.body.appendChild(particle);

                const angle = Math.random() * Math.PI * 2;
                const velocity = Math.random() * 110 + 50;
                const vx = Math.cos(angle) * velocity;
                const vy = Math.sin(angle) * velocity - 35;
                const startTime = performance.now();
                const duration = 700 + Math.random() * 300;

                const animate = (now) => {
                    const elapsed = now - startTime;
                    const progress = elapsed / duration;

                    if (progress < 1) {
                        const curX = x + vx * progress;
                        const curY = y + vy * progress + 0.5 * 220 * progress * progress;
                        const scale = 1 - progress * 0.65;
                        particle.style.transform = `translate3d(${curX - x}px, ${curY - y}px, 0) scale(${scale})`;
                        particle.style.opacity = `${1 - progress}`;
                        requestAnimationFrame(animate);
                    } else {
                        particle.remove();
                    }
                };

                requestAnimationFrame(animate);
            }
        },

        celebrate() {
            if (prefersReducedMotion) return;
            const width = window.innerWidth;
            const height = window.innerHeight;

            this.burst(width * 0.25, height * 0.35, 30);
            this.burst(width * 0.5, height * 0.25, 40);
            this.burst(width * 0.75, height * 0.35, 30);
            Toast.show('🎉 100% Document Verification Complete! Readiness Certified.', 'fa-trophy', '#f59e0b');
        }
    };

    /* ==========================================================================
       8. QUICK APPLY WORKFLOW CELEBRATION HELPER
       ========================================================================== */
    const QuickApplyFlow = {
        init() {
            // Provide global celebrateApplication hook for main.js Quick Apply Modal
            window.celebrateApplication = function (btn, title) {
                if (btn) {
                    btn.innerHTML = `<i class="fas fa-check-circle mr-1.5 text-emerald-500"></i> Already Applied ✓`;
                    btn.classList.remove('btn-primary');
                    btn.classList.add('btn-applied');
                    btn.disabled = true;
                    try {
                        const rect = btn.getBoundingClientRect();
                        ParticleSystem.burst(rect.left + rect.width / 2, rect.top + rect.height / 2, 24);
                    } catch (e) {}
                }
                // Update tracker badge count
                const badge = document.querySelector('.tracker-badge, #applicationCountBadge');
                if (badge) {
                    const count = parseInt(badge.innerText.trim(), 10) || 0;
                    badge.innerText = count + 1;
                    badge.classList.add('animate-bounce');
                    setTimeout(() => badge.classList.remove('animate-bounce'), 1200);
                }
            };
        }
    };

    /* ==========================================================================
       9. SAVE / BOOKMARK FLOW WITH CONFETTI SPARKS
       ========================================================================== */
    const BookmarkFlow = {
        init() {
            document.addEventListener('click', (e) => {
                const btn = e.target.closest('.save-btn, .btn-bookmark, .heart-pop');
                if (!btn) return;

                const rect = btn.getBoundingClientRect();
                const icon = btn.querySelector('i');
                const isSaved = btn.classList.contains('is-saved') || btn.classList.contains('bookmarked');

                if (!isSaved) {
                    ParticleSystem.burst(rect.left + rect.width / 2, rect.top + rect.height / 2, 16, ['#ef4444', '#f87171', '#fca5a5', '#ec4899']);
                    Toast.show('Opportunity saved to your wishlist!', 'fa-heart', '#ef4444');
                } else {
                    Toast.show('Removed from your wishlist.', 'fa-heart-crack', '#94a3b8');
                }
            });
        }
    };

    /* ==========================================================================
       10. NUMBER ROLLUP COUNTERS
       ========================================================================== */
    const NumberRollup = {
        init() {
            const counters = document.querySelectorAll('.counter-value, [data-counter]');
            if (!counters.length) return;

            if (prefersReducedMotion || !('IntersectionObserver' in window)) {
                counters.forEach(el => this.setFinalValue(el));
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

        animateCounter(element) {
            const rawText = element.dataset.counter || element.innerText.trim();
            const match = rawText.match(/^([^\d]*)([\d,.]+)(.*)$/);
            if (!match) return;

            const prefix = match[1] || '';
            const numStr = match[2].replace(/,/g, '');
            const targetNum = parseFloat(numStr);
            const suffix = match[3] || '';

            if (isNaN(targetNum)) return;

            const hasDecimals = numStr.includes('.');
            const decimalPlaces = hasDecimals ? numStr.split('.')[1].length : 0;
            const hasComma = match[2].includes(',');

            const duration = 1500;
            const startTime = performance.now();

            const easeOutExpo = (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

            const update = (now) => {
                const elapsed = now - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = easeOutExpo(progress);
                const current = targetNum * eased;

                let formattedNum = hasDecimals ? current.toFixed(decimalPlaces) : Math.floor(current).toString();
                if (hasComma) {
                    const parts = formattedNum.split('.');
                    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
                    formattedNum = parts.join('.');
                }

                element.innerText = `${prefix}${formattedNum}${suffix}`;

                if (progress < 1) {
                    requestAnimationFrame(update);
                } else {
                    this.setFinalValue(element, rawText);
                }
            };

            requestAnimationFrame(update);
        },

        setFinalValue(element, text) {
            element.innerText = text || element.dataset.counter || element.innerText;
        }
    };

    /* ==========================================================================
       11. SVG CHECKMARKS & PROGRESS RINGS
       ========================================================================== */
    const SvgAnimations = {
        init() {
            this.initChecklist();
            this.initCircularProgress();
        },

        initChecklist() {
            const items = document.querySelectorAll('.checklist-interactive-item');
            if (!items.length) return;

            items.forEach(item => {
                item.addEventListener('click', (e) => {
                    const checkbox = item.querySelector('input[type="checkbox"]');
                    if (checkbox && e.target !== checkbox) {
                        checkbox.checked = !checkbox.checked;
                        checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                    }

                    const isChecked = checkbox ? checkbox.checked : !item.classList.contains('checked');
                    item.classList.toggle('checked', isChecked);

                    if (isChecked) {
                        const rect = item.getBoundingClientRect();
                        ParticleSystem.burst(rect.right - 40, rect.top + rect.height / 2, 10, ['#10b981', '#06b6d4', '#00f2fe']);
                    }

                    const allChecked = Array.from(items).every(it => {
                        const cb = it.querySelector('input[type="checkbox"]');
                        return cb ? cb.checked : it.classList.contains('checked');
                    });

                    if (allChecked) {
                        ParticleSystem.celebrate();
                    }
                });
            });
        },

        initCircularProgress() {
            const rings = document.querySelectorAll('.circle-progress-bar');
            rings.forEach(ring => {
                const percent = parseFloat(ring.dataset.percent || 0);
                let circumference = 100;
                if (ring.r && ring.r.baseVal) {
                    circumference = 2 * Math.PI * ring.r.baseVal.value;
                } else if (typeof ring.getTotalLength === 'function') {
                    try {
                        circumference = ring.getTotalLength();
                    } catch (err) {
                        circumference = 100;
                    }
                }
                ring.style.strokeDasharray = `${circumference} ${circumference}`;
                ring.style.strokeDashoffset = `${circumference}`;

                setTimeout(() => {
                    const offset = circumference - (percent / 100) * circumference;
                    ring.style.strokeDashoffset = `${offset}`;
                }, 200);
            });
        }
    };

    /* ==========================================================================
       12. NAVIGATION INDICATOR & TRANSLATOR
       ========================================================================== */
    const NavIndicator = {
        init() {
            // Find the desktop nav links container — Tailwind's 'lg:flex' class
            // contains a colon that needs careful querySelector handling.
            // We use a more robust selector targeting the nav's direct child div.
            let nav = null;
            try {
                // Try the escaped Tailwind class selector first
                nav = document.querySelector('nav .hidden.lg\\:flex');
            } catch (e) {}
            if (!nav) {
                // Fallback: find the div inside nav that contains .nav-link elements
                const navEl = document.querySelector('nav');
                if (navEl) {
                    nav = navEl.querySelector('div.hidden') ||
                          navEl.querySelector('[class*="lg:flex"]') ||
                          navEl.querySelector('div:has(a.nav-link)');
                }
            }
            if (!nav) return;

            let pill = nav.querySelector('.nav-sliding-pill');
            if (!pill) {
                pill = document.createElement('div');
                pill.className = 'nav-sliding-pill';
                nav.style.position = 'relative';
                nav.appendChild(pill);
            }

            const links = nav.querySelectorAll('.nav-link');
            const activeLink = nav.querySelector('.nav-link.active') || links[0];

            const movePill = (target) => {
                if (!target || !pill) return;
                const rect = target.getBoundingClientRect();
                const navRect = nav.getBoundingClientRect();
                pill.style.width = `${rect.width * 0.82}px`;
                pill.style.left = `${(rect.left - navRect.left) + (rect.width * 0.09)}px`;
                pill.style.opacity = '1';
            };

            if (activeLink) movePill(activeLink);

            links.forEach(link => {
                link.addEventListener('mouseenter', () => movePill(link));
            });

            nav.addEventListener('mouseleave', () => {
                if (activeLink) movePill(activeLink);
                else if (pill) pill.style.opacity = '0';
            });
        }
    };

    const TranslatorCrossfade = {
        init() {
            const langToggles = document.querySelectorAll('.lang-toggle-btn, [data-lang-toggle], #rocLanguageSelector');
            if (!langToggles.length) return;

            langToggles.forEach(btn => {
                btn.addEventListener('change', () => {
                    const mainContent = document.querySelector('main') || document.body;
                    mainContent.classList.add('lang-crossfade', 'fading');
                    setTimeout(() => mainContent.classList.remove('fading'), 220);
                });
            });
        }
    };

    /* ==========================================================================
       13. INITIALIZE ALL ENGINES ON DOM READY
       ========================================================================== */
    const initAllEngines = () => {
        Toast.init();
        PageTransitions.init();
        ScrollAnimations.init();
        KineticTypography.init();
        MouseEffects.init();
        ButtonInteractions.init();
        QuickApplyFlow.init();
        BookmarkFlow.init();
        NumberRollup.init();
        SvgAnimations.init();
        NavIndicator.init();
        TranslatorCrossfade.init();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAllEngines);
    } else {
        initAllEngines();
    }

    window.Animmaster = {
        Toast,
        PageTransitions,
        ScrollAnimations,
        KineticTypography,
        MouseEffects,
        ParticleSystem,
        QuickApplyFlow,
        BookmarkFlow,
        NumberRollup,
        SvgAnimations
    };
})();
