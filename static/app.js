const form = document.getElementById("converterForm");
const submitButton = document.getElementById("submitButton");
const statusLabel = document.getElementById("statusLabel");
const statusMessage = document.getElementById("statusMessage");
const progressBar = document.getElementById("progressBar");
const toolStatus = document.getElementById("toolStatus");

const fields = {
  video_url: document.getElementById("video_url"),
  output_name: document.getElementById("output_name"),
  bitrate: document.getElementById("bitrate"),
};

let pollTimer = null;

function setStatus(label, message, progress = 0) {
  statusLabel.textContent = label;
  statusMessage.textContent = message;
  progressBar.style.width = `${progress}%`;
}

function clearErrors() {
  Object.entries(fields).forEach(([name, element]) => {
    element.classList.remove("input-error");
    document.getElementById(`${name}_error`).textContent = "";
  });
}

function showErrors(fieldErrors = {}) {
  Object.entries(fieldErrors).forEach(([name, message]) => {
    if (!message || !fields[name]) return;
    fields[name].classList.add("input-error");
    document.getElementById(`${name}_error`).textContent = message;
  });
}

async function loadToolStatus() {
  try {
    const response = await fetch("/api/health");
    const data = await response.json();
    const ffmpegText = data.tools.ffmpeg ? "FFmpeg ready" : "Install FFmpeg";
    const ytdlpCliText = data.tools.yt_dlp_cli ? "yt-dlp ready" : "Install yt-dlp";
    const cookiesText = data.tools.youtube_cookies ? "YouTube cookies ready" : "Add YouTube cookies file";
    toolStatus.textContent = `${ffmpegText} • ${ytdlpCliText} • ${cookiesText}`;
  } catch (error) {
    toolStatus.textContent = "Could not check local tools";
  }
}

async function pollJob(jobId) {
  if (pollTimer) {
    clearTimeout(pollTimer);
  }

  try {
    const response = await fetch(`/api/jobs/${jobId}`);
    const job = await response.json();

    if (!response.ok) {
      throw new Error(job.error || "Could not fetch job status.");
    }

    const labelMap = {
      queued: "Queued",
      running: "Working",
      completed: "Complete",
      failed: "Error",
    };

    setStatus(labelMap[job.status] || "Working", job.message, job.progress || 0);

    if (job.status === "queued" || job.status === "running") {
      pollTimer = setTimeout(() => pollJob(jobId), 1200);
      return;
    }

    submitButton.disabled = false;
    submitButton.textContent = "Download and convert";
  } catch (error) {
    submitButton.disabled = false;
    submitButton.textContent = "Download and convert";
    setStatus("Error", error.message, 0);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearErrors();
  submitButton.disabled = true;
  submitButton.textContent = "Starting...";
  setStatus("Checking", "Validating your request...", 4);

  const payload = {
    video_url: fields.video_url.value.trim(),
    output_name: fields.output_name.value.trim(),
    bitrate: fields.bitrate.value,
  };

  try {
    const response = await fetch("/api/jobs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      showErrors(data.field_errors);
      throw new Error(data.error || "Please check the form and try again.");
    }

    submitButton.textContent = "Working...";
    setStatus("Queued", "Your conversion job has started.", 10);
    pollJob(data.job_id);
  } catch (error) {
    submitButton.disabled = false;
    submitButton.textContent = "Download and convert";
    setStatus("Error", error.message, 0);
  }
});

loadToolStatus();
