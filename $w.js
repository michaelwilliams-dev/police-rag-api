$w.onReady(() => {
  console.log("✅ Page is ready");

  $w('#submitQueryButton').onClick(submitQueryButton_click);

  $w('#dropdownJobTitle').options = [
    { label: "CEO", value: "CEO" },
    { label: "Managing Director", value: "Managing Director" },
    { label: "Strategy Director", value: "Strategy Director" },
    { label: "Divisional Manager", value: "Divisional Manager" },
    { label: "HR Director", value: "HR Director" },
    { label: "Finance Director", value: "Finance Director" },
    { label: "Non-Executive Director", value: "Non-Executive Director" },
    { label: "Sales Director", value: "Sales Director" },
    { label: "Marketing Director", value: "Marketing Director" }
  ];
  $w('#dropdownJobTitle').selectedIndex = 0;

  $w('#dropdownFunnel1').options = [
    { label: "Phase 1 – Intelligence", value: "Intelligence" },
    { label: "Phase 2 – Planning", value: "Planning" },
    { label: "Phase 3 – Deployment", value: "Deployment" },
    { label: "Phase 4 – Execution", value: "Execution" },
    { label: "Phase 5 – After Action Review", value: "Review" }
  ];
  $w('#dropdownFunnel1').selectedIndex = 0;

  $w('#dropdownFunnel2').options = [
    { label: "Executive Thinking", value: "Executive" },
    { label: "Risk Posture", value: "Risk" },
    { label: "Operational Focus", value: "Ops" },
    { label: "Adaptive Strategy", value: "Adaptive" },
    { label: "Transformative Leadership", value: "Change" }
  ];
  $w('#dropdownFunnel2').selectedIndex = 0;

  $w('#dropdownFunnel3').options = [
    { label: "Cash Flow Crisis", value: "CashFlow" },
    { label: "Executive Turnover", value: "ExecExit" },
    { label: "Internal Political Battles", value: "Politics" },
    { label: "Toxic or Failing Management", value: "BadManagement" },
    { label: "Downsizing / Redundancy", value: "Layoffs" },
    { label: "Crisis Recovery / Catastrophe Plan", value: "DisasterPlan" },
    { label: "M&A / Restructuring Shock", value: "MergerShock" },
    { label: "Ethics Breakdown / Trust Collapse", value: "EthicsCrisis" },
    { label: "Shareholder Pressure", value: "Shareholder" }
  ];
  $w('#dropdownFunnel3').selectedIndex = 0;

  $w('#dropdownSearchType').options = [
    { label: "General Strategic Query", value: "general" },
    { label: "Urgent / Crisis Situation", value: "urgent" },
    { label: "Scenario-Based Planning", value: "scenario" },
    { label: "Competitive Intelligence", value: "competitive" },
    { label: "Compliance / Governance", value: "compliance" }
  ];
  $w('#dropdownSearchType').selectedIndex = 0;

  $w('#dropdownTimeline').options = [
    { label: "Immediate (0–30 days)", value: "immediate" },
    { label: "Short-Term (1–3 months)", value: "short" },
    { label: "Mid-Term (3–12 months)", value: "mid" },
    { label: "Long-Term (1–3 years)", value: "long" },
    { label: "Visionary (5+ years)", value: "vision" }
  ];
  $w('#dropdownTimeline').selectedIndex = 0;

  $w('#inputDiscipline').value = "Strategic Management";
  $w('#inputSourceContext').value = "This response is shaped by the strategic philosophies of Sun Tzu, Machiavelli, and Plato.";
  $w('#inputJobCode').value = 9999;
});

export function submitQueryButton_click(event) {
  console.log("🚀 Submit button clicked");

  const name = $w('#inputName').value;
  const email = $w('#inputEmail').value;
  const query = $w('#inputQuery').value;
  const jobTitle = $w('#dropdownJobTitle').value;
  const discipline = $w('#inputDiscipline').value;
  const searchType = $w('#dropdownSearchType').value;
  const timeline = $w('#dropdownTimeline').value;
  const site = $w('#inputSiteName').value;
  const bonusValue = $w('#dropdownBonus').value;
  const funnel1 = $w('#dropdownFunnel1').value;
  const funnel2 = $w('#dropdownFunnel2').value;
  const funnel3 = $w('#dropdownFunnel3').value;
  const supervisorName = $w('#inputSupervisorFullName').value;
  const supervisorEmail = $w('#inputSupervisorEmail').value;
  const hrEmail = $w('#inputHrEmail').value;
  const sourceContext = $w('#inputSourceContext').value;

  let jobCode = 9999;
  let requiresActionSheet = false;

  switch (jobTitle) {
    case "CEO":
    case "Managing Director":
    case "Strategy Director":
    case "Finance Director":
    case "Non-Executive Director":
    case "Sales Director":
    case "Marketing Director":
      jobCode = 1001;
      requiresActionSheet = true;
      break;
    case "HR Director":
      jobCode = 2001;
      requiresActionSheet = true;
      break;
    case "Divisional Manager":
      jobCode = 3001;
      requiresActionSheet = true;
      break;
    default:
      jobCode = 9999;
  }

  const payload = {
    full_name: name,
    email: email,
    query: query,
    job_title: jobTitle,
    discipline: discipline,
    search_type: searchType,
    timeline: timeline,
    site: site,
    funnel_1: funnel1,
    funnel_2: funnel2,
    funnel_3: funnel3,
    dropdown_bonus: bonusValue,
    job_code: jobCode,
    requires_action_sheet: requiresActionSheet,
    source_context: sourceContext,
    supervisor_email: supervisorEmail,
    supervisor_name: supervisorName,
    hr_email: hrEmail
  };

  console.log("📤 Payload:", payload);
  $w('#statusText').text = "⏳ Sending your query...";

  fetch("https://flask-deploy-final.onrender.com/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(result => {
      console.log("✅ API Response:", result);
      $w('#statusText').text = result.message || "✅ Your response has been emailed!";
    })
    .catch(err => {
      console.error("❌ Fetch Error:", err);
      $w('#statusText').text = "❌ Request failed: " + err.message;
    });
}