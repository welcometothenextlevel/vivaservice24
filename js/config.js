/* Viva Service24 · site settings
   Change the contact details, the form address or the Google Ads IDs here.
   Every page reads this file, so one edit updates the whole site. */

// Address that receives the quote requests (via FormSubmit).
// The very first request sends an activation e-mail to this address: click the link in it once.
var VIVA_EMAIL = "info@vivaservice24.ch";

window.VIVA_CONFIG = {
  email: VIVA_EMAIL,
  formEndpoint: "https://formsubmit.co/ajax/" + VIVA_EMAIL,

  phoneDisplay: "076 741 25 27",
  phoneTel: "+41767412527",
  whatsappNumber: "41767412527",

  googleReviewsUrl:
    "https://www.google.com/maps/search/?api=1&query=Entreprise%20de%20nettoyage%20VIVA%20service24%20Crissier",

  // Google Ads. Leave empty to load nothing from Google.
  // Example: googleAdsId: "AW-123456789", conversionLabels: { lead: "AbCdEf123", call: "...", whatsapp: "..." }
  googleAdsId: "",
  conversionLabels: {
    lead: "",      // fired once on the merci/ page (the form conversion)
    call: "",      // click on any phone link
    whatsapp: ""   // click on any WhatsApp link
  }
};
