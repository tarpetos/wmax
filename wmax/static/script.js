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
            showError("Please enter a valid weight (1-500 kg).");
            return;
        }
        if (isNaN(reps) || reps <= 0 || reps > 100) {
            showError("Please enter valid repetitions (1-100).");
            return;
        }

        btn.classList.add("loading");
        btn.querySelector("span").textContent = "Calculating...";
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
            btn.querySelector("span").textContent = "Calculate Max";
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
                // Column 0 is %, Column 1 is Power, Column 2 is Average, Column 3 is Endurance
                const targetCell = targetRow.cells[mode + 1];
                if (targetCell) {
                    targetCell.classList.add('highlight-cell');
                }
            }
        }
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
});
