async function loadStatus() {
  const statusText = document.getElementById("status-text");
  const uptimeText = document.getElementById("uptime-text");
  const timestampText = document.getElementById("timestamp-text");
  const checksText = document.getElementById("checks-text");
  const uptimeBar = document.getElementById("uptime-bar");

  try {
    const response = await fetch("status.json", { cache: "no-store" });
    if (!response.ok) {
      statusText.textContent = "Could not load status";
      return;
    }

    const data = await response.json();

    const status = data.status || "UNKNOWN";
    const uptime = data.uptime_percentage ?? 0;
    const totalChecks = data.total_checks ?? 0;
    const downChecks = data.down_checks ?? 0;
    const timestamp = data.timestamp_utc || "";

    statusText.textContent = status;
    statusText.className = "";

    if (status === "UP") {
      statusText.classList.add("status-up");
    } else if (status === "DOWN") {
      statusText.classList.add("status-down");
    }

    uptimeText.textContent = uptime.toFixed(2) + "% uptime";
    uptimeBar.style.width = Math.max(0, Math.min(100, uptime)) + "%";

    timestampText.textContent = "Last check (UTC) " + timestamp;
    checksText.textContent =
      "Total checks " + totalChecks + "  |  Down events " + downChecks;
  } catch (error) {
    statusText.textContent = "Error loading status";
  }
}

loadStatus();
setInterval(loadStatus, 60000);
