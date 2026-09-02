(() => {
  "use strict";

  const CONFIG = globalThis.ISQ_XAPI_TEST_CONFIG || {};
  const DEFAULT_ENDPOINT = "https://lrs2.isq.qld.edu.au/glenn-testing/xapi/";
  const XAPI_VERSION = "1.0.3";

  function log(stage, detail) {
    console.log(`[ISQ xAPI test runtime] ${stage}`, detail ?? "");
    document.dispatchEvent(new CustomEvent("isq:test-runtime-status", {
      detail: { stage, detail }
    }));
  }

  function findAPI(propName) {
    const seen = [];
    let current = window;
    let guard = 0;

    while (current && guard++ < 12) {
      seen.push(current);
      if (current.parent === current) break;
      try { current = current.parent; } catch (_) { break; }
    }

    for (const candidate of seen) {
      try {
        if (candidate[propName]) return candidate[propName];
      } catch (_) {}
    }

    return null;
  }

  function tidyName(name) {
    if (!name) return null;
    let value = String(name).trim();
    if (value.includes(",")) {
      const parts = value.split(",");
      value = `${(parts[1] || "").trim()} ${(parts[0] || "").trim()}`.trim();
    }
    return value.replace(/\s+/g, " ").trim() || null;
  }

  function actorFromLearner(id, name) {
    const cleanId = String(id || "").trim();
    const cleanName = tidyName(name) || cleanId;
    if (!cleanId) return null;

    if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(cleanId)) {
      return { objectType: "Agent", name: cleanName, mbox: `mailto:${cleanId}` };
    }

    return {
      objectType: "Agent",
      name: cleanName,
      account: {
        homePage: window.location.origin || "https://isq.qld.edu.au",
        name: cleanId
      }
    };
  }

  function readScormLearner() {
    const api2004 = findAPI("API_1484_11");
    if (api2004 && typeof api2004.GetValue === "function") {
      try {
        const id = api2004.GetValue("cmi.learner_id");
        const name = api2004.GetValue("cmi.learner_name");
        if (id || name) return { id, name, version: "2004" };
      } catch (error) {
        log("SCORM 2004 read failed", error?.message || error);
      }
    }

    const api12 = findAPI("API");
    if (api12 && typeof api12.LMSGetValue === "function") {
      try {
        const id = api12.LMSGetValue("cmi.core.student_id");
        const name = api12.LMSGetValue("cmi.core.student_name");
        if (id || name) return { id, name, version: "1.2" };
      } catch (error) {
        log("SCORM 1.2 read failed", error?.message || error);
      }
    }

    return null;
  }

  async function getActor() {
    for (let attempt = 0; attempt <= 8; attempt += 1) {
      const learner = readScormLearner();
      if (learner) {
        const actor = actorFromLearner(learner.id, learner.name);
        log(`actor resolved via SCORM ${learner.version}`, actor);
        return actor;
      }
      await new Promise(resolve => setTimeout(resolve, 300));
    }

    log("actor unavailable");
    return null;
  }

  async function getRegistration() {
    const api2004 = findAPI("API_1484_11");
    if (!api2004 || typeof api2004.GetValue !== "function") return null;

    try {
      const value = api2004.GetValue("cmi.entry");
      log("registration not derived from SCORM entry", value || "none");
    } catch (_) {}

    return null;
  }

  function sendStatement(statement) {
    const endpoint = String(CONFIG.endpoint || DEFAULT_ENDPOINT).replace(/\/+$/, "");
    const auth = CONFIG.auth;

    if (!auth || !/^Basic\s+\S+/i.test(auth)) {
      return Promise.reject(new Error("ISQ_XAPI_TEST_CONFIG.auth is missing. Supply the controlled test Basic credential for qualification only."));
    }

    log("transport attempt", { endpoint: `${endpoint}/statements`, statementId: statement.id });

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open("POST", `${endpoint}/statements`, true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.setRequestHeader("X-Experience-API-Version", XAPI_VERSION);
      xhr.setRequestHeader("Authorization", auth);

      xhr.onreadystatechange = () => {
        if (xhr.readyState !== 4) return;

        if (xhr.status >= 200 && xhr.status < 300) {
          log("LRS accepted statement", { status: xhr.status, statementId: statement.id });
          resolve({ status: xhr.status, statementId: statement.id });
        } else {
          const error = new Error(`LRS returned HTTP ${xhr.status}.`);
          log("LRS rejected statement", { status: xhr.status, body: xhr.responseText });
          reject(error);
        }
      };

      xhr.onerror = () => {
        const error = new Error("Network/CORS failure while sending xAPI statement.");
        log("transport network failure", error.message);
        reject(error);
      };

      xhr.send(JSON.stringify(statement));
    });
  }

  globalThis.ISQ_XAPI_RUNTIME = Object.freeze({
    getActor,
    getRegistration,
    sendStatement,
    version: "0.1.0-test"
  });

  log("runtime ready", { endpoint: CONFIG.endpoint || DEFAULT_ENDPOINT });
})();
