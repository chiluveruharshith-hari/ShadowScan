/**
 * ShadowScan Landing Page — Analysis Controller
 * Collects phone metadata, SMS text, and URL inputs.
 * Sends all vectors to POST /analyze/all and redirects to results.
 */

const API_BASE = window.location.origin;

/**
 * Gather all form inputs and call the fusion API.
 */
async function runAnalysis() {
    // --- Gather phone fields ---
    const callNo = document.getElementById('phone-call-no').value.trim();
    const totalCalls = document.getElementById('phone-total-calls').value.trim();
    const uniqueNumbers = document.getElementById('phone-unique-numbers').value.trim();
    const avgDuration = document.getElementById('phone-avg-duration').value.trim();
    const callsPerHour = document.getElementById('phone-calls-per-hour').value.trim();
    const spamReports = document.getElementById('phone-spam-reports').value.trim();

    // --- Gather SMS & URL ---
    const smsVal = document.getElementById('sms-input').value.trim();
    const urlVal = document.getElementById('url-input').value.trim();

    // --- Check if phone section has any data ---
    const hasPhone = callNo || totalCalls || uniqueNumbers || avgDuration || callsPerHour || spamReports;

    // --- Validate: at least one vector ---
    if (!hasPhone && !smsVal && !urlVal) {
        showError('Please provide at least one input (call data, SMS, or URL) to analyze.');
        return;
    }

    // --- Validate phone: if call_no filled, require all other fields ---
    if (hasPhone) {
        if (!callNo) {
            showError('Phone Number (call_no) is required for call analysis.');
            return;
        }
        if (!totalCalls || !uniqueNumbers || !avgDuration || !callsPerHour || !spamReports) {
            showError('All call metadata fields are required for call analysis.');
            return;
        }
        if (isNaN(parseInt(totalCalls)) || isNaN(parseInt(uniqueNumbers)) ||
            isNaN(parseFloat(avgDuration)) || isNaN(parseFloat(callsPerHour)) ||
            isNaN(parseInt(spamReports))) {
            showError('Call metadata fields must be valid numbers.');
            return;
        }
    }

    // --- Set loading state ---
    setLoadingState(true);

    try {
        // --- Build payload ---
        const payload = {};

        if (hasPhone) {
            payload.phone = {
                call_no: callNo,
                total_calls_made: parseInt(totalCalls),
                unique_numbers_contacted: parseInt(uniqueNumbers),
                avg_call_duration_min: parseFloat(avgDuration),
                calls_per_hour: parseFloat(callsPerHour),
                spam_reports: parseInt(spamReports),
            };
        }

        if (smsVal) payload.sms = smsVal;
        if (urlVal) payload.url = urlVal;

        // --- Call the API ---
        const response = await fetch(`${API_BASE}/analyze/all`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.detail || `Server error: ${response.status}`);
        }

        const data = await response.json();

        // --- Store inputs alongside results for the results page ---
        data._inputs = {
            phone: hasPhone ? payload.phone : null,
            sms: smsVal || null,
            url: urlVal || null,
        };

        localStorage.setItem('shadowscan_results', JSON.stringify(data));

        // --- Brief success feedback ---
        const btnText = document.getElementById('btn-text');
        const btnIcon = document.getElementById('btn-icon');
        const btn = document.getElementById('analyze-btn');

        btnText.textContent = 'THREAT DETECTED';
        btnIcon.textContent = 'check_circle';
        btn.classList.remove('bg-primary');
        btn.classList.add('bg-secondary');

        setTimeout(() => {
            window.location.href = 'res.html';
        }, 600);

    } catch (err) {
        console.error('Analysis failed:', err);
        showError(err.message || 'Failed to connect to ShadowScan API. Is the backend running?');
        setLoadingState(false);
    }
}


/**
 * Show/hide loading state on the submit button.
 */
function setLoadingState(loading) {
    const btn = document.getElementById('analyze-btn');
    const btnText = document.getElementById('btn-text');
    const btnIcon = document.getElementById('btn-icon');
    const errorMsg = document.getElementById('error-msg');

    errorMsg.classList.add('hidden');

    if (loading) {
        btn.disabled = true;
        btn.style.opacity = '0.6';
        btn.style.cursor = 'wait';
        btnText.textContent = 'SCANNING...';
        btnIcon.textContent = 'hourglass_top';
    } else {
        btn.disabled = false;
        btn.style.opacity = '1';
        btn.style.cursor = 'pointer';
        btnText.textContent = 'ANALYZE THREAT';
        btnIcon.textContent = 'biotech';
        btn.classList.remove('bg-secondary');
        btn.classList.add('bg-primary');
    }
}


/**
 * Display an error message below the submit button.
 */
function showError(msg) {
    const errorMsg = document.getElementById('error-msg');
    errorMsg.textContent = msg;
    errorMsg.classList.remove('hidden');
}
