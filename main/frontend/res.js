/**
 * ShadowScan Results Dashboard — Dynamic Data Population
 * Reads analysis results from localStorage and renders the threat report
 * with animated counters, progress bars, and color-coded severity levels.
 */

document.addEventListener('DOMContentLoaded', () => {
    const raw = localStorage.getItem('shadowscan_results');

    if (!raw) {
        document.getElementById('scan-status').textContent =
            'No scan data found. Please run an analysis first.';
        document.getElementById('risk-badge-text').innerHTML =
            '<span class="material-symbols-outlined" style="font-variation-settings: \'FILL\' 1;">error</span> NO DATA';
        return;
    }

    const data = JSON.parse(raw);

    const smsPct   = data.sms_pct   ?? null;
    const callPct  = data.phone_pct ?? null;
    const urlPct   = data.url_pct   ?? null;
    const avgPct   = data.avg_pct   ?? 0;
    const avgLevel = data.avg_level ?? 'UNKNOWN';

    // --- Status text ---
    const vectors = [];
    if (smsPct  !== null) vectors.push('SMS');
    if (callPct !== null) vectors.push('Call');
    if (urlPct  !== null) vectors.push('URL');

    document.getElementById('scan-status').textContent =
        `Deep scan completed across ${vectors.length} vector${vectors.length !== 1 ? 's' : ''}: ${vectors.join(', ')}.`;

    // --- Risk badge ---
    updateRiskBadge(avgPct, avgLevel);

    // --- Aggregate circle ---
    animateCircle(avgPct);

    // --- Aggregate percentage text ---
    animateCounter('agg-pct', avgPct, '%');

    setTimeout(() => {
        const sevEl = document.getElementById('agg-severity');
        if (avgPct >= 70) sevEl.textContent = 'SEVERE';
        else if (avgPct >= 40) sevEl.textContent = 'MODERATE';
        else sevEl.textContent = 'LOW';
    }, 800);

    // --- Individual bars ---
    setTimeout(() => {
        populateBar('sms',  smsPct);
        populateBar('call', callPct);
        populateBar('url',  urlPct);
    }, 300);

    // --- Color the aggregate text ---
    const aggPctEl = document.getElementById('agg-pct');
    if (avgPct < 40) {
        aggPctEl.classList.remove('text-secondary');
        aggPctEl.classList.add('text-primary');
    } else if (avgPct < 70) {
        aggPctEl.classList.remove('text-secondary');
        aggPctEl.classList.add('text-tertiary');
    }
});


/**
 * Update the risk level badge color, icon, and text.
 */
function updateRiskBadge(avgPct, avgLevel) {
    const badgeEl   = document.getElementById('risk-badge');
    const badgeText = document.getElementById('risk-badge-text');

    let badgeIcon   = 'check_circle';
    let badgeColor  = 'text-primary';
    let badgeBorder = 'border-primary/30';
    let badgeBg     = 'bg-primary/10';

    if (avgPct >= 70) {
        badgeIcon   = 'warning';
        badgeColor  = 'text-secondary';
        badgeBorder = 'border-secondary/30';
        badgeBg     = 'bg-secondary-container/20';
    } else if (avgPct >= 40) {
        badgeIcon   = 'info';
        badgeColor  = 'text-tertiary';
        badgeBorder = 'border-tertiary/30';
        badgeBg     = 'bg-tertiary/10';
    }

    badgeEl.className  = `px-4 py-2 ${badgeBg} border ${badgeBorder} rounded-sm`;
    badgeText.className = `flex items-center gap-2 font-headline font-black ${badgeColor} tracking-widest text-lg uppercase`;
    badgeText.innerHTML = `<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">${badgeIcon}</span> ${avgLevel} RISK`;
}


/**
 * Animate the SVG circular progress indicator.
 */
function animateCircle(avgPct) {
    const circumference = 2 * Math.PI * 88; // ≈ 552.92
    const circle = document.querySelectorAll('circle')[1];

    if (circle) {
        const offset = circumference - (circumference * avgPct / 100);
        circle.style.transition = 'stroke-dashoffset 1.5s ease-out';
        circle.setAttribute('stroke-dashoffset', String(circumference));
        setTimeout(() => circle.setAttribute('stroke-dashoffset', String(offset)), 100);
    }
}


/**
 * Populate an individual risk bar + percentage label.
 */
function populateBar(prefix, pct) {
    const pctEl = document.getElementById(`${prefix}-pct`);
    const barEl = document.getElementById(`${prefix}-bar`);

    if (pct === null || pct === undefined) {
        pctEl.textContent = 'N/A';
        barEl.style.width = '0%';
        return;
    }

    animateCounter(`${prefix}-pct`, pct, '%');
    barEl.style.width = `${Math.min(pct, 100)}%`;

    // Color logic — bar
    if (pct >= 70) {
        barEl.classList.remove('bg-tertiary', 'bg-primary');
        barEl.classList.add('bg-secondary');
        barEl.style.boxShadow = '0 0 8px rgba(255,113,106,0.5)';
    } else if (pct >= 40) {
        barEl.classList.remove('bg-secondary', 'bg-primary');
        barEl.classList.add('bg-tertiary');
        barEl.style.boxShadow = '0 0 8px rgba(254,208,27,0.5)';
    } else {
        barEl.classList.remove('bg-secondary', 'bg-tertiary');
        barEl.classList.add('bg-primary');
        barEl.style.boxShadow = '0 0 8px rgba(107,255,143,0.5)';
    }

    // Color logic — percentage text
    pctEl.classList.remove('text-secondary', 'text-tertiary', 'text-primary');
    if (pct >= 70)      pctEl.classList.add('text-secondary');
    else if (pct >= 40)  pctEl.classList.add('text-tertiary');
    else                 pctEl.classList.add('text-primary');
}


/**
 * Animate a number counting up from 0 to target.
 */
function animateCounter(elementId, target, suffix) {
    suffix = suffix || '';
    const el = document.getElementById(elementId);
    if (!el) return;

    const duration = 1200;
    const start    = performance.now();

    function update(now) {
        const elapsed  = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased    = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current  = Math.round(target * eased);
        el.textContent = `${current}${suffix}`;
        if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
}
