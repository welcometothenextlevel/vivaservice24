/* Viva Service24 · site behaviour. No dependencies.
   Settings (phone, e-mail, Google Ads IDs) live in js/config.js, reviews in js/reviews.js. */
(function () {
  "use strict";

  var CFG = window.VIVA_CONFIG || {};
  var REVIEWS = window.VIVA_REVIEWS || [];
  var doc = document;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };

  function store(kind) {
    try { var s = window[kind]; var k = "__t"; s.setItem(k, "1"); s.removeItem(k); return s; } catch (e) { return null; }
  }
  var SS = store("sessionStorage");
  var LS = store("localStorage");
  function sget(k) { try { return SS ? JSON.parse(SS.getItem(k) || "null") : null; } catch (e) { return null; } }
  function sset(k, v) { try { if (SS) SS.setItem(k, JSON.stringify(v)); } catch (e) {} }

  /* ---------------------------------------------------------------- tracking */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  var adsId = (CFG.googleAdsId || "").trim();
  var labels = CFG.conversionLabels || {};
  var adsOn = false;

  function loadAds() {
    if (!adsId || adsOn) return;
    adsOn = true;
    gtag("js", new Date());
    gtag("config", adsId);
    var s = doc.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(adsId);
    doc.head.appendChild(s);
  }

  function track(name, params, label) {
    params = params || {};
    var ev = { event: name };
    for (var k in params) ev[k] = params[k];
    window.dataLayer.push(ev);
    if (!adsOn) return;
    gtag("event", name, params);
    if (label && labels[label]) gtag("event", "conversion", { send_to: adsId + "/" + labels[label] });
  }
  window.vivaTrack = track;

  function consentNotice() {
    if (!adsId) return;
    var choice = LS ? LS.getItem("viva_consent") : null;
    if (choice === "denied") return;
    loadAds();
    if (choice === "granted") return;
    var pl = doc.querySelector('a[href$="confidentialite/"]');
    var href = pl ? pl.getAttribute("href") : "confidentialite/";
    var box = doc.createElement("div");
    box.className = "cnote";
    box.setAttribute("role", "region");
    box.setAttribute("aria-label", "Information sur les cookies");
    box.innerHTML = '<p>Nous utilisons Google Ads pour mesurer les demandes qui viennent de nos annonces. <a href="' + href + '">En savoir plus</a></p>' +
      '<div class="cnote__b"><button type="button" class="btn btn--primary btn--sm" data-c="granted">D\'accord</button>' +
      '<button type="button" class="btn btn--ghost btn--sm" data-c="denied">Refuser</button></div>';
    doc.body.appendChild(box);
    box.addEventListener("click", function (e) {
      var b = e.target.closest("[data-c]");
      if (!b) return;
      var v = b.getAttribute("data-c");
      try { if (LS) LS.setItem("viva_consent", v); } catch (err) {}
      if (v === "denied") {
        gtag("consent", "update", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "denied" });
        adsOn = false;
      }
      box.remove();
    });
  }

  /* attribution: gclid + utm, kept for the session and sent with the form */
  (function () {
    var keys = ["gclid", "gbraid", "wbraid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"];
    var q = new URLSearchParams(location.search);
    var cur = sget("viva_attr") || {};
    var got = false;
    keys.forEach(function (k) { var v = q.get(k); if (v) { cur[k] = v.slice(0, 200); got = true; } });
    if (got) { cur.landing = location.pathname; sset("viva_attr", cur); }
  })();

  doc.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (href.indexOf("tel:") === 0) track("call_click", { link_url: href, page_path: location.pathname }, "call");
    else if (href.indexOf("wa.me") > -1) track("whatsapp_click", { link_url: href.split("?")[0], page_path: location.pathname }, "whatsapp");
  }, true);

  /* ---------------------------------------------------------------- header */
  var hd = $("[data-header]");
  if (hd) {
    var onScroll = function () { hd.classList.toggle("is-stuck", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------------------------------------------------------------- form */
  var form = $("#devis-form");
  var formBox = $("#devis");

  function setChip(name, value) {
    if (!form) return;
    $$('input[name="' + name + '"]', form).forEach(function (i) { i.checked = i.value === value; });
    syncBail();
  }

  function goToForm(focus) {
    if (!formBox) return;
    if (form && form.classList.contains("is-step2") && focus !== "keep") showStep(1, true);
    formBox.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    window.setTimeout(function () {
      var t = form && ($('input[name="service"]:checked', form) || $('input[name="service"]', form));
      if (t) t.focus({ preventScroll: true });
    }, reduce ? 0 : 450);
  }

  doc.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-to-form]");
    if (!a || !formBox) return;
    e.preventDefault();
    var s = a.getAttribute("data-service");
    if (s) setChip("service", s);
    goToForm();
  });

  function syncBail() {
    if (!form) return;
    var bail = $("[data-bail]", form);
    var s = $('input[name="service"]:checked', form);
    if (bail) bail.hidden = !(s && s.value === "Fin de bail");
  }

  function err(name, msg) {
    var p = form && $('[data-err="' + name + '"]', form);
    var input = form && form.elements[name];
    if (p) { p.textContent = msg || ""; p.classList.toggle("is-on", !!msg); }
    if (input && input.setAttribute && input.type !== "radio" && !input.length) {
      if (msg) input.setAttribute("aria-invalid", "true"); else input.removeAttribute("aria-invalid");
      if (p) { p.id = p.id || "err-" + name; if (msg) input.setAttribute("aria-describedby", p.id); else input.removeAttribute("aria-describedby"); }
    }
    return !msg;
  }

  function showStep(n, quiet) {
    form.classList.toggle("is-step2", n === 2);
    var no = $("[data-stepno]", form);
    if (no) no.textContent = n;
    if (quiet) return;
    var first = n === 2 ? form.elements.nom : ($('input[name="service"]:checked', form) || $('input[name="service"]', form));
    if (first) first.focus({ preventScroll: true });
    var top = form.getBoundingClientRect().top;
    if (top < 60 || top > window.innerHeight * 0.6) formBox.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
  }

  function val(name) {
    var el = form.elements[name];
    if (!el) return "";
    if (el.length !== undefined && !el.tagName) { var c = $('input[name="' + name + '"]:checked', form); return c ? c.value : ""; }
    return (el.value || "").trim();
  }

  function validStep1() {
    var ok = err("service", val("service") ? "" : "Choisissez le type de nettoyage.");
    if (val("service") === "Fin de bail") ok = err("pieces", val("pieces") ? "" : "Indiquez la taille du logement.") && ok;
    else err("pieces", "");
    return ok;
  }

  function validStep2() {
    var ok = true, firstBad = null;
    var nom = val("nom");
    if (!err("nom", nom.length >= 2 ? "" : "Indiquez votre nom.")) { ok = false; firstBad = firstBad || "nom"; }
    var digits = val("telephone").replace(/\D/g, "").replace(/^00/, "");
    var telOk = digits.length >= 9 && digits.length <= 13;
    if (!err("telephone", telOk ? "" : (digits.length ? "Ce numéro semble incomplet. Exemple : 076 123 45 67" : "Indiquez votre numéro de téléphone pour qu'on puisse vous rappeler."))) { ok = false; firstBad = firstBad || "telephone"; }
    var mail = val("email");
    if (!err("email", !mail || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail) ? "" : "Cette adresse e-mail ne semble pas valide.")) { ok = false; firstBad = firstBad || "email"; }
    if (firstBad) form.elements[firstBad].focus();
    return ok;
  }

  if (form) {
    syncBail();
    form.addEventListener("change", function (e) {
      if (e.target.name === "service") { syncBail(); err("service", ""); }
      if (e.target.name === "pieces") err("pieces", "");
    });
    form.addEventListener("input", function (e) {
      var n = e.target.name;
      if (n && $('[data-err="' + n + '"].is-on', form)) err(n, "");
    });
    $("[data-next]", form).addEventListener("click", function () {
      if (!validStep1()) { var f = $('.qf__err.is-on', form); if (f) f.previousElementSibling.querySelector("input").focus(); return; }
      showStep(2);
      track("form_step2", { service: val("service") });
    });
    $("[data-prev]", form).addEventListener("click", function () { showStep(1); });

    var status = $("[data-status]", form);
    var btn = $("[data-submit]", form);

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validStep1()) { showStep(1); return; }
      if (!validStep2()) return;
      status.textContent = "";

      var service = val("service");
      var loc = val("localite");
      var attr = sget("viva_attr") || {};
      var data = {
        _subject: "Nouvelle demande de devis · " + service + " · " + (loc || "localité non précisée"),
        _template: "table",
        _captcha: "false",
        "Service": service,
        "Pièces": service === "Fin de bail" ? val("pieces") : "",
        "Date souhaitée": val("date") ? val("date").split("-").reverse().join(".") : "",
        "Nom": val("nom"),
        "Téléphone": val("telephone"),
        "Localité": loc,
        "E-mail": val("email"),
        "Message": val("message"),
        "Page": form.getAttribute("data-page") + " (" + location.pathname + ")"
      };
      if (val("email")) data._replyto = val("email");
      ["gclid", "gbraid", "wbraid", "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "landing"].forEach(function (k) {
        if (attr[k]) data[k] = attr[k];
      });

      var done = function () {
        sset("viva_lead", { prenom: val("nom").split(/\s+/)[0], service: service });
        track("generate_lead", { service: service, locality: loc || "", rooms: data["Pièces"] || "" });
        var go = function () { location.href = form.getAttribute("data-merci"); };
        window.setTimeout(go, adsOn ? 400 : 0);
      };
      var fail = function () {
        btn.disabled = false;
        btn.textContent = "Recevoir mon devis gratuit";
        status.innerHTML = "L'envoi n'a pas abouti. Appelez-nous au <a href=\"tel:" + (CFG.phoneTel || "+41767412527") + "\">" +
          (CFG.phoneDisplay || "076 741 25 27") + "</a> ou écrivez-nous sur <a href=\"https://wa.me/" + (CFG.whatsappNumber || "41767412527") +
          "?text=" + encodeURIComponent("Bonjour, je souhaite un devis (" + service + ").") + "\" target=\"_blank\" rel=\"noopener\">WhatsApp</a>.";
        track("form_error", { service: service });
      };

      if (val("_honey")) { done(); return; } // bots: pretend it worked, send nothing

      btn.disabled = true;
      btn.textContent = "Envoi en cours…";

      var send = typeof window.VIVA_MOCK_SUBMIT === "function"
        ? window.VIVA_MOCK_SUBMIT(data)
        : fetch(CFG.formEndpoint || "https://formsubmit.co/ajax/info@vivaservice24.ch", {
            method: "POST",
            headers: { "Content-Type": "application/json", Accept: "application/json" },
            body: JSON.stringify(data)
          }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, json: j }; }); });

      Promise.resolve(send).then(function (res) {
        var ok = res && res.ok && !(res.json && String(res.json.success) === "false");
        if (ok) done(); else fail();
      }).catch(fail);
    });
  }

  /* hide the mobile bar (and the WhatsApp bubble) while the form is on screen */
  (function () {
    var bar = $("[data-mbar]"), bubble = $(".wafloat");
    if (!form || !("IntersectionObserver" in window)) return;
    new IntersectionObserver(function (en) {
      var on = en[0].isIntersecting;
      if (bar) bar.classList.toggle("is-hidden", on);
      if (bubble) bubble.classList.toggle("is-hidden", on);
    }, { rootMargin: "-10% 0px -10% 0px" }).observe(form);
  })();

  /* ---------------------------------------------------------------- estimator */
  var ROOM_MAP = { studio: "Studio", "2": "2", "3": "3", "4": "4", "5": "5+" };
  $$("[data-est]").forEach(function (est) {
    var price = $("[data-est-price]", est), label = $("[data-est-label]", est);
    var upd = function () {
      var c = $('input[name="est"]:checked', est);
      if (!c) return;
      price.textContent = c.getAttribute("data-price").replace(/ /g, " ").replace(/CHF /, "CHF ");
      label.textContent = c.getAttribute("data-label");
    };
    est.addEventListener("change", upd);
    upd();
    $("[data-est-cta]", est).addEventListener("click", function (e) {
      e.preventDefault();
      var c = $('input[name="est"]:checked', est);
      setChip("service", "Fin de bail");
      if (c) setChip("pieces", ROOM_MAP[c.value]);
      track("estimator_cta", { rooms: c ? c.value : "" });
      goToForm();
    });
  });

  /* ---------------------------------------------------------------- reviews */
  function ago(iso) {
    var d = new Date(iso + "T12:00:00");
    var days = Math.max(0, Math.round((Date.now() - d.getTime()) / 864e5));
    if (days < 1) return "aujourd'hui";
    if (days === 1) return "hier";
    if (days < 7) return "il y a " + days + " jours";
    if (days < 14) return "il y a 1 semaine";
    if (days < 30) return "il y a " + Math.floor(days / 7) + " semaines";
    if (days < 60) return "il y a 1 mois";
    if (days < 365) return "il y a " + Math.floor(days / 30) + " mois";
    var y = Math.floor(days / 365);
    return "il y a " + y + (y > 1 ? " ans" : " an");
  }

  var STAR = '<span class="stars" aria-hidden="true">' + new Array(6).join('<svg viewBox="0 0 24 24"><use href="#i-star"></use></svg>') + "</span>";
  var GLOGO = '<svg class="ic ic--g rc__g" aria-hidden="true"><use href="#i-g"></use></svg>';

  function card(r, i) {
    var li = doc.createElement("li");
    li.className = "rc rc--c" + (i % 5);
    li.innerHTML = '<div class="rc__top"><span class="rc__av" aria-hidden="true"></span><span class="rc__who"><b></b>' +
      '<span class="rc__meta">' + STAR + '<span class="sr-only">5 étoiles sur 5, </span><span class="rc__d"></span></span></span>' + GLOGO + "</div>" +
      '<p class="rc__t"></p>' + (r.service ? '<span class="rc__tag"></span>' : "");
    $(".rc__av", li).textContent = (r.name || "?").charAt(0).toUpperCase();
    $(".rc__who b", li).textContent = r.name;
    $(".rc__d", li).textContent = ago(r.date);
    $(".rc__t", li).textContent = r.text;
    if (r.service) $(".rc__tag", li).textContent = r.service;
    return li;
  }

  function addMore(root) {
    $$(".rc__t", root).forEach(function (t) {
      var c = t.parentNode;
      if (c.querySelector(".rc__more")) return;
      if (t.scrollHeight - t.clientHeight < 4) return;
      var b = doc.createElement("button");
      b.type = "button";
      b.className = "rc__more";
      b.textContent = "Lire plus";
      b.setAttribute("aria-expanded", "false");
      b.addEventListener("click", function () {
        var open = c.classList.toggle("is-open");
        b.textContent = open ? "Réduire" : "Lire plus";
        b.setAttribute("aria-expanded", open ? "true" : "false");
      });
      t.insertAdjacentElement("afterend", b);
    });
  }

  function ordered(filter) {
    var list = REVIEWS.slice();
    if (!filter) return list;
    var a = [], b = [];
    list.forEach(function (r) { (r.service === filter ? a : b).push(r); });
    return a.concat(b);
  }

  $$("[data-reviews]").forEach(function (wall) {
    if (!REVIEWS.length) return;
    var filter = wall.getAttribute("data-filter") || "";
    var list = ordered(filter);
    var mqDesk = matchMedia("(min-width: 768px)");
    var mode = null, showAll = false;

    function render() {
      var m = showAll || reduce ? "static" : (mqDesk.matches ? "marquee" : "scroll");
      if (m === mode) return;
      mode = m;
      wall.innerHTML = "";
      if (m === "static") {
        var ul = doc.createElement("ul");
        ul.className = "rstatic container";
        list.forEach(function (r, i) { ul.appendChild(card(r, i)); });
        wall.appendChild(ul);
      } else if (m === "scroll") {
        var sc = doc.createElement("ul");
        sc.className = "rscroll";
        sc.setAttribute("aria-label", "Avis Google, faites glisser pour en voir plus");
        list.forEach(function (r, i) { sc.appendChild(card(r, i)); });
        wall.appendChild(sc);
        var dots = doc.createElement("div");
        dots.className = "rdots";
        dots.setAttribute("aria-hidden", "true");
        list.forEach(function () { dots.appendChild(doc.createElement("i")); });
        wall.appendChild(dots);
        var upd = function () {
          var w = sc.firstElementChild ? sc.firstElementChild.getBoundingClientRect().width + 12 : 1;
          var idx = Math.min(list.length - 1, Math.round(sc.scrollLeft / w));
          $$("i", dots).forEach(function (d, j) { d.classList.toggle("is-on", j === idx); });
        };
        sc.addEventListener("scroll", upd, { passive: true });
        upd();
      } else {
        var box = doc.createElement("div");
        box.className = "marq";
        var rows = [[], []];
        list.forEach(function (r, i) { rows[i % 2].push([r, i]); });
        rows.forEach(function (items, ri) {
          var row = doc.createElement("div");
          row.className = "marq__row" + (ri ? " marq__row--rev" : "");
          for (var copy = 0; copy < 2; copy++) {
            var set = doc.createElement("ul");
            set.className = "marq__set";
            if (copy) { set.setAttribute("aria-hidden", "true"); set.setAttribute("inert", ""); }
            items.forEach(function (x) { set.appendChild(card(x[0], x[1])); });
            row.appendChild(set);
          }
          box.appendChild(row);
        });
        wall.appendChild(box);
        requestAnimationFrame(function () {
          $$(".marq__row", box).forEach(function (row) {
            row.style.setProperty("--dur", Math.round(row.scrollWidth / 2 / 32) + "s");
          });
        });
        var t;
        wall.addEventListener("touchstart", function () { wall.classList.add("is-paused"); clearTimeout(t); }, { passive: true });
        wall.addEventListener("touchend", function () { t = setTimeout(function () { wall.classList.remove("is-paused"); }, 2500); }, { passive: true });
      }
      var all = doc.createElement("div");
      all.className = "container cta-row cta-row--c";
      all.style.marginTop = "18px";
      var tog = doc.createElement("button");
      tog.type = "button";
      tog.className = "btn btn--text btn--sm";
      tog.textContent = m === "static" ? (reduce ? "" : "Revenir au défilement") : "Afficher tous les avis";
      if (tog.textContent) {
        tog.addEventListener("click", function () { showAll = !showAll; mode = null; render(); if (showAll) wall.querySelector(".rc").setAttribute("tabindex", "-1"), wall.querySelector(".rc").focus(); });
        all.appendChild(tog);
        wall.appendChild(all);
      }
      (doc.fonts && doc.fonts.ready ? doc.fonts.ready : Promise.resolve()).then(function () { addMore(wall); });
    }
    render();
    if (mqDesk.addEventListener) mqDesk.addEventListener("change", render);
  });

  $$("[data-strip]").forEach(function (strip) {
    var names = strip.getAttribute("data-strip").split("|");
    var picks = names.map(function (n) { return REVIEWS.filter(function (r) { return r.name === n; })[0]; }).filter(Boolean);
    if (!picks.length) return;
    var wrap = doc.createElement("div");
    wrap.className = "rstrip__in";
    wrap.setAttribute("aria-label", "Extraits d'avis Google");
    wrap.setAttribute("role", "region");
    picks.forEach(function (r) {
      var f = doc.createElement("figure");
      f.className = "rq";
      f.innerHTML = '<p></p><figcaption class="rq__by">' + STAR + "<b></b><span>avis Google</span></figcaption>";
      $("p", f).textContent = "« " + r.text + " »";
      $("b", f).textContent = r.name;
      wrap.appendChild(f);
    });
    strip.appendChild(wrap);
  });

  /* ---------------------------------------------------------------- before / after */
  $$("[data-ba]").forEach(function (ba) {
    var handle = $(".ba__handle", ba);
    var pos = 50, drag = false;
    function set(p) {
      pos = Math.max(0, Math.min(100, p));
      ba.style.setProperty("--pos", pos + "%");
      handle.setAttribute("aria-valuenow", Math.round(pos));
      handle.setAttribute("aria-valuetext", Math.round(pos) + " % avant");
    }
    function fromX(x) { var r = ba.getBoundingClientRect(); set(((x - r.left) / r.width) * 100); }
    ba.addEventListener("pointerdown", function (e) {
      if (e.button !== undefined && e.button !== 0) return;
      drag = true;
      try { ba.setPointerCapture(e.pointerId); } catch (err) {}
      fromX(e.clientX);
      if (e.pointerType === "mouse") handle.focus({ preventScroll: true });
    });
    ba.addEventListener("pointermove", function (e) { if (drag) fromX(e.clientX); });
    ["pointerup", "pointercancel", "lostpointercapture"].forEach(function (t) { ba.addEventListener(t, function () { drag = false; }); });
    handle.addEventListener("keydown", function (e) {
      var k = e.key, step = e.shiftKey ? 10 : 5;
      if (k === "ArrowLeft" || k === "ArrowDown") set(pos - step);
      else if (k === "ArrowRight" || k === "ArrowUp") set(pos + step);
      else if (k === "PageDown") set(pos - 20);
      else if (k === "PageUp") set(pos + 20);
      else if (k === "Home") set(0);
      else if (k === "End") set(100);
      else return;
      e.preventDefault();
    });
  });

  $$(".ba__tabs").forEach(function (tl) {
    var tabs = $$('[role="tab"]', tl);
    function sel(t, focus) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute("aria-selected", on ? "true" : "false");
        x.tabIndex = on ? 0 : -1;
        var pane = doc.getElementById(x.getAttribute("aria-controls"));
        if (pane) pane.hidden = !on;
      });
      if (focus) t.focus();
    }
    tl.addEventListener("click", function (e) { var t = e.target.closest('[role="tab"]'); if (t) sel(t); });
    tl.addEventListener("keydown", function (e) {
      var i = tabs.indexOf(doc.activeElement);
      if (i < 0) return;
      if (e.key === "ArrowRight") sel(tabs[(i + 1) % tabs.length], true);
      else if (e.key === "ArrowLeft") sel(tabs[(i - 1 + tabs.length) % tabs.length], true);
      else return;
      e.preventDefault();
    });
  });

  /* ---------------------------------------------------------------- videos */
  var conn = navigator.connection || {};
  var slow = !!(conn.saveData || /(^|-)2g|3g/.test(conn.effectiveType || ""));

  var hv = $(".hero__video");
  if (hv && !reduce && !slow) {
    var startHero = function () {
      var base = hv.getAttribute(window.innerWidth < 800 ? "data-sm" : "data-lg");
      hv.innerHTML = '<source src="' + base + '.webm" type="video/webm"><source src="' + base + '.mp4" type="video/mp4">';
      hv.addEventListener("playing", function () { hv.classList.add("is-on"); }, { once: true });
      hv.load();
      var p = hv.play();
      if (p && p.catch) p.catch(function () {});
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (en) {
          if (en[0].isIntersecting) { var q = hv.play(); if (q && q.catch) q.catch(function () {}); } else hv.pause();
        }).observe(hv);
      }
    };
    var idle = window.requestIdleCallback || function (f) { return setTimeout(f, 200); };
    if (doc.readyState === "complete") idle(startHero); else window.addEventListener("load", function () { idle(startHero); });
  }

  var clips = $$("video[data-autoplay]");
  if (clips.length) {
    clips.forEach(function (v) {
      if (reduce || slow) {
        v.setAttribute("controls", "");
        v.setAttribute("preload", "none");
        v.src = v.getAttribute("data-src");
      }
    });
    if (!reduce && !slow && "IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (en) {
        en.forEach(function (x) {
          var v = x.target;
          if (x.isIntersecting) {
            if (!v.getAttribute("src")) v.src = v.getAttribute("data-src");
            var p = v.play();
            if (p && p.catch) p.catch(function () {});
          } else if (!v.paused) v.pause();
        });
      }, { threshold: 0.35 });
      clips.forEach(function (v) { io.observe(v); });
    }
  }

  /* ---------------------------------------------------------------- reveal on scroll */
  if (!reduce && "IntersectionObserver" in window) {
    var sel = ".sec__head,.svc,.steps li,.inc__g,.alt,.vclip,.about__photos,.case__media,.ptable,.est,.pq--float,.zone__map,.faq__list,.ba-sec__view,.final__in";
    var vh = window.innerHeight;
    var rio = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("is-in"); rio.unobserve(x.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(sel).forEach(function (el, i) {
      if (el.getBoundingClientRect().top < vh * 0.95) return;
      el.classList.add("rv");
      el.style.transitionDelay = (el.matches(".svc,.steps li,.inc__g,.vclip") ? (i % 4) * 70 : 0) + "ms";
      rio.observe(el);
    });
  }

  /* ---------------------------------------------------------------- merci page */
  if (window.VIVA_PAGE === "merci") {
    var lead = sget("viva_lead");
    var lead_el = $("[data-merci-name]");
    if (lead && lead.prenom && lead_el) lead_el.textContent = "Merci " + lead.prenom + ", votre demande est bien envoyée.";
    if (!sget("viva_merci_counted")) {
      sset("viva_merci_counted", 1);
      // wait for the consent/gtag setup below, then count the conversion once per session
      setTimeout(function () { track("lead_thank_you_view", { service: lead ? lead.service : "" }, "lead"); }, 0);
    }
  }

  consentNotice();
})();
