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

// 3. Global 1-Click Quick Apply Modal System (Delegated to Base Unified Engine)
var currentApplyBtn = window.currentApplyBtn || null;

function openQuickApplyModal(type, id, name, org, btn) {
    currentApplyBtn = btn || null;
    if (typeof window.__qaOpen === 'function' && window.__qaOpen !== openQuickApplyModal) {
        return window.__qaOpen(type, id, name, org, btn);
    }
}

function closeQuickApplyModal() {
    if (typeof window.__qaClose === 'function' && window.__qaClose !== closeQuickApplyModal) {
        return window.__qaClose();
    }
    const modal = document.getElementById('quickApplyModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        modal.style.display = 'none';
        modal.style.visibility = 'hidden';
        document.body.classList.remove('overflow-hidden');
    }
}

function quickApply(type, id, name, org, btn) {
    if (typeof window.__qaApply === 'function' && window.__qaApply !== quickApply) {
        return window.__qaApply(type, id, name, org, btn);
    }
    if (typeof window.__qaOpen === 'function') {
        return window.__qaOpen(type, id, name, org, btn);
    }
    if (typeof window.openQuickApplyModal === 'function' && window.openQuickApplyModal !== openQuickApplyModal) {
        return window.openQuickApplyModal(type, id, name, org, btn);
    }
}


function restoreAppliedButtons() {
    try {
        const applied = JSON.parse(localStorage.getItem('roc_applied_keys') || '[]');
        if (!applied.length) return;

        document.querySelectorAll('button[onclick*="quickApply"]').forEach(btn => {
            const onclick = btn.getAttribute('onclick') || '';
            for (const key of applied) {
                const [type, id] = key.split('_');
                if (id && onclick.includes(`'${id}'`)) {
                    btn.classList.remove('btn-primary', 'btn-magnetic', 'btn-sheen', 'hover-scale-102');
                    btn.classList.add('btn-applied');
                    btn.disabled = true;
                    btn.innerHTML = `
                        <span class="inline-flex items-center gap-1 text-emerald-700 font-bold pointer-events-none">
                            <svg class="w-4 h-4 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                            </svg>
                            Applied ✓
                        </span>
                    `;
                    break;
                }
            }
        });
    } catch (e) {}
}

window.quickApply = quickApply;
window.restoreAppliedButtons = restoreAppliedButtons;
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
    if (window.__qaSubmit) {
        return window.__qaSubmit(event);
    }
}
window.submitQuickApplyModal = submitQuickApplyModal;


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
    if (!btn && window.event && window.event.currentTarget) {
        btn = window.event.currentTarget;
    }
    if (!btn) {
        btn = document.querySelector(`.save-btn[data-id="${id}"][data-type="${type}"]`);
    }
    if (!btn) return;

    const icon = btn.querySelector('i');
    const wasSaved = btn.classList.contains('is-saved');

    // 1. Optimistic UI update
    if (wasSaved) {
        btn.classList.remove('is-saved');
        if (icon) {
            icon.classList.remove('fa-solid', 'text-red-500');
            icon.classList.add('fa-regular', 'text-slate-400');
        }
        showToast('Removed from your Wishlist.', 'info', 3000);
    } else {
        btn.classList.add('is-saved');
        if (icon) {
            icon.classList.remove('fa-regular', 'text-slate-400');
            icon.classList.add('fa-solid', 'text-red-500');
        }
        showToast('Saved to your Wishlist!', 'success', 4000, '/saved-opportunities/', 'View Saved →');
        if (window.GlowCursor && typeof window.GlowCursor.particleBurst === 'function') {
            const rect = btn.getBoundingClientRect();
            window.GlowCursor.particleBurst(rect.left + rect.width / 2, rect.top + rect.height / 2, { r: 239, g: 68, b: 68 }, 16);
        }
    }

    // Sync localStorage
    try {
        const key = `${type}_${id}`;
        let savedKeys = JSON.parse(localStorage.getItem('roc_saved_keys') || '[]');
        if (wasSaved) {
            savedKeys = savedKeys.filter(k => k !== key);
        } else {
            if (!savedKeys.includes(key)) savedKeys.push(key);
        }
        localStorage.setItem('roc_saved_keys', JSON.stringify(savedKeys));
    } catch (e) {}

    // Send backend sync
    try {
        const token = (typeof getCsrfToken === 'function') ? getCsrfToken() : '';
        const formData = new FormData();
        formData.append('type', type);
        formData.append('id', id);

        await fetch('/save-opportunity/', {
            method: 'POST',
            body: formData,
            headers: {
                ...(token ? { 'X-CSRFToken': token } : {}),
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        });
    } catch (err) {}
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
// 9. ZERO-ANIMATION STABILIZER: 3D Spatial Effects Disabled
// ==============================================================================
function init3DCardTilt() {
    // Disabled in zero-animation mode
}

function init3DHeroGlobe() {
    // Disabled in zero-animation mode
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

    // 4. Live Document Checklist Interactive Toggling & Real-time Progress Ring
    document.querySelectorAll('.checklist-interactive-item input[type="checkbox"]').forEach(chk => {
        chk.addEventListener('change', function() {
            const parent = this.closest('.checklist-interactive-item');
            if (parent) {
                if (this.checked) {
                    parent.classList.add('checked');
                } else {
                    parent.classList.remove('checked');
                }
            }
            const allBoxes = document.querySelectorAll('.checklist-interactive-item input[type="checkbox"]');
            if (allBoxes.length) {
                const checkedCount = Array.from(allBoxes).filter(c => c.checked).length;
                const pct = Math.round((checkedCount / allBoxes.length) * 100);
                document.querySelectorAll('.circle-progress-bar').forEach(bar => {
                    const radius = 26;
                    const circumference = 2 * Math.PI * radius;
                    const offset = circumference - (pct / 100) * circumference;
                    bar.style.strokeDashoffset = offset;
                });
                document.querySelectorAll('.counter-value').forEach(cv => {
                    if (cv.closest('.circle-progress-bar') || cv.closest('.bg-white\\/10') || cv.dataset.counter !== undefined) {
                        cv.textContent = pct;
                    }
                });
            }
        });
    });

    // 5. Initialize 3D Card Tilt Engine
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

// Explicit Global Window Exports for All Buttons & Handlers
window.showToast = typeof showToast === 'function' ? showToast : function() {};
window.openQuickApplyModal = typeof openQuickApplyModal === 'function' ? openQuickApplyModal : function() {};
window.closeQuickApplyModal = typeof closeQuickApplyModal === 'function' ? closeQuickApplyModal : function() {};
window.openQuickAccessModal = typeof openQuickAccessModal === 'function' ? openQuickAccessModal : function() {};
window.closeQuickAccessModal = typeof closeQuickAccessModal === 'function' ? closeQuickAccessModal : function() {};
window.toggleUserDropdown = typeof toggleUserDropdown === 'function' ? toggleUserDropdown : function() {};
window.toggleMobileMenu = typeof toggleMobileMenu === 'function' ? toggleMobileMenu : function() {};
window.closeVoiceAssistant = typeof closeVoiceAssistant === 'function' ? closeVoiceAssistant : function() {};
window.triggerVoiceAssistant = typeof triggerVoiceAssistant === 'function' ? triggerVoiceAssistant : function() {};
window.getCsrfToken = typeof getCsrfToken === 'function' ? getCsrfToken : function() { return ''; };
window.toggleSaveOpportunity = typeof toggleSaveOpportunity === 'function' ? toggleSaveOpportunity : function() {};
window.quickApply = typeof quickApply === 'function' ? quickApply : function() {};
window.restoreAppliedButtons = typeof restoreAppliedButtons === 'function' ? restoreAppliedButtons : function() {};

