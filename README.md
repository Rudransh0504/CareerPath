CareerPath AI - Static Demo with Mock API and Chart.js

Files:
- index.html : main dashboard (uses Chart.js via CDN)
- style.css : styles for layout, glassmorphism, themes
- script.js : loads mock-api.json, renders charts and UI dynamically
- mock-api.json : sample data for skills, matches, badges
- assets/: simple SVG badge icons

How to run:
1. Download the ZIP and extract.
2. Open the folder in VS Code.
3. (Recommended) Install Live Server extension and right-click index.html -> Open with Live Server.
4. Or open index.html directly in browser (some browsers block local fetch from file:// - Live Server recommended).

This demo is static and uses mock-api.json for data. For a real backend, replace fetch('mock-api.json') with your API endpoint.
