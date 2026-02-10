# CampusConnect - Campus Event Management Mobile App

A full-stack mobile application for managing campus events, built with React Native (Expo) and FastAPI.

## 📱 Features

- **User Authentication** - Register, login, and secure JWT-based authentication
- **Event Management** - Create, view, update, and delete campus events
- **Event Participation** - Join and leave events with capacity tracking
- **Real-time Chat** - WebSocket-based chat for each event
- **Offline Support** - Local caching with network state management
- **Secure Storage** - Encrypted local storage for sensitive data

---

## 🏗️ Project Structure

```
CampusConnect/
├── mobile_fixed_v2/          # React Native mobile app (Expo)
│   ├── src/
│   │   ├── config/           # API configuration
│   │   ├── screens/          # UI screens
│   │   ├── store/            # State management (Zustand)
│   │   └── ...
│   ├── App.tsx               # Main app component
│   ├── package.json          # Dependencies
│   └── app.json              # Expo configuration
│
└── backend/                  # FastAPI backend
    ├── app/
    │   ├── api/              # API endpoints
    │   ├── core/             # Security & config
    │   ├── db/               # Database models
    │   ├── models/           # SQLAlchemy models
    │   ├── schemas/          # Pydantic schemas
    │   ├── services/         # Business logic
    │   └── websocket/        # WebSocket manager
    ├── docker-compose.yml    # Docker setup
    ├── Dockerfile
    └── requirements.txt      # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

**For Mobile App:**
- Node.js (v16 or higher)
- npm or yarn
- Expo Go app on your iPhone/Android
- Expo CLI: `npm install -g expo-cli`

**For Backend:**
- Docker & Docker Compose
- OR Python 3.10+, PostgreSQL, Redis (for manual setup)

---

## 📱 Mobile App Setup

### 1. Install Dependencies

```bash
cd mobile_fixed_v2

# Delete old dependencies (if any)
rm -rf node_modules
rm package-lock.json

# Install fresh
npm install
```

### 2. Fix Expo SDK Version Compatibility

```bash
# This ensures all packages match Expo SDK 54
npx expo install --fix
```

### 3. Configure API Endpoint

Edit `src/config/api.ts`:

```typescript
const API_BASE_URL = __DEV__ 
  ? 'https://your-ngrok-url.ngrok-free.dev/api/v1'  // Use ngrok URL (see backend setup)
  : 'https://your-production-api.com/api/v1';
```

### 4. Start Development Server

```bash
npx expo start -c
```

The `-c` flag clears the cache (important!)

### 5. Run on Your Phone

1. Install **Expo Go** from App Store (iOS) or Play Store (Android)
2. Scan the QR code from terminal
3. App will load on your phone

---

## 🔧 Backend Setup

### Option A: Using Docker (Recommended)

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Start all services (PostgreSQL, Redis, Backend):**
```bash
docker-compose up --build
```

3. **Verify it's running:**
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- Status: http://localhost:8000/api/v1/status

### Option B: Manual Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up PostgreSQL database:**
```sql
CREATE DATABASE campusconnect;
```

3. **Set up Redis:**
```bash
# Install and start Redis
redis-server
```

4. **Configure environment variables:**
Create `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost/campusconnect
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
```

5. **Run the server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 Connecting Mobile App to Backend

### Problem: Mobile app can't reach localhost

Your iPhone/Android can't access `localhost` on your computer. Solutions:

### Solution 1: ngrok (Easiest for Development) ⭐ RECOMMENDED

1. **Download ngrok:** https://ngrok.com/download

2. **Start ngrok tunnel:**
```bash
ngrok http 8000
```

3. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.dev`)

4. **Update mobile app** `src/config/api.ts`:
```typescript
const API_BASE_URL = __DEV__ 
  ? 'https://abc123.ngrok-free.dev/api/v1'
  : 'https://abc123.ngrok-free.dev/api/v1';
```

5. **Restart Expo:**
```bash
npx expo start -c
```

**Note:** Keep ngrok running! If you close it, the URL stops working.

### Solution 2: Use Your Computer's IP (Same WiFi Required)

1. **Find your computer's IP:**

**Windows:**
```cmd
ipconfig
```
Look for IPv4 Address (e.g., `192.168.1.100`)

**Mac/Linux:**
```bash
ifconfig
```

2. **Update mobile app:**
```typescript
const API_BASE_URL = 'http://192.168.1.100:8000/api/v1';
```

3. **Ensure both devices are on the SAME WiFi network**

4. **Allow through firewall (Windows):**
```cmd
netsh advfirewall firewall add rule name="Docker Backend" dir=in action=allow protocol=TCP localport=8000
```

---

## 🔐 Key Technologies

### Mobile App
- **React Native** (via Expo SDK 54)
- **TypeScript**
- **Zustand** - State management
- **Expo SecureStore** - Encrypted storage
- **Expo Network** - Network status
- **React Navigation** - Navigation
- **Axios** - HTTP client

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Redis** - WebSocket pub/sub
- **JWT** - Authentication
- **WebSockets** - Real-time chat
- **Docker** - Containerization

---

## 📋 API Endpoints

### Authentication
- `POST /login/access-token` - Login
- `POST /users/` - Register new user
- `GET /users/me` - Get current user

### Events
- `GET /events/` - List all events
- `POST /events/` - Create event
- `GET /events/{id}` - Get event details
- `PUT /events/{id}` - Update event
- `DELETE /events/{id}` - Delete event
- `POST /events/{id}/join` - Join event
- `POST /events/{id}/leave` - Leave event

### Chat
- `WS /ws/chat/{event_id}` - WebSocket chat connection

---

## 🐛 Troubleshooting

### Issue: "Invariant Violation: TurboModuleRegistry" error

**Cause:** Package version mismatch with Expo SDK

**Solution:**
```bash
npx expo install --fix
npx expo start -c
```

On iPhone: Force close Expo Go → Clear cache → Reopen

### Issue: Login/Register doesn't work

**Check:**
1. Backend is running: `http://localhost:8000/api/v1/status`
2. Mobile app API URL is correct in `src/config/api.ts`
3. ngrok is running (if using ngrok)
4. Check Expo terminal for error messages
5. Check backend logs: `docker-compose logs -f`

### Issue: "Network Error" or backend not receiving requests

**Causes:**
- Backend not accessible from phone
- Wrong API URL in `api.ts`
- Firewall blocking port 8000
- Phone and computer on different WiFi networks

**Solution (Use ngrok):**
1. Download ngrok
2. Run `ngrok http 8000`
3. Copy the HTTPS URL
4. Update `src/config/api.ts` with the ngrok URL
5. Restart Expo: `npx expo start -c`

**Alternative (Same WiFi):**
1. Get your computer's IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Allow through firewall:
```cmd
netsh advfirewall firewall add rule name="Docker Backend" dir=in action=allow protocol=TCP localport=8000
```
3. Update `src/config/api.ts` with your IP: `http://192.168.x.x:8000/api/v1`
4. Ensure phone and laptop on SAME WiFi

### Issue: Old code still running after fixes

**Solution:**
```bash
# Delete everything
rm -rf node_modules
rm package-lock.json
rm -rf .expo

# Fresh install
npm install
npx expo start -c
```

On iPhone: 
1. Force close Expo Go (swipe up, close app)
2. Shake phone → Clear cache
3. Close and reopen Expo Go
4. Scan QR code again

### Issue: Docker containers not starting

**Check:**
```bash
docker ps  # See running containers
docker-compose logs -f  # View logs
```

**Restart Docker:**
```bash
docker-compose down
docker-compose up --build
```

---

## 🔑 Important Notes

### Expo Go Limitations

This app uses **Expo Go**, which has limitations:
- ✅ Works with: `expo-secure-store`, `expo-network`, and other Expo SDK packages
- ❌ Doesn't work with: Native modules like `@react-native-async-storage/async-storage`

If you see native module errors, it means a non-Expo package was added. Use `npx expo install --fix` to get compatible versions.

### File Organization

**Mobile and Backend DO NOT need to be in the same folder!** They communicate over HTTP/WebSockets. You can have:
```
Desktop/
├── my-mobile-app/     # Mobile app
└── somewhere-else/
    └── my-backend/    # Backend
```

As long as the mobile app knows the backend URL, it will work.

### Development vs Production

**Development:**
- Uses ngrok or local IP
- CORS allows all origins
- Database runs in Docker

**Production (when you deploy):**
- Deploy backend to cloud (Heroku, Railway, AWS, etc.)
- Update mobile app with production API URL
- Configure proper CORS origins
- Use production database

---

## 📦 Dependencies Reference

### Mobile App Key Dependencies

```json
{
  "expo": "~54.0.0",
  "expo-secure-store": "~15.0.8",
  "expo-network": "~8.0.8",
  "react-native": "0.81.5",
  "zustand": "^4.4.7",
  "axios": "^1.6.2",
  "@react-navigation/native": "^6.1.9",
  "@react-navigation/stack": "^6.3.20",
  "@react-navigation/bottom-tabs": "^6.5.11"
}
```

### Backend Key Dependencies

```txt
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
redis>=5.0.0
```

---

## 🎯 Quick Start Guide

### Step-by-Step for Complete Setup

1. **Start Backend:**
```bash
cd backend
docker-compose up --build
```

2. **Start ngrok (in new terminal):**
```bash
ngrok http 8000
```
Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.dev`)

3. **Update Mobile App:**
Edit `mobile_fixed_v2/src/config/api.ts`:
```typescript
const API_BASE_URL = 'https://abc123.ngrok-free.dev/api/v1';
```

4. **Install Mobile Dependencies:**
```bash
cd mobile_fixed_v2
npm install
npx expo install --fix
```

5. **Start Mobile App:**
```bash
npx expo start -c
```

6. **Run on Phone:**
- Open Expo Go
- Scan QR code
- Test registration/login

---

## 📝 Common Commands Cheat Sheet

### Mobile App
```bash
# Install dependencies
npm install

# Fix Expo SDK versions
npx expo install --fix

# Start with cache clear
npx expo start -c

# Clear everything and start fresh
rm -rf node_modules package-lock.json .expo
npm install
npx expo start -c
```

### Backend
```bash
# Start with Docker
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Check running containers
docker ps

# Restart everything
docker-compose down
docker-compose up --build
```

### ngrok
```bash
# Start tunnel
ngrok http 8000

# Keep this terminal open!
# Every time you restart ngrok, you get a new URL
```

### Network Troubleshooting
```bash
# Windows: Find your IP
ipconfig

# Windows: Allow port through firewall
netsh advfirewall firewall add rule name="Docker Backend" dir=in action=allow protocol=TCP localport=8000

# Check what's running on port 8000
netstat -an | findstr :8000

# Mac/Linux: Find your IP
ifconfig
```

---

## 🔍 Verification Checklist

Before running the app, verify:

**Backend:**
- [ ] Docker containers running: `docker ps`
- [ ] Can access http://localhost:8000/api/v1/status
- [ ] ngrok tunnel active (if using ngrok)

**Mobile App:**
- [ ] Dependencies installed: `npm install` completed
- [ ] SDK versions fixed: `npx expo install --fix` ran
- [ ] Correct API URL in `src/config/api.ts`
- [ ] No native module errors

**Network:**
- [ ] Phone and laptop on same WiFi (if not using ngrok)
- [ ] Firewall allows port 8000 (if not using ngrok)
- [ ] Can access backend from phone's Safari browser

---

## 👥 Support & Debugging

If you encounter issues:

1. **Check Backend Logs:**
```bash
docker-compose logs -f
```

2. **Check Mobile App Terminal:**
Look for red error messages in the Expo terminal

3. **Test Backend Manually:**
Open in browser: `http://localhost:8000/api/v1/docs`
Try the endpoints in Swagger UI

4. **Verify API Connection:**
Open Safari on iPhone and go to your backend URL

5. **Clear All Caches:**
```bash
# Mobile
rm -rf node_modules .expo package-lock.json
npm install
npx expo start -c

# Phone: Force close Expo Go, clear cache, reopen
```

---

## 🚀 Deployment (Production)

### Backend Deployment Options:

1. **Railway** (Easiest)
   - Connect GitHub repo
   - Auto-deploys on push
   - Provides PostgreSQL & Redis
   - Free tier available

2. **Heroku**
   - `git push heroku main`
   - Add PostgreSQL & Redis addons

3. **AWS/DigitalOcean**
   - More control, more setup
   - Use Docker Compose

### Mobile App Deployment:

1. **Build for iOS:**
```bash
expo build:ios
```

2. **Build for Android:**
```bash
expo build:android
```

3. **Submit to stores:**
```bash
expo upload:ios
expo upload:android
```

---

## 📄 License

This project is for educational purposes.

---

## 🎉 Credits

Built with:
- React Native (Expo)
- FastAPI
- PostgreSQL
- Redis
- Docker

---

**Happy Coding! 🚀**

For questions or issues, refer to the troubleshooting section above.