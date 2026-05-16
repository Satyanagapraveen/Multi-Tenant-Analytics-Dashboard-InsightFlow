# 🚀 InsightFlow Analytics

![InsightFlow](https://img.shields.io/badge/Status-Active-success) ![Docker](https://img.shields.io/badge/Docker-Enabled-blue) ![Django](https://img.shields.io/badge/Django-5.0-092E20) ![React](https://img.shields.io/badge/React-18-61DAFB) ![Redis](https://img.shields.io/badge/Redis-Cache-DC382D)

**InsightFlow** is a production-grade, multi-tenant analytics platform designed to track user events across external websites and display them in a centralized, secure dashboard.

Built as a decoupled Single Page Application (SPA), this project demonstrates advanced full-stack architectural patterns including distributed caching, server-to-server OAuth 2.0 handshakes, cross-origin resource sharing (CORS), and containerized orchestration.

---

## 🏗️ Architecture Overview

The application is fully containerized using Docker and is split into four distinct microservices:

1. **Frontend (React/Vite):** The visual layer. Uses `@tanstack/react-query` for state management and caching, `axios` for network requests with secure cookie inclusion, and `recharts` for interactive data visualization.
2. **Backend (Django REST Framework):** The brain. Handles business logic, authentication, multi-tenant data isolation, and exposes RESTful APIs.
3. **Primary Database (PostgreSQL):** The source of truth. Handles relational data (Users, Workspaces, Events) with robust ACID compliance.
4. **Speed Layer (Redis):** An in-memory datastore acting as a caching layer to protect PostgreSQL from traffic spikes during heavy dashboard load.

---

## 🧠 Key Design Decisions

### 1. Multi-Tenant Isolation

Data is strictly isolated using a Workspace model. Users can belong to multiple workspaces, but analytics events are securely bound to specific `workspace_slug` identifiers. Database queries enforce tenant boundaries at the ORM level.

### 2. Aggressive Caching Strategy

To prevent database throttling when thousands of users load their dashboards simultaneously, the `DashboardSummaryView` caches its PostgreSQL aggregations into **Redis** with a 15-minute Time-To-Live (TTL). This reduces database load for heavy `COUNT()` and `GROUP BY` operations from $O(N)$ to $O(1)$ memory lookups.

### 3. Server-to-Server OAuth 2.0

Instead of relying on insecure client-side JWTs, the application uses a strict 3-way Google OAuth handshake. The React frontend obtains a temporary authorization code and passes it to Django. Django performs a secure server-to-server exchange with Google, creating a session in the database and returning an HTTP-Only session cookie.

### 4. Decoupled Ingestion API

The `EventIngestView` is intentionally unbolted (`AllowAny` + `csrf_exempt`) from the standard authentication flow. This allows lightweight, dependency-free JavaScript tracking snippets to be embedded on customer websites without requiring API keys or exposing backend security credentials.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Docker** & **Docker Compose**
- A Google Cloud Console account (to generate OAuth 2.0 Credentials)

---

## 🚀 Setup & Installation

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd insightflow
```

### Step 2: Configure Environment Variables

You need two `.env` files.

**1. Root Directory (`./.env`)**
Create a `.env` file in the root folder for the Backend/Database:

```env
POSTGRES_DB=insightflow_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgres://postgres:your_secure_password@db:5432/insightflow_db

# Get these from Google Cloud Console (Authorized Redirect URI: http://localhost:5173)
GOOGLE_OAUTH2_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=your_google_client_secret
GOOGLE_OAUTH2_REDIRECT_URI=http://localhost:5173
```

**2. Frontend Directory (`./frontend/.env`)**
Create a `.env` file in the frontend folder for React:

```env
VITE_GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
```

### Step 3: Boot the Infrastructure

Run the following command to download the images and build the containers:

```bash
docker-compose up --build -d
```

### Step 4: Run Database Migrations

Initialize the PostgreSQL tables:

```bash
docker-compose exec backend python manage.py migrate
```

### Step 5: Access the Application

- **Frontend Dashboard:** http://localhost:5173
- **Backend API / Admin:** http://localhost:8000/admin

---

## 📈 How to Use the Tracking Snippet

To test the analytics ingestion, embed the following snippet into any standard HTML file. Open the HTML file in your browser, and interactions will be tracked in real-time.

```html
<script>
  (function () {
    window.InsightFlow = {
      // Replace with your actual workspace slug from the dashboard!
      workspaceSlug: "your-workspace-slug",

      track: function (eventName, payload = {}) {
        fetch(`http://localhost:8000/api/w/${this.workspaceSlug}/events/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ event_name: eventName, payload: payload }),
        }).then(() => console.log(`Tracked: ${eventName}`));
      },
    };

    // Track a page view immediately
    window.InsightFlow.track("page_view", { url: window.location.href });
  })();
</script>

<button onclick="InsightFlow.track('button_click', { id: 'test_btn' })">
  Test Analytics
</button>
```

---

## 🧹 Useful Commands

**View Backend Logs:**

```bash
docker-compose logs -f backend
```

**Clear Redis Cache** (If dashboard data goes stale during testing):

```bash
docker-compose exec redis redis-cli flushall
```

**Tear Down the Environment:**

```bash
docker-compose down
# Add -v to delete the database volumes entirely:
# docker-compose down -v
```
