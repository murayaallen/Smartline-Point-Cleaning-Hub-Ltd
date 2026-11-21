/* Smartline — browser QA through real device emulation (puppeteer-core + an installed Chromium:
 * $QA_BROWSER if set, else Chrome, else Edge — the first one that actually launches).
 *
 *   NODE_PATH=<folder with puppeteer-core/node_modules> node tools/qa_browser.cjs <out_dir> [base_url]
 *
 * For every page, at desktop (1440) and phone (390, iPhone-class emulation):
 *   - console errors, uncaught exceptions, failed requests and HTTP errors
 *   - horizontal overflow, naming the elements that stick out
 *   - a full-page screenshot with motion settled
 * Then it clicks through the site like a visitor: mobile menu, mega menu, the
 * two-step quote form (validation, then a real submit), client filter, lightbox,
 * and one pass with animations ON to prove the loader clears itself.
 * Exit code 1 if anything fails.
 */
const path = require("path");
const fs = require("fs");
const puppeteer = require("puppeteer-core");

const BROWSERS = [process.env.QA_BROWSER,
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"].filter((x) => x && fs.existsSync(x));
async function launch() {          // an Edge mid-update refuses to start headless; try the next one
  for (const exe of BROWSERS) {
    try { return await puppeteer.launch({ executablePath: exe, headless: true, protocolTimeout: 120000, args: ["--no-first-run", "--disable-gpu"] }); }
    catch (e) { console.log("  (could not start " + exe + ")"); }
  }
  throw new Error("no Chromium browser would start: " + BROWSERS.join(", "));
}
const OUT = process.argv[2] || "qa_out";
const BASE = process.argv[3] || "http://127.0.0.1:8765";
const PAGES = ["/", "/about", "/services", "/commercial-cleaning", "/residential-apartment-cleaning",
  "/post-construction-cleaning", "/clients", "/contact", "/thank-you", "/privacy", "/no-such-page"];
const DEVICES = {
  desktop: { width: 1440, height: 900, deviceScaleFactor: 1, isMobile: false, hasTouch: false },
  mobile: { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
};
const IPHONE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1";
fs.mkdirSync(OUT, { recursive: true });

const failures = [];
const log = (...a) => console.log(...a);
const fail = (msg) => { failures.push(msg); log("  FAIL " + msg); };
const name = (p, d) => (p === "/" ? "home" : p.replace(/^\//, "").replace(/\//g, "_")) + "-" + d;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function tap(page, sel) {
  await page.$eval(sel, (el) => el.scrollIntoView({ block: "center" }));
  await sleep(120);
  await page.click(sel);
}

async function newPage(browser, device, motion) {
  const page = await browser.newPage();
  await page.setViewport(DEVICES[device]);
  if (device === "mobile") await page.setUserAgent(IPHONE_UA);
  await page.emulateMediaFeatures([{ name: "prefers-reduced-motion", value: motion ? "no-preference" : "reduce" }]);
  page._problems = [];
  page.on("console", (m) => { if (m.type() === "error" && !(m.text().includes("404") && page.url().endsWith("/no-such-page"))) page._problems.push("console: " + m.text()); });
  page.on("pageerror", (e) => page._problems.push("exception: " + e.message));
  page.on("requestfailed", (r) => {
    const u = r.url();
    if (!u.includes("googletagmanager")) page._problems.push("request failed: " + u + " " + (r.failure() || {}).errorText);
  });
  page.on("response", (r) => {
    const u = r.url();
    if (r.status() >= 400 && !u.endsWith("/no-such-page")) page._problems.push("HTTP " + r.status() + ": " + u);
  });
  return page;
}

async function scrollThrough(page) {          // like a visitor: triggers lazy images and reveals
  await page.evaluate(async () => {
    const step = Math.round(innerHeight * 0.8);
    for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 120));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForNetworkIdle({ idleTime: 400, timeout: 20000 }).catch(() => {});
  // images in the sideways swipe deck load when swiped to, not when the page scrolls past
  const pending = await page.$$eval("img", (imgs) => imgs.filter((i) => i.getAttribute("src") && !(i.complete && i.naturalWidth > 0) && !i.closest(".rail__viewport")).map((i) => i.getAttribute("src")));
  return pending;
}

async function overflow(page) {
  return page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const sw = document.documentElement.scrollWidth;
    const out = [];
    if (sw > vw) {
      document.querySelectorAll("body *").forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.width && r.right > vw + 1 && getComputedStyle(el).position !== "fixed") {
          const anc = el.closest(".marquee, .lightbox, .drawer, .mega, .cta__bg, .phero__bg");
          if (!anc) out.push((el.className && el.className.baseVal === undefined ? "." + String(el.className).split(" ")[0] : el.tagName) + " right=" + Math.round(r.right));
        }
      });
    }
    return { vw, sw, offenders: out.slice(0, 8) };
  });
}

(async () => {
  const browser = await launch();
  log("browser: " + (await browser.version()));

  // ---------------------------------------------------------- 1. every page, both devices
  for (const p of PAGES) {
    for (const d of Object.keys(DEVICES)) {
      const page = await newPage(browser, d, false);
      const res = await page.goto(BASE + p, { waitUntil: "networkidle0", timeout: 60000 });
      await sleep(400);
      const st = res.status();
      if (p === "/no-such-page" ? st !== 404 : (st !== 200 && st !== 304)) fail(`${p} [${d}] status ${st}`);
      const of = await overflow(page);
      if (of.sw > of.vw) fail(`${p} [${d}] page is ${of.sw}px in a ${of.vw}px screen`);
      if (of.offenders.length) fail(`${p} [${d}] horizontal overflow ${of.sw}>${of.vw}: ${of.offenders.join(", ")}`);
      const leaks = await page.$$eval("[hidden]", (els) => els.filter((e) => getComputedStyle(e).display !== "none").map((e) => e.tagName + "." + e.className));
      if (leaks.length) fail(`${p} [${d}] elements marked hidden are showing: ${leaks.slice(0, 4).join(", ")}`);
      const focused = await page.evaluate(() => document.activeElement === document.body || document.activeElement === null);
      if (!focused) fail(`${p} [${d}] focus moved on load to ${await page.evaluate(() => document.activeElement.tagName)}`);
      const h1 = await page.$$eval("h1", (x) => x.length);
      if (h1 !== 1) fail(`${p} [${d}] has ${h1} h1`);
      const broken = await page.$$eval("img[src]", (imgs) => imgs.filter((i) => i.getAttribute("src") && i.complete && i.naturalWidth === 0 && i.loading !== "lazy").map((i) => i.src));
      if (broken.length) fail(`${p} [${d}] broken images: ${broken.join(", ")}`);
      const unloaded = await scrollThrough(page);
      if (unloaded.length) fail(`${p} [${d}] images never loaded after scrolling: ${unloaded.slice(0, 4).join(", ")}`);
      await page.screenshot({ path: path.join(OUT, name(p, d) + ".png"), fullPage: true });
      page._problems.forEach((x) => fail(`${p} [${d}] ${x}`));
      log(`ok  ${p.padEnd(34)} ${d.padEnd(8)} ${of.sw}px`);
      await page.close();
    }
  }

  // ---------------------------------------------------------- 2. interactions
  // mobile drawer
  {
    const page = await newPage(browser, "mobile", false);
    await page.goto(BASE + "/", { waitUntil: "networkidle0" });
    await page.click(".hdr__burger");
    await sleep(700);
    const open = await page.$eval(".drawer", (e) => e.classList.contains("is-open") && !e.hidden);
    if (!open) fail("mobile drawer did not open");
    const locked = await page.$eval("body", (b) => b.classList.contains("no-scroll"));
    if (!locked) fail("body scroll not locked while drawer open");
    const focusIn = await page.evaluate(() => document.querySelector(".drawer").contains(document.activeElement));
    if (!focusIn) fail("focus did not move into the drawer");
    await page.screenshot({ path: path.join(OUT, "ix-drawer-mobile.png") });
    await page.keyboard.press("Escape");
    await sleep(700);
    const closed = await page.$eval(".drawer", (e) => !e.classList.contains("is-open"));
    if (!closed) fail("Escape did not close the drawer");
    page._problems.forEach((x) => fail("drawer " + x));
    log("ok  drawer: opens, locks scroll, takes focus, closes on Escape");
    await page.close();
  }
  // desktop mega menu
  {
    const page = await newPage(browser, "desktop", false);
    await page.goto(BASE + "/about", { waitUntil: "networkidle0" });
    await page.click(".nav__item--mega .nav__link");
    await sleep(500);
    const open = await page.$eval(".nav__item--mega", (e) => e.classList.contains("is-open"));
    const exp = await page.$eval(".nav__item--mega .nav__link", (e) => e.getAttribute("aria-expanded"));
    if (!open || exp !== "true") fail("mega menu did not open on click");
    else log("ok  mega menu stays open after hover-then-click");
    await page.screenshot({ path: path.join(OUT, "ix-mega-desktop.png"), clip: { x: 0, y: 0, width: 1440, height: 560 } });
    await page.keyboard.press("Escape");
    await sleep(300);
    const shut = await page.$eval(".nav__item--mega", (e) => !e.classList.contains("is-open"));
    if (!shut) fail("Escape did not close the mega menu");
    log("ok  mega menu: opens, aria-expanded, closes on Escape");
    await page.close();
  }
  // quote form: validation, step change, prefill, submit
  for (const d of ["mobile", "desktop"]) {
    const page = await newPage(browser, d, false);
    await page.goto(BASE + "/contact?service=" + encodeURIComponent("Office carpet cleaning") + "#quote", { waitUntil: "networkidle0" });
    const pre = await page.$eval("#f-service", (s) => s.value);
    if (pre !== "Office carpet cleaning") fail(`[${d}] ?service= did not prefill (got "${pre}")`);
    const btns1 = await page.$$eval(".form-actions button", (bs) => bs.filter((b) => b.offsetParent).map((b) => b.textContent.trim()));
    if (btns1.join("|") !== "Continue") fail(`[${d}] step 1 shows buttons: ${btns1.join(", ")}`);
    const step2hidden = await page.$eval('[data-step="2"]', (f) => f.hidden);
    if (!step2hidden) fail(`[${d}] step 2 visible before step 1 is done`);
    await page.select("#f-service", "");
    await tap(page, "[data-next]");
    await sleep(200);
    const errs = await page.$$eval(".field.has-error", (x) => x.length);
    if (errs < 2) fail(`[${d}] empty step 1 did not show errors (${errs})`);
    await page.select("#f-service", "Commercial cleaning");
    await page.select("#f-property", "Office");
    await page.type("#f-location", "Westlands");
    await tap(page, "[data-next]");
    await sleep(300);
    const onStep2 = await page.$eval('[data-step="2"]', (f) => !f.hidden);
    if (!onStep2) fail(`[${d}] did not advance to step 2`);
    const btns2 = await page.$$eval(".form-actions button", (bs) => bs.filter((b) => b.offsetParent).map((b) => b.textContent.trim()));
    if (btns2.join("|") !== "Back|Send request") fail(`[${d}] step 2 shows buttons: ${btns2.join(", ")}`);
    await page.type("#f-name", "Test Visitor");
    await page.type("#f-phone", "0711 000 000");
    await page.type("#f-email", "not-an-email");
    await tap(page, "#f-consent");
    await tap(page, "[data-submit]");
    await sleep(300);
    const emailErr = await page.$eval("#f-email-err", (e) => e.textContent);
    if (!emailErr) fail(`[${d}] bad email was not flagged`);
    await page.click("#f-email", { clickCount: 3 });   // delete it the way a person does
    await page.keyboard.press("Backspace");
    const cleared = await page.$eval("#f-email-err", (e) => e.textContent);
    if (cleared) fail(`[${d}] email error did not clear while deleting`);
    if (d === "mobile") await page.screenshot({ path: path.join(OUT, "ix-form-step2-mobile.png"), fullPage: false });
    await sleep(3200);                       // past the 3-second time-trap
    await Promise.all([page.waitForNavigation({ waitUntil: "networkidle0" }), tap(page, "[data-submit]")]);
    if (!page.url().endsWith("/thank-you")) fail(`[${d}] submit did not reach /thank-you (${page.url()})`);
    page._problems.forEach((x) => fail(`form [${d}] ` + x));
    log(`ok  quote form [${d}]: prefill, validation, step change, submit -> /thank-you`);
    await page.close();
  }
  // service-page quick quote posts too
  {
    const page = await newPage(browser, "mobile", false);
    await page.goto(BASE + "/post-construction-cleaning", { waitUntil: "networkidle0" });
    await page.type("#qq-name", "Test Visitor");
    await page.type("#qq-phone", "0711000000");
    await page.type("#qq-location", "Ruiru");
    await tap(page, "#qq-consent");
    await sleep(3200);
    await Promise.all([page.waitForNavigation({ waitUntil: "networkidle0" }), tap(page, ".qq [type=submit]")]);
    if (!page.url().endsWith("/thank-you")) fail("quick quote did not reach /thank-you");
    log("ok  quick quote on a service page submits");
    await page.close();
  }
  // client filter + deep link
  {
    const page = await newPage(browser, "desktop", false);
    await page.goto(BASE + "/clients?sector=banking", { waitUntil: "networkidle0" });
    const shown = await page.$$eval(".client:not(.is-hidden)", (x) => x.length);
    if (shown !== 1) fail(`?sector=banking shows ${shown} clients, expected 1`);
    await page.click('[data-filter="residential"]');
    const res = await page.$$eval(".client:not(.is-hidden)", (x) => x.length);
    if (res !== 3) fail(`residential filter shows ${res}, expected 3`);
    await page.click('[data-filter="all"]');
    const all = await page.$$eval(".client:not(.is-hidden)", (x) => x.length);
    if (all !== 9) fail(`all filter shows ${all}, expected 9`);
    const letterbox = await page.$eval(".tile", (t) => t.clientWidth - t.querySelector("img").clientWidth);
    if (letterbox > 1) fail(`gallery photo is ${letterbox}px narrower than its tile`);
    // lightbox
    await page.click("a.tile");
    await sleep(500);
    const lb = await page.$eval("dialog.lightbox", (d) => d.open);
    if (!lb) fail("lightbox did not open");
    await page.keyboard.press("ArrowRight");
    await sleep(300);
    await page.screenshot({ path: path.join(OUT, "ix-lightbox.png") });
    await page.keyboard.press("Escape");
    page._problems.forEach((x) => fail("clients " + x));
    log("ok  clients: deep-link filter, filter buttons, lightbox");
    await page.close();
  }
  // motion ON: the loader must clear itself, no errors with animations running
  {
    const page = await newPage(browser, "desktop", true);
    await page.goto(BASE + "/", { waitUntil: "load" });
    await sleep(3600);
    const gone = await page.$(".loader");
    if (gone) fail("loader still in the page 3.6 s after load (motion on)");
    const heroIn = await page.$eval(".hero", (h) => h.classList.contains("is-in"));
    if (!heroIn) fail("hero entrance did not run");
    // v2 header: solid once scrolled, tucks away on the way down, returns on the way up
    for (let yy = 0; yy <= 2400; yy += 200) { await page.evaluate((v) => window.scrollTo(0, v), yy); await sleep(60); }
    await sleep(900);
    const down = await page.$eval(".hdr", (h) => ({ scrolled: h.classList.contains("is-scrolled"), hidden: h.classList.contains("is-hidden") }));
    if (!down.scrolled || !down.hidden) fail(`header did not go solid + tuck away scrolling down (solid=${down.scrolled}, hidden=${down.hidden})`);
    for (let yy = 2400; yy >= 2000; yy -= 100) { await page.evaluate((v) => window.scrollTo(0, v), yy); await sleep(60); }
    await sleep(900);
    const hdr = await page.$eval(".hdr", (h) => ({ top: Math.round(h.getBoundingClientRect().top), scrolled: h.classList.contains("is-scrolled") }));
    if (hdr.top !== 0 || !hdr.scrolled) fail(`header did not come back scrolling up (top=${hdr.top}, solid=${hdr.scrolled})`);
    const prog = await page.$eval(".hdr__progress span", (s) => parseFloat(getComputedStyle(s).transform.split(",")[0].replace("matrix(", "")) || 0);
    if (!(prog > 0)) fail("scroll progress bar did not move");
    const counted = await page.$eval("[data-count='13']", (e) => e.textContent.trim());
    if (counted !== "13") fail(`counter ended at ${counted}`);
    page._problems.forEach((x) => fail("motion " + x));
    log("ok  motion on: loader clears, hero entrance runs, counters land");
    await page.close();
  }

  await browser.close();
  fs.writeFileSync(path.join(OUT, "report.txt"), failures.length ? failures.join("\n") : "ALL CHECKS PASSED\n");
  log(failures.length ? `\n${failures.length} FAILURE(S)` : "\nALL CHECKS PASSED");
  process.exit(failures.length ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
