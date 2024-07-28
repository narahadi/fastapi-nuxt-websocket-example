# Nuxt.js and FastAPI WebSocket Sample

This repository demonstrates a simple application using Nuxt 3 for the frontend and FastAPI for the backend, with WebSocket communication between them.

## Project Structure

```
app
├── src
│ ├── api (FastAPI backend)
│ └── web (Nuxt3 frontend)
└── README.md
```

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Set up the API (FastAPI backend):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r src/api/requirements.txt
   ```

3. Set up the Web (Nuxt.js frontend):
   ```
   cd src/web
   bun install
   ```

## Running the Application

1. Start the API server:
   ```
   cd src/api
   fastapi dev
   ```

2. In a new terminal, start the Nuxt.js development server:
   ```
   cd src/web
   bun run dev
   ```

3. Open your browser and navigate to `http://localhost:3000`

## Usage

1. You will be redirected to the login page. Enter a username to generate a token.
2. After logging in, you'll be on the main page where you can start a background job.
3. Click "Start Background Job" to initiate a job on the server.
4. Once the job is complete, you'll receive a WebSocket message and see a notification.

## Features

- FastAPI backend with WebSocket support
- Nuxt.js frontend with real-time updates
- JWT-based authentication
- Background job simulation

## Development

- The FastAPI backend is in `src/api/main.py`
- The Nuxt.js frontend is in `src/web/`
- WebSocket logic is handled in `src/web/composables/useWebSocket.ts`

## Notes

- This is a sample application for demonstration purposes.
- In a production environment, ensure proper security measures are implemented.