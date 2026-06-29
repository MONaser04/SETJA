// Elements
const engineOffline = document.getElementById('engineOffline');
const engineGemini = document.getElementById('engineGemini');
const apiKeyContainer = document.getElementById('apiKeyContainer');
const apiURLInput = document.getElementById('apiURLInput');
const apiModelInput = document.getElementById('apiModelInput');
const apiKeyInput = document.getElementById('apiKeyInput');
const browseModelBtn = document.getElementById('browseModelBtn');
const startBtn = document.getElementById('startBtn');
const startBtnText = startBtn.querySelector('.btn-text');
const spinner = startBtn.querySelector('.spinner');
const toast = document.getElementById('toast');
const minBtn = document.getElementById('minBtn');
const closeBtn = document.getElementById('closeBtn');

let isRunning = false;
let toastTimeout;

// Titlebar Controls
minBtn.addEventListener('click', () => {
    if (window.pywebview) pywebview.api.minimize();
});

closeBtn.addEventListener('click', () => {
    if (window.pywebview) pywebview.api.close_app();
});

// Initialize when pywebview is ready
window.addEventListener('pywebviewready', function() {
    pywebview.api.get_settings().then(settings => {
        if (settings.engine === 'gemini') {
            engineGemini.checked = true;
            apiKeyContainer.classList.remove('hidden');
        } else {
            engineOffline.checked = true;
        }
        
        if (settings.api_key) {
            apiKeyInput.value = settings.api_key;
        }
        if (settings.api_url) {
            apiURLInput.value = settings.api_url;
        }
        if (settings.api_model) {
            apiModelInput.value = settings.api_model;
        }
    });
});

// Event Listeners
function updateEngine() {
    if (engineGemini.checked) {
        apiKeyContainer.classList.remove('hidden');
    } else {
        apiKeyContainer.classList.add('hidden');
    }
    saveSettings();
}

engineOffline.addEventListener('change', updateEngine);
engineGemini.addEventListener('change', updateEngine);

apiKeyInput.addEventListener('input', () => {
    // Debounce save
    clearTimeout(window.saveTimeout);
    window.saveTimeout = setTimeout(saveSettings, 500);
});

apiURLInput.addEventListener('input', () => {
    clearTimeout(window.saveTimeout);
    window.saveTimeout = setTimeout(saveSettings, 500);
});

apiModelInput.addEventListener('input', () => {
    clearTimeout(window.saveTimeout);
    window.saveTimeout = setTimeout(saveSettings, 500);
});

browseModelBtn.addEventListener('click', async () => {
    const result = await pywebview.api.install_model();
    if (result.success) {
        showToast(result.message);
    } else if (result.message) {
        showToast(result.message, true);
    }
});

startBtn.addEventListener('click', async () => {
    // Validate
    const engine = engineGemini.checked ? 'gemini' : 'offline';
    const apiKey = apiKeyInput.value.trim();
    if (engine === 'gemini' && !apiKey) {
        showToast("Please enter your Cloud API Key first!", true);
        return;
    }

    // Save settings before starting
    saveSettings();
    
    // Toggle UI State
    if (!isRunning) {
        startBtnText.textContent = 'STARTING...';
        spinner.classList.remove('hidden');
        startBtn.classList.add('running');
        
        const success = await pywebview.api.start_setja();
        
        spinner.classList.add('hidden');
        if (success) {
            isRunning = true;
            startBtnText.textContent = 'STOP SETJA';
            showToast('SETJA is running in the background!');
        } else {
            startBtn.classList.remove('running');
            startBtnText.textContent = 'START SETJA';
            showToast('Failed to start SETJA. Check console.', true);
        }
    } else {
        startBtnText.textContent = 'STOPPING...';
        spinner.classList.remove('hidden');
        
        await pywebview.api.stop_setja();
        
        isRunning = false;
        spinner.classList.add('hidden');
        startBtn.classList.remove('running');
        startBtnText.textContent = 'START SETJA';
        showToast('SETJA stopped successfully.');
    }
});

// Helpers
function saveSettings() {
    const settings = {
        engine: engineGemini.checked ? 'gemini' : 'offline',
        api_key: apiKeyInput.value.trim(),
        api_url: apiURLInput.value.trim(),
        api_model: apiModelInput.value.trim()
    };
    if (window.pywebview) {
        pywebview.api.save_settings(settings);
    }
}

function showToast(message, isError = false) {
    toast.textContent = message;
    if (isError) {
        toast.classList.add('error');
    } else {
        toast.classList.remove('error');
    }
    
    toast.classList.add('show');
    
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
