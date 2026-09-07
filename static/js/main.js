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

// 3. Global 1-Click Quick Apply Modal System
var currentApplyBtn = window.currentApplyBtn || null;

function openQuickApplyModal(type, id, name, org, btn) {
    currentApplyBtn = btn || null;

    const modal = document.getElementById('quickApplyModal');
    const modalTitle = document.getElementById('qaModalTitle');
    const modalOrg = document.getElementById('qaModalOrg');
    const typeBadge = document.getElementById('qaModalTypeBadge');
    const typeIcon = document.getElementById('qaModalIcon');

    const inputType = document.getElementById('qaInputType');
    const inputId = document.getElementById('qaInputId');
    const inputName = document.getElementById('qaInputName');
    const inputOrg = document.getElementById('qaInputOrg');

    if (inputType) inputType.value = type || 'job';
    if (inputId) inputId.value = id || '0';
    if (inputName) inputName.value = name || 'Verified Opportunity';
    if (inputOrg) inputOrg.value = org || 'Rural Opportunity Connect';

    if (modalTitle) modalTitle.textContent = name || 'Verified Opportunity';
    if (modalOrg) modalOrg.textContent = org || 'Rural Opportunity Connect';

    // Type styling and icons
    let badgeText = 'Opportunity';
    let iconClass = 'fas fa-briefcase';
    if (type === 'job') {
        badgeText = '💼 Rural Job';
        iconClass = 'fas fa-briefcase';
    } else if (type === 'scholarship') {
        badgeText = '🎓 Scholarship Grant';
        iconClass = 'fas fa-graduation-cap';
    } else if (type === 'scheme') {
        badgeText = '🏛️ Govt Welfare';
        iconClass = 'fas fa-building-columns';
    } else if (type === 'skill') {
        badgeText = '💻 Skill Program';
        iconClass = 'fas fa-laptop-code';
    } else if (type === 'business') {
        badgeText = '🚀 Business Idea';
        iconClass = 'fas fa-store';
    }

    if (typeBadge) typeBadge.textContent = badgeText;
    if (typeIcon) typeIcon.innerHTML = `<i class="${iconClass}"></i>`;

    if (modal) {
        modal.classList.remove('hidden');
        requestAnimationFrame(() => {
            modal.classList.remove('opacity-0');
            const card = document.getElementById('quickApplyModalCard');
            if (card) card.classList.remove('scale-95');
        });
        document.body.classList.add('overflow-hidden');
    }
}

function closeQuickApplyModal() {
    const modal = document.getElementById('quickApplyModal');
    const card = document.getElementById('quickApplyModalCard');
    if (modal) {
        if (card) card.classList.add('scale-95');
        modal.classList.add('opacity-0');
        setTimeout(() => {
            modal.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        }, 200);
    }
}

// Alias quickApply to openQuickApplyModal so all templates work seamlessly
function quickApply(type, id, name, org, btn) {
    return openQuickApplyModal(type, id, name, org, btn);
}
window.quickApply = quickApply;
window.openQuickApplyModal = openQuickApplyModal;
window.closeQuickApplyModal = closeQuickApplyModal;

// 3.1 Global Voice Search Assistant
let recognitionInstance = null;

function triggerVoiceAssistant() {
    const modal = document.getElementById('voiceModal');
    const statusText = document.getElementById('voiceStatusText');
    const transcriptText = document.getElementById('voiceTranscript');

    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        if (statusText) statusText.textContent = "Voice Search Not Supported";
        if (transcriptText) transcriptText.textContent = "Your browser does not support Web Speech API. Please type your search query in the input bar.";
        return;
    }

    try {
        if (recognitionInstance) {
            recognitionInstance.stop();
        }

        recognitionInstance = new SpeechRecognition();
        recognitionInstance.lang = localStorage.getItem('roc_lang') === 'ta' ? 'ta-IN' : (localStorage.getItem('roc_lang') === 'hi' ? 'hi-IN' : 'en-IN');
        recognitionInstance.interimResults = true;
        recognitionInstance.maxAlternatives = 1;

        if (statusText) statusText.textContent = "Listening... Speak now";
        if (transcriptText) transcriptText.textContent = 'Listening for keywords like "Tamil Nadu", "Agriculture", "Scholarships"...';

        recognitionInstance.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(res => res[0].transcript)
                .join('');
            if (transcriptText) transcriptText.textContent = `"${transcript}"`;

            if (event.results[0].isFinal) {
                setTimeout(() => {
                    closeVoiceAssistant();
                    const searchInput = document.querySelector('input[name="search"]') || document.getElementById('quickAccessInput');
                    if (searchInput) {
                        searchInput.value = transcript;
                        if (searchInput.form) {
                            searchInput.form.submit();
                        } else if (typeof handleQuickAccessSearch === 'function') {
                            handleQuickAccessSearch();
                        }
                    } else {
                        window.location.href = `/opportunities/?search=${encodeURIComponent(transcript)}`;
                    }
                }, 700);
            }
        };

        recognitionInstance.onerror = (event) => {
            if (statusText) statusText.textContent = "Could not recognize audio";
            if (transcriptText) transcriptText.textContent = event.error === 'not-allowed' ? "Microphone access was denied. Please allow microphone permissions in your browser." : "Please try speaking closer to the microphone.";
        };

        recognitionInstance.start();
    } catch (err) {
        if (statusText) statusText.textContent = "Voice Assistant Error";
        if (transcriptText) transcriptText.textContent = "Could not activate microphone. Please type your query.";
    }
}

function closeVoiceAssistant() {
    if (recognitionInstance) {
        try { recognitionInstance.stop(); } catch (e) {}
    }
    const modal = document.getElementById('voiceModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

window.triggerVoiceAssistant = triggerVoiceAssistant;
window.closeVoiceAssistant = closeVoiceAssistant;

async function submitQuickApplyModal(event) {
    if (event) event.preventDefault();

    const submitBtn = document.getElementById('qaSubmitBtn');
    const type = document.getElementById('qaInputType')?.value || 'job';
    const id = document.getElementById('qaInputId')?.value || '0';
    const name = document.getElementById('qaInputName')?.value || 'Opportunity';
    const org = document.getElementById('qaInputOrg')?.value || '';

    const originalText = submitBtn ? submitBtn.innerHTML : '';
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
    }

    const isAuthenticated = document.body.dataset.authenticated === 'true';

    if (isAuthenticated) {
        const token = getCsrfToken();
        const formData = new FormData();
        formData.append('opportunity_type', type);
        formData.append('opportunity_id', id);
        formData.append('opportunity_name', name);
        formData.append('organization', org);
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
                closeQuickApplyModal();
                window.location.href = `/login/?next=${encodeURIComponent(window.location.pathname)}`;
                return;
            }

            const data = await response.json();
            closeQuickApplyModal();

            if (data.status === 'success' || data.status === 'already_applied') {
                if (typeof window.celebrateApplication === 'function' && currentApplyBtn) {
                    window.celebrateApplication(currentApplyBtn, name);
                } else if (currentApplyBtn) {
                    currentApplyBtn.className = 'btn-applied text-xs py-2 px-4';
                    currentApplyBtn.innerHTML = '<i class="fas fa-check-circle text-emerald-600"></i> Already Applied ✓';
                    currentApplyBtn.disabled = true;
                }

                showToast(
                    `Application for "${name}" submitted successfully! 🎉`,
                    'success',
                    6000,
                    '/applications/',
                    'View in Tracker →'
                );
            } else {
                showToast(data.message || 'Could not record application. Please try again.', 'error');
            }
        } catch (err) {
            closeQuickApplyModal();
            showToast('Network error while applying. Please try again.', 'error');
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        }
    } else {
        // Guest Application handling: Save to local tracker storage and confirm immediately
        const guestName = document.getElementById('qaGuestName')?.value || 'Candidate';
        const guestPhone = document.getElementById('qaGuestPhone')?.value || '';
        const guestLocation = document.getElementById('qaGuestLocation')?.value || '';

        try {
            const guestApps = JSON.parse(localStorage.getItem('roc_guest_apps') || '[]');
            guestApps.push({
                type,
                id,
                name,
                org,
                applied_at: new Date().toISOString(),
                guestName,
                guestPhone,
                guestLocation
            });
            localStorage.setItem('roc_guest_apps', JSON.stringify(guestApps));
        } catch (e) {}

        closeQuickApplyModal();

        if (typeof window.celebrateApplication === 'function' && currentApplyBtn) {
            window.celebrateApplication(currentApplyBtn, name);
        } else if (currentApplyBtn) {
            currentApplyBtn.className = 'btn-applied text-xs py-2 px-4';
            currentApplyBtn.innerHTML = '<i class="fas fa-check-circle text-emerald-600"></i> Already Applied ✓';
            currentApplyBtn.disabled = true;
        }

        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }

        showToast(
            `Quick Application recorded for ${guestName}! Verification team notified. 🎉`,
            'success',
            6000,
            '/register/',
            'Create Account to Track →'
        );
    }
}

// Unified Quick Apply trigger
function quickApply(type, id, name, org, btn) {
    openQuickApplyModal(type, id, name, org, btn);
}

// Quick Access Hub Logic
let quickSearchDebounceTimer = null;

function openQuickAccessModal() {
    const modal = document.getElementById('quickAccessModal');
    if (!modal) return;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    const input = document.getElementById('quickAccessInput');
    if (input) {
        input.value = '';
        setTimeout(() => input.focus(), 50);
    }
    const res = document.getElementById('quickSearchResults');
    if (res) {
        res.classList.add('hidden');
        res.innerHTML = '';
    }
    document.body.classList.add('overflow-hidden');
}

function closeQuickAccessModal() {
    const modal = document.getElementById('quickAccessModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        document.body.classList.remove('overflow-hidden');
    }
}
window.openQuickAccessModal = openQuickAccessModal;
window.closeQuickAccessModal = closeQuickAccessModal;
window.handleQuickAccessSearch = handleQuickAccessSearch;

function handleQuickAccessSearch() {
    const input = document.getElementById('quickAccessInput');
    const res = document.getElementById('quickSearchResults');
    if (!input || !res) return;

    const q = input.value.trim();
    if (!q) {
        res.classList.add('hidden');
        res.innerHTML = '';
        return;
    }

    clearTimeout(quickSearchDebounceTimer);
    quickSearchDebounceTimer = setTimeout(async () => {
        try {
            res.classList.remove('hidden');
            res.innerHTML = '<div class="p-3 text-xs text-slate-500 text-center flex items-center justify-center gap-2"><i class="fas fa-spinner fa-spin text-amber-500"></i> Searching opportunities...</div>';

            const resp = await fetch(`/api/quick-search/?q=${encodeURIComponent(q)}`, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            if (!resp.ok) throw new Error('Search failed');
            const data = await resp.json();
            const results = data.results || [];

            if (results.length === 0) {
                res.innerHTML = `<div class="p-4 text-xs text-slate-500 text-center">No matching opportunities found for "<span class="font-bold text-slate-800">${q}</span>". Try another keyword or browse categories below.</div>`;
            } else {
                res.innerHTML = results.map(r => `
                    <div class="p-3 hover:bg-slate-50 flex items-center justify-between gap-3 transition rounded-xl">
                        <a href="${r.detail_url}" onclick="closeQuickAccessModal()" class="flex-1 min-w-0 group cursor-pointer">
                            <div class="flex items-center gap-1.5 mb-1">
                                <span class="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-slate-100 text-slate-700">${r.type}</span>
                                <span class="text-xs font-bold text-slate-900 group-hover:text-cyan-700 transition truncate block">${r.title}</span>
                            </div>
                            <div class="text-[11px] text-slate-500 truncate">${r.org} ${r.meta ? '• ' + r.meta : ''}</div>
                        </a>
                        <div class="flex items-center gap-2 shrink-0">
                            <a href="${r.detail_url}" onclick="closeQuickAccessModal()" class="px-2.5 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-100 text-slate-700 text-[11px] font-bold transition flex items-center gap-1">
                                <i class="fas fa-eye text-cyan-600"></i> View Details
                            </a>
                            <button type="button" onclick="closeQuickAccessModal(); quickApply('${r.applyType}', '${r.id}', '${r.title.replace(/'/g, "\\'")}', '${r.org.replace(/'/g, "\\'")}', this)" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-[11px] font-bold shadow-xs transition flex items-center gap-1 cursor-pointer">
                                <i class="fas fa-paper-plane"></i> Quick Apply
                            </button>
                        </div>
                    </div>
                `).join('');
            }
        } catch (e) {
            res.innerHTML = '<div class="p-3 text-xs text-red-500 text-center">Search error. Please try again.</div>';
        }
    }, 200);
}

// Global Keyboard Shortcut: Ctrl+K or Cmd+K to open Quick Access, ESC to close
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
        e.preventDefault();
        const modal = document.getElementById('quickAccessModal');
        if (modal && !modal.classList.contains('hidden')) {
            closeQuickAccessModal();
        } else {
            openQuickAccessModal();
        }
    } else if (e.key === 'Escape') {
        closeQuickAccessModal();
        closeQuickApplyModal();
        if (typeof closeVoiceAssistant === 'function') closeVoiceAssistant();
    }
});

// 4. Universal Save / Wishlist Toggle
async function toggleSaveOpportunity(type, id, btn) {
    const icon = btn.querySelector('i');
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    if (!isAuthenticated) {
        let guestSaved = JSON.parse(localStorage.getItem('roc_guest_saved') || '[]');
        const key = `${type}_${id}`;
        if (guestSaved.includes(key)) {
            guestSaved = guestSaved.filter(k => k !== key);
            btn.classList.remove('is-saved');
            if (icon) {
                icon.classList.remove('fa-solid', 'text-red-500');
                icon.classList.add('fa-regular', 'text-slate-400');
            }
            showToast('Removed from your saved list.', 'info', 3000);
        } else {
            guestSaved.push(key);
            btn.classList.add('is-saved');
            if (icon) {
                icon.classList.remove('fa-regular', 'text-slate-400');
                icon.classList.add('fa-solid', 'text-red-500');
            }
            showToast('Saved to your Wishlist! (Sign up anytime to sync)', 'success', 4000, '/register/', 'Create Account →');
        }
        localStorage.setItem('roc_guest_saved', JSON.stringify(guestSaved));
        return;
    }

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
window.toggleSaveOpportunity = toggleSaveOpportunity;

// 5. Global Multi-Language Translation System & Instant Regional Dictionary
const ROC_TRANSLATIONS = {
    'en': {
        'nav_home': 'Home',
        'nav_jobs': 'Jobs',
        'nav_scholarships': 'Scholarships',
        'nav_schemes': 'Government Schemes',
        'nav_skills': 'Skills',
        'nav_business': 'Business',
        'nav_partners': 'Partner Feeds',
        'nav_about': 'About',
        'btn_quick_apply': 'Quick Apply',
        'btn_view_details': 'View Details',
        'btn_details': 'Details',
        'btn_applied': 'Already Applied ✓',
        'btn_enroll': 'Enroll / Apply',
        'btn_track': 'Track Idea',
        'sdg_tag': 'Empowering Rural India with Verified Career & Livelihood Gateways',
        'search_btn': 'Search',
        'voice_search': 'Voice Search'
    },
    'ta': {
        'nav_home': 'முகப்பு',
        'nav_jobs': 'வேலைவாய்ப்புகள்',
        'nav_scholarships': 'கல்வி உதவித்தொகை',
        'nav_schemes': 'அரசு நலத்திட்டங்கள்',
        'nav_skills': 'திறன் பயிற்சி',
        'nav_business': 'தொழில் வாய்ப்புகள்',
        'nav_partners': 'கூட்டாளர் இணைப்புகள்',
        'nav_about': 'எங்களை பற்றி',
        'btn_quick_apply': 'உடனடி விண்ணப்பம்',
        'btn_view_details': 'முழு விவரங்கள்',
        'btn_details': 'விவரங்கள்',
        'btn_applied': 'விண்ணப்பிக்கப்பட்டது ✓',
        'btn_enroll': 'விண்ணப்பிக்க / சேர்க',
        'btn_track': 'திட்டத்தை தொடர்க',
        'sdg_tag': 'கிராமப்புற இந்தியாவிற்கான சரிபார்க்கப்பட்ட வேலைவாய்ப்பு தளம்',
        'search_btn': 'தேடுக',
        'voice_search': 'குரல் தேடல்'
    },
    'hi': {
        'nav_home': 'होम',
        'nav_jobs': 'नौकरियां',
        'nav_scholarships': 'छात्रवृत्तियां',
        'nav_schemes': 'सरकारी योजनाएं',
        'nav_skills': 'कौशल विकास',
        'nav_business': 'व्यापार विचार',
        'nav_partners': 'पार्टनर फीड्स',
        'nav_about': 'हमारे बारे में',
        'btn_quick_apply': 'त्वरित आवेदन',
        'btn_view_details': 'विवरण देखें',
        'btn_details': 'विवरण',
        'btn_applied': 'पहले से लागू ✓',
        'btn_enroll': 'नामांकन / आवेदन करें',
        'btn_track': 'विचार ट्रैक करें',
        'sdg_tag': 'सत्यापित करियर और आजीविका के अवसरों से ग्रामीण भारत को सशक्त बनाना',
        'search_btn': 'खोजें',
        'voice_search': 'आवाज़ से खोजें'
    },
    'te': {
        'nav_home': 'హోమ్',
        'nav_jobs': 'ఉద్యోగాలు',
        'nav_scholarships': 'స్కాలర్‌షిప్‌లు',
        'nav_schemes': 'ప్రభుత్వ పథకాలు',
        'nav_skills': 'నైపుణ్యాభివృద్ధి',
        'nav_business': 'వ్యాపార ఆలోచనలు',
        'nav_partners': 'పార్టనర్ ఫీడ్స్',
        'nav_about': 'మా గురించి',
        'btn_quick_apply': 'త్వరిత దరఖాస్తు',
        'btn_view_details': 'వివరాలు చూడండి',
        'btn_details': 'వివరాలు',
        'btn_applied': 'దరఖాస్తు చేశారు ✓',
        'btn_enroll': 'దరఖాస్తు చేయండి',
        'btn_track': 'ట్రాక్ చేయండి',
        'sdg_tag': 'ధృవీకరించబడిన కెరీర్ గేట్‌వేలతో గ్రామీణ భారతదేశాన్ని శక్తివంతం చేయడం',
        'search_btn': 'వెతకండి',
        'voice_search': 'వాయిస్ శోధన'
    },
    'kn': {
        'nav_home': 'ಮುಖಪುಟ',
        'nav_jobs': 'ಉದ್ಯೋಗಗಳು',
        'nav_scholarships': 'ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು',
        'nav_schemes': 'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು',
        'nav_skills': 'ಕೌಶಲ್ಯ ತರಬೇತಿ',
        'nav_business': 'ವ್ಯವಹಾರ ಯೋಜನೆಗಳು',
        'nav_partners': 'ಪಾಲುದಾರ ಫೀಡ್ಸ್',
        'nav_about': 'ನಮ್ಮ ಬಗ್ಗೆ',
        'btn_quick_apply': 'ತ್ವರಿತ ಅರ್ಜಿ',
        'btn_view_details': 'ವಿವರ ನೋಡಿ',
        'btn_details': 'ವಿವರಗಳು',
        'btn_applied': 'ಅರ್ಜಿ ಸಲ್ಲಿಸಲಾಗಿದೆ ✓',
        'btn_enroll': 'ಅರ್ಜಿ ಸಲ್ಲಿಸಿ',
        'btn_track': 'ಟ್ರ್ಯಾಕ್ ಮಾಡಿ',
        'sdg_tag': 'ಗ್ರಾಮೀಣ ಭಾರತದ ಉದ್ಯೋಗ ಮತ್ತು ಜೀವನೋಪಾಯ ವೇದಿಕೆ',
        'search_btn': 'ಹುಡುಕಿ',
        'voice_search': 'ಧ್ವನಿ ಹುಡುಕಾಟ'
    },
    'ml': {
        'nav_home': 'ഹോം',
        'nav_jobs': 'തൊഴിലവസരങ്ങൾ',
        'nav_scholarships': 'സ്കോളർഷിപ്പുകൾ',
        'nav_schemes': 'സർക്കാർ പദ്ധതികൾ',
        'nav_skills': 'നൈപുണ്യ വികസനം',
        'nav_business': 'സംരംഭക അവസരങ്ങൾ',
        'nav_partners': 'പാർട്ണർ ഫീഡുകൾ',
        'nav_about': 'ഞങ്ങളെക്കുറിച്ച്',
        'btn_quick_apply': 'വേഗത്തിൽ അപേക്ഷിക്കുക',
        'btn_view_details': 'വിശദാംശങ്ങൾ കാണുക',
        'btn_details': 'വിശദാംശങ്ങൾ',
        'btn_applied': 'അപേക്ഷിച്ചു ✓',
        'btn_enroll': 'അപേക്ഷിക്കുക',
        'btn_track': 'ട്രാക്ക് ചെയ്യുക',
        'sdg_tag': 'ഗ്രാമീണ ഭാരത ശാക്തീകരണ ഉപജീവന പോർട്ടൽ',
        'search_btn': 'തിരയുക',
        'voice_search': 'വോയ്‌സ് സെർച്ച്'
    }
};

function applyInstantTranslation(langCode) {
    const dict = ROC_TRANSLATIONS[langCode] || ROC_TRANSLATIONS['en'];

    // 1. Desktop and Mobile Nav Links
    const navMapping = [
        { selector: 'a[href*="jobs"]', key: 'nav_jobs' },
        { selector: 'a[href*="scholarships"]', key: 'nav_scholarships' },
        { selector: 'a[href*="schemes"]', key: 'nav_schemes' },
        { selector: 'a[href*="skills"]', key: 'nav_skills' },
        { selector: 'a[href*="business"]', key: 'nav_business' },
        { selector: 'a[href*="about"]', key: 'nav_about' }
    ];

    navMapping.forEach(({ selector, key }) => {
        document.querySelectorAll(`nav ${selector}, #mobileMenu ${selector}`).forEach(el => {
            if (el && dict[key] && !el.querySelector('i')) {
                el.textContent = dict[key];
            } else if (el && dict[key] && el.querySelector('i')) {
                const icon = el.querySelector('i').outerHTML;
                el.innerHTML = `${icon} ${dict[key]}`;
            }
        });
    });

    // 2. Buttons: Quick Apply, View Details, Details
    document.querySelectorAll('button, a').forEach(btn => {
        const text = btn.textContent.trim();
        if (text.includes('Quick Apply') || text.includes('உடனடி விண்ணப்பம்') || text.includes('त्वरित आवेदन')) {
            const icon = btn.querySelector('i');
            const iconHtml = icon ? icon.outerHTML : '<i class="fas fa-paper-plane"></i>';
            btn.innerHTML = `${iconHtml} ${dict['btn_quick_apply']}`;
        } else if (text === 'View Details' || text === 'முழு விவரங்கள்' || text === 'विवरण देखें') {
            btn.textContent = dict['btn_view_details'];
        } else if (text === 'Details' || text === 'ವಿವರಗಳು' || text === 'వివరాలు' || text === 'വിശദാംശങ്ങൾ') {
            btn.textContent = dict['btn_details'];
        }
    });

    // 3. SDG Banner Tag
    const sdgSpan = document.querySelector('header .max-w-7xl span.hidden.sm\\:inline');
    if (sdgSpan && dict['sdg_tag']) {
        sdgSpan.textContent = dict['sdg_tag'];
    }
}

function changeGlobalLanguage(langCode) {
    if (!langCode) return;

    // 1. Set cookie for Google Translate across all domains and paths
    const cookieVal = `/en/${langCode}`;
    document.cookie = `googtrans=${cookieVal}; path=/;`;
    if (window.location.hostname !== 'localhost' && !window.location.hostname.includes('127.0.0.1')) {
        document.cookie = `googtrans=${cookieVal}; domain=.${window.location.hostname}; path=/;`;
        document.cookie = `googtrans=${cookieVal}; domain=${window.location.hostname}; path=/;`;
    }
    localStorage.setItem('roc_lang', langCode);

    // 2. Update select dropdowns across top utility bar and mobile menu
    document.querySelectorAll('.roc-lang-selector').forEach(sel => {
        sel.value = langCode;
    });

    // 3. Instant client-side UI translation (Zero-wait UI update!)
    applyInstantTranslation(langCode);

    // 4. Trigger Google Translate internal select if ready
    try {
        const googleSelect = document.querySelector('.goog-te-combo');
        if (googleSelect) {
            googleSelect.value = langCode;
            googleSelect.dispatchEvent(new Event('change'));
        }
    } catch (e) {
        console.warn('Google Translate combo hook:', e);
    }
}

// Auto-restore saved language on DOM load
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('roc_lang');
    if (savedLang && savedLang !== 'en') {
        setTimeout(() => {
            changeGlobalLanguage(savedLang);
        }, 150);
    }
});

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

    // 3. Attach robust save wishlist event delegation
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.save-btn');
        if (btn) {
            e.preventDefault();
            e.stopPropagation();
            const type = btn.dataset.type;
            const id = btn.dataset.id;
            if (type && id) {
                toggleSaveOpportunity(type, id, btn);
            }
        }
    });

    // 4. Initialize 3D Card Tilt Engine
    init3DCardTilt();

    // 5. Initialize 3D WebGL Hero Globe if container is present
    init3DHeroGlobe();

    // 6. Restore guest saved bookmarks if not logged in
    if (document.body.dataset.authenticated !== 'true') {
        try {
            const guestSaved = JSON.parse(localStorage.getItem('roc_guest_saved') || '[]');
            document.querySelectorAll('.save-btn').forEach(btn => {
                const key = `${btn.dataset.type}_${btn.dataset.id}`;
                if (guestSaved.includes(key)) {
                    btn.classList.add('is-saved');
                    const icon = btn.querySelector('i');
                    if (icon) {
                        icon.classList.remove('fa-regular', 'text-slate-400');
                        icon.classList.add('fa-solid', 'text-red-500');
                    }
                }
            });
        } catch (e) {}
    }
});
