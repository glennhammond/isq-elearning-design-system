(() => {
  "use strict";

  const CONTRACT_VERSION = "0.1.0";
  const COMPONENT_VERSION = "0.1.0";

  function parseIds(value) {
    return String(value || "")
      .split(",")
      .map(item => item.trim())
      .filter(Boolean);
  }

  function clearFeedback(feedback) {
    feedback.classList.remove(
      "isq-callout--success",
      "isq-callout--warning",
      "isq-callout--error"
    );
  }

  function sameSet(left, right) {
    if (left.length !== right.length) return false;
    const rightSet = new Set(right);
    return left.every(item => rightSet.has(item));
  }

  function selectedInputs(question) {
    return [
      ...question.querySelectorAll(
        '.isq-options input[type="radio"]:checked, .isq-options input[type="checkbox"]:checked'
      )
    ];
  }

  function choiceRegister(question) {
    return [
      ...question.querySelectorAll(
        '.isq-options input[type="radio"], .isq-options input[type="checkbox"]'
      )
    ].map(input => ({
      id: input.value,
      label: input.closest("label")?.innerText.trim() || input.value
    }));
  }

  function emitAnswered(root, question, responseIds, correctIds, success, attemptNumber) {
    const detail = {
      contractVersion: CONTRACT_VERSION,
      component: root.dataset.component || "isq-kc-single",
      componentVersion: COMPONENT_VERSION,
      questionKey: question.dataset.questionKey,
      activityId: question.dataset.activityId || null,
      parentActivityId: question.dataset.parentActivityId || root.dataset.parentActivityId || null,
      groupingActivityId: question.dataset.groupingActivityId || root.dataset.groupingActivityId || null,
      interactionType: "choice",
      responseIds,
      correctResponseIds: correctIds,
      success,
      completion: true,
      attemptNumber,
      choices: choiceRegister(question)
    };

    root.dispatchEvent(new CustomEvent("isq:knowledge-check-answered", {
      bubbles: true,
      detail
    }));
  }

  function showQuestion(root, key, moveFocus = false) {
    const questions = [...root.querySelectorAll("[data-kc-question]")];
    const nav = [...root.querySelectorAll("[data-kc-nav]")];

    questions.forEach(question => {
      const active = question.dataset.questionKey === key;
      question.hidden = !active;
      question.classList.toggle("is-active", active);

      if (active && moveFocus) {
        const heading = question.querySelector("h2, h3, legend, input, button");
        if (heading && !heading.matches("input, button")) {
          heading.setAttribute("tabindex", "-1");
        }
        heading?.focus();
      }
    });

    nav.forEach(button => {
      const active = button.dataset.kcNav === key;
      button.setAttribute("aria-current", active ? "step" : "false");
    });
  }

  function initialise(root) {
    if (root.dataset.initialised === "true") return;
    root.dataset.initialised = "true";

    const attempts = {};

    root.querySelectorAll("[data-kc-question]").forEach(question => {
      const key = question.dataset.questionKey;
      const checkButton = question.querySelector("[data-kc-check]");
      const feedback = question.querySelector("[data-kc-feedback]");
      const nextButton = question.querySelector("[data-kc-next]");

      if (!key || !checkButton || !feedback) return;
      attempts[key] = 0;

      checkButton.addEventListener("click", () => {
        const selected = selectedInputs(question);
        const correctIds = parseIds(question.dataset.correctResponses);

        clearFeedback(feedback);
        feedback.hidden = false;

        if (selected.length === 0) {
          feedback.classList.add("isq-callout--warning");
          feedback.innerHTML =
            '<p class="isq-body isq-body--strong">Select an answer.</p>' +
            '<p class="isq-body">Choose the best response, then check your answer.</p>';
          if (nextButton) nextButton.hidden = true;
          return;
        }

        const responseIds = selected.map(input => input.value);
        const success = sameSet(responseIds, correctIds);
        attempts[key] += 1;

        feedback.classList.add(success ? "isq-callout--success" : "isq-callout--error");
        feedback.innerHTML = success
          ? question.dataset.correctFeedback
          : question.dataset.incorrectFeedback;

        if (nextButton) nextButton.hidden = !success;

        emitAnswered(root, question, responseIds, correctIds, success, attempts[key]);
      });

      nextButton?.addEventListener("click", () => {
        showQuestion(root, nextButton.dataset.kcNext, true);
      });
    });

    root.querySelectorAll("[data-kc-nav]").forEach(button => {
      button.addEventListener("click", () => showQuestion(root, button.dataset.kcNav, true));
    });
  }

  function initialiseAll() {
    document.querySelectorAll("[data-isq-knowledge-check]").forEach(initialise);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialiseAll, { once: true });
  } else {
    initialiseAll();
  }
})();