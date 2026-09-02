(() => {
  "use strict";

  const EVENT_NAME = "isq:knowledge-check-answered";
  const XAPI_VERSION = "1.0.3";
  const LANGUAGE = "en-AU";
  const RESPONSE_DELIMITER = "[,]";
  const ANSWERED_VERB = {
    id: "http://adlnet.gov/expapi/verbs/answered",
    display: { [LANGUAGE]: "answered" }
  };
  const CMI_INTERACTION = "http://adlnet.gov/expapi/activities/cmi.interaction";

  function isNonEmptyString(value) {
    return typeof value === "string" && value.trim().length > 0;
  }

  function uuidV4() {
    if (globalThis.crypto?.randomUUID) return globalThis.crypto.randomUUID();

    const bytes = new Uint8Array(16);
    globalThis.crypto?.getRandomValues?.(bytes);
    bytes[6] = (bytes[6] & 0x0f) | 0x40;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;

    return [...bytes].map((byte, index) => {
      const hex = byte.toString(16).padStart(2, "0");
      return [4, 6, 8, 10].includes(index) ? `-${hex}` : hex;
    }).join("");
  }

  function requireTelemetryMetadata(detail) {
    const required = [
      "activityId",
      "activityName",
      "parentActivityId",
      "groupingActivityId"
    ];

    return required.every(key => isNonEmptyString(detail?.[key]));
  }

  function encodeResponses(responseIds) {
    return responseIds.join(RESPONSE_DELIMITER);
  }

  function buildChoices(choices) {
    return choices.map(choice => ({
      id: choice.id,
      description: { [LANGUAGE]: choice.label }
    }));
  }

  function buildStatement(detail, actor, registration) {
    if (!requireTelemetryMetadata(detail)) {
      throw new Error("Knowledge Check telemetry metadata is incomplete.");
    }

    if (!actor || actor.objectType === "Group") {
      throw new Error("A trusted learner Agent is required for governed Knowledge Check telemetry.");
    }

    const correctPattern = encodeResponses(detail.correctResponseIds || []);
    const response = encodeResponses(detail.responseIds || []);

    const context = {
      contextActivities: {
        parent: [{ id: detail.parentActivityId, objectType: "Activity" }],
        grouping: [{ id: detail.groupingActivityId, objectType: "Activity" }]
      },
      extensions: {
        "https://isq.qld.edu.au/xapi/extensions/component-key": detail.component,
        "https://isq.qld.edu.au/xapi/extensions/component-version": detail.componentVersion,
        "https://isq.qld.edu.au/xapi/extensions/attempt-number": detail.attemptNumber
      }
    };

    if (isNonEmptyString(registration)) context.registration = registration;

    const definition = {
      type: CMI_INTERACTION,
      name: { [LANGUAGE]: detail.activityName },
      interactionType: "choice",
      correctResponsesPattern: [correctPattern],
      choices: buildChoices(detail.choices || [])
    };

    if (isNonEmptyString(detail.activityDescription)) {
      definition.description = { [LANGUAGE]: detail.activityDescription };
    }

    return {
      id: uuidV4(),
      actor,
      verb: ANSWERED_VERB,
      object: {
        id: detail.activityId,
        objectType: "Activity",
        definition
      },
      result: {
        response,
        success: Boolean(detail.success),
        completion: true
      },
      context,
      timestamp: new Date().toISOString()
    };
  }

  function emitStatus(target, status, detail = {}) {
    target.dispatchEvent(new CustomEvent("isq:telemetry-status", {
      bubbles: true,
      detail: { status, ...detail }
    }));
  }

  async function handleAnswered(event) {
    const detail = event.detail;
    if (!detail || !requireTelemetryMetadata(detail)) return;

    const runtime = globalThis.ISQ_XAPI_RUNTIME;
    if (!runtime || typeof runtime.getActor !== "function" || typeof runtime.sendStatement !== "function") {
      emitStatus(event.target, "unavailable", { component: detail.component });
      return;
    }

    try {
      const actor = await runtime.getActor();
      if (!actor) {
        emitStatus(event.target, "identity-unavailable", { component: detail.component });
        return;
      }

      const registration = typeof runtime.getRegistration === "function"
        ? await runtime.getRegistration()
        : null;

      const statement = buildStatement(detail, actor, registration);
      await runtime.sendStatement(statement, {
        xapiVersion: XAPI_VERSION,
        idempotencyKey: statement.id
      });

      emitStatus(event.target, "sent", {
        component: detail.component,
        statementId: statement.id
      });
    } catch (error) {
      console.error("[ISQ xAPI] Knowledge Check telemetry failed.", error);
      emitStatus(event.target, "failed", {
        component: detail?.component,
        message: error?.message || "Unknown telemetry error"
      });
    }
  }

  globalThis.ISQKnowledgeCheckXAPI = Object.freeze({
    buildStatement,
    encodeResponses,
    version: "0.1.0"
  });

  document.addEventListener(EVENT_NAME, handleAnswered);
})();
