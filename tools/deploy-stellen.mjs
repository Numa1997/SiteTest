// Deploys the job list (stellen.phyeinusul.com, Worker `stellenrecherche`, code in stellen/) as part of the
// website build. Cloudflare Workers Builds runs `npm run build` for every push to main with an account-wide
// deploy token in the environment (see docs/usul.md, "Build and deploy"), so a second `wrangler deploy` in
// that build publishes the second Worker. Nothing to connect, no token to keep anywhere.
//
// Runs only inside a Cloudflare build of main: Workers Builds sets WORKERS_CI=1 and WORKERS_CI_BRANCH.
// A local `npm run build`, a GitHub Pages build or a preview build of another branch prints one line and skips.
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const dir = join(dirname(fileURLToPath(import.meta.url)), '..', 'stellen');
const branch = process.env.WORKERS_CI_BRANCH;

if (process.env.WORKERS_CI !== '1' || branch !== 'main') {
  console.log(`stellen: skipped (WORKERS_CI=${process.env.WORKERS_CI ?? ''}, WORKERS_CI_BRANCH=${branch ?? ''}); ` +
    'deploys only in a Cloudflare build of main');
  process.exit(0);
}

const run = cmd => { console.log(`stellen: ${cmd}`); execSync(cmd, { cwd: dir, stdio: 'inherit' }); };
run('npm install --no-audit --no-fund --ignore-scripts');
run('npm test');
run('npx wrangler deploy');
console.log('stellen: deployed to stellen.phyeinusul.com');
