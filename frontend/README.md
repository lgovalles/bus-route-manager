# Frontend Bus Route Manager

This is a React frontend for managing bus routes, built with Vite, consuming a FastAPI backend.

## Prerequisites

- Node.js (version 18 or higher)

## Installation

1. Install Node.js from https://nodejs.org/

2. Optionally configure the backend URL by creating a `.env` file from `.env.example`.

3. Install dependencies:

```bash
npm install
```

## Development

Environment variables:

```bash
VITE_API_BASE_URL=http://localhost:8000
```

Run the development server:

```bash
npm run dev
```

## Build

Build for production:

```bash
npm run build
```

## Quality Gates (Local CI Parity)

Run the same checks enforced by CI:

```bash
npm run typecheck
npm run lint
npm run test:coverage
npm run build
```

## Testing

Run unit tests:

```bash
npm run test
```

Run E2E tests with Playwright:

```bash
npm run test:e2e
```

Open Playwright UI mode:

```bash
npm run test:e2e:ui
```

Install Playwright browsers (first time only):

```bash
npx playwright install
```

## Features

- Interactive map with Leaflet showing bus stops
- State management with Zustand
- API integration with Axios
- Routing with React Router
- Styled with Tailwind CSS

## Project Structure

- `src/components`: React components
- `src/services`: API services
- `src/store`: Zustand stores
- `src`: Main app files

## Usage

After installing dependencies, start the development server. The app will load bus routes and stops from the FastAPI backend configured in `VITE_API_BASE_URL`.

## Troubleshooting

- Ensure the FastAPI backend is running on the URL defined by `VITE_API_BASE_URL`.
- If CORS errors occur, configure CORS in the FastAPI backend.

## DevOps Strategy

See `DEVOPS_CICD_STRATEGY.md` for the CI/CD, security, quality, and branching model used by this project.