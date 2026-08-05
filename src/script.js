document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("calc-form");
    const weightInput = document.getElementById("weight");
    const repsInput = document.getElementById("reps");
    const modeSelect = document.getElementById("mode");
    const resultBox = document.getElementById("result-box");
    const maxResult = document.getElementById("max-result");
    const errorBox = document.getElementById("error-box");

    function showError(msg) {
        errorBox.textContent = msg;
        errorBox.classList.add("show");
        resultBox.classList.remove("show");
    }

    const unitToggle = document.getElementById("unit-toggle");
    const resultUnitMain = document.getElementById("result-unit-main");
    const resultUnitAlt = document.getElementById("result-unit-alt");
    const maxResultAlt = document.getElementById("max-result-alt");

    const UNIT_MULTIPLIERS = {
        "kg": 1.0,
        "lbs": 2.20462262
    };

    const BASE_LIMITS = {
        minWeight: 1,
        maxWeight: 500
    };

    let isCalculating = false;

    async function performCalculation() {
        if (weightInput.value.trim() === "" || repsInput.value.trim() === "") {
            resultBox.classList.remove("show");
            errorBox.classList.remove("show");
            return;
        }

        const weight = parseFloat(weightInput.value);
        const reps = parseInt(repsInput.value);
        const mode = parseInt(modeSelect.value);
        const unit = unitToggle ? unitToggle.getAttribute("data-unit") : "kg";

        const multiplier = UNIT_MULTIPLIERS[unit] || 1.0;
        const minW = BASE_LIMITS.minWeight * multiplier;
        const maxW = BASE_LIMITS.maxWeight * multiplier;

        if (isNaN(weight) || weight < minW || weight > maxW) {
            resultBox.classList.remove("show");
            let msg = window.translations[currentLang].errWeight || "Enter valid weight ({min}-{max}).";
            msg = msg.replace("{min}", minW % 1 === 0 ? minW : minW.toFixed(1));
            msg = msg.replace("{max}", maxW % 1 === 0 ? maxW : maxW.toFixed(1));
            showError(msg);
            return;
        }

        if (isNaN(reps) || reps <= 0 || reps > 100) {
            resultBox.classList.remove("show");
            showError(window.translations[currentLang].errReps || "Enter valid reps (1-100).");
            return;
        }

        errorBox.classList.remove("show");

        try {
            isCalculating = true;

            function myRound(number, unitStr) {
                const mul = UNIT_MULTIPLIERS[unitStr] || 1.0;
                const threshold = 50.0 * mul;
                if (number >= threshold) {
                    return 2.5 * Math.round(number / 2.5);
                }
                return 1.0 * Math.round(number / 1.0);
            }

            const ratesMode = [
                [1, 2, 3, 4, 6, 8, 10, 12, 18, 26, 30],
                [1, 2, 4, 6, 8, 10, 12, 18, 26, 30, 38],
                [1, 2, 4, 8, 10, 12, 18, 26, 30, 38, 50],
            ];
            let found_i = ratesMode[mode].length;
            for (let i = 0; i < ratesMode[mode].length; i++) {
                if (ratesMode[mode][i] > reps) {
                    found_i = i;
                    break;
                }
            }
            const percent = 100 - (found_i - 1) * 5;
            const raw_maximum = weight / (percent / 100.0);
            
            const maximum = myRound(raw_maximum, unit);
            const altUnit = unit === "kg" ? "lbs" : "kg";
            const altWeight = unit === "kg" ? raw_maximum * 2.20462262 : raw_maximum / 2.20462262;
            const maximum_alt = myRound(altWeight, altUnit);

            const data = { maximum, maximum_alt };
            
            // Animate number
            let start = 0;
            let startAlt = 0;
            const end = data.maximum;
            const endAlt = data.maximum_alt;
            const duration = 600;
            const startTime = performance.now();

            resultBox.classList.add("show");

            function updateNumber(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing out cubic
                const easeOut = 1 - Math.pow(1 - progress, 3);
                
                const currentVal = start + (end - start) * easeOut;
                const currentValAlt = startAlt + (endAlt - startAlt) * easeOut;
                
                const hasDecimal = end % 1 !== 0;
                const hasDecimalAlt = endAlt % 1 !== 0;
                
                maxResult.textContent = hasDecimal ? currentVal.toFixed(1) : Math.round(currentVal);
                maxResultAlt.textContent = hasDecimalAlt ? currentValAlt.toFixed(1) : Math.round(currentValAlt);

                if (progress < 1) {
                    requestAnimationFrame(updateNumber);
                } else {
                    maxResult.textContent = hasDecimal ? end.toFixed(1) : end;
                    maxResultAlt.textContent = hasDecimalAlt ? endAlt.toFixed(1) : endAlt;
                }
            }

            requestAnimationFrame(updateNumber);

        } catch (err) {
            showError(err.message);
        } finally {
            isCalculating = false;
        }
    }

    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    const autoCalc = debounce(performCalculation, 300);


    weightInput.addEventListener("input", autoCalc);
    repsInput.addEventListener("input", autoCalc);
    modeSelect.addEventListener("change", performCalculation);
    
    if (unitToggle) {
        unitToggle.addEventListener("click", () => {
            const currentUnit = unitToggle.getAttribute("data-unit");
            const newUnit = currentUnit === "kg" ? "lbs" : "kg";
            
            unitToggle.setAttribute("data-unit", newUnit);
            const i18nKey = newUnit === "kg" ? "unitKg" : "unitLbs";
            unitToggle.setAttribute("data-i18n", i18nKey);
            unitToggle.textContent = window.translations[currentLang][i18nKey];
            
            if (newUnit === "kg") {
                resultUnitMain.setAttribute("data-i18n", "unitKg");
                resultUnitMain.textContent = window.translations[currentLang].unitKg;
                resultUnitAlt.setAttribute("data-i18n", "unitLbs");
                resultUnitAlt.textContent = window.translations[currentLang].unitLbs;
            } else {
                resultUnitMain.setAttribute("data-i18n", "unitLbs");
                resultUnitMain.textContent = window.translations[currentLang].unitLbs;
                resultUnitAlt.setAttribute("data-i18n", "unitKg");
                resultUnitAlt.textContent = window.translations[currentLang].unitKg;
            }

            const multiplier = UNIT_MULTIPLIERS[newUnit] || 1.0;
            weightInput.min = (BASE_LIMITS.minWeight * multiplier).toFixed(newUnit === 'kg' ? 0 : 1);
            weightInput.max = (BASE_LIMITS.maxWeight * multiplier).toFixed(newUnit === 'kg' ? 0 : 1);
            
            performCalculation();
        });
    }

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
        
    }

    function initLanguage() {
        const langDropdown = document.getElementById('lang-dropdown');
        const langBtn = document.getElementById('lang-btn');
        const langCodeSpan = document.getElementById('lang-code');
        const langFlagSpan = document.getElementById('lang-flag');

        const displayCodes = { en: 'EN', uk: 'UA', ru: 'RU', es: 'ES', fr: 'FR', de: 'DE', zh: 'CN', ja: 'JP', ko: 'KR', it: 'IT', pt: 'PT', ar: 'AR', hi: 'IN', bn: 'BD', tr: 'TR', pl: 'PL', nl: 'NL', vi: 'VN', th: 'TH', id: 'ID' };

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
            const flagImg = activeLi.querySelector('.flag-icon');
            if (flagImg) {
                langFlagSpan.src = flagImg.src;
            }
            langCodeSpan.textContent = displayCodes[detectedLang] || detectedLang.toUpperCase();
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
                const flagImg = li.querySelector('.flag-icon');
                if (flagImg) {
                    langFlagSpan.src = flagImg.src;
                }
                langCodeSpan.textContent = displayCodes[lang] || lang.toUpperCase();
                langDropdown.classList.remove('show');
                setLanguage(lang);
            });
        });
    }

    initLanguage();
    performCalculation();
});

