document.addEventListener("DOMContentLoaded", () => {
    const urlInput = document.getElementById("urlInput");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const btnText = analyzeBtn.querySelector(".btn-text");
    const spinner = document.getElementById("loadingSpinner");
    const errorMessage = document.getElementById("errorMessage");
    const resultCard = document.getElementById("resultCard");

    const statusBadge = document.getElementById("statusBadge");
    const riskScoreValue = document.getElementById("riskScoreValue");
    const riskProgressBar = document.getElementById("riskProgressBar");
    const riskLevelText = document.getElementById("riskLevelText");

    const charUrlLength = document.getElementById("charUrlLength");
    const charSpecialChars = document.getElementById("charSpecialChars");
    const charSubdomains = document.getElementById("charSubdomains");
    const charIp = document.getElementById("charIp");
    const charHttps = document.getElementById("charHttps");

    const reasonsList = document.getElementById("reasonsList");
    const quickChips = document.querySelectorAll(".btn-chip");

    // Quick chip click handler
    quickChips.forEach(chip => {
        chip.addEventListener("click", () => {
            const url = chip.getAttribute("data-url");
            urlInput.value = url;
            analyzeUrl(url);
        });
    });

    // Button click handler
    analyzeBtn.addEventListener("click", () => {
        const url = urlInput.value.trim();
        analyzeUrl(url);
    });

    // Enter key handler
    urlInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            analyzeUrl(urlInput.value.trim());
        }
    });

    function showLoading(isLoading) {
        if (isLoading) {
            analyzeBtn.disabled = true;
            btnText.style.display = "none";
            spinner.style.display = "inline-block";
            errorMessage.classList.add("hidden");
        } else {
            analyzeBtn.disabled = false;
            btnText.style.display = "inline-block";
            spinner.style.display = "none";
        }
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.classList.remove("hidden");
        resultCard.classList.add("hidden");
    }

    async function analyzeUrl(url) {
        if (!url) {
            showError("Please enter a valid URL to analyze.");
            return;
        }

        showLoading(true);

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Analysis failed.");
            }

            renderResults(data);
        } catch (err) {
            showError(err.message || "Failed to communicate with prediction service.");
        } finally {
            showLoading(false);
        }
    }

    function renderResults(data) {
        errorMessage.classList.add("hidden");
        resultCard.classList.remove("hidden");

        const isPhishing = data.is_phishing;
        const score = data.risk_score;

        // Status Badge
        if (isPhishing) {
            statusBadge.textContent = "POTENTIAL PHISHING";
            statusBadge.className = "status-badge badge-phishing";
        } else {
            statusBadge.textContent = "LEGITIMATE";
            statusBadge.className = "status-badge badge-legitimate";
        }

        // Risk Meter
        riskScoreValue.textContent = Math.round(score);
        riskProgressBar.style.width = `${Math.min(Math.max(score, 4), 100)}%`;

        if (score >= 70) {
            riskProgressBar.style.backgroundColor = "var(--danger-red)";
            riskLevelText.textContent = "High Risk";
            riskLevelText.style.color = "var(--danger-red)";
        } else if (score >= 40) {
            riskProgressBar.style.backgroundColor = "var(--warning-orange)";
            riskLevelText.textContent = "Medium Risk";
            riskLevelText.style.color = "var(--warning-orange)";
        } else {
            riskProgressBar.style.backgroundColor = "var(--safe-green)";
            riskLevelText.textContent = "Low Risk / Safe";
            riskLevelText.style.color = "var(--safe-green)";
        }

        // Characteristics
        const chars = data.characteristics || {};
        charUrlLength.textContent = chars.url_length || "Normal";
        charUrlLength.className = `char-val ${chars.url_length === "High" ? "val-alert" : "val-safe"}`;

        charSpecialChars.textContent = chars.special_characters || "Normal";
        charSpecialChars.className = `char-val ${chars.special_characters === "High" ? "val-alert" : "val-safe"}`;

        charSubdomains.textContent = chars.subdomains || "Normal";
        charSubdomains.className = `char-val ${chars.subdomains === "High" ? "val-alert" : "val-safe"}`;

        charIp.textContent = chars.ip_address || "Not detected";
        charIp.className = `char-val ${chars.ip_address === "Detected" ? "val-alert" : "val-safe"}`;

        charHttps.textContent = chars.https || "Not detected";
        charHttps.className = `char-val ${chars.https === "Not detected" ? "val-alert" : "val-safe"}`;

        // Decision Explainability
        reasonsList.innerHTML = "";
        const explanations = data.explanations || [];
        explanations.forEach(exp => {
            const item = document.createElement("div");
            let riskClass = "risk-safe";
            let impactClass = "impact-safe";

            if (exp.impact === "High Risk") {
                riskClass = "risk-high";
                impactClass = "impact-high";
            } else if (exp.impact === "Moderate Risk") {
                riskClass = "risk-moderate";
                impactClass = "impact-moderate";
            }

            item.className = `reason-item ${riskClass}`;
            item.innerHTML = `
                <div>
                    <div class="reason-name">${exp.feature}</div>
                    <div class="reason-detail">${exp.detail}</div>
                </div>
                <span class="reason-impact ${impactClass}">${exp.impact}</span>
            `;
            reasonsList.appendChild(item);
        });

        // Smooth scroll to results
        resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
});
