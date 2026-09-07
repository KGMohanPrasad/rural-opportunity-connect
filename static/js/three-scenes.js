/**
 * Rural Opportunity Connect — Enterprise 3D WebGL Engine (v10.0)
 * Powered by Three.js (r128) + Vanilla WebGL
 * 
 * Modules:
 * 1. GlobalParticleField — Background WebGL constellation with cursor inertia
 * 2. HeroOpportunityNetwork — Full-width interactive 3D Opportunity Network with Raycasting
 * 3. Category3DViewer — Miniature WebGL models for 5 opportunity sectors
 * 4. Opportunity3DCarousel — Horizontal 3D perspective opportunity carousel
 * 5. Timeline3DProgress — 5-stage interactive connected process pipeline
 * 6. Header3DCanvases — Ambient 3D floating header elements for internal pages
 * 7. Profile3DProgressRing — WebGL/SVG 3D progress ring for Dashboard and Profile
 */

(function () {
    'use strict';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isTouchDevice = window.matchMedia('(hover: none) and (pointer: coarse)').matches || ('ontouchstart' in window);

    /* ==========================================================================
       1. GLOBAL BACKGROUND PARTICLE FIELD (All Pages)
       ========================================================================== */
    const GlobalParticleField = {
        scene: null,
        camera: null,
        renderer: null,
        particles: null,
        animationId: null,
        mouseX: 0,
        mouseY: 0,
        targetMouseX: 0,
        targetMouseY: 0,
        isPaused: false,

        init() {
            if (!window.THREE || prefersReducedMotion) return;

            const canvas = document.getElementById('globalWebglCanvas');
            if (!canvas) return;

            try {
                this.renderer = new THREE.WebGLRenderer({
                    canvas: canvas,
                    alpha: true,
                    antialias: false,
                    powerPreference: "low-power"
                });
            } catch (e) {
                console.warn('Global WebGL not active:', e);
                return;
            }

            const width = window.innerWidth;
            const height = window.innerHeight;

            this.renderer.setSize(width, height);
            this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

            this.scene = new THREE.Scene();
            this.camera = new THREE.PerspectiveCamera(60, width / height, 1, 1000);
            this.camera.position.z = 300;

            // Constellation Particles
            const count = isTouchDevice ? 150 : 380;
            const positions = new Float32Array(count * 3);
            const colors = new Float32Array(count * 3);

            for (let i = 0; i < count; i++) {
                positions[i * 3] = (Math.random() - 0.5) * 800;
                positions[i * 3 + 1] = (Math.random() - 0.5) * 800;
                positions[i * 3 + 2] = (Math.random() - 0.5) * 600;

                // Color palette: Cyan, Sky Blue, Navy
                const r = Math.random();
                if (r > 0.6) {
                    colors[i * 3] = 0.02; colors[i * 3 + 1] = 0.71; colors[i * 3 + 2] = 0.83; // #06b6d4
                } else if (r > 0.3) {
                    colors[i * 3] = 0.01; colors[i * 3 + 1] = 0.52; colors[i * 3 + 2] = 0.78; // #0284c7
                } else {
                    colors[i * 3] = 0.0; colors[i * 3 + 1] = 0.95; colors[i * 3 + 2] = 1.0;  // #00f2fe
                }
            }

            const geometry = new THREE.BufferGeometry();
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

            const material = new THREE.PointsMaterial({
                size: isTouchDevice ? 2.5 : 3.0,
                vertexColors: true,
                transparent: true,
                opacity: 0.55,
                blending: THREE.AdditiveBlending
            });

            this.particles = new THREE.Points(geometry, material);
            this.scene.add(this.particles);

            // Mouse tracking with inertia
            if (!isTouchDevice) {
                window.addEventListener('mousemove', (e) => {
                    this.targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2;
                    this.targetMouseY = (e.clientY / window.innerHeight - 0.5) * 2;
                }, { passive: true });
            }

            // Window Resize
            window.addEventListener('resize', () => {
                if (!this.camera || !this.renderer) return;
                const w = window.innerWidth;
                const h = window.innerHeight;
                this.camera.aspect = w / h;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize(w, h);
            }, { passive: true });

            // Visibility API to save battery
            document.addEventListener('visibilitychange', () => {
                this.isPaused = document.hidden;
            });

            this.animate();
        },

        animate() {
            this.animationId = requestAnimationFrame(() => this.animate());

            if (this.isPaused || !this.particles) return;

            // Smooth mouse follow
            this.mouseX += (this.targetMouseX - this.mouseX) * 0.04;
            this.mouseY += (this.targetMouseY - this.mouseY) * 0.04;

            this.particles.rotation.y += 0.0006;
            this.particles.rotation.x = this.mouseY * 0.15;
            this.particles.rotation.y += this.mouseX * 0.002;

            this.renderer.render(this.scene, this.camera);
        }
    };

    /* ==========================================================================
       2. HERO 3D OPPORTUNITY NETWORK (Landing Page)
       ========================================================================== */
    const HeroOpportunityNetwork = {
        container: null,
        canvas: null,
        scene: null,
        camera: null,
        renderer: null,
        raycaster: null,
        mouse: null,
        networkGroup: null,
        coreMesh: null,
        coreGlowMesh: null,
        orbitalRings: [],
        nodeMeshes: [],
        connectionCurves: [],
        floatingCardsGroup: null,
        hoveredNode: null,
        isDragging: false,
        prevPointerX: 0,
        prevPointerY: 0,
        rotVelocityX: 0,
        rotVelocityY: 0,
        cameraTargetZ: 260,
        cameraCurrentZ: 260,
        mouseX: 0,
        mouseY: 0,
        targetMouseX: 0,
        targetMouseY: 0,
        clock: null,
        tooltipEl: null,

        // 5 Core Opportunity Sectors
        sectors: [
            {
                id: 'jobs',
                title: 'Rural Jobs',
                count: '35+ Live',
                desc: 'Local, semi-urban & remote verified livelihoods',
                url: '/jobs/',
                color: 0x0284c7, // Tech Blue
                glowColor: 0x38bdf8,
                radius: 110,
                angle: (0 * Math.PI * 2) / 5,
                y: 28,
                speed: 0.008,
                icon: '💼'
            },
            {
                id: 'scholarships',
                title: 'Higher Scholarships',
                count: '25+ Grants',
                desc: 'Post-matric tuition waivers & CSR funding',
                url: '/scholarships/',
                color: 0xa855f7, // Purple
                glowColor: 0xd8b4fe,
                radius: 125,
                angle: (1 * Math.PI * 2) / 5,
                y: -22,
                speed: 0.006,
                icon: '🎓'
            },
            {
                id: 'schemes',
                title: 'Government Schemes',
                count: '40+ Welfare',
                desc: 'Central & State DBT direct benefit transfers',
                url: '/schemes/',
                color: 0x06b6d4, // Cyan
                glowColor: 0x67e8f9,
                radius: 105,
                angle: (2 * Math.PI * 2) / 5,
                y: 36,
                speed: 0.009,
                icon: '🏛️'
            },
            {
                id: 'skills',
                title: 'Skill Programs',
                count: '20+ Courses',
                desc: 'Certified technical, digital & vocational courses',
                url: '/skills/',
                color: 0x38bdf8, // Sky Blue
                glowColor: 0xbae6fd,
                radius: 130,
                angle: (3 * Math.PI * 2) / 5,
                y: -14,
                speed: 0.007,
                icon: '💻'
            },
            {
                id: 'business',
                title: 'Micro-Enterprises',
                count: '15+ Blueprints',
                desc: 'Village business models & PMEGP subsidies',
                url: '/business/',
                color: 0x00f2fe, // Neon Cyan
                glowColor: 0xa5f3fc,
                radius: 115,
                angle: (4 * Math.PI * 2) / 5,
                y: 8,
                speed: 0.008,
                icon: '🚀'
            }
        ],

        init() {
            this.container = document.getElementById('heroOpportunityNetworkContainer');
            this.canvas = document.getElementById('heroOpportunityNetworkCanvas');
            this.tooltipEl = document.getElementById('heroNodeTooltip');

            if (!this.container || !this.canvas || !window.THREE) return;

            const width = this.container.clientWidth || 800;
            const height = this.container.clientHeight || 560;

            try {
                this.renderer = new THREE.WebGLRenderer({
                    canvas: this.canvas,
                    alpha: true,
                    antialias: true,
                    powerPreference: "high-performance"
                });
            } catch (e) {
                console.warn('Hero 3D Network WebGL failed:', e);
                return;
            }

            this.renderer.setSize(width, height);
            this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

            this.scene = new THREE.Scene();
            this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
            this.camera.position.z = this.cameraTargetZ;

            this.raycaster = new THREE.Raycaster();
            this.mouse = new THREE.Vector2(-999, -999);
            this.clock = new THREE.Clock();

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
            this.scene.add(ambientLight);

            const dirLight = new THREE.DirectionalLight(0x00f2fe, 1.2);
            dirLight.position.set(120, 150, 180);
            this.scene.add(dirLight);

            const pointLight = new THREE.PointLight(0x06b6d4, 2.5, 400);
            pointLight.position.set(0, 0, 0);
            this.scene.add(pointLight);

            // Master Group
            this.networkGroup = new THREE.Group();
            this.scene.add(this.networkGroup);

            this.buildOpportunityCore();
            this.buildOrbitalRings();
            this.buildSectorNodesAndBeziers();
            this.buildConstellationDust();

            this.bindEvents();
            this.animate();
        },

        // 1. Central Opportunity Core
        buildOpportunityCore() {
            // Outer Wireframe Polyhedron
            const coreGeo = new THREE.IcosahedronGeometry(42, 1);
            const coreMat = new THREE.MeshStandardMaterial({
                color: 0x06b6d4,
                wireframe: true,
                transparent: true,
                opacity: 0.45,
                emissive: 0x0284c7,
                emissiveIntensity: 0.3
            });
            this.coreMesh = new THREE.Mesh(coreGeo, coreMat);
            this.networkGroup.add(this.coreMesh);

            // Inner Pulsating Core Sphere
            const innerGeo = new THREE.SphereGeometry(22, 32, 32);
            const innerMat = new THREE.MeshStandardMaterial({
                color: 0x00f2fe,
                emissive: 0x06b6d4,
                emissiveIntensity: 0.8,
                roughness: 0.2,
                metalness: 0.8,
                transparent: true,
                opacity: 0.85
            });
            this.coreGlowMesh = new THREE.Mesh(innerGeo, innerMat);
            this.networkGroup.add(this.coreGlowMesh);

            // Central Pulsing Aura Sprite
            const auraCanvas = document.createElement('canvas');
            auraCanvas.width = 128;
            auraCanvas.height = 128;
            const ctx = auraCanvas.getContext('2d');
            const grad = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
            grad.addColorStop(0, 'rgba(0, 242, 254, 0.85)');
            grad.addColorStop(0.4, 'rgba(6, 182, 212, 0.35)');
            grad.addColorStop(1, 'rgba(7, 21, 38, 0)');
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, 128, 128);

            const auraTexture = new THREE.CanvasTexture(auraCanvas);
            const auraMat = new THREE.SpriteMaterial({
                map: auraTexture,
                transparent: true,
                blending: THREE.AdditiveBlending,
                opacity: 0.75
            });
            const auraSprite = new THREE.Sprite(auraMat);
            auraSprite.scale.set(110, 110, 1);
            this.networkGroup.add(auraSprite);
        },

        // 2. Holographic Orbital Rings
        buildOrbitalRings() {
            const ringConfigs = [
                { r: 72, tiltX: 0.45, tiltY: 0.2, color: 0x00f2fe, opacity: 0.3 },
                { r: 96, tiltX: -0.55, tiltY: 0.4, color: 0x38bdf8, opacity: 0.22 },
                { r: 128, tiltX: 0.2, tiltY: -0.6, color: 0x0284c7, opacity: 0.18 }
            ];

            ringConfigs.forEach(cfg => {
                const ringGeo = new THREE.RingGeometry(cfg.r - 0.7, cfg.r + 0.7, 96);
                const ringMat = new THREE.MeshBasicMaterial({
                    color: cfg.color,
                    side: THREE.DoubleSide,
                    transparent: true,
                    opacity: cfg.opacity
                });
                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.x = Math.PI / 2 + cfg.tiltX;
                ring.rotation.y = cfg.tiltY;
                this.networkGroup.add(ring);
                this.orbitalRings.push({ mesh: ring, speedX: cfg.tiltX * 0.003, speedY: cfg.tiltY * 0.002 });
            });
        },

        // 3. Five Luminous Sector Nodes & Connected Beziers
        buildSectorNodesAndBeziers() {
            this.sectors.forEach((sec, idx) => {
                // Group for Node + Glow + Beacon
                const nodeGroup = new THREE.Group();

                // Core Sphere
                const sphereGeo = new THREE.SphereGeometry(7.5, 24, 24);
                const sphereMat = new THREE.MeshStandardMaterial({
                    color: sec.color,
                    emissive: sec.glowColor,
                    emissiveIntensity: 0.75,
                    roughness: 0.2,
                    metalness: 0.6
                });
                const sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
                sphereMesh.userData = { sector: sec, isNode: true };
                nodeGroup.add(sphereMesh);

                // Halo Wireframe Ring around each node
                const haloGeo = new THREE.TorusGeometry(11, 0.6, 12, 32);
                const haloMat = new THREE.MeshBasicMaterial({
                    color: sec.glowColor,
                    transparent: true,
                    opacity: 0.6
                });
                const haloMesh = new THREE.Mesh(haloGeo, haloMat);
                haloMesh.rotation.x = Math.PI / 3;
                nodeGroup.add(haloMesh);

                // Initial positioning
                const x = Math.cos(sec.angle) * sec.radius;
                const z = Math.sin(sec.angle) * sec.radius;
                nodeGroup.position.set(x, sec.y, z);

                this.networkGroup.add(nodeGroup);

                // Connecting Line / Dynamic Bezier from (0,0,0) to node
                const curve = new THREE.QuadraticBezierCurve3(
                    new THREE.Vector3(0, 0, 0),
                    new THREE.Vector3(x * 0.5, sec.y + 16, z * 0.5),
                    new THREE.Vector3(x, sec.y, z)
                );

                const points = curve.getPoints(32);
                const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
                const lineMat = new THREE.LineBasicMaterial({
                    color: sec.color,
                    transparent: true,
                    opacity: 0.45,
                    linewidth: 1.5
                });
                const lineMesh = new THREE.Line(lineGeo, lineMat);
                this.networkGroup.add(lineMesh);

                // Traveling Light Pulse on line
                const pulseGeo = new THREE.SphereGeometry(2.0, 12, 12);
                const pulseMat = new THREE.MeshBasicMaterial({
                    color: 0xffffff,
                    transparent: true,
                    opacity: 0.95
                });
                const pulseMesh = new THREE.Mesh(pulseGeo, pulseMat);
                this.networkGroup.add(pulseMesh);

                this.nodeMeshes.push({
                    group: nodeGroup,
                    sphere: sphereMesh,
                    halo: haloMesh,
                    curve: curve,
                    line: lineMesh,
                    pulse: pulseMesh,
                    pulseT: Math.random(),
                    sector: sec,
                    baseRadius: sec.radius,
                    angle: sec.angle,
                    speed: sec.speed,
                    baseY: sec.y
                });
            });
        },

        // 4. Ambient Constellation Dust Particles
        buildConstellationDust() {
            const count = 180;
            const positions = new Float32Array(count * 3);
            const colors = new Float32Array(count * 3);

            for (let i = 0; i < count; i++) {
                const r = 45 + Math.random() * 115;
                const theta = Math.random() * Math.PI * 2;
                const phi = (Math.random() - 0.5) * Math.PI * 0.8;

                positions[i * 3] = r * Math.cos(theta) * Math.cos(phi);
                positions[i * 3 + 1] = r * Math.sin(phi);
                positions[i * 3 + 2] = r * Math.sin(theta) * Math.cos(phi);

                colors[i * 3] = 0.02;
                colors[i * 3 + 1] = 0.71;
                colors[i * 3 + 2] = 0.83;
            }

            const geo = new THREE.BufferGeometry();
            geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

            const mat = new THREE.PointsMaterial({
                size: 2.2,
                vertexColors: true,
                transparent: true,
                opacity: 0.6,
                blending: THREE.AdditiveBlending
            });

            const dust = new THREE.Points(geo, mat);
            this.networkGroup.add(dust);
        },

        // Event Handling
        bindEvents() {
            // Mouse Raycasting & Inertia Parallax
            this.container.addEventListener('mousemove', (e) => {
                const rect = this.canvas.getBoundingClientRect();
                this.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                this.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

                this.targetMouseX = this.mouse.x * 0.4;
                this.targetMouseY = this.mouse.y * 0.4;

                this.checkRaycast(e);
            }, { passive: true });

            this.container.addEventListener('mouseleave', () => {
                this.mouse.set(-999, -999);
                this.resetHover();
                this.targetMouseX = 0;
                this.targetMouseY = 0;
            });

            // Drag Rotation with Momentum
            this.container.addEventListener('pointerdown', (e) => {
                this.isDragging = true;
                this.prevPointerX = e.clientX;
                this.prevPointerY = e.clientY;
                this.rotVelocityX = 0;
                this.rotVelocityY = 0;
                this.canvas.style.cursor = 'grabbing';
            });

            window.addEventListener('pointermove', (e) => {
                if (!this.isDragging) return;
                const deltaX = e.clientX - this.prevPointerX;
                const deltaY = e.clientY - this.prevPointerY;
                this.rotVelocityY = deltaX * 0.007;
                this.rotVelocityX = deltaY * 0.007;
                this.networkGroup.rotation.y += this.rotVelocityY;
                this.networkGroup.rotation.x += this.rotVelocityX;
                this.prevPointerX = e.clientX;
                this.prevPointerY = e.clientY;
            }, { passive: true });

            window.addEventListener('pointerup', () => {
                this.isDragging = false;
                if (this.canvas) this.canvas.style.cursor = 'grab';
            });

            // Scroll-Driven Camera Depth & Transitions
            window.addEventListener('scroll', () => {
                const scrollY = window.pageYOffset || document.documentElement.scrollTop;
                if (scrollY < 900) {
                    // Pull back camera and gently tilt
                    this.cameraTargetZ = 260 + (scrollY * 0.15);
                    if (this.networkGroup) {
                        this.networkGroup.position.y = -scrollY * 0.08;
                    }
                }
            }, { passive: true });

            // Responsive Resize
            window.addEventListener('resize', () => {
                if (!this.container || !this.camera || !this.renderer) return;
                const w = this.container.clientWidth;
                const h = this.container.clientHeight;
                this.camera.aspect = w / h;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize(w, h);
            }, { passive: true });
        },

        // Raycasting for interactive hover nodes
        checkRaycast(event) {
            this.raycaster.setFromCamera(this.mouse, this.camera);
            const interactables = this.nodeMeshes.map(n => n.sphere);
            const intersects = this.raycaster.intersectObjects(interactables);

            if (intersects.length > 0) {
                const hit = intersects[0].object;
                const hitNode = this.nodeMeshes.find(n => n.sphere === hit);

                if (hitNode && this.hoveredNode !== hitNode) {
                    this.setHover(hitNode, event);
                }
            } else if (this.hoveredNode) {
                this.resetHover();
            }
        },

        setHover(nodeData, event) {
            this.hoveredNode = nodeData;
            this.canvas.style.cursor = 'pointer';

            // Scale up node & intensify halo
            nodeData.group.scale.set(1.4, 1.4, 1.4);
            nodeData.halo.scale.set(1.3, 1.3, 1.3);
            nodeData.sphere.material.emissiveIntensity = 1.3;
            nodeData.line.material.opacity = 0.95;
            nodeData.line.material.color.setHex(0x00f2fe);

            // Update interactive Tooltip
            if (this.tooltipEl) {
                const sec = nodeData.sector;
                this.tooltipEl.innerHTML = `
                    <div class="flex items-center gap-2 mb-1">
                        <span class="text-base">${sec.icon}</span>
                        <h4 class="font-extrabold text-white text-xs leading-none">${sec.title}</h4>
                        <span class="bg-cyan-400/20 text-cyan-300 text-[9px] font-black px-2 py-0.5 rounded-full border border-cyan-400/30 ml-auto">${sec.count}</span>
                    </div>
                    <p class="text-[10px] text-slate-300 leading-snug mb-2">${sec.desc}</p>
                    <a href="${sec.url}" class="inline-flex items-center gap-1 text-[10px] font-bold text-cyan-300 hover:text-white transition">
                        Explore Category <i class="fas fa-arrow-right text-[8px]"></i>
                    </a>
                `;

                const rect = this.container.getBoundingClientRect();
                const x = Math.min(Math.max(event.clientX - rect.left + 15, 10), rect.width - 240);
                const y = Math.min(Math.max(event.clientY - rect.top - 60, 10), rect.height - 110);

                this.tooltipEl.style.left = `${x}px`;
                this.tooltipEl.style.top = `${y}px`;
                this.tooltipEl.classList.add('visible');
            }
        },

        resetHover() {
            if (this.hoveredNode) {
                this.hoveredNode.group.scale.set(1, 1, 1);
                this.hoveredNode.halo.scale.set(1, 1, 1);
                this.hoveredNode.sphere.material.emissiveIntensity = 0.75;
                this.hoveredNode.line.material.opacity = 0.45;
                this.hoveredNode.line.material.color.setHex(this.hoveredNode.sector.color);
                this.hoveredNode = null;
            }
            if (this.tooltipEl) {
                this.tooltipEl.classList.remove('visible');
            }
            if (this.canvas) this.canvas.style.cursor = 'grab';
        },

        // Master Animation Loop
        animate() {
            requestAnimationFrame(() => this.animate());

            const delta = this.clock.getDelta();
            const time = this.clock.getElapsedTime();

            // 1. Inertia Drag Friction
            if (!this.isDragging) {
                this.networkGroup.rotation.y += 0.003 + this.rotVelocityY;
                this.networkGroup.rotation.x += this.rotVelocityX;
                this.rotVelocityY *= 0.94;
                this.rotVelocityX *= 0.94;

                // Subtle mouse parallax
                this.mouseX += (this.targetMouseX - this.mouseX) * 0.05;
                this.mouseY += (this.targetMouseY - this.mouseY) * 0.05;
                this.networkGroup.rotation.x = (this.networkGroup.rotation.x * 0.96) + (this.mouseY * 0.25 * 0.04);
            }

            // Smooth Camera Z
            this.cameraCurrentZ += (this.cameraTargetZ - this.cameraCurrentZ) * 0.06;
            this.camera.position.z = this.cameraCurrentZ;

            // 2. Animate Core Pulsing
            const pulseScale = 1 + Math.sin(time * 2.2) * 0.06;
            if (this.coreGlowMesh) this.coreGlowMesh.scale.set(pulseScale, pulseScale, pulseScale);
            if (this.coreMesh) {
                this.coreMesh.rotation.y += 0.006;
                this.coreMesh.rotation.z += 0.004;
            }

            // 3. Animate Orbital Rings
            this.orbitalRings.forEach(r => {
                r.mesh.rotation.z += 0.004;
            });

            // 4. Animate Nodes and Traveling Pulses
            this.nodeMeshes.forEach(node => {
                // Orbit movement
                node.angle += node.speed;
                const x = Math.cos(node.angle) * node.baseRadius;
                const z = Math.sin(node.angle) * node.baseRadius;
                const y = node.baseY + Math.sin(time * 2 + node.angle) * 7;

                node.group.position.set(x, y, z);
                node.halo.rotation.z += 0.02;

                // Update dynamic curve endpoints
                node.curve.v1.set(x * 0.5, y + 14, z * 0.5);
                node.curve.v2.set(x, y, z);
                const points = node.curve.getPoints(24);
                node.line.geometry.setFromPoints(points);

                // Traveling pulse on curve
                node.pulseT = (node.pulseT + 0.012) % 1;
                const pulsePos = node.curve.getPoint(node.pulseT);
                node.pulse.position.copy(pulsePos);
            });

            this.renderer.render(this.scene, this.camera);
        }
    };

    /* ==========================================================================
       3. CATEGORY 3D MINI-OBJECTS (Homepage Sectors)
       ========================================================================== */
    const Category3DViewer = {
        instances: [],

        init() {
            if (!window.THREE || prefersReducedMotion) return;

            const canvases = document.querySelectorAll('.category-3d-canvas');
            if (!canvases.length) return;

            canvases.forEach(canvas => {
                const category = canvas.dataset.category || 'jobs';
                this.createCategoryScene(canvas, category);
            });
        },

        createCategoryScene(canvas, category) {
            let renderer;
            try {
                renderer = new THREE.WebGLRenderer({
                    canvas: canvas,
                    alpha: true,
                    antialias: true,
                    powerPreference: "low-power"
                });
            } catch (e) {
                return;
            }

            const size = 96;
            renderer.setSize(size, size);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
            camera.position.z = 28;

            const ambient = new THREE.AmbientLight(0xffffff, 0.9);
            scene.add(ambient);

            const dirLight = new THREE.DirectionalLight(0x00f2fe, 1.4);
            dirLight.position.set(10, 15, 20);
            scene.add(dirLight);

            const group = new THREE.Group();
            scene.add(group);

            // Distinct 3D Model based on category
            if (category === 'jobs') {
                // 3D Career Node: Octahedron + Orbiting Torus
                const geo = new THREE.OctahedronGeometry(6.5, 0);
                const mat = new THREE.MeshStandardMaterial({ color: 0x0284c7, metalness: 0.6, roughness: 0.2 });
                const mesh = new THREE.Mesh(geo, mat);
                group.add(mesh);

                const ringGeo = new THREE.TorusGeometry(9.5, 0.4, 8, 32);
                const ringMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });
                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.x = Math.PI / 3;
                group.add(ring);
            } else if (category === 'scholarships') {
                // 3D Academic Crest: Icosahedron + Diamond Cap
                const geo = new THREE.IcosahedronGeometry(6.5, 0);
                const mat = new THREE.MeshStandardMaterial({ color: 0xa855f7, metalness: 0.7, roughness: 0.2 });
                const mesh = new THREE.Mesh(geo, mat);
                group.add(mesh);

                const starGeo = new THREE.RingGeometry(8.5, 9.5, 6);
                const starMat = new THREE.MeshBasicMaterial({ color: 0xd8b4fe, side: THREE.DoubleSide });
                const star = new THREE.Mesh(starGeo, starMat);
                group.add(star);
            } else if (category === 'schemes') {
                // 3D Government Pillar/Shield: Cylinder + Halo
                const geo = new THREE.CylinderGeometry(4.5, 5.5, 9, 6);
                const mat = new THREE.MeshStandardMaterial({ color: 0x06b6d4, metalness: 0.5, roughness: 0.3 });
                const mesh = new THREE.Mesh(geo, mat);
                group.add(mesh);

                const ringGeo = new THREE.TorusGeometry(8.5, 0.5, 8, 32);
                const ringMat = new THREE.MeshBasicMaterial({ color: 0x67e8f9 });
                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.x = Math.PI / 2;
                group.add(ring);
            } else if (category === 'skills') {
                // 3D Skill Matrix: Dodecahedron + Double Ring
                const geo = new THREE.DodecahedronGeometry(6.5, 0);
                const mat = new THREE.MeshStandardMaterial({ color: 0x0284c7, metalness: 0.8, roughness: 0.2 });
                const mesh = new THREE.Mesh(geo, mat);
                group.add(mesh);

                const ringGeo = new THREE.TorusGeometry(9.0, 0.4, 8, 24);
                const ringMat = new THREE.MeshBasicMaterial({ color: 0x00f2fe, wireframe: true });
                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.y = Math.PI / 4;
                group.add(ring);
            } else {
                // 3D Enterprise Prism: Cone Rocket Node
                const geo = new THREE.ConeGeometry(5.5, 11, 5);
                const mat = new THREE.MeshStandardMaterial({ color: 0x00f2fe, metalness: 0.7, roughness: 0.2 });
                const mesh = new THREE.Mesh(geo, mat);
                mesh.rotation.x = -Math.PI / 6;
                group.add(mesh);

                const baseGeo = new THREE.TorusGeometry(7.0, 0.5, 8, 24);
                const baseMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
                const base = new THREE.Mesh(baseGeo, baseMat);
                base.rotation.x = Math.PI / 2;
                group.add(base);
            }

            const card = canvas.closest('.tilt-card-3d, .roc-card');
            let isHovered = false;

            if (card) {
                card.addEventListener('mouseenter', () => { isHovered = true; });
                card.addEventListener('mouseleave', () => { isHovered = false; });
            }

            const animate = () => {
                requestAnimationFrame(animate);
                const rotSpeed = isHovered ? 0.04 : 0.012;
                group.rotation.y += rotSpeed;
                group.rotation.x += isHovered ? 0.02 : 0.006;
                renderer.render(scene, camera);
            };
            animate();
        }
    };

    /* ==========================================================================
       4. 3D PERSPECTIVE OPPORTUNITY CAROUSEL
       ========================================================================== */
    const Opportunity3DCarousel = {
        stage: null,
        cards: [],
        prevBtn: null,
        nextBtn: null,
        currentIndex: 0,
        startX: 0,
        isSwiping: false,

        init() {
            this.stage = document.getElementById('carousel3dStage');
            if (!this.stage) return;

            this.cards = Array.from(this.stage.querySelectorAll('.carousel-3d-card'));
            this.prevBtn = document.getElementById('carouselPrevBtn');
            this.nextBtn = document.getElementById('carouselNextBtn');

            if (!this.cards.length) return;

            this.updateCarousel();

            if (this.prevBtn) {
                this.prevBtn.addEventListener('click', () => this.prev());
            }
            if (this.nextBtn) {
                this.nextBtn.addEventListener('click', () => this.next());
            }

            // Drag / Touch Navigation
            this.stage.addEventListener('pointerdown', (e) => {
                this.isSwiping = true;
                this.startX = e.clientX;
            });

            window.addEventListener('pointerup', (e) => {
                if (!this.isSwiping) return;
                this.isSwiping = false;
                const diff = e.clientX - this.startX;
                if (diff > 45) this.prev();
                else if (diff < -45) this.next();
            });

            // Wheel navigation
            this.stage.addEventListener('wheel', (e) => {
                if (Math.abs(e.deltaX) > 30) {
                    if (e.deltaX > 0) this.next();
                    else this.prev();
                }
            }, { passive: true });
        },

        prev() {
            this.currentIndex = (this.currentIndex - 1 + this.cards.length) % this.cards.length;
            this.updateCarousel();
        },

        next() {
            this.currentIndex = (this.currentIndex + 1) % this.cards.length;
            this.updateCarousel();
        },

        updateCarousel() {
            const total = this.cards.length;

            this.cards.forEach((card, idx) => {
                // Calculate relative offset from currentIndex
                let offset = idx - this.currentIndex;
                if (offset > total / 2) offset -= total;
                if (offset < -total / 2) offset += total;

                card.classList.remove('active', 'prev', 'next', 'hidden-card');

                if (offset === 0) {
                    // Center Card: scale 1, Z 0
                    card.classList.add('active');
                    card.style.transform = 'translate3d(0, 0, 0) scale(1) rotateY(0deg)';
                    card.style.opacity = '1';
                    card.style.zIndex = '30';
                    card.style.filter = 'none';
                    card.style.pointerEvents = 'auto';
                } else if (offset === -1 || (offset > 0 && offset === total - 1)) {
                    // Left Card: scale 0.85, -Z
                    card.classList.add('prev');
                    card.style.transform = 'translate3d(-55%, 0, -120px) scale(0.85) rotateY(18deg)';
                    card.style.opacity = '0.75';
                    card.style.zIndex = '20';
                    card.style.filter = 'blur(1px)';
                    card.style.pointerEvents = 'auto';
                } else if (offset === 1 || (offset < 0 && offset === -(total - 1))) {
                    // Right Card: scale 0.85, -Z
                    card.classList.add('next');
                    card.style.transform = 'translate3d(55%, 0, -120px) scale(0.85) rotateY(-18deg)';
                    card.style.opacity = '0.75';
                    card.style.zIndex = '20';
                    card.style.filter = 'blur(1px)';
                    card.style.pointerEvents = 'auto';
                } else {
                    // Deep Background Cards
                    card.classList.add('hidden-card');
                    const dir = offset > 0 ? 1 : -1;
                    card.style.transform = `translate3d(${dir * 110}%, 0, -260px) scale(0.65)`;
                    card.style.opacity = '0';
                    card.style.zIndex = '10';
                    card.style.pointerEvents = 'none';
                }
            });
        }
    };

    /* ==========================================================================
       5. 3D "HOW IT WORKS" PROGRESS TIMELINE
       ========================================================================== */
    const Timeline3DProgress = {
        container: null,
        beamFill: null,
        nodes: [],

        init() {
            this.container = document.getElementById('timeline3dProcess');
            if (!this.container) return;

            this.beamFill = this.container.querySelector('.timeline-beam-fill');
            this.nodes = Array.from(this.container.querySelectorAll('.timeline-3d-node'));

            if (!this.nodes.length) return;

            this.initScrollObserver();
        },

        initScrollObserver() {
            const onScroll = () => {
                const rect = this.container.getBoundingClientRect();
                const windowHeight = window.innerHeight;

                if (rect.top < windowHeight * 0.8 && rect.bottom > 0) {
                    const progress = Math.min(Math.max((windowHeight * 0.8 - rect.top) / rect.height, 0), 1);

                    if (this.beamFill) {
                        this.beamFill.style.width = `${progress * 100}%`;
                    }

                    // Activate nodes sequentially
                    const activeStepCount = Math.floor(progress * this.nodes.length) + 1;
                    this.nodes.forEach((node, idx) => {
                        if (idx < activeStepCount) {
                            node.classList.add('active');
                        } else {
                            node.classList.remove('active');
                        }
                    });
                }
            };

            window.addEventListener('scroll', onScroll, { passive: true });
            onScroll();
        }
    };

    /* ==========================================================================
       6. AMBIENT 3D HEADER CANVASES (Internal Pages)
       ========================================================================== */
    const Header3DCanvases = {
        init() {
            if (!window.THREE || prefersReducedMotion) return;

            const headerCanvases = document.querySelectorAll('.header-3d-canvas');
            if (!headerCanvases.length) return;

            headerCanvases.forEach(canvas => {
                this.createHeaderScene(canvas);
            });
        },

        createHeaderScene(canvas) {
            let renderer;
            try {
                renderer = new THREE.WebGLRenderer({
                    canvas: canvas,
                    alpha: true,
                    antialias: true,
                    powerPreference: "low-power"
                });
            } catch (e) {
                return;
            }

            const width = canvas.clientWidth || 240;
            const height = canvas.clientHeight || 180;

            renderer.setSize(width, height);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
            camera.position.z = 45;

            const ambient = new THREE.AmbientLight(0xffffff, 0.85);
            scene.add(ambient);

            const point = new THREE.PointLight(0x00f2fe, 1.8, 100);
            point.position.set(10, 20, 20);
            scene.add(point);

            // Floating Geometric Crest
            const crestGeo = new THREE.IcosahedronGeometry(12, 1);
            const crestMat = new THREE.MeshStandardMaterial({
                color: 0x06b6d4,
                wireframe: true,
                transparent: true,
                opacity: 0.55
            });
            const crest = new THREE.Mesh(crestGeo, crestMat);
            scene.add(crest);

            const innerGeo = new THREE.SphereGeometry(6, 16, 16);
            const innerMat = new THREE.MeshBasicMaterial({ color: 0x00f2fe });
            const inner = new THREE.Mesh(innerGeo, innerMat);
            scene.add(inner);

            const animate = () => {
                requestAnimationFrame(animate);
                crest.rotation.y += 0.008;
                crest.rotation.x += 0.005;
                renderer.render(scene, camera);
            };
            animate();
        }
    };

    /* ==========================================================================
       7. GLOBAL INITIALIZATION
       ========================================================================== */
    const initAll3D = () => {
        GlobalParticleField.init();
        HeroOpportunityNetwork.init();
        Category3DViewer.init();
        Opportunity3DCarousel.init();
        Timeline3DProgress.init();
        Header3DCanvases.init();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAll3D);
    } else {
        initAll3D();
    }

    // Expose to window for manual re-triggering if needed
    window.ROC3D = {
        GlobalParticleField,
        HeroOpportunityNetwork,
        Category3DViewer,
        Opportunity3DCarousel,
        Timeline3DProgress,
        Header3DCanvases
    };

})();
