document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("calc-form");
    const weightInput = document.getElementById("weight");
    const repsInput = document.getElementById("reps");
    const modeSelect = document.getElementById("mode");
    const btn = document.getElementById("calc-btn");
    const resultBox = document.getElementById("result-box");
    const maxResult = document.getElementById("max-result");
    const errorBox = document.getElementById("error-box");

    function showError(msg) {
        errorBox.textContent = msg;
        errorBox.classList.add("show");
        resultBox.classList.remove("show");
        setTimeout(() => {
            errorBox.classList.remove("show");
        }, 5000);
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const weight = parseFloat(weightInput.value);
        const reps = parseInt(repsInput.value);
        const mode = parseInt(modeSelect.value);

        if (isNaN(weight) || weight <= 0 || weight > 500) {
            const t = window.translations[currentLang];
            showError(t.errWeight);
            return;
        }
        if (isNaN(reps) || reps <= 0 || reps > 100) {
            const t = window.translations[currentLang];
            showError(t.errReps);
            return;
        }

        btn.classList.add("loading");
        const t = window.translations[currentLang];
        btn.querySelector("span").textContent = t.calculating;
        errorBox.classList.remove("show");

        try {
            const response = await fetch("/api/calculate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ weight, reps, mode })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Failed to calculate.");
            }

            const data = await response.json();
            
            // Animate number
            let start = 0;
            const end = data.maximum;
            const duration = 1000;
            const startTime = performance.now();

            resultBox.classList.add("show");

            function updateNumber(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing out cubic
                const easeOut = 1 - Math.pow(1 - progress, 3);
                
                const currentVal = Math.round(start + (end - start) * easeOut);
                maxResult.textContent = currentVal;

                if (progress < 1) {
                    requestAnimationFrame(updateNumber);
                } else {
                    maxResult.textContent = end;
                }
            }

            requestAnimationFrame(updateNumber);

        } catch (err) {
            showError(err.message);
        } finally {
            btn.classList.remove("loading");
            const t = window.translations[currentLang];
            btn.querySelector("span").textContent = t.calcBtn;
        }
    });

    // Auto calculate on input change if valid
    const autoCalc = () => {
        if (weightInput.value && repsInput.value) {
            form.dispatchEvent(new Event("submit", { cancelable: true }));
        }
    };

    modeSelect.addEventListener("change", autoCalc);

    const rates = [
        [1, 2, 3, 4, 6, 8, 10, 12, 18, 26, 30],
        [1, 2, 4, 6, 8, 10, 12, 18, 26, 30, 38],
        [1, 2, 4, 8, 10, 12, 18, 26, 30, 38, 50],
    ];

    function updateTableHighlight(mode, reps) {
        // Clear previous highlights
        document.querySelectorAll('.highlight-header').forEach(el => el.classList.remove('highlight-header'));
        document.querySelectorAll('.highlight-cell').forEach(el => el.classList.remove('highlight-cell'));

        // Highlight header
        const modeHeader = document.getElementById(`th-mode-${mode}`);
        if (modeHeader) modeHeader.classList.add('highlight-header');

        // Find correct row index
        let found_i = rates[mode].length;
        for (let i = 0; i < rates[mode].length; i++) {
            if (rates[mode][i] > reps) {
                found_i = i;
                break;
            }
        }
        
        const rowIndex = 11 - found_i;
        const tbody = document.getElementById("rates-tbody");
        if (tbody) {
            const targetRow = tbody.rows[rowIndex];
            if (targetRow) {
                // Highlight % of 1RM column
                const percentCell = targetRow.cells[0];
                if (percentCell) {
                    percentCell.classList.add('highlight-cell');
                }
                
                // Column 0 is %, Column 1 is Power, Column 2 is Average, Column 3 is Endurance
                const targetCell = targetRow.cells[mode + 1];
                if (targetCell) {
                    targetCell.classList.add('highlight-cell');
                }
            }
        }
    }

    const toggleTableBtn = document.getElementById("toggle-table-btn");
    const tableContainer = document.getElementById("reference-table-container");
    const backdrop = document.getElementById("modal-backdrop");
    const closeBtn = document.getElementById("close-table-btn");

    function toggleTable() {
        if (tableContainer) tableContainer.classList.toggle("show");
        if (backdrop) backdrop.classList.toggle("show");
        
        const t = window.translations[currentLang];
        if (tableContainer && tableContainer.classList.contains("show")) {
            toggleTableBtn.querySelector("span").textContent = t.hideTable;
        } else {
            toggleTableBtn.querySelector("span").textContent = t.viewTable;
        }
    }

    if (toggleTableBtn) {
        toggleTableBtn.addEventListener("click", toggleTable);
    }
    if (backdrop) {
        backdrop.addEventListener("click", toggleTable);
    }
    if (closeBtn) {
        closeBtn.addEventListener("click", toggleTable);
    }

    // Add listener to inputs to live update highlighting
    repsInput.addEventListener("input", () => {
        const r = parseInt(repsInput.value);
        const m = parseInt(modeSelect.value);
        if (!isNaN(r) && r > 0) updateTableHighlight(m, r);
    });

    modeSelect.addEventListener("change", () => {
        const r = parseInt(repsInput.value);
        const m = parseInt(modeSelect.value);
        if (!isNaN(r) && r > 0) updateTableHighlight(m, r);
    });

    // Initial highlight
    updateTableHighlight(parseInt(modeSelect.value), parseInt(repsInput.value));

    // Language logic
    let currentLang = 'en';

    function setLanguage(langCode) {
        if (!window.translations[langCode]) {
            langCode = 'en';
        }
        currentLang = langCode;
        const t = window.translations[langCode];
        
        // Update all data-i18n texts
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (t[key]) {
                el.textContent = t[key];
            }
        });
        
        // Update button text contextually
        if (toggleTableBtn) {
            const span = toggleTableBtn.querySelector('span');
            if (tableContainer && tableContainer.classList.contains('show')) {
                span.textContent = t.hideTable;
            } else {
                span.textContent = t.viewTable;
            }
            // Update calc button contextually if loading
            const calcSpan = btn.querySelector('span');
            if (btn.classList.contains('loading')) {
                calcSpan.textContent = t.calculating;
            } else {
                calcSpan.textContent = t.calcBtn;
            }
        }
    }

    function initLanguage() {
        const langDropdown = document.getElementById('lang-dropdown');
        const langBtn = document.getElementById('lang-btn');
        const langCodeSpan = document.getElementById('lang-code');
        const langFlagSpan = document.getElementById('lang-flag');

        // Detect user locale
        const userLocale = navigator.language || navigator.userLanguage;
        let detectedLang = userLocale.split('-')[0].toLowerCase();
        
        // Fallback or use detected
        if (!window.translations[detectedLang]) {
            detectedLang = 'en';
        }

        // Set initial
        setLanguage(detectedLang);

        // Update button UI
        const activeLi = langDropdown.querySelector(`li[data-lang="${detectedLang}"]`);
        if (activeLi) {
            const text = activeLi.textContent.trim();
            const flag = text.split(' ')[0];
            langFlagSpan.textContent = flag;
            langCodeSpan.textContent = detectedLang.toUpperCase();
        }

        // Dropdown interactions
        langBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            langDropdown.classList.toggle('show');
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.lang-selector')) {
                langDropdown.classList.remove('show');
            }
        });

        langDropdown.querySelectorAll('li').forEach(li => {
            li.addEventListener('click', () => {
                const lang = li.getAttribute('data-lang');
                const text = li.textContent.trim();
                const flag = text.split(' ')[0];
                langFlagSpan.textContent = flag;
                langCodeSpan.textContent = lang.toUpperCase();
                langDropdown.classList.remove('show');
                setLanguage(lang);
            });
        });
    }

    initLanguage();
});
