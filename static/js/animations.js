/**
 * Rural Opportunity Connect — Core Animations Engine
 * Handles:
 * - Kinetic Typography Word/Line Reveals
 * - 3D Horizontal Carousel Drag & Navigation
 * - Floating Elements & Ambient Light Rays
 * - Input Focus Micro-Animations
 */

(function () {
    'use strict';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ==========================================================================
       1. KINETIC TYPOGRAPHY HEADLINE WORD REVEAL
       ========================================================================== */
    const KineticTypography = {
        init() {

            const headlines = document.querySelectorAll('.kinetic-headline');
            headlines.forEach(hl => {
                if (hl.dataset.kineticSplit) return;
                hl.dataset.kineticSplit = 'true';

                const words = hl.innerText.trim().split(/\s+/);
                hl.innerHTML = '';

                words.forEach((word, idx) => {
                    const spanOuter = document.createElement('span');
                    spanOuter.className = 'inline-block overflow-hidden mr-1.5 pb-1 align-top';
                    const spanInner = document.createElement('span');
                    spanInner.className = 'kinetic-hero-word';
                    spanInner.style.animationDelay = `${0.08 + idx * 0.06}s`;
                    spanInner.innerText = word;
                    spanOuter.appendChild(spanInner);
                    hl.appendChild(spanOuter);
                });
            });
        }
    };

    /* ==========================================================================
       2. 3D HORIZONTAL PERSPECTIVE CAROUSEL
       ========================================================================== */
    const Carousel3D = {
        stage: null,
        cards: [],
        currentIndex: 0,
        prevBtn: null,
        nextBtn: null,
        isDragging: false,
        startX: 0,
        currentTranslate: 0,
        prevTranslate: 0,

        init() {
            this.stage = document.getElementById('carousel3dStage');
            if (!this.stage) return;

            this.cards = Array.from(this.stage.querySelectorAll('.carousel-3d-card'));
            this.prevBtn = document.getElementById('carouselPrevBtn');
            this.nextBtn = document.getElementById('carouselNextBtn');

            if (!this.cards.length) return;

            this.updateCarousel();
            this.bindEvents();
        },

        bindEvents() {
            if (this.prevBtn) {
                this.prevBtn.addEventListener('click', () => {
                    this.currentIndex = Math.max(0, this.currentIndex - 1);
                    this.updateCarousel();
                });
            }

            if (this.nextBtn) {
                this.nextBtn.addEventListener('click', () => {
                    this.currentIndex = Math.min(this.cards.length - 1, this.currentIndex + 1);
                    this.updateCarousel();
                });
            }

            // Touch / Mouse drag
            this.stage.addEventListener('mousedown', (e) => this.dragStart(e), { passive: true });
            window.addEventListener('mousemove', (e) => this.dragMove(e), { passive: true });
            window.addEventListener('mouseup', () => this.dragEnd());

            this.stage.addEventListener('touchstart', (e) => this.dragStart(e), { passive: true });
            window.addEventListener('touchmove', (e) => this.dragMove(e), { passive: true });
            window.addEventListener('touchend', () => this.dragEnd());
        },

        dragStart(e) {
            this.isDragging = true;
            this.startX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
        },

        dragMove(e) {
            if (!this.isDragging) return;
            const currentX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
            const diff = currentX - this.startX;

            if (Math.abs(diff) > 50) {
                if (diff > 0 && this.currentIndex > 0) {
                    this.currentIndex--;
                    this.updateCarousel();
                    this.isDragging = false;
                } else if (diff < 0 && this.currentIndex < this.cards.length - 1) {
                    this.currentIndex++;
                    this.updateCarousel();
                    this.isDragging = false;
                }
            }
        },

        dragEnd() {
            this.isDragging = false;
        },

        updateCarousel() {
            const cardWidth = this.cards[0].offsetWidth + 24; // Width + gap
            const offset = -this.currentIndex * cardWidth;

            this.stage.style.transform = `translateX(${offset}px)`;

            this.cards.forEach((card, index) => {
                const diff = index - this.currentIndex;
                if (diff === 0) {
                    card.style.transform = 'scale(1) rotateY(0deg) translateZ(0)';
                    card.style.opacity = '1';
                } else if (diff === 1) {
                    card.style.transform = 'scale(0.94) rotateY(-8deg) translateZ(-40px)';
                    card.style.opacity = '0.75';
                } else if (diff === -1) {
                    card.style.transform = 'scale(0.94) rotateY(8deg) translateZ(-40px)';
                    card.style.opacity = '0.75';
                } else {
                    card.style.transform = 'scale(0.88) translateZ(-80px)';
                    card.style.opacity = '0.4';
                }
            });

            if (this.prevBtn) this.prevBtn.disabled = this.currentIndex === 0;
            if (this.nextBtn) this.nextBtn.disabled = this.currentIndex === this.cards.length - 1;
        }
    };

    /* ==========================================================================
       3. BOOT ANIMATIONS
       ========================================================================== */
    const bootAnimations = () => {
        KineticTypography.init();
        Carousel3D.init();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bootAnimations);
    } else {
        bootAnimations();
    }

    window.KineticTypography = KineticTypography;
    window.Carousel3D = Carousel3D;
})();
