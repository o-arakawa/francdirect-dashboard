 GET / 500 in 156ms
 GET / 500 in 3ms
 GET / 500 in 28ms
 GET /_next/static/chunks/fallback/webpack.js 500 in 6ms
 GET /_next/static/chunks/fallback/main.js 500 in 8ms
 GET /_next/static/chunks/fallback/react-refresh.js 500 in 6ms
 GET /_next/static/chunks/fallback/pages/_app.js 500 in 10ms
 GET /_next/static/chunks/fallback/pages/_error.js 500 in 10ms
^C
o.arakawa@osamunoMacBook-Pro ad-meeting-mvp % npm run dev


> ad-meeting-mvp@0.1.0 dev
> next dev

 ⚠ You are using a non-standard "NODE_ENV" value in your environment. This creates inconsistencies in the project and is strongly advised against. Read more: https://nextjs.org/docs/messages/non-standard-node-env
  ▲ Next.js 14.2.23
  - Local:        http://localhost:3000
  - Environments: .env

 ✓ Starting...
 ✓ Ready in 1341ms
 ○ Compiling / ...
 ⨯ ./app/globals.css
Module parse failed: Unexpected character '@' (1:0)
> @tailwind base;
| @tailwind components;
| @tailwind utilities;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⨯ ./app/globals.css
Module parse failed: Unexpected character '@' (1:0)
> @tailwind base;
| @tailwind components;
| @tailwind utilities;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⨯ ./app/globals.css
Module parse failed: Unexpected character '@' (1:0)
> @tailwind base;
| @tailwind components;
| @tailwind utilities;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET / 500 in 1762ms
 GET / 500 in 11ms
 GET / 500 in 9ms

warn - The `content` option in your Tailwind CSS configuration is missing or empty.
warn - Configure your content sources or your generated CSS will be missing styles.
warn - https://tailwindcss.com/docs/content-configuration
 ✓ Compiled /_error in 167ms (440 modules)
 GET / 500 in 7ms
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:0)
> *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
| 
| body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #17202a; font-size: 14px; line-height: 1.6; }

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 125ms
 GET / 500 in 8ms
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET / 500 in 5ms
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:0)
> *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
| 
| body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #17202a; font-size: 14px; line-height: 1.6; }

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 84ms
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET / 500 in 6ms
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:0)
> *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
| 
| body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #17202a; font-size: 14px; line-height: 1.6; }

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 243ms
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET / 500 in 16ms
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:0)
> *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
| 
| body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #17202a; font-size: 14px; line-height: 1.6; }

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 103ms
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET / 500 in 5ms
[Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'
}
<w> [webpack.cache.PackFileCacheStrategy] Caching failed for pack: Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'
çCC^C
o.arakawa@osamunoMacBook-Pro ad-meeting-mvp % npm run dev


> ad-meeting-mvp@0.1.0 dev
> next dev

 ⚠ You are using a non-standard "NODE_ENV" value in your environment. This creates inconsistencies in the project and is strongly advised against. Read more: https://nextjs.org/docs/messages/non-standard-node-env
  ▲ Next.js 14.2.23
  - Local:        http://localhost:3000
  - Environments: .env

 ✓ Starting...
 ✓ Ready in 934ms
 ○ Compiling /_not-found ...
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:0)
> *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
| 
| body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #17202a; font-size: 14px; line-height: 1.6; }

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:0)
> *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
| 
| body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #17202a; font-size: 14px; line-height: 1.6; }

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 1462ms
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:0)
> *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
| 
| body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f6f8fb; color: #17202a; font-size: 14px; line-height: 1.6; }

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET / 500 in 66ms
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:146)
> html, body, div, span, h1, h2, h3, h4, h5, h6, p, a, ul, li, form, input, textarea, select, button, nav, main, section, article, details, summary {
|   box-sizing: border-box;
|   margin: 0;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 144ms
 GET / 500 in 4ms
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET / 500 in 3ms
[Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/1.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/1.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/1.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/1.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/1.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/1.pack.gz'
}
[Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/3.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/3.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/3.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/3.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/3.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/3.pack.gz'
}
[Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'
}
<w> [webpack.cache.PackFileCacheStrategy] Caching failed for pack: Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/1.pack.gz'
<w> [webpack.cache.PackFileCacheStrategy] Caching failed for pack: Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/1.pack.gz'
^C
o.arakawa@osamunoMacBook-Pro ad-meeting-mvp % npm run dev


> ad-meeting-mvp@0.1.0 dev
> next dev

 ⚠ You are using a non-standard "NODE_ENV" value in your environment. This creates inconsistencies in the project and is strongly advised against. Read more: https://nextjs.org/docs/messages/non-standard-node-env
  ▲ Next.js 14.2.23
  - Local:        http://localhost:3000
  - Environments: .env

 ✓ Starting...
 ✓ Ready in 1437ms
 ○ Compiling / ...
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:146)
> html, body, div, span, h1, h2, h3, h4, h5, h6, p, a, ul, li, form, input, textarea, select, button, nav, main, section, article, details, summary {
|   box-sizing: border-box;
|   margin: 0;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:146)
> html, body, div, span, h1, h2, h3, h4, h5, h6, p, a, ul, li, form, input, textarea, select, button, nav, main, section, article, details, summary {
|   box-sizing: border-box;
|   margin: 0;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:146)
> html, body, div, span, h1, h2, h3, h4, h5, h6, p, a, ul, li, form, input, textarea, select, button, nav, main, section, article, details, summary {
|   box-sizing: border-box;
|   margin: 0;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 1787ms
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET / 500 in 116ms
 GET / 500 in 4ms
<w> [webpack.cache.PackFileCacheStrategy] Caching failed for pack: Error: ENOENT: no such file or directory, rename '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development-fallback/0.pack.gz_' -> '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development-fallback/0.pack.gz'
^C
o.arakawa@osamunoMacBook-Pro ad-meeting-mvp % rm -rf .next

o.arakawa@osamunoMacBook-Pro ad-meeting-mvp % npm run dev


> ad-meeting-mvp@0.1.0 dev
> next dev

 ⚠ You are using a non-standard "NODE_ENV" value in your environment. This creates inconsistencies in the project and is strongly advised against. Read more: https://nextjs.org/docs/messages/non-standard-node-env
  ▲ Next.js 14.2.23
  - Local:        http://localhost:3000
  - Environments: .env

 ✓ Starting...
 ✓ Ready in 965ms
 ○ Compiling /_not-found ...
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:146)
> html, body, div, span, h1, h2, h3, h4, h5, h6, p, a, ul, li, form, input, textarea, select, button, nav, main, section, article, details, summary {
|   box-sizing: border-box;
|   margin: 0;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:146)
> html, body, div, span, h1, h2, h3, h4, h5, h6, p, a, ul, li, form, input, textarea, select, button, nav, main, section, article, details, summary {
|   box-sizing: border-box;
|   margin: 0;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ✓ Compiled / in 53ms (426 modules)
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 1596ms
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET / 500 in 210ms
 GET / 500 in 4ms
 GET / 500 in 21ms
 GET / 500 in 8ms
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:5)
> body {
|   font-family: -apple-system, BlinkMacSystemFont, sans-serif;
|   background: #f6f8fb;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 169ms
 GET / 500 in 6ms
 ⚠ Fast Refresh had to perform a full reload due to a runtime error.
 GET / 500 in 6ms
[Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/0.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/0.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/0.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/0.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/0.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/0.pack.gz'
}
[Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/0.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/0.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/0.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/0.pack.gz'
}
 ⨯ unhandledRejection: [Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/0.pack.gz'] {
  errno: -2,
  code: 'ENOENT',
  syscall: 'stat',
  path: '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/0.pack.gz'
}
<w> [webpack.cache.PackFileCacheStrategy] Caching failed for pack: Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/server-development/0.pack.gz'
<w> [webpack.cache.PackFileCacheStrategy] Caching failed for pack: Error: ENOENT: no such file or directory, stat '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development/0.pack.gz'
^C
o.arakawa@osamunoMacBook-Pro ad-meeting-mvp % npm run dev


> ad-meeting-mvp@0.1.0 dev
> next dev

 ⚠ You are using a non-standard "NODE_ENV" value in your environment. This creates inconsistencies in the project and is strongly advised against. Read more: https://nextjs.org/docs/messages/non-standard-node-env
  ▲ Next.js 14.2.23
  - Local:        http://localhost:3000
  - Environments: .env

 ✓ Starting...
 ✓ Ready in 1008ms
 ○ Compiling /_not-found ...
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:5)
> body {
|   font-family: -apple-system, BlinkMacSystemFont, sans-serif;
|   background: #f6f8fb;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:5)
> body {
|   font-family: -apple-system, BlinkMacSystemFont, sans-serif;
|   background: #f6f8fb;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ✓ Compiled / in 38ms (426 modules)
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 1862ms
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET / 500 in 246ms
 GET / 500 in 4ms
 GET / 500 in 10ms
^C
o.arakawa@osamunoMacBook-Pro ad-meeting-mvp % npm install

npm warn EBADENGINE Unsupported engine {
npm warn EBADENGINE   package: 'eslint-visitor-keys@5.0.1',
npm warn EBADENGINE   required: { node: '^20.19.0 || ^22.13.0 || >=24' },
npm warn EBADENGINE   current: { node: 'v22.12.0', npm: '10.9.0' }
npm warn EBADENGINE }
npm warn deprecated node-domexception@1.0.0: Use your platform's native DOMException instead
npm warn deprecated next@14.2.23: This version has a security vulnerability. Please upgrade to a patched version. See https://nextjs.org/blog/security-update-2025-12-11 for more details.

added 67 packages, and audited 68 packages in 16s

9 packages are looking for funding
  run `npm fund` for details

2 vulnerabilities (1 moderate, 1 critical)

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
o.arakawa@osamunoMacBook-Pro ad-meeting-mvp % npm run dev


> ad-meeting-mvp@0.1.0 dev
> next dev

 ⚠ You are using a non-standard "NODE_ENV" value in your environment. This creates inconsistencies in the project and is strongly advised against. Read more: https://nextjs.org/docs/messages/non-standard-node-env
  ▲ Next.js 14.2.23
  - Local:        http://localhost:3000
  - Environments: .env

 ✓ Starting...
It looks like you're trying to use TypeScript but do not have the required package(s) installed.
Installing dependencies

If you are not trying to use TypeScript, please remove the tsconfig.json file from your package root (and any TypeScript files in your pages directory).


Installing devDependencies (npm):
- typescript
- @types/react

npm warn EBADENGINE Unsupported engine {
npm warn EBADENGINE   package: 'eslint-visitor-keys@5.0.1',
npm warn EBADENGINE   required: { node: '^20.19.0 || ^22.13.0 || >=24' },
npm warn EBADENGINE   current: { node: 'v22.12.0', npm: '10.9.0' }
npm warn EBADENGINE }
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm warn deprecated @humanwhocodes/config-array@0.13.0: Use @eslint/config-array instead
npm warn deprecated rimraf@3.0.2: Rimraf versions prior to v4 are no longer supported
npm warn deprecated @humanwhocodes/object-schema@2.0.3: Use @eslint/object-schema instead
npm warn deprecated glob@7.2.3: Old versions of glob are not supported, and contain widely publicized security vulnerabilities, which have been fixed in the current version. Please update. Support for old versions may be purchased (at exorbitant rates) by contacting i@izs.me
npm warn deprecated glob@10.3.10: Old versions of glob are not supported, and contain widely publicized security vulnerabilities, which have been fixed in the current version. Please update. Support for old versions may be purchased (at exorbitant rates) by contacting i@izs.me
npm warn deprecated eslint@8.57.1: This version is no longer supported. Please see https://eslint.org/version-support for other options.

added 353 packages, and audited 421 packages in 2s

156 packages are looking for funding
  run `npm fund` for details

5 vulnerabilities (1 moderate, 3 high, 1 critical)

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.

 ✓ Ready in 5s
 ○ Compiling / ...
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:5)
> body {
|   font-family: -apple-system, BlinkMacSystemFont, sans-serif;
|   background: #f6f8fb;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:5)
> body {
|   font-family: -apple-system, BlinkMacSystemFont, sans-serif;
|   background: #f6f8fb;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 ⨯ ./app/globals.css
Module parse failed: Unexpected token (1:5)
> body {
|   font-family: -apple-system, BlinkMacSystemFont, sans-serif;
|   background: #f6f8fb;

Import trace for requested module:
./app/globals.css
./app/layout.tsx
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 2334ms
 ⚠ Fast Refresh had to perform a full reload due to a runtime error.
 GET / 500 in 168ms
 GET / 500 in 5ms
<w> [webpack.cache.PackFileCacheStrategy] Caching failed for pack: Error: ENOENT: no such file or directory, rename '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development-fallback/0.pack.gz_' -> '/Users/o.arakawa/projects/ad-meeting-mvp/.next/cache/webpack/client-development-fallback/0.pack.gz'
 ⨯ ./app/globals.css
Module not found: Can't resolve '/Users/o.arakawa/projects/ad-meeting-mvp/app/globals.css'

https://nextjs.org/docs/messages/module-not-found
 GET /_next/static/webpack/53b1ffa83c7b7de7.webpack.hot-update.json 500 in 140ms
 ⚠ Fast Refresh had to perform a full reload. Read more: https://nextjs.org/docs/messages/fast-refresh-reload
 GET / 500 in 8ms
