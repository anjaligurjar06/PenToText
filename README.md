# PenToText — Frontend Prototype

A clickable, six-screen frontend prototype for PenToText, built from the SRS
(landing page, auth, dashboard, upload, review/result, history). All data is
mocked client-side — there's no backend wired up yet.

## Structure

```
pentotext-app/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── main.jsx              # React entry point, imports the global stylesheet
    ├── App.jsx                # Root component — holds the current view in state
    ├── data.js                 # Mock data: categories, document history, transcript
    ├── styles/
    │   ├── index.css          # Imports the three files below, in order
    │   ├── tokens.css         # Colors, fonts, spacing/layout primitives
    │   ├── components.css     # Buttons, cards, inputs, badges, toast, chips…
    │   └── pages.css          # Layout for each page + responsive rules
    ├── components/
    │   ├── Shared.jsx         # SquiggleLine, PageMock, HeroDemo, Field
    │   ├── MarketingNav.jsx
    │   ├── Footer.jsx
    │   ├── Sidebar.jsx
    │   └── AppShell.jsx       # Sidebar + main content wrapper for app pages
    └── pages/
        ├── Landing.jsx
        ├── Auth.jsx
        ├── Dashboard.jsx
        ├── Upload.jsx
        ├── Review.jsx
        └── History.jsx
```

## Running it

```bash
npm install
npm run dev
```

Then open the local URL Vite prints (usually `http://localhost:5173`).

## Notes for wiring up the real backend

- **Navigation is state-based, not routed.** `App.jsx` just swaps which page
  component renders based on a `view` string. If you want real URLs
  (`/upload`, `/history/:id`, browser back/forward), swap this for
  `react-router-dom` — the `go(view)` calls map almost directly to
  `navigate('/view')`.
- **`data.js`** is where the mock documents, categories, and transcript live.
  Replace these with `fetch`/`axios` calls to your FastAPI endpoints
  (`/documents`, `/documents/:id`, etc.).
- **`Upload.jsx`** currently fakes the transcription call with a
  `setTimeout`. Replace `handleSubmit` with a real `multipart/form-data`
  POST to your upload endpoint, and navigate to the review page once the
  response comes back (pass the returned document id instead of hardcoding
  the review page's content).
- **`Review.jsx`** hardcodes one sample transcript. It should instead load
  the transcript, confidence flags, and extracted fields for whatever
  document id was passed in.
- Depends on `lucide-react` for icons — already listed in `package.json`.

## Design notes

Palette and type are built around the actual product idea — ink becoming
type — rather than a generic SaaS look: deep indigo "ink," warm linen
"paper," and a marigold highlighter color used consistently for
low-confidence flags, both in the hero demo and the review page.
