/**
 * Rural Opportunity Connect - Global Production JavaScript
 * Handles:
 * 1. Global Multi-language Translation (Google Translate API + Cookie/LocalStorage persistence)
 * 2. 1-Click Quick Apply with duplicate handling and instant UI status update
 * 3. Save / Wishlist Bookmarks
 * 4. Responsive Mobile Slideout Menu
 * 5. Toast Notifications & Alerts
 * 6. Regional Voice Search Assistant
 */

// 1. CSRF Token Helper
function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === ('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    if (cookieValue) return cookieValue;

    const input = document.querySelector('input[name=csrfmiddlewaretoken]');
    if (input) return input.value;

    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');

    return '';
}

// 2. Toast Notification System
function showToast(message, type = 'success', duration = 4000, actionUrl = null, actionText = null) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'roc-toast';

    let iconHtml = '<i class="fas fa-circle-check text-cyan-500 text-lg"></i>';
    if (type === 'error') iconHtml = '<i class="fas fa-circle-exclamation text-red-600 text-lg"></i>';
    else if (type === 'info') iconHtml = '<i class="fas fa-circle-info text-blue-600 text-lg"></i>';
    else if (type === 'warning') iconHtml = '<i class="fas fa-triangle-exclamation text-amber-600 text-lg"></i>';

    let actionBtnHtml = '';
    if (actionUrl && actionText) {
        actionBtnHtml = `<a href="${actionUrl}" class="text-xs font-bold text-cyan-900 hover:underline bg-cyan-50 px-2.5 py-1 rounded-md border border-cyan-200 shrink-0">${actionText}</a>`;
    }

    toast.innerHTML = `
        ${iconHtml}
        <div class="text-xs sm:text-sm font-semibold text-slate-800 flex-1 leading-snug">${message}</div>
        ${actionBtnHtml}
        <button onclick="this.parentElement.remove()" class="text-slate-400 hover:text-slate-600 text-xs p-1" aria-label="Close notification">
            <i class="fas fa-xmark"></i>
        </button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('hiding');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// 3. 1-Click Quick Apply Function
async function quickApply(type, id, name, org, btn) {
    // If not authenticated, redirect to login with next parameter
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    if (!isAuthenticated) {
        const nextUrl = encodeURIComponent(window.location.pathname + window.location.search);
        window.location.href = `/login/?next=${nextUrl}`;
        return;
    }

    if (!btn) return;
    const originalHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Applying...';

    const token = getCsrfToken();
    const formData = new FormData();
    formData.append('opportunity_type', type);
    formData.append('opportunity_id', id);
    formData.append('opportunity_name', name || '');
    formData.append('organization', org || '');
    formData.append('is_ajax', '1');

    try {
        const response = await fetch('/applications/apply/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': token,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        });

        if (response.redirected && response.url.includes('/login/')) {
            const nextUrl = encodeURIComponent(window.location.pathname + window.location.search);
            window.location.href = `/login/?next=${nextUrl}`;
            return;
        }

        const data = await response.json();

        if (data.status === 'success') {
            // Transform button to Already Applied state
            btn.className = 'btn-applied text-xs py-2 px-4';
            btn.innerHTML = '<i class="fas fa-check-circle text-emerald-600"></i> Already Applied ✓';
            btn.disabled = true;

            showToast(
                `Application for "${name || 'opportunity'}" submitted successfully! 🎉`,
                'success',
                6000,
                '/applications/',
                'View Tracker →'
            );
        } else if (data.status === 'already_applied') {
            btn.className = 'btn-applied text-xs py-2 px-4';
            btn.innerHTML = '<i class="fas fa-check-circle text-emerald-600"></i> Already Applied ✓';
            btn.disabled = true;

            showToast(
                `You have already applied for "${name || 'this opportunity'}".`,
                'info',
                5000,
                '/applications/',
                'Open Tracker →'
            );
        } else {
            btn.disabled = false;
            btn.innerHTML = originalHtml;
            showToast(data.message || 'Could not submit application. Please try again.', 'error');
        }
    } catch (err) {
        btn.disabled = false;
        btn.innerHTML = originalHtml;
        showToast('Application submission failed. Please check your network and try again.', 'error');
    }
}

// 4. Universal Save / Wishlist Toggle
async function toggleSaveOpportunity(type, id, btn) {
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    if (!isAuthenticated) {
        const nextUrl = encodeURIComponent(window.location.pathname + window.location.search);
        window.location.href = `/login/?next=${nextUrl}`;
        return;
    }

    const icon = btn.querySelector('i');
    const token = getCsrfToken();

    try {
        const formData = new FormData();
        formData.append('type', type);
        formData.append('id', id);

        const response = await fetch('/save-opportunity/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': token,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        });

        if (response.redirected && response.url.includes('/login/')) {
            window.location.href = `/login/?next=${encodeURIComponent(window.location.pathname)}`;
            return;
        }

        const data = await response.json();
        if (data.status === 'saved') {
            btn.classList.add('is-saved');
            if (icon) {
                icon.classList.remove('fa-regular', 'text-slate-400');
                icon.classList.add('fa-solid', 'text-red-500');
            }
            showToast('Saved to your Wishlist!', 'success', 3500, '/saved-opportunities/', 'View Saved →');
        } else if (data.status === 'removed') {
            btn.classList.remove('is-saved');
            if (icon) {
                icon.classList.remove('fa-solid', 'text-red-500');
                icon.classList.add('fa-regular', 'text-slate-400');
            }
            showToast('Removed from your Wishlist.', 'info', 3000);
        }
    } catch (err) {
        showToast('Please sign in to save opportunities.', 'info');
    }
}

// 5. Global Multi-Language Translation System
function googleTranslateElementInit() {
    if (window.google && window.google.translate) {
        new google.translate.TranslateElement({
            pageLanguage: 'en',
            includedLanguages: 'en,ta,hi,te,kn,ml',
            autoDisplay: false
        }, 'google_translate_element');
    }
}

function changeGlobalLanguage(langCode) {
    // 1. Set cookie for Google Translate (googtrans=/en/ta etc.)
    const cookieVal = `/en/${langCode}`;
    document.cookie = `googtrans=${cookieVal}; path=/;`;
    document.cookie = `googtrans=${cookieVal}; domain=${window.location.hostname}; path=/;`;
    localStorage.setItem('roc_lang', langCode);

    // 2. Update select dropdowns across navbar and mobile menu
    document.querySelectorAll('.roc-lang-selector').forEach(sel => {
        sel.value = langCode;
    });

    // 3. Trigger Google Translate internal select if loaded
    const googleSelect = document.querySelector('.goog-te-combo');
    if (googleSelect) {
        googleSelect.value = langCode;
        googleSelect.dispatchEvent(new Event('change'));
    } else {
        // If Google widget hasn't finished initial rendering yet, reload to let cookie take effect
        window.location.reload();
    }
}

// 6. Mobile Slideout Menu Toggle
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    if (menu && overlay) {
        const isClosed = menu.classList.contains('translate-x-full');
        if (isClosed) {
            menu.classList.remove('translate-x-full');
            overlay.classList.remove('hidden');
            document.body.classList.add('overflow-hidden');
        } else {
            menu.classList.add('translate-x-full');
            overlay.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        }
    }
}

// 7. Voice Search Assistant
let voiceRecognitionInstance;
function triggerVoiceAssistant() {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
        showToast("Voice search is supported on Chrome, Edge, and Android browsers.", "info");
        return;
    }

    const modal = document.getElementById('voiceModal');
    const statusText = document.getElementById('voiceStatusText');
    const transcriptText = document.getElementById('voiceTranscript');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }

    voiceRecognitionInstance = new SpeechRec();
    const currentLang = localStorage.getItem('roc_lang') || 'en';
    if (currentLang === 'ta') voiceRecognitionInstance.lang = 'ta-IN';
    else if (currentLang === 'hi') voiceRecognitionInstance.lang = 'hi-IN';
    else if (currentLang === 'te') voiceRecognitionInstance.lang = 'te-IN';
    else if (currentLang === 'kn') voiceRecognitionInstance.lang = 'kn-IN';
    else if (currentLang === 'ml') voiceRecognitionInstance.lang = 'ml-IN';
    else voiceRecognitionInstance.lang = 'en-IN';

    voiceRecognitionInstance.interimResults = false;
    voiceRecognitionInstance.maxAlternatives = 1;

    voiceRecognitionInstance.onstart = () => {
        if (statusText) statusText.textContent = "Listening... Speak your query";
    };

    voiceRecognitionInstance.onresult = (event) => {
        const speechResult = event.results[0][0].transcript;
        if (transcriptText) transcriptText.textContent = `"${speechResult}"`;
        if (statusText) statusText.textContent = "Searching...";

        setTimeout(() => {
            closeVoiceAssistant();
            const searchInput = document.querySelector('input[name="search"]') || document.querySelector('input[type="search"]');
            if (searchInput) {
                searchInput.value = speechResult;
                const searchForm = searchInput.closest('form');
                if (searchForm) searchForm.submit();
            } else {
                window.location.href = `/jobs/?search=${encodeURIComponent(speechResult)}`;
            }
        }, 700);
    };

    voiceRecognitionInstance.onerror = () => {
        if (statusText) statusText.textContent = "Could not catch audio clearly. Try again.";
    };

    voiceRecognitionInstance.start();
}

function closeVoiceAssistant() {
    if (voiceRecognitionInstance) {
        try { voiceRecognitionInstance.stop(); } catch(e) {}
    }
    const modal = document.getElementById('voiceModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// ==============================================================================
// 9. 3D SPATIAL ENGINE: Perspective Card Tilt & Specular Glare
// ==============================================================================
function init3DCardTilt() {
    const cards = document.querySelectorAll('.tilt-card-3d');
    if (!cards.length) return;

    cards.forEach(card => {
        // Ensure specular glare element exists
        let glare = card.querySelector('.tilt-glare');
        if (!glare) {
            glare = document.createElement('div');
            glare.className = 'tilt-glare';
            card.appendChild(glare);
        }

        let isHovered = false;
        let bounds = null;

        card.addEventListener('mouseenter', () => {
            isHovered = true;
            bounds = card.getBoundingClientRect();
        });

        card.addEventListener('mousemove', (e) => {
            if (!isHovered || !bounds) return;
            const mouseX = e.clientX - bounds.left;
            const mouseY = e.clientY - bounds.top;

            const percentX = (mouseX / bounds.width) - 0.5;
            const percentY = (mouseY / bounds.height) - 0.5;

            // Compute 3D rotation angles (-12 to 12 degrees)
            const rotateY = (percentX * 16).toFixed(2);
            const rotateX = (-percentY * 16).toFixed(2);

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;

            // Position specular glare radial reflection
            glare.style.background = `radial-gradient(circle at ${mouseX}px ${mouseY}px, rgba(255, 255, 255, 0.45) 0%, rgba(255, 255, 255, 0) 65%)`;
        });

        card.addEventListener('mouseleave', () => {
            isHovered = false;
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    });
}

// ==============================================================================
// 10. 3D WEBGL HERO CANVAS: Opportunity Network Globe (Three.js)
// ==============================================================================
function init3DHeroGlobe() {
    const container = document.getElementById('hero3dCanvasContainer');
    if (!container || !window.THREE) return;

    let renderer;
    try {
        renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: "high-performance" });
    } catch (e) {
        console.log("WebGL not active for 3D Hero:", e);
        return;
    }

    const width = container.clientWidth || 500;
    const height = container.clientHeight || 480;

    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.domElement.style.position = 'absolute';
    renderer.domElement.style.inset = '0';
    renderer.domElement.style.width = '100%';
    renderer.domElement.style.height = '100%';
    renderer.domElement.style.zIndex = '1';
    
    // Insert behind overlay badges
    container.insertBefore(renderer.domElement, container.firstChild);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.z = 240;

    // Opportunity Globe Master Group
    const globeGroup = new THREE.Group();
    scene.add(globeGroup);

    // 1. Core Cyan / Tech Blue Wireframe Sphere
    const sphereGeo = new THREE.IcosahedronGeometry(72, 2);
    const sphereMat = new THREE.MeshBasicMaterial({
        color: 0x06b6d4, // Vibrant Cyan
        wireframe: true,
        transparent: true,
        opacity: 0.32
    });
    const sphereMesh = new THREE.Mesh(sphereGeo, sphereMat);
    globeGroup.add(sphereMesh);

    // 2. High-Tech Particle Constellations (Cyan & Deep Tech Blue)
    const particleCount = 280;
    const particlePositions = new Float32Array(particleCount * 3);
    const particleColors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
        const phi = Math.acos(-1 + (2 * i) / particleCount);
        const theta = Math.sqrt(particleCount * Math.PI) * phi;
        const radius = 72 + (Math.random() * 4 - 2);

        particlePositions[i * 3] = radius * Math.cos(theta) * Math.sin(phi);
        particlePositions[i * 3 + 1] = radius * Math.sin(theta) * Math.sin(phi);
        particlePositions[i * 3 + 2] = radius * Math.cos(phi);

        if (i % 3 === 0) {
            particleColors[i * 3] = 0.0; particleColors[i * 3 + 1] = 0.95; particleColors[i * 3 + 2] = 1.0; // Neon Cyan
        } else if (i % 3 === 1) {
            particleColors[i * 3] = 0.01; particleColors[i * 3 + 1] = 0.52; particleColors[i * 3 + 2] = 0.78; // Tech Blue
        } else {
            particleColors[i * 3] = 0.22; particleColors[i * 3 + 1] = 0.74; particleColors[i * 3 + 2] = 0.97; // Sky Blue
        }
    }

    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    const particleMat = new THREE.PointsMaterial({
        size: 3.4,
        vertexColors: true,
        transparent: true,
        opacity: 0.90
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    globeGroup.add(particles);

    // 3. Five Luminous Orbiting Sector Nodes
    const sectors = [
        { color: 0x0284c7, radius: 102, speed: 0.015, yOff: 15 },  // Jobs (Tech Blue)
        { color: 0xa855f7, radius: 114, speed: 0.012, yOff: -20 }, // Scholarships (Purple)
        { color: 0x06b6d4, radius: 92, speed: 0.018, yOff: 28 },   // Schemes (Cyan)
        { color: 0x38bdf8, radius: 122, speed: 0.010, yOff: -10 }, // Skills (Sky Blue)
        { color: 0x00f2fe, radius: 108, speed: 0.014, yOff: 5 },   // Business (Bright Cyan)
    ];

    const nodeMeshes = [];
    sectors.forEach((sec, idx) => {
        // Orbit ring
        const ringGeo = new THREE.RingGeometry(sec.radius - 0.6, sec.radius + 0.6, 64);
        const ringMat = new THREE.MeshBasicMaterial({
            color: sec.color,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.25
        });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.rotation.x = Math.PI / 2 + (idx * 0.25 - 0.5);
        ring.rotation.y = (idx * 0.2);
        globeGroup.add(ring);

        // Node sphere
        const nodeGeo = new THREE.SphereGeometry(4.2, 16, 16);
        const nodeMat = new THREE.MeshBasicMaterial({ color: sec.color });
        const nodeMesh = new THREE.Mesh(nodeGeo, nodeMat);
        globeGroup.add(nodeMesh);

        nodeMeshes.push({
            mesh: nodeMesh,
            radius: sec.radius,
            speed: sec.speed,
            yOff: sec.yOff,
            angle: (idx * (Math.PI * 2 / sectors.length))
        });
    });

    // 4. Mouse Interactive Parallax & Touch Dragging
    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;
    let isDragging = false;
    let prevPointerX = 0, prevPointerY = 0;

    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        mouseX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
        mouseY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
        targetX = mouseX * 0.35;
        targetY = mouseY * 0.35;
    });

    container.addEventListener('pointerdown', (e) => {
        isDragging = true;
        prevPointerX = e.clientX;
        prevPointerY = e.clientY;
    });

    window.addEventListener('pointermove', (e) => {
        if (!isDragging) return;
        const deltaX = e.clientX - prevPointerX;
        const deltaY = e.clientY - prevPointerY;
        globeGroup.rotation.y += deltaX * 0.008;
        globeGroup.rotation.x += deltaY * 0.008;
        prevPointerX = e.clientX;
        prevPointerY = e.clientY;
    });

    window.addEventListener('pointerup', () => { isDragging = false; });

    // 5. Animation Loop
    let clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);

        const time = clock.getElapsedTime();

        if (!isDragging) {
            globeGroup.rotation.y += 0.005;
            globeGroup.rotation.x += (targetY - globeGroup.rotation.x) * 0.05;
        }

        // Animate orbiting sector nodes
        nodeMeshes.forEach(node => {
            node.angle += node.speed;
            node.mesh.position.x = Math.cos(node.angle) * node.radius;
            node.mesh.position.z = Math.sin(node.angle) * node.radius;
            node.mesh.position.y = Math.sin(time * 2 + node.angle) * 8 + node.yOff;
        });

        // Pulse particles
        const scale = 1 + Math.sin(time * 1.5) * 0.02;
        particles.scale.set(scale, scale, scale);

        renderer.render(scene, camera);
    }
    animate();

    // 6. Responsive Resize
    window.addEventListener('resize', () => {
        const newW = container.clientWidth;
        const newH = container.clientHeight || 480;
        camera.aspect = newW / newH;
        camera.updateProjectionMatrix();
        renderer.setSize(newW, newH);
    });
}

// 11. Auto Initialize on Page Ready
document.addEventListener('DOMContentLoaded', () => {
    // 1. Language selector state sync
    const savedLang = localStorage.getItem('roc_lang') || 'en';
    document.querySelectorAll('.roc-lang-selector').forEach(sel => {
        sel.value = savedLang;
    });

    // 2. Active nav link highlighting
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });

    // 3. Attach save wishlist listeners
    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const type = this.dataset.type;
            const id = this.dataset.id;
            if (type && id) {
                toggleSaveOpportunity(type, id, this);
            }
        });
    });

    // 4. Initialize 3D Card Tilt Engine
    init3DCardTilt();

    // 5. Initialize 3D WebGL Hero Globe if container is present
    init3DHeroGlobe();
});
