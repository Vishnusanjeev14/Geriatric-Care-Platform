document.documentElement.classList.add("js-enabled");

const tamilDictionary = {
  "CareConnect": "கேர்கனெக்ட்",
  "Dashboard": "டாஷ்போர்ட",
  "Medicines": "மருந்துகள்",
  "Medicine": "மருந்து",
  "Hospitals": "மருத்துவமனைகள்",
  "Hospital": "மருத்துவமனை",
  "Caretaker": "கெயர்டேக்கர்",
  "Home Services": "வீட்டு சேவைகள்",
  "Home": "முகப்பு",
  "Family": "குடும்பம்",
  "Reports": "ரிப்போர்ட்கள்",
  "Settings": "அமைப்புகள்",
  "Inventory": "செட்டிங்ஸ்",
  "Orders": "ஆர்டர்கள்",
  "Calendar": "காலண்டர்",
  "Visits": "வருகைகள்",
  "Select Profile": "ப்ரொபைல் தேர்வு",
  "Add Profile": "ப்ரொபைல் சேர்",
  "Edit Profile": "ப்ரொபைல் திருத்து",
  "Emergency Information": "அவசர தகவல்",
  "Logout": "வெளியேறு",
  "Login": "உள்நுழை",
  "Signup": "பதிவு செய்",
  "Create account": "கணக்கு உருவாக்கு",
  "Forgot password?": "பச்ச்வோர்து மறந்துவிட்டதா?",
  "Email": "ஈமெயில்",
  "Password": "பச்ச்வோர்து",
  "Welcome back": "மீண்டும் வரவேற்கிறோம்",
  "Sign into your care workspace.": "உங்கள் பராமரிப்பு பணியிடத்தில் உள்நுழைக.",
  "Demo credentials": "டெமோ உள்நுழைவு விவரங்கள்",
  "Profile": "ப்ரொபைல்",
  "Select who you are caring for.": "நீங்கள் யாரை பராமரிக்கிறீர்கள் என்பதை தேர்வு செய்யுங்கள்.",
  "Add New Profile": "புதிய ப்ரொபைல் சேர்",
  "Managing": "நிர்வகிப்பு",
  "Emergency card": "அவசர அட்டை",
  "Timeline": "காலவரிசை",
  "Edit profile": "ப்ரொபைல் திருத்து",
  "Adherence today": "இன்றைய பின்பற்றல்",
  "Due today": "இன்று நிலுவை",
  "Appointments": "சந்திப்புகள்",
  "Today's medicines": "இன்றைய மருந்துகள்",
  "Upcoming appointment": "வரவிருக்கும் சந்திப்பு",
  "Current caretaker": "தற்போதைய பராமரிப்பாளர்",
  "Health summary": "ஆரோக்கிய சுருக்கம்",
  "Quick actions": "விரைவு செயல்கள்",
  "Recent timeline": "சமீபத்திய காலவரிசை",
  "Open medicine schedule": "மருந்து அட்டவணையைத் திற",
  "Find hospitals": "மருத்துவமனைகள் தேடு",
  "Open care requests": "பராமரிப்பு கோரிக்கைகள் திற",
  "Order medicines": "மருந்துகள் ஆர்டர் செய்",
  "Book appointment": "சந்திப்பு பதிவு செய்",
  "Upload prescription": "மருந்துச் சீட்டு பதிவேற்று",
  "Request caretaker": "பராமரிப்பாளர் கோரிக்கை",
  "No medicines scheduled.": "மருந்துகள் திட்டமிடப்படவில்லை.",
  "No appointments.": "சந்திப்புகள் இல்லை.",
  "No active caretaker.": "செயலில் உள்ள பராமரிப்பாளர் இல்லை.",
  "No timeline events yet.": "காலவரிசை நிகழ்வுகள் இன்னும் இல்லை.",
  "Pharmacy": "மருந்தகம்",
  "Find medicines with confidence.": "நம்பிக்கையுடன் மருந்துகளைத் தேடுங்கள்.",
  "Search": "தேடு",
  "All categories": "அனைத்து வகைகள்",
  "Review cart": "கார்ட்டைப் பார்வையிடு",
  "Add to cart": "கார்ட்டில் சேர்",
  "Add to profile schedule": "சுயவிவர அட்டவணையில் சேர்",
  "Quantity": "அளவு",
  "Unit": "அலகு",
  "Tablets": "மாத்திரைகள்",
  "Capsules": "கேப்சூல்கள்",
  "Sheets / Strips": "ஷீட் / ஸ்ட்ரிப்",
  "Boxes": "பெட்டிகள்",
  "Bottles": "பாட்டில்கள்",
  "Stock": "கையிருப்பு",
  "No medicines found": "மருந்துகள் கிடைக்கவில்லை",
  "Prescription OCR": "மருந்துச் சீட்டு OCR",
  "OCR workflow": "OCR செயல்முறை",
  "Upload prescription": "மருந்துச் சீட்டு பதிவேற்று",
  "Printed prescriptions only": "அச்சிடப்பட்ட மருந்துச் சீட்டுகள் மட்டும்",
  "Upload and process OCR": "பதிவேற்றி OCR செய்",
  "Recent prescriptions": "சமீபத்திய மருந்துச் சீட்டுகள்",
  "No prescriptions uploaded.": "மருந்துச் சீட்டுகள் பதிவேற்றப்படவில்லை.",
  "Manual review": "கையேடு சரிபார்ப்பு",
  "Review recognized medicines.": "அடையாளம் காணப்பட்ட மருந்துகளைச் சரிபார்.",
  "Matched medicines": "பொருந்திய மருந்துகள்",
  "Unmatched text": "பொருந்தாத உரை",
  "Manual correction": "கையேடு திருத்தம்",
  "Everything was matched.": "அனைத்தும் பொருந்தியது.",
  "Add matched medicines to cart": "பொருந்திய மருந்துகளை கார்ட்டில் சேர்",
  "Care Assistant": "பராமரிப்பு உதவியாளர்",
  "Run": "இயக்கு",
  "Speak": "பேசு",
  "Open navigation": "வழிசெலுத்தலைத் திற",
  "Close navigation": "வழிசெலுத்தலை மூடு",
  "Open account menu": "கணக்கு மெனுவைத் திற",
  "Switch language": "மொழியை மாற்று",
  "Toggle light and dark mode": "ஒளி/இருள் முறையை மாற்று",
  "Light": "ஒளி",
  "Dark": "இருள்",
  "English": "English",
  "Tamil": "தமிழ்",
  "Paracetamol": "பாராசிட்டமால்",
  "Metformin": "மெட்ஃபார்மின்",
  "Aspirin": "ஆஸ்பிரின்",
  "Amoxicillin": "அமோக்சிசிலின்",
  "Azithromycin": "அசித்ரோமைசின்",
  "Amlodipine": "அம்லோடிபைன்",
  "Atorvastatin": "அட்டோர்வாஸ்டாட்டின்",
  "Losartan": "லோசார்டன்",
  "Omeprazole": "ஓமேப்ரசோல்",
  "Pantoprazole": "பாண்டோப்ரசோல்",
  "Cetirizine": "செடிரிசின்",
  "Loratadine": "லோரடடின்",
  "Salbutamol": "சால்புடமால்",
  "Montelukast": "மொன்டெலுகாஸ்ட்",
  "Levothyroxine": "லெவோதைரோக்சின்",
  "Vitamin D3": "வைட்டமின் D3",
  "Calcium Citrate": "கால்சியம் சிட்ரேட்",
  "Ferrous Sulfate": "ஃபெரஸ் சல்பேட்",
  "Insulin Glargine": "இன்சுலின் கிளார்ஜின்",
  "Ibuprofen": "ஐபுபுரோஃபென்",
};

const translationEntries = Object.entries(tamilDictionary).sort((a, b) => b[0].length - a[0].length);
const originalTextNodes = new WeakMap();
const originalAttributes = new WeakMap();
const translatableAttributes = ["placeholder", "aria-label", "title"];

function translateText(value, language) {
  if (language !== "ta" || !value) return value;
  let translated = value;
  translationEntries.forEach(([english, tamil]) => {
    translated = translated.replaceAll(english, tamil);
  });
  return translated;
}

function applyLanguage(language) {
  document.documentElement.dataset.language = language;
  document.documentElement.lang = language === "ta" ? "ta" : "en";
  localStorage.setItem("careconnect-language", language);
  document.title = translateText(document.documentElement.dataset.originalTitle || document.title, language);
  document.querySelectorAll("[data-language-toggle]").forEach((button) => {
    button.textContent = language === "ta" ? "English" : "தமிழ்";
  });
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      if (node.parentElement?.closest("script, style, textarea, [data-no-translate]")) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    },
  });
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach((node) => {
    if (!originalTextNodes.has(node)) originalTextNodes.set(node, node.nodeValue);
    node.nodeValue = translateText(originalTextNodes.get(node), language);
  });
  document.querySelectorAll("input, button, a, select, textarea").forEach((element) => {
    translatableAttributes.forEach((attribute) => {
      if (!element.hasAttribute(attribute)) return;
      if (!originalAttributes.has(element)) originalAttributes.set(element, {});
      const originals = originalAttributes.get(element);
      if (!Object.prototype.hasOwnProperty.call(originals, attribute)) originals[attribute] = element.getAttribute(attribute);
      element.setAttribute(attribute, translateText(originals[attribute], language));
    });
  });
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("careconnect-theme", theme);
  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.textContent = theme === "dark" ? "Light" : "Dark";
    button.setAttribute("aria-pressed", String(theme === "dark"));
  });
}

document.documentElement.dataset.originalTitle = document.title;
applyTheme(localStorage.getItem("careconnect-theme") || document.documentElement.dataset.theme || "dark");
applyLanguage(localStorage.getItem("careconnect-language") || document.documentElement.dataset.language || "en");

document.querySelectorAll("[data-language-toggle]").forEach((button) => {
  button.addEventListener("click", () => {
    applyLanguage(document.documentElement.dataset.language === "ta" ? "en" : "ta");
  });
});

document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
  button.addEventListener("click", () => {
    applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
  });
});

const switcher = document.querySelector("[data-profile-switcher]");
if (switcher) {
  switcher.addEventListener("change", () => {
    window.location.href = switcher.value;
  });
}

const sidebar = document.querySelector("[data-sidebar]");
const sidebarBackdrop = document.querySelector("[data-sidebar-backdrop]");
const sidebarToggle = document.querySelector("[data-sidebar-toggle]");
const sidebarClose = document.querySelector("[data-sidebar-close]");
let sidebarCloseTimer = null;

function setSidebar(open) {
  if (!sidebar || !sidebarBackdrop) return;
  window.clearTimeout(sidebarCloseTimer);
  sidebar.hidden = false;
  sidebarBackdrop.hidden = false;
  sidebarToggle?.setAttribute("aria-expanded", String(open));
  requestAnimationFrame(() => {
    sidebar.classList.toggle("is-open", open);
    sidebarBackdrop.classList.toggle("is-open", open);
  });
  if (!open) {
    sidebarCloseTimer = window.setTimeout(() => {
      sidebar.hidden = true;
      sidebarBackdrop.hidden = true;
    }, 230);
  }
}

sidebarToggle?.setAttribute("aria-expanded", "false");
sidebarToggle?.addEventListener("click", () => setSidebar(!sidebar?.classList.contains("is-open")));
sidebarClose?.addEventListener("click", () => setSidebar(false));
sidebarBackdrop?.addEventListener("click", () => setSidebar(false));
document.querySelectorAll("[data-nav-link]").forEach((link) => {
  link.addEventListener("click", () => setSidebar(false));
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setSidebar(false);
    if (accountMenu) accountMenu.hidden = true;
  }
});

const accountMenuToggle = document.querySelector("[data-account-menu-toggle]");
const accountMenu = document.querySelector("[data-account-menu]");
accountMenuToggle?.addEventListener("click", () => {
  accountMenu.hidden = !accountMenu.hidden;
});
document.addEventListener("click", (event) => {
  if (!accountMenu || !accountMenuToggle) return;
  if (!accountMenu.hidden && !accountMenu.contains(event.target) && !accountMenuToggle.contains(event.target)) {
    accountMenu.hidden = true;
  }
});

const largeTextButton = document.querySelector("[data-large-text]");
const contrastButton = document.querySelector("[data-contrast]");
const storedLargeText = localStorage.getItem("careconnect-large-text") === "true";
const storedContrast = localStorage.getItem("careconnect-high-contrast") === "true";
document.body.classList.toggle("large-text", storedLargeText);
document.body.classList.toggle("high-contrast", storedContrast);

largeTextButton?.addEventListener("click", () => {
  document.body.classList.toggle("large-text");
  localStorage.setItem("careconnect-large-text", document.body.classList.contains("large-text"));
});

contrastButton?.addEventListener("click", () => {
  document.body.classList.toggle("high-contrast");
  localStorage.setItem("careconnect-high-contrast", document.body.classList.contains("high-contrast"));
});

const assistantPanel = document.querySelector("[data-assistant-panel]");
const assistantToggle = document.querySelector("[data-assistant-toggle]");
const assistantClose = document.querySelector("[data-assistant-close]");
const assistantForm = document.querySelector("[data-assistant-form]");
const assistantInput = document.querySelector("[data-assistant-input]");
const assistantStatus = document.querySelector("[data-assistant-status]");
const assistantMic = document.querySelector("[data-assistant-mic]");

function setAssistantStatus(message) {
  if (!assistantStatus || !assistantPanel) return;
  assistantPanel.hidden = false;
  assistantStatus.textContent = message;
}

function toggleAssistant(open) {
  if (!assistantPanel || !assistantToggle) return;
  assistantPanel.hidden = !open;
  assistantToggle.setAttribute("aria-expanded", String(open));
  if (open) assistantInput?.focus();
}

assistantToggle?.setAttribute("aria-expanded", "false");
assistantToggle?.addEventListener("click", () => toggleAssistant(assistantPanel?.hidden));
assistantClose?.addEventListener("click", () => toggleAssistant(false));

function normalizeCommand(value) {
  return value
    .toLowerCase()
    .replace(/[^\w\s]/g, " ")
    .replace(/\bmeds\b/g, "medicines")
    .replace(/\bchemist\b/g, "pharmacy")
    .replace(/\bdoctor\b/g, "hospital")
    .replace(/\bto\b/g, "two")
    .replace(/\s+/g, " ")
    .trim();
}

function includesAny(text, phrases) {
  return phrases.some((phrase) => text.includes(phrase));
}

function activeDashboardRoute() {
  return document.querySelector("[data-nav-link][href*='/dashboard']")?.getAttribute("href")
    || document.querySelector("[data-nav-link][href*='/workspace']")?.getAttribute("href")
    || "/family/workspace";
}

function routeForCommand(text) {
  const directRoutes = {
    dashboard: activeDashboardRoute(),
    home: activeDashboardRoute(),
    pharmacy: "/pharmacy/",
    medicines: "/pharmacy/",
    medicine: "/pharmacy/",
    hospitals: "/hospitals/",
    hospital: "/hospitals/",
    caretaker: "/care/",
    care: "/care/",
    services: "/home-services/",
    family: "/family/view",
    reports: document.querySelector("[data-nav-link][href*='/timeline']")?.getAttribute("href") || activeDashboardRoute(),
    cart: "/pharmacy/cart",
  };
  if (directRoutes[text]) return directRoutes[text];
  if (includesAny(text, ["open dashboard", "show dashboard", "go dashboard"])) return activeDashboardRoute();
  if (includesAny(text, ["open pharmacy", "show pharmacy", "open medicines", "show medicines"])) return "/pharmacy/";
  if (includesAny(text, ["open hospitals", "show hospitals", "open hospital"])) return "/hospitals/";
  if (includesAny(text, ["open caretaker", "open care requests", "show care requests"])) return "/care/";
  if (includesAny(text, ["open home services", "show home services"])) return "/home-services/";
  if (includesAny(text, ["open family", "show family"])) return "/family/view";
  if (includesAny(text, ["open cart", "show cart", "view cart"])) return "/pharmacy/cart";
  if (includesAny(text, ["open reports", "show reports", "open timeline"])) return directRoutes.reports;
  return null;
}

const commandWords = new Set([
  "add", "put", "place", "search", "find", "show", "remove", "delete", "clear", "open", "order", "medicine", "medicines",
  "one", "won", "two", "too", "three", "four", "for", "five", "six", "seven", "eight", "nine", "ten",
  "tablet", "tablets", "capsule", "capsules", "sheet", "sheets", "strip", "strips", "box", "boxes", "bottle", "bottles",
  "of", "the", "a", "an", "cart", "please", "me", "some", "pack", "packs"
]);

function medicineTokens(value) {
  return normalizeCommand(value)
    .split(/\s+/)
    .filter((word) => word.length > 1 && !commandWords.has(word) && !/^\d+$/.test(word));
}

function quantityFrom(text) {
  const words = { one: 1, won: 1, two: 2, too: 2, three: 3, four: 4, for: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10 };
  const digit = text.match(/\b\d+\b/);
  if (digit) return Number(digit[0]);
  const match = Object.keys(words).find((word) => text.includes(word));
  return match ? words[match] : 1;
}

function unitFrom(text) {
  if (text.includes("capsule")) return "Capsules";
  if (text.includes("sheet") || text.includes("strip")) return "Sheets / Strips";
  if (text.includes("box")) return "Boxes";
  if (text.includes("bottle")) return "Bottles";
  return "Tablets";
}

function spokenMedicine(text) {
  const match = text.match(/\b(?:add|put|place|search|find|show|remove|delete)\b(?:\s+\w+){0,5}?\s+(?:of\s+)?(.+)$/);
  const raw = match ? match[1] : text;
  return raw
    .split(/\s+/)
    .filter((word) => !commandWords.has(word) && !/^\d+$/.test(word))
    .join(" ")
    .trim();
}

function visibleMedicineMatch(medicine) {
  const terms = medicineTokens(medicine);
  if (!terms.length) return null;
  return Array.from(document.querySelectorAll("[data-medicine-card]"))
    .map((card) => {
      const haystack = `${card.dataset.medicineName || ""} ${card.dataset.genericName || ""}`;
      const tokens = medicineTokens(haystack);
      const score = terms.filter((term) => tokens.some((token) => token.includes(term) || term.includes(token))).length;
      return { card, score };
    })
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score)[0]?.card || null;
}

function submitClosestForm(element) {
  const form = element?.closest("form") || element;
  if (!form) return false;
  if (typeof form.requestSubmit === "function") form.requestSubmit();
  else form.submit();
  return true;
}

function runPharmacySearch(medicine) {
  const searchInput = document.querySelector("[data-pharmacy-search]");
  const searchForm = document.querySelector("[data-pharmacy-search-form]");
  if (!searchInput || !searchForm) return false;
  searchInput.value = medicine;
  submitClosestForm(searchForm);
  return true;
}

function addVisibleMedicine(text, medicine) {
  const card = visibleMedicineMatch(medicine);
  if (!card) return false;
  card.scrollIntoView({ behavior: "smooth", block: "center" });
  card.classList.add("is-assistant-target");
  card.querySelector("[data-cart-quantity]").value = quantityFrom(text);
  card.querySelector("[data-cart-unit]").value = unitFrom(text);
  const label = card.querySelector("h2")?.textContent?.trim() || medicine;
  if (!window.confirm(`Add ${quantityFrom(text)} ${unitFrom(text).toLowerCase()} of ${label} to cart?`)) return true;
  submitClosestForm(card.querySelector("[data-add-cart-form]"));
  return true;
}

function removeVisibleMedicine(medicine) {
  const terms = medicineTokens(medicine);
  const form = Array.from(document.querySelectorAll("[data-remove-medicine]")).find((item) => {
    const tokens = medicineTokens(item.dataset.removeMedicine || "");
    return terms.some((term) => tokens.some((token) => token.includes(term) || term.includes(token)));
  });
  if (!form) return false;
  if (!window.confirm(`Remove ${medicine} from cart?`)) return true;
  submitClosestForm(form);
  return true;
}

function goToPharmacyWithCommand(command, medicine) {
  sessionStorage.setItem("careconnect-pending-assistant-command", command);
  window.location.href = `/pharmacy/?q=${encodeURIComponent(medicine)}`;
}

function handleMedicineCommand(rawCommand, text) {
  const medicine = spokenMedicine(text);
  if (!medicine && !includesAny(text, ["clear cart", "empty cart", "order medicines", "place order", "checkout"])) return false;

  if (includesAny(text, ["search", "find", "show"]) && medicine) {
    if (runPharmacySearch(medicine)) {
      setAssistantStatus(`Searching for ${medicine}.`);
      return true;
    }
    window.location.href = `/pharmacy/?q=${encodeURIComponent(medicine)}`;
    return true;
  }

  if (includesAny(text, ["add", "put", "place"]) && medicine) {
    if (addVisibleMedicine(text, medicine)) {
      setAssistantStatus(`Preparing ${medicine}.`);
      return true;
    }
    const searchInput = document.querySelector("[data-pharmacy-search]");
    if (searchInput) {
      if (normalizeCommand(searchInput.value || "") !== normalizeCommand(medicine)) {
        runPharmacySearch(medicine);
      } else {
        setAssistantStatus(`I could not find a visible medicine match for "${medicine}".`);
      }
      return true;
    }
    goToPharmacyWithCommand(rawCommand, medicine);
    return true;
  }

  if (includesAny(text, ["remove", "delete"]) && medicine) {
    if (removeVisibleMedicine(medicine)) return true;
    if (document.querySelector("[data-clear-cart-form]")) {
      setAssistantStatus(`I could not find "${medicine}" in the cart.`);
      return true;
    }
    sessionStorage.setItem("careconnect-pending-assistant-command", rawCommand);
    window.location.href = "/pharmacy/cart";
    return true;
  }

  if (includesAny(text, ["clear cart", "empty cart"])) {
    const form = document.querySelector("[data-clear-cart-form]");
    if (form) {
      if (window.confirm("Clear the cart?")) submitClosestForm(form);
      return true;
    }
    window.location.href = "/pharmacy/cart";
    return true;
  }

  if (includesAny(text, ["order medicines", "place order", "checkout"])) {
    const form = document.querySelector("[data-order-form]");
    if (form) {
      if (window.confirm("Place this medicine order?")) submitClosestForm(form);
      return true;
    }
    window.location.href = "/pharmacy/cart";
    return true;
  }
  return false;
}

function handleHospitalCommand(text) {
  if (!document.querySelector("[data-hospital-card]")) return false;
  if (!includesAny(text, ["first hospital", "second hospital"])) return false;
  const index = includesAny(text, ["second hospital", "number two hospital"]) ? 1 : 0;
  const card = document.querySelectorAll("[data-hospital-card]")[index];
  if (!card) return false;
  card.scrollIntoView({ behavior: "smooth", block: "center" });
  card.classList.add("is-assistant-target");
  setAssistantStatus("Opened the hospital record.");
  return true;
}

function runAssistantCommand(command) {
  const rawCommand = command.trim();
  const text = normalizeCommand(rawCommand);
  if (!text) return;
  if (assistantInput) assistantInput.value = rawCommand;
  if (handleHospitalCommand(text)) return;
  if (handleMedicineCommand(rawCommand, text)) return;
  if (includesAny(text, ["cardiology hospital", "search cardiology"])) {
    window.location.href = "/hospitals/?q=cardiology";
    return;
  }
  if (includesAny(text, ["emergency hospital", "search emergency"])) {
    window.location.href = "/hospitals/?q=emergency";
    return;
  }
  const route = routeForCommand(text);
  if (route) {
    setAssistantStatus(`Opening ${rawCommand}.`);
    window.setTimeout(() => {
      window.location.href = route;
    }, 250);
    return;
  }
  setAssistantStatus(`I could not match "${rawCommand}". Try "open pharmacy" or "add two strips of aspirin".`);
}

assistantForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  runAssistantCommand(assistantInput?.value || "");
});

assistantMic?.addEventListener("click", () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    setAssistantStatus("Speech input is unavailable in this browser. Type the command instead.");
    assistantInput?.focus();
    return;
  }
  const recognition = new SpeechRecognition();
  recognition.lang = "en-IN";
  recognition.interimResults = false;
  recognition.maxAlternatives = 4;
  assistantMic.classList.add("is-listening");
  setAssistantStatus("Listening now. Say one command.");
  recognition.onresult = (event) => {
    const alternatives = Array.from(event.results[0] || []).map((item) => item.transcript);
    const transcript = alternatives[0] || "";
    setAssistantStatus(`Heard "${transcript}".`);
    runAssistantCommand(transcript);
  };
  recognition.onerror = (event) => {
    setAssistantStatus(`Speech input failed: ${event.error}. You can type the command.`);
  };
  recognition.onend = () => {
    assistantMic.classList.remove("is-listening");
  };
  recognition.start();
});

const pendingAssistantCommand = sessionStorage.getItem("careconnect-pending-assistant-command");
if (pendingAssistantCommand && assistantPanel) {
  sessionStorage.removeItem("careconnect-pending-assistant-command");
  window.setTimeout(() => runAssistantCommand(pendingAssistantCommand), 650);
}

const hospitalSearch = document.querySelector("[data-osm-hospital-search]");
if (hospitalSearch) {
  hospitalSearch.addEventListener("click", async () => {
    const output = document.querySelector("[data-osm-results]");
    if (!output) return;
    output.innerHTML = "<p class='muted'>Searching OpenStreetMap around Chennai...</p>";
    try {
      const response = await fetch("https://nominatim.openstreetmap.org/search?format=json&q=hospital%20Chennai&limit=5");
      const results = await response.json();
      output.innerHTML = results
        .map((place) => `<article class="timeline-card"><span class="timeline-dot"></span><div><h2>${place.display_name.split(",")[0]}</h2><p>${place.display_name}</p><a target="_blank" rel="noopener" href="https://www.openstreetmap.org/?mlat=${place.lat}&mlon=${place.lon}#map=16/${place.lat}/${place.lon}">Open map</a></div></article>`)
        .join("");
    } catch (error) {
      output.innerHTML = "<p class='muted'>Live map lookup is unavailable. Showing curated nearby care options above.</p>";
    }
  });
}

const locationButton = document.querySelector("[data-location-button]");
locationButton?.addEventListener("click", () => {
  if (!navigator.geolocation) {
    window.location.href = "/hospitals/?location=disabled";
    return;
  }
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const params = new URLSearchParams(window.location.search);
      params.set("lat", position.coords.latitude);
      params.set("lon", position.coords.longitude);
      window.location.href = `/hospitals/?${params.toString()}`;
    },
    () => {
      window.location.href = "/hospitals/?location=disabled";
    },
    { enableHighAccuracy: true, timeout: 8000 }
  );
});
