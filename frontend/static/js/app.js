/* ═══════════════════════════════════════════════════════════════
   CodeFlow — app.js  (FIXED)
   ═══════════════════════════════════════════════════════════════ */

const API_BASE = "";

const state = {
  token:           localStorage.getItem("cm_token") || "",
  theme:           localStorage.getItem("cm_theme")   || "dark",
  palette:         localStorage.getItem("cm_palette") || "green",
  page:            "landing",
  result:          null,
  history:         [],
  filteredHistory: [],
  selectedRun:     null,
  searchTerm:      "",
  langFilter:      "all",
};

const $  = (id)  => document.getElementById(id);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

/* ── Theme ──────────────────────────────────────────────── */
function applyTheme() {
  document.body.classList.toggle("light", state.theme === "light");
  document.body.dataset.palette = state.palette;
  localStorage.setItem("cm_theme",   state.theme);
  localStorage.setItem("cm_palette", state.palette);
}

$("themeToggleBtn")?.addEventListener("click", () => {
  state.theme = state.theme === "light" ? "dark" : "light";
  applyTheme();
  showToast(`Switched to ${state.theme} mode`);
});

$("paletteToggleBtn")?.addEventListener("click", () => {
  state.palette = state.palette === "green" ? "brown" : "green";
  applyTheme();
  showToast(`Palette: ${state.palette === "green" ? "Sage Green" : "Aesthetic Brown"}`);
});

/* ── Toast ──────────────────────────────────────────────── */
let toastTimer;
function showToast(msg) {
  const t = $("toast");
  if (!t) return;
  t.textContent = msg;
  t.classList.remove("hidden");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.add("hidden"), 3000);
}

/* ── Page routing ───────────────────────────────────────── */
function showPage(name) {
  state.page = name;
  $$(".page").forEach(p => p.classList.toggle("active", p.dataset.page === name));
  $$(".nav-link").forEach(l => l.classList.toggle("active", l.dataset.nav === name));
  $("navLinks")?.classList.remove("open");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

document.addEventListener("click", (e) => {
  const trigger = e.target.closest("[data-nav]");
  if (!trigger) return;
  e.preventDefault();
  showPage(trigger.dataset.nav);
});

$("mobileMenuBtn")?.addEventListener("click", () => {
  $("navLinks")?.classList.toggle("open");
});

/* ── Session UI ─────────────────────────────────────────── */
function updateSessionUi() {
  const loggedIn = Boolean(state.token);
  const badge    = $("sessionBadge");
  const label    = badge?.querySelector(".session-label");
  if (label) label.textContent = loggedIn ? "Authenticated" : "Guest";
  badge?.classList.toggle("authed", loggedIn);
  $("logoutBtn")?.classList.toggle("hidden",    !loggedIn);
  $("signInNavBtn")?.classList.toggle("hidden",  loggedIn);
}

/* ── Status helpers ─────────────────────────────────────── */
function setAuthMsg(msg, type = "") {
  const el = $("authMessage");
  if (!el) return;
  el.textContent = msg;
  el.className = "auth-msg" + (type ? " " + type : "");
}
function setStatus(msg, type = "") {
  const el = $("statusBanner");
  if (!el) return;
  el.textContent = msg;
  el.className = "status-banner" + (type ? " " + type : "");
}
function setPsPill(text, type = "") {
  const el = $("psPill");
  if (!el) return;
  el.textContent = text;
  el.className = "ps-pill" + (type ? " " + type : "");
}
function setCurrentRun(label) {
  const el = $("currentRunLabel");
  if (el) el.textContent = label;
}

/* ── API ────────────────────────────────────────────────── */
async function api(path, opts = {}) {
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const res  = await fetch(`${API_BASE}${path}`, { ...opts, headers });
  const text = await res.text();
  let data   = null;
  try   { data = text ? JSON.parse(text) : null; }
  catch { data = { detail: text || "Unexpected response." }; }
  if (!res.ok) {
    const msg = data?.detail || data?.message || "Request failed.";
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  return data;
}

/* ── FIXED: getRunId — covers ALL possible field names ──── */
function getRunId(r) {
  if (!r) return null;
  // Try every possible field the backend might return
  const id = r.id ?? r.analysis_id ?? r.run_id ?? r.analysisId ?? r.runId ?? null;
  if (!id) {
    // Debug: log the actual keys so we can see what backend returns
    console.warn("[CodeFlow] getRunId: could not find id in object:", Object.keys(r));
  }
  return id;
}

const getRunTitle = (r, i = 0) =>
  r?.project_name || r?.Project_Name || r?.projectName || `Analysis #${i + 1}`;

const ext = (lang) =>
  ({ python: "py", cpp: "cpp", java: "java", javascript: "js" }[
    String(lang || "").toLowerCase()
  ] || "txt");

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

function downloadText(name, content) {
  if (!content) { showToast("Nothing to download yet."); return; }
  const a = Object.assign(document.createElement("a"), {
    href: URL.createObjectURL(new Blob([content], { type: "text/plain;charset=utf-8" })),
    download: name,
  });
  document.body.appendChild(a); a.click(); a.remove();
}

/* ── Content getters ────────────────────────────────────── */
function getContent(kind) {
  const r = state.result || {};
  switch (kind) {
    case "review":        return `BUGS FOUND: ${r.bugs_found ?? "unknown"}\n\n${r.review_report || ""}`.trim();
    case "fixed":         return r.fixed_code         || "";
    case "optimized":     return r.optimized_code     || r.code || "";
    case "explanation":   return r.explanation        || "";
    case "documentation": return r.documentation      || r.readme_content || "";
    default: return "";
  }
}

/* ── Render results ─────────────────────────────────────── */
function renderResults() {
  const map = {
    review:        $("outReview"),
    fixed:         $("outFixed"),
    optimized:     $("outOptimized"),
    documentation: $("outDocumentation"),
    explanation:   $("outExplanation"),
  };
  const placeholders = {
    review:        "Run an analysis to see the review report.",
    fixed:         "No fixed code — either no bugs found or analysis not run yet.",
    optimized:     "Run an analysis to see optimized code.",
    documentation: "Run an analysis to see generated documentation.",
    explanation:   "Run an analysis to see the dry-run explanation.",
  };
  Object.entries(map).forEach(([key, el]) => {
    if (!el) return;
    const c = getContent(key);
    el.textContent = c || placeholders[key];
  });

  const meta = $("rcMetaReview");
  if (meta && state.result && typeof state.result.bugs_found !== "undefined") {
    meta.textContent = `· ${state.result.bugs_found ? "Bugs found" : "Clean"}`;
  } else if (meta) meta.textContent = "";
}

/* ── Progress strip ─────────────────────────────────────── */
function resetProgress() {
  $$(".ps-step").forEach(s => s.classList.remove("active", "done"));
}
function setProgressStep(step) {
  const order = ["review", "fixed", "optimized", "documentation", "explanation", "github"];
  const idx   = order.indexOf(step);
  $$(".ps-step").forEach((el, i) => {
    el.classList.remove("active", "done");
    if (i < idx)      el.classList.add("done");
    else if (i === idx) el.classList.add("active");
  });
}
function completeAllProgress() {
  $$(".ps-step").forEach(el => { el.classList.remove("active"); el.classList.add("done"); });
}
async function animateProgress() {
  const steps = ["review", "fixed", "optimized", "documentation", "explanation"];
  for (const s of steps) {
    setProgressStep(s);
    await new Promise(r => setTimeout(r, 900));
  }
}

/* ── History filters ────────────────────────────────────── */
function applyHistoryFilters() {
  let list = state.history;
  if (state.langFilter !== "all")
    list = list.filter(r => String(r.language || "").toLowerCase() === state.langFilter);
  if (state.searchTerm) {
    const q = state.searchTerm.toLowerCase();
    list = list.filter(r => getRunTitle(r).toLowerCase().includes(q));
  }
  state.filteredHistory = list;
  renderHistory();
}

function renderHistory() {
  const el = $("historyList");
  if (!el) return;
  const list = state.filteredHistory;
  if (!list.length) {
    el.innerHTML = state.token
      ? `<p class="empty-msg">No runs match your filters.</p>`
      : `<p class="empty-msg">Login to view your saved runs.</p>`;
    return;
  }
  el.innerHTML = list.map((item, i) => {
    const id       = getRunId(item);
    const title    = esc(getRunTitle(item, i));
    const lang     = esc(item.language || "unknown");
    const bugs     = item.bugs_found;
    const selected = getRunId(state.selectedRun) === id ? "selected" : "";
    const bugBadge = bugs === true
      ? `<span class="bug-badge yes">⚑ Bugs</span>`
      : bugs === false
        ? `<span class="bug-badge no">✓ Clean</span>`
        : "";
    const date = item.created_at || item.timestamp || "";
    return `
      <article class="history-item ${selected}" data-id="${id}">
        <div class="hi-top">
          <div class="history-item-name">${title}</div>
          <span class="lang-badge">${lang}</span>
        </div>
        <div class="history-item-meta">
          ${bugBadge}
          ${date ? `<span>🕐 ${esc(String(date).slice(0, 10))}</span>` : ""}
        </div>
        <div class="history-actions">
          <button class="ghost-btn sm" data-action="select" data-id="${id}">👁 View</button>
          <button class="ghost-btn sm danger" data-action="delete" data-id="${id}">🗑</button>
        </div>
      </article>`;
  }).join("");
}

async function loadHistory() {
  const el = $("historyList");
  if (!state.token) {
    if (el) el.innerHTML = `<p class="empty-msg">Login to view your saved runs.</p>`;
    state.history = []; state.filteredHistory = [];
    return;
  }
  try {
    if (el) el.innerHTML = `<p class="empty-msg">Loading…</p>`;
    const data     = await api("/assistant/me");
    state.history  = Array.isArray(data) ? data : (data?.history || data?.data || []);
    applyHistoryFilters();
  } catch (e) {
    if (el) el.innerHTML = `<p class="empty-msg">${esc(e.message)}</p>`;
  }
}

/* ── FIXED: selectRun — stores full run object ──────────── */
function selectRun(run) {
  state.selectedRun = run;               // full object stored
  state.result = {
    ...run,
    documentation: run.documentation || run.readme_content || "",
    code:          run.original_code  || run.code || "",
  };
  const title = getRunTitle(run);
  setCurrentRun(title);

  const repoEl = $("repoName");
  if (repoEl)
    repoEl.value = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 80);

  completeAllProgress();
  setPsPill("Loaded", "done");
  renderHistory();
  renderResults();

  // Debug log so you can see exactly what is stored
  console.log("[CodeFlow] selectedRun set:", { id: getRunId(run), title });
}

/* ── GitHub status ──────────────────────────────────────── */
async function checkGithubStatus() {
  const el = $("githubStatus");
  if (!el) return;
  if (!state.token) { el.textContent = "Login first, then connect GitHub."; return; }
  try {
    const data = await api("/auth/github/status");
    el.textContent = data.message || (data.connected ? "✓ GitHub connected." : "✗ GitHub not connected.");
    el.className   = data.connected ? "status-info connected" : "status-info";
  } catch (e) { el.textContent = e.message; }
}

/* ── Auth tabs ──────────────────────────────────────────── */
$$(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    $$(".tab").forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    const isLogin = tab.dataset.tab === "login";
    $("loginForm")?.classList.toggle("hidden",   !isLogin);
    $("registerForm")?.classList.toggle("hidden",  isLogin);
  });
});

/* ── Password toggles ───────────────────────────────────── */
$$(".pw-toggle").forEach(btn => {
  btn.addEventListener("click", () => {
    const input = $(btn.dataset.toggle);
    if (!input) return;
    const isPw  = input.type === "password";
    input.type  = isPw ? "text" : "password";
    btn.textContent = isPw ? "🙈" : "👁";
  });
});

/* ── Register ───────────────────────────────────────────── */
$("registerForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const pw = $("registerPassword").value;
  const cf = $("registerConfirm")?.value;
  if (pw.length < 8)       { setAuthMsg("Password must be at least 8 characters.", "error"); return; }
  if (cf && pw !== cf)     { setAuthMsg("Passwords do not match.", "error"); return; }
  try {
    const data = await api("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        username: $("registerUsername").value.trim(),
        email:    $("registerEmail").value.trim(),
        password: pw,
      }),
    });
    setAuthMsg(data?.message || "Account created. You can now login.", "success");
    showToast("Registered successfully!");
    // Auto-switch to login tab
    $$(".tab").forEach(t => t.classList.toggle("active", t.dataset.tab === "login"));
    $("loginForm")?.classList.remove("hidden");
    $("registerForm")?.classList.add("hidden");
  } catch (err) { setAuthMsg(err.message, "error"); }
});

/* ── Login ──────────────────────────────────────────────── */
$("loginForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    const data = await api("/auth/login", {
      method: "POST",
      body: JSON.stringify({
        username_or_email: $("loginUsername").value.trim(),
        password:          $("loginPassword").value,
      }),
    });
    state.token = data.access_token;
    localStorage.setItem("cm_token", state.token);
    updateSessionUi();
    setAuthMsg("Logged in successfully.", "success");
    showToast("Welcome back!");
    await loadHistory();
    checkGithubStatus();
    setTimeout(() => showPage("dashboard"), 600);
  } catch (err) { setAuthMsg(err.message, "error"); }
});

/* ── Logout ─────────────────────────────────────────────── */
$("logoutBtn")?.addEventListener("click", () => {
  state.token = ""; state.result = null; state.selectedRun = null;
  state.history = []; state.filteredHistory = [];
  localStorage.removeItem("cm_token");
  updateSessionUi(); renderResults(); renderHistory();
  checkGithubStatus();
  setAuthMsg("Signed out.");
  resetProgress();
  setPsPill("Idle");
  setCurrentRun("No run yet — paste code to start.");
  showToast("Signed out.");
  showPage("landing");
});

/* ── FIXED: Analyze ─────────────────────────────────────── */
$("analyzeForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!state.token) { showToast("Please login first."); showPage("auth"); return; }

  const payload = {
    project_name: $("projectName").value.trim(),
    language:     $("language").value,
    code:         $("codeInput").value,
    github:       $("githubPush")?.checked || false,
  };

  const btn     = $("analyzeBtn");
  const btnText = btn?.querySelector(".btn-text") || btn;
  const origTxt = btnText?.textContent;

  try {
    if (btn) btn.disabled = true;
    if (btnText) btnText.textContent = "Running agents…";
    setStatus("Agents running: review → fix → optimize → explain…", "running");
    setPsPill("Running", "running");
    setCurrentRun(payload.project_name);
    resetProgress();

    const [data] = await Promise.all([
      api("/assistant/analyze", { method: "POST", body: JSON.stringify(payload) }),
      animateProgress(),
    ]);

    // FIXED: store both result and selectedRun from API response
    state.result      = data;
    state.selectedRun = data;   // so push works immediately after analyze

    // Debug log — verify the id field name
    console.log("[CodeFlow] analyze response keys:", Object.keys(data));
    console.log("[CodeFlow] analysis id resolved:", getRunId(data));

    completeAllProgress();
    setStatus(data?.message || "Analysis complete.", "success");
    setPsPill("Complete", "done");
    renderResults();
    await loadHistory();
    showToast("Analysis complete!");
  } catch (err) {
    setStatus(err.message, "error");
    setPsPill("Failed", "error");
  } finally {
    if (btn) btn.disabled = false;
    if (btnText) btnText.textContent = origTxt || "Run AI Workflow";
  }
});

/* ── History actions ────────────────────────────────────── */
$("historyList")?.addEventListener("click", async (e) => {
  const btn = e.target.closest("button[data-action]");
  if (!btn) return;
  const run = state.history.find(r => String(getRunId(r)) === String(btn.dataset.id));
  if (!run) return;

  if (btn.dataset.action === "select") {
    selectRun(run);
    showToast("Run loaded.");
    showPage("dashboard");
  }
  if (btn.dataset.action === "delete") {
    if (!confirm("Delete this analysis run?")) return;
    try {
      await api(`/assistant/history/${getRunId(run)}`, { method: "DELETE" });
      if (getRunId(state.selectedRun) === getRunId(run)) {
        state.selectedRun = null; state.result = null;
        setCurrentRun("No run selected"); renderResults(); resetProgress();
      }
      await loadHistory();
      showToast("Deleted.");
    } catch (err) { showToast(err.message); }
  }
});

$("refreshHistoryBtn")?.addEventListener("click", loadHistory);

$("clearHistoryBtn")?.addEventListener("click", async () => {
  if (!confirm("Clear all saved history?")) return;
  try {
    await api("/assistant/history", { method: "DELETE" });
    state.selectedRun = null; state.result = null;
    setCurrentRun("No run selected"); renderResults();
    await loadHistory();
    showToast("History cleared.");
  } catch (err) { showToast(err.message); }
});

$("historySearch")?.addEventListener("input", (e) => {
  state.searchTerm = e.target.value.trim();
  applyHistoryFilters();
});

$("historyFilters")?.addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (!chip) return;
  $$(".chip").forEach(c => c.classList.remove("active"));
  chip.classList.add("active");
  state.langFilter = chip.dataset.filter;
  applyHistoryFilters();
});

/* ── GitHub connect ─────────────────────────────────────── */
$("githubConnectBtn")?.addEventListener("click", async () => {
  if (!state.token) { showToast("Login first."); showPage("auth"); return; }
  try {
    const data = await api("/auth/github/login");
    if (data?.redirect_url) {
      window.open(data.redirect_url, "_blank");
      showToast("Complete GitHub authorization in the new tab.");
      // Re-check status after 5 seconds (user may have authorized)
      setTimeout(checkGithubStatus, 5000);
    }
  } catch (err) { showToast(err.message); }
});

/* ── FIXED: GitHub push ─────────────────────────────────── */
$("pushGithubBtn")?.addEventListener("click", async () => {
  // Guard: must have a selected run
  if (!state.selectedRun) {
    showToast("Run an analysis first or select one from history.");
    return;
  }

  const analysisId = getRunId(state.selectedRun);

  // Guard: id must be resolvable
  if (!analysisId) {
    showToast("Could not find analysis ID. Please re-select the run from history.");
    console.error("[CodeFlow] pushGithubBtn: analysisId is null. selectedRun =", state.selectedRun);
    return;
  }

  const repoName = $("repoName")?.value.trim();
  if (!repoName) { showToast("Enter a repository name."); return; }

  const btn      = $("pushGithubBtn");
  const original = btn.innerHTML;

  try {
    btn.disabled  = true;
    btn.textContent = "Pushing…";
    setProgressStep("github");

    const data = await api("/auth/github/push", {
      method: "POST",
      body: JSON.stringify({
        analysis_id: analysisId,          // ✅ always sent
        repo_name:   repoName,
        is_private:  $("repoPrivate")?.checked || false,
      }),
    });

    completeAllProgress();
    showToast(data.message || "Pushed to GitHub!");
    if (data.repo_url) window.open(data.repo_url, "_blank");
  } catch (err) {
    showToast(err.message);
    console.error("[CodeFlow] push error:", err);
  } finally {
    btn.disabled  = false;
    btn.innerHTML = original;
  }
});

/* ── Load sample / clear ────────────────────────────────── */
$("loadSampleBtn")?.addEventListener("click", () => {
  if ($("projectName")) $("projectName").value = "Second largest element in array";
  if ($("language"))    $("language").value    = "cpp";
  if ($("codeInput"))   $("codeInput").value   = `#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int getSecondLargest(vector<int> arr) {
    sort(arr.begin(), arr.end());
    return arr[arr.size() - 2];
}

int main() {
    vector<int> arr = {12, 35, 1, 10, 34, 1};
    cout << getSecondLargest(arr);
    return 0;
}`;
  updateCharCounter();
});

$("clearCodeBtn")?.addEventListener("click", () => {
  if ($("projectName")) $("projectName").value = "";
  if ($("codeInput"))   $("codeInput").value   = "";
  updateCharCounter();
});

/* ── Char counter ───────────────────────────────────────── */
function updateCharCounter() {
  const counter = $("charCounter");
  const code    = $("codeInput");
  if (counter && code) counter.textContent = `${code.value.length.toLocaleString()} chars`;
}
$("codeInput")?.addEventListener("input", updateCharCounter);

/* ── Result card actions (copy / download / collapse) ───── */
document.addEventListener("click", async (e) => {
  // Copy
  const copyEl = e.target.closest("[data-copy]");
  if (copyEl) {
    const c = getContent(copyEl.dataset.copy);
    if (!c) { showToast("Nothing to copy."); return; }
    await navigator.clipboard.writeText(c);
    showToast("Copied to clipboard!");
    return;
  }
  // Download
  const dlEl = e.target.closest("[data-download]");
  if (dlEl) {
    const kind = dlEl.dataset.download;
    const c    = getContent(kind);
    const name = (state.result?.project_name || "codeflow").toLowerCase().replace(/[^a-z0-9]+/g, "-");
    const lang = state.result?.language;
    const map  = {
      review:        `${name}-review.txt`,
      fixed:         `${name}-fixed.${ext(lang)}`,
      optimized:     `${name}-optimized.${ext(lang)}`,
      explanation:   `${name}-explanation.md`,
      documentation: `${name}-README.md`,
    };
    downloadText(map[kind] || `${name}.txt`, c);
    return;
  }
  // Collapse toggle
  const toggle = e.target.closest(".rc-toggle");
  if (toggle) {
    toggle.closest(".result-card")?.classList.toggle("collapsed");
    return;
  }
});

$("collapseAllBtn")?.addEventListener("click", () => {
  const cards   = $$(".result-card");
  const anyOpen = cards.some(c => !c.classList.contains("collapsed"));
  cards.forEach(c => c.classList.toggle("collapsed", anyOpen));
  const btn = $("collapseAllBtn");
  if (btn) btn.textContent = anyOpen ? "Expand all" : "Collapse all";
});

/* ── Download PDF ───────────────────────────────────────── */
$("downloadPdfBtn")?.addEventListener("click", () => {
  const docs = getContent("documentation");
  if (!docs) { showToast("No documentation to export."); return; }
  const project = state.result?.project_name || "AI Code Documentation";
  const lang    = state.result?.language     || "Unknown";
  const win     = window.open("", "_blank", "width=900,height=1100");
  if (!win) { showToast("Allow popups to download PDF."); return; }

  const body = String(docs)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/^### (.*)$/gm, "<h3>$1</h3>")
    .replace(/^## (.*)$/gm,  "<h2>$1</h2>")
    .replace(/^# (.*)$/gm,   "<h1>$1</h1>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/^- (.*)$/gm, "<li>$1</li>")
    .replace(/\n/g, "<br>");

  win.document.write(`<!DOCTYPE html><html><head>
    <title>${esc(project)}</title>
    <style>
      @page{margin:22mm}
      body{color:#1d1207;font-family:Inter,Arial,sans-serif;line-height:1.7}
      h1{font-size:32px;margin-bottom:8px;color:#1a3a2a}
      h2{margin-top:28px;color:#2d6a4f}
      h3{margin-top:18px;color:#1a3a2a}
      .meta{color:#52796f;font-size:13px;margin-bottom:28px;border-bottom:2px solid #52b788;padding-bottom:14px}
      .footer{color:#52796f;font-size:12px;margin-top:36px;border-top:1px solid #d8f3dc;padding-top:12px}
      strong{color:#1a3a2a}li{margin-left:18px}
    </style>
  </head><body>
    <h1>${esc(project)}</h1>
    <div class="meta">Language: ${esc(lang)} · CodeFlow — AI Powered Coding Assistant</div>
    <main>${body}</main>
    <div class="footer">Generated by CodeFlow</div>
    <script>window.onload=()=>window.print()<\/script>
  </body></html>`);
  win.document.close();
});

/* ── INIT ───────────────────────────────────────────────── */
applyTheme();
updateSessionUi();
updateCharCounter();
renderResults();
showPage(state.token ? "dashboard" : "landing");
loadHistory();
checkGithubStatus();