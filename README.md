# Team members:

- Juan Camilo Valencia - 2259459
- Luis Carabalí Rivera - 2410006

# 👽 Alien Immigration Control System - Saga Pattern Simulation

This project simulates the **Saga Pattern** for an Alien Immigration Control System using microservices communicating over HTTP via REST. The architecture follows a centralized orchestrator model to coordinate the distributed transaction.

Each service uses in-memory storage, making it ideal for quick testing and learning environments.

---

## 🚀 Microservices Overview

| Service                     | Port | Description                                   | Compensation Action(s)                     |
| --------------------------- | ---- | --------------------------------------------- | ------------------------------------------ |
| verification_service        | 5001 | Verifies alien identity (tentacle scan)       | Logged (Mainly GC Notification)            |
| tech_confiscation_service   | 5002 | Confiscates alien tech (with random failure)  | Return Tech                                |
| quarantine_service          | 5003 | Puts alien through quarantine                 | Undo Quarantine Log                        |
| location_assignment_service | 5004 | Assigns alien to a random Earth city          | Remove From City List                      |
| galactic_command_service    | 5005 | Notifies Galactic Command of failures         | N/A                                        |
| orchestrator                | 5000 | Coordinates the immigration flow (Saga logic) | Calls compensation endpoints + Notifies GC |

---

## 🧱 Technologies Used

- Python + Flask (`verification_service`, `quarantine_service`, `location_assignment_service`, `galactic_command_service`, `orchestrator`)
- Node.js + Express (`tech_confiscation_service`)
- Docker + Docker Compose

---

## 📦 How to Run It

```bash
# Ensure you are in the root directory (taller-saga)
docker-compose up --build -d # Run in detached mode
```

To view logs: `docker-compose logs -f`
To stop: `docker-compose down`

---

## 🧪 Testing Each Microservice (Example)

Use `curl` or a tool like Postman. Replace `Zorp_7` with any alien ID.

### 👽 Verification Service (http://localhost:5001)

```bash
# Verify Alien
curl -X POST http://localhost:5001/verify -H "Content-Type: application/json" -d '{"alien_id": "Zorp_7"}'

# View Verifications
curl http://localhost:5001/verifications
```

### 💥 Tech Confiscation Service (http://localhost:5002)

```bash
# Confiscate Tech (may fail randomly)
curl -X POST http://localhost:5002/confiscate -H "Content-Type: application/json" -d '{"alien_id": "Zorp_7"}'

# Return Tech (Compensation)
curl -X POST http://localhost:5002/return-tech -H "Content-Type: application/json" -d '{"alien_id": "Zorp_7"}'

# View Confiscated Items
curl http://localhost:5002/confiscated-items
```

### 🦠 Quarantine Service (http://localhost:5003)

```bash
# Start Quarantine
curl -X POST http://localhost:5003/start-quarantine -H "Content-Type: application/json" -d '{"alien_id": "Zorp_7"}'

# Undo Log (Compensation)
curl -X POST http://localhost:5003/undo-quarantine-log -H "Content-Type: application/json" -d '{"alien_id": "Zorp_7"}'

# View Logs
curl http://localhost:5003/quarantine-logs
```

### 🏙️ Location Assignment Service (http://localhost:5004)

```bash
# Assign City
curl -X POST http://localhost:5004/assign-city -H "Content-Type: application/json" -d '{"alien_id": "Zorp_7"}'

# Remove From City (Compensation)
curl -X POST http://localhost:5004/remove-from-city -H "Content-Type: application/json" -d '{"alien_id": "Zorp_7"}'

# View Assignments
curl http://localhost:5004/assignments
```

### 🚓 Galactic Command Service (http://localhost:5005)

```bash
# Notify Failure (Called by Orchestrator)
curl -X POST http://localhost:5005/notify-failure -H "Content-Type: application/json" -d '{"alien_id": "Zorp_7", "reason": "Test notification"}'
# Check service logs for output
```

### 🤖 Orchestrator (http://localhost:5000)

```bash
# Process a full immigration application
curl -X POST http://localhost:5000/process-immigration -H "Content-Type: application/json" -d '{"alien_id": "Glar_Blar"}'
```

_Observe the orchestrator and individual service logs to see the flow and potential compensations._

---

## 🔄 Saga Flow Diagram (Orchestration)

```
Applicant
  |
  v
Orchestrator --> Verification Service (/verify)
      |
      v
      --> Tech Confiscation Service (/confiscate)   <-- may fail randomly
      |
      v
      --> Quarantine Service (/start-quarantine)
      |
      v
      --> Location Assignment Service (/assign-city)
      |
      v
      On Error: Compensation (reverse order) + Notify Galactic Command
```

---
