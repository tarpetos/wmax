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

    const toggleTableBtn = document.getElementById("toggle-table-btn");
    const tableContainer = document.getElementById("reference-table-container");

    if (toggleTableBtn && tableContainer) {
        toggleTableBtn.addEventListener("click", () => {
            tableContainer.classList.toggle("show");
            if (tableContainer.classList.contains("show")) {
                toggleTableBtn.querySelector("span").textContent = "Hide Reference Table";
            } else {
                toggleTableBtn.querySelector("span").textContent = "View Reference Table";
            }
        });
    }
});
