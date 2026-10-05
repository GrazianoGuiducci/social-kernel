const path = require('node:path');
const { pathToFileURL } = require('node:url');
const runtimeModules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
const { chromium } = require(require.resolve('playwright', { paths: runtimeModules ? [runtimeModules] : [process.cwd()] }));

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 423, height: 950 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(__dirname, 'local-preview-v1.html')).href);
  await page.locator('img').evaluate(image => image.decode());
  const measurement = await page.locator('img').evaluate(image => ({
    naturalWidth: image.naturalWidth,
    naturalHeight: image.naturalHeight,
    displayedWidth: image.getBoundingClientRect().width,
    displayedHeight: image.getBoundingClientRect().height,
    complete: image.complete
  }));
  await page.screenshot({ path: path.join(__dirname, 'local-preview-v1.png'), fullPage: true });
  console.log(JSON.stringify(measurement));
  await browser.close();
})().catch(error => { console.error(error.message); process.exitCode = 1; });
