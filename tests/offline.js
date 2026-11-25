// Tests run offline: requests to the web (e.g., the GoatCounter visitor counter) are answered with an empty response,
// so they neither count test visits nor depend on the network.
const {chromium}=require('playwright');
const stub=r=>r.fulfill({status:200,contentType:'text/javascript',body:''});
const launch=chromium.launch.bind(chromium);
chromium.launch=async(...a)=>{const br=await launch(...a);
  const np=br.newPage.bind(br);br.newPage=async(...o)=>{const pg=await np(...o);await pg.route(/^https?:\/\//,stub);return pg};
  const nc=br.newContext.bind(br);br.newContext=async(...o)=>{const c=await nc(...o);await c.route(/^https?:\/\//,stub);return c};
  return br};
