(() => {
  const storageKey = "netsafeit-cookie-policy-choice";
  const banner = document.createElement("aside");
  banner.className = "cookie-notice";
  banner.setAttribute("role", "region");
  banner.setAttribute("aria-label", "Cookie policy notice");
  banner.hidden = true;

  const content = document.createElement("div");
  content.className = "cookie-notice-inner";

  const message = document.createElement("p");
  message.append("Do you accept our Cookie Policy? We do not set cookies. Your choice is saved in this browser so we do not ask again. ");
  const policyLink = document.createElement("a");
  policyLink.href = "/cookie-policy.html";
  policyLink.textContent = "Read the policy";
  message.append(policyLink);
  content.append(message);

  const actions = document.createElement("div");
  actions.className = "cookie-notice-actions";

  function saveChoice(choice) {
    try {
      localStorage.setItem(storageKey, choice);
    } catch {
      // Keep the choice for this page view if browser storage is unavailable.
    }
    banner.hidden = true;
  }

  for (const choice of ["accepted", "declined"]) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = choice === "accepted" ? "button button-small" : "button button-small button-ghost";
    button.textContent = choice === "accepted" ? "Accept" : "Decline";
    button.addEventListener("click", () => saveChoice(choice));
    actions.append(button);
  }

  content.append(actions);
  banner.append(content);
  document.body.append(banner);

  let savedChoice;
  try {
    savedChoice = localStorage.getItem(storageKey);
  } catch {
    savedChoice = null;
  }
  banner.hidden = savedChoice === "accepted" || savedChoice === "declined";

  const footerLinks = document.querySelector(".footer-links");
  if (footerLinks) {
    const settingsItem = document.createElement("li");
    const settingsLink = document.createElement("a");
    settingsLink.href = "/cookie-policy.html";
    settingsLink.textContent = "Cookie settings";
    settingsLink.addEventListener("click", (event) => {
      event.preventDefault();
      banner.hidden = false;
      actions.querySelector("button").focus();
    });
    settingsItem.append(settingsLink);
    footerLinks.append(settingsItem);
  }
})();