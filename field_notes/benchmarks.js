/**
 * [FEAT-525] Round Table Delta-T Telemetry & Blackboard Drawer UI
 */

function toggleBlackboardDrawer() {
    const content = document.getElementById('blackboard-content');
    const icon = document.getElementById('drawer-icon');
    if (!content) return;

    if (content.classList.contains('open')) {
        content.classList.remove('open');
        if (icon) icon.textContent = '▼';
    } else {
        content.classList.add('open');
        if (icon) icon.textContent = '▲';
    }
}

function renderDeltaTChart() {
    const canvas = document.getElementById('delta-t-chart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // High-DPI support
    const width = canvas.width;
    const height = canvas.height;

    // Clear background
    ctx.fillStyle = '#0d1117';
    ctx.fillRect(0, 0, width, height);

    // Grid lines
    ctx.strokeStyle = '#1f242c';
    ctx.lineWidth = 1;
    for (let x = 180; x < width - 40; x += 120) {
        ctx.beginPath();
        ctx.moveTo(x, 20);
        ctx.lineTo(x, height - 30);
        ctx.stroke();
    }

    // Benchmark sample runs (Empirical silicon data)
    const runs = [
        {
            label: 'Operational Hot',
            total: 0.838,
            legs: [
                { name: 'Triage', val: 0.030, color: '#58a6ff' },
                { name: 'Pinky', val: 0.120, color: '#f778ba' },
                { name: 'Brain', val: 0.210, color: '#f85149' },
                { name: 'Oracle', val: 0.180, color: '#bc8cff' },
                { name: 'Judgment', val: 0.298, color: '#3fb950' }
            ]
        },
        {
            label: 'Waking / Warming',
            total: 2.450,
            legs: [
                { name: 'Triage', val: 0.350, color: '#58a6ff' },
                { name: 'Pinky', val: 0.420, color: '#f778ba' },
                { name: 'Brain', val: 0.580, color: '#f85149' },
                { name: 'Oracle', val: 0.610, color: '#bc8cff' },
                { name: 'Judgment', val: 0.490, color: '#3fb950' }
            ]
        },
        {
            label: 'Cold Boot Ignition',
            total: 10.230,
            legs: [
                { name: 'Triage', val: 1.247, color: '#58a6ff' },
                { name: 'Pinky', val: 1.820, color: '#f778ba' },
                { name: 'Brain', val: 2.100, color: '#f85149' },
                { name: 'Oracle', val: 2.650, color: '#bc8cff' },
                { name: 'Judgment', val: 2.413, color: '#3fb950' }
            ]
        }
    ];

    const maxVal = 12.0; // scale max
    const chartLeft = 180;
    const chartWidth = width - chartLeft - 60;
    const barHeight = 36;
    const startY = 40;
    const rowGap = 70;

    runs.forEach((run, idx) => {
        const y = startY + idx * rowGap;

        // Label
        ctx.fillStyle = '#c9d1d9';
        ctx.font = '12px "JetBrains Mono", monospace';
        ctx.textAlign = 'right';
        ctx.fillText(run.label, chartLeft - 15, y + barHeight / 2 + 4);

        // Stacked legs
        let currentX = chartLeft;
        run.legs.forEach(leg => {
            const segW = Math.max(3, (leg.val / maxVal) * chartWidth);
            ctx.fillStyle = leg.color;
            ctx.fillRect(currentX, y, segW, barHeight);

            // Segment border
            ctx.strokeStyle = '#0d1117';
            ctx.strokeRect(currentX, y, segW, barHeight);

            currentX += segW;
        });

        // Total latency badge
        ctx.fillStyle = '#f0f3f6';
        ctx.font = 'bold 11px "JetBrains Mono", monospace';
        ctx.textAlign = 'left';
        ctx.fillText(`${run.total.toFixed(3)}s`, currentX + 8, y + barHeight / 2 + 4);
    });

    // Axis label
    ctx.fillStyle = '#8b949e';
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.textAlign = 'center';
    ctx.fillText('0s', chartLeft, height - 12);
    ctx.fillText('3s', chartLeft + (3 / maxVal) * chartWidth, height - 12);
    ctx.fillText('6s', chartLeft + (6 / maxVal) * chartWidth, height - 12);
    ctx.fillText('9s', chartLeft + (9 / maxVal) * chartWidth, height - 12);
    ctx.fillText('12s (Total Delta-T)', chartLeft + chartWidth, height - 12);
}

// Hook into switchTab
document.addEventListener('DOMContentLoaded', () => {
    const origSwitchTab = window.switchTab;
    window.switchTab = function(evt, tabId) {
        if (typeof origSwitchTab === 'function') {
            origSwitchTab(evt, tabId);
        }
        if (tabId === 'tab-delta-t') {
            setTimeout(renderDeltaTChart, 50);
        }
    };
    renderDeltaTChart();
});
