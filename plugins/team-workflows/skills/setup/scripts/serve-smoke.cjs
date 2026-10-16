#!/usr/bin/env node
'use strict';

// Serve only the bundled smoke page, on an unused loopback port.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const content = fs.readFileSync(path.join(__dirname, '..', 'assets', 'playwright-smoke.html'));
const server = http.createServer((request, response) => {
  if (!['GET', 'HEAD'].includes(request.method)) {
    response.writeHead(405, { Allow: 'GET, HEAD' });
    response.end();
    return;
  }
  if (!['/', '/playwright-smoke.html'].includes(request.url)) {
    response.writeHead(404);
    response.end();
    return;
  }
  response.writeHead(200, {
    'Content-Type': 'text/html; charset=utf-8',
    'Content-Length': content.length,
    'Cache-Control': 'no-store',
    'Content-Security-Policy': "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'",
  });
  response.end(request.method === 'HEAD' ? undefined : content);
});

server.on('error', (error) => {
  console.error(`Smoke server failed: ${error.code || 'unknown error'}`);
  process.exitCode = 1;
});
server.listen(0, '127.0.0.1', () => {
  console.log(JSON.stringify({ url: `http://127.0.0.1:${server.address().port}/playwright-smoke.html`, pid: process.pid }));
});
for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => server.close());
}
