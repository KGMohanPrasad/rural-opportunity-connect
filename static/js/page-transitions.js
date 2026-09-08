/**
 * Rural Opportunity Connect — Cinematic Page Transitions & Scroll Storytelling
 * 
 * Features:
 * - High-speed, 250-350ms seamless navigation transition
 * - Cyan glowing progress bar + subtle blur backdrop
 * - Zero lag on browser back/forward (pageshow cache handling)
 * - IntersectionObserver scroll storytelling (fade-up, fade-left, fade-right, scale-up, blur-to-sharp)
 * - Staggered children reveals for grids and cards
 * - Respects prefers-reduced-motion
 */

(function () {
    'use strict';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ==========================================================================
       1. CINEMATIC PAGE TRANSITIONS
       ========================================================================== */
    const CinematicNavigation = {
        bar: null,
        overlay: null,
        isTransitioning: false,

        init() {
            if (prefersReducedMotion) return;

            // Create progress bar if not exists
            this.bar = document.getElementById('cinematicTransitionBar');
            if (!this.bar) {
                this.bar = document.createElement('div');
                this.bar.id = 'cinematicTransitionBar';
                document.body.appendChild(this.bar);
            }

            // Create overlay if not exists
            this.overlay = document.getElementById('cinematicTransitionOverlay');
            if (!this.overlay) {
                this.overlay = document.createElement('div');
                this.overlay.id = 'cinematicTransitionOverlay';
                document.body.appendChild(this.overlay);
            }

            this.reset();
            this.bindEvents();
        },

        bindEvents() {
            // Handle Link clicks
            document.addEventListener('click', (e) => {
                const link = e.target.closest('a');
                if (!link) return;

                const href = link.getAttribute('href');
                const target = link.getAttribute('target');

                // Ignore external, anchor hashes, javascript, mailto, tel, downloads
                if (!href || href.startsWith('#') || href.startsWith('javascript:') || 
                    href.startsWith('mailto:') || href.startsWith('tel:') || link.hasAttribute('download')) {
                    return;
                }

                // Ignore new tabs or modifier keys
                if (target === '_blank' || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0) {
                    return;
                }

                // Check same origin
                try {
                    const targetUrl = new URL(link.href, window.location.origin);
                    if (targetUrl.origin !== window.location.origin) return;
                    // Ignore same page anchor navigation
                    if (targetUrl.pathname === window.location.pathname && targetUrl.search === window.location.search) {
                        return;
                    }

                    if (this.isTransitioning) return;
                    this.isTransitioning = true;

                    e.preventDefault();
                    this.startTransition(link.href);
                } catch (err) {
                    // Normal link fallback
                }
            });

            // Browser back/forward restoration
            window.addEventListener('pageshow', (event) => {
                this.reset();
            });

            // Finish on window load
            window.addEventListener('load', () => {
                this.reset();
            });
        },

        startTransition(targetHref) {
            if (this.bar) {
                this.bar.classList.add('active');
                this.bar.style.width = '45%';
            }
            if (this.overlay) {
                this.overlay.classList.add('active');
            }

            // Smooth forward progress
            setTimeout(() => {
                if (this.bar) this.bar.style.width = '85%';
            }, 100);

            // Execute navigation after short aesthetic delay (240ms)
            setTimeout(() => {
                window.location.href = targetHref;
            }, 240);
        },

        reset() {
            this.isTransitioning = false;
            if (this.bar) {
                this.bar.style.width = '100%';
                setTimeout(() => {
                    if (this.bar) {
                        this.bar.classList.remove('active');
                        this.bar.style.width = '0%';
                    }
                }, 200);
            }
            if (this.overlay) {
                this.overlay.classList.remove('active');
            }
        }
    };

    /* ==========================================================================
       2. SCROLL STORYTELLING OBSERVER
       ========================================================================== */
    const ScrollStorytelling = {
        init() {
            const elements = document.querySelectorAll(
                '[data-scroll-reveal], [data-anim], .anim-reveal, .anim-grid-stagger, .stat-3d-pedestal'
            );

            if (!elements.length) return;

            if (prefersReducedMotion || !('IntersectionObserver' in window)) {
                elements.forEach(el => {
                    el.classList.add('revealed', 'anim-in');
                });
                return;
            }

            const observer = new IntersectionObserver((entries, obs) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const target = entry.target;
                        target.classList.add('revealed', 'anim-in');
                        obs.unobserve(target);
                    }
                });
            }, {
                threshold: 0.08,
                rootMargin: '0px 0px 80px 0px'
            });

            elements.forEach(el => observer.observe(el));

            // Instant above-the-fold reveal
            const revealAboveFold = () => {
                const vh = window.innerHeight * 1.1;
                elements.forEach((el, index) => {
                    const rect = el.getBoundingClientRect();
                    if (rect.top < vh && rect.bottom > 0) {
                        setTimeout(() => {
                            el.classList.add('revealed', 'anim-in');
                        }, index * 40);
                    }
                });
            };

            requestAnimationFrame(revealAboveFold);
            setTimeout(revealAboveFold, 150);
        }
    };

    /* ==========================================================================
       3. BOOT ENGINE ON DOM READY
       ========================================================================== */
    const bootPageTransitions = () => {
        CinematicNavigation.init();
        ScrollStorytelling.init();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootPageTransitions);
    } else {
        bootPageTransitions();
    }

    window.CinematicNavigation = CinematicNavigation;
    window.ScrollStorytelling = ScrollStorytelling;
})();
