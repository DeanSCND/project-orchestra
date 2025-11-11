# Orchestra Daemon API Reference

## Base URL

```
http://localhost:8080  (Development)
https://daemon.twingate (Production via Twingate)
```

## Authentication

All API requests require JWT authentication:

**WebSocket:**
```
wss://daemon/ws/observe?token=<JWT_TOKEN>
```

**HTTP:**
```
Authorization: Bearer <JWT_TOKEN>
```

---

## REST API Endpoints

### Health Check

**GET /api/health**

Check daemon health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "uptime_seconds": 3600
}
```

---

### Spawn Agent

**POST /api/agents/spawn**

Create a new agent session in tmux.

**Request Body:**
```json
{
  "agent_type": "droid",
  "working_dir": "/workspace/project",
  "env": {
    "PROJECT_NAME": "my-app"
  }
}
```

**Response:**
```json
{
  "session_id": "sess-droid-a1b2c3d4",
  "agent_type": "droid",
  "status": "running",
  "tmux_session": "agent-droid-a1b2c3d4",
  "created_at": "2025-01-10T12:00:00Z"
}
```

**Status Codes:**
- `201` - Created successfully
- `400` - Invalid agent_type
- `500` - Failed to spawn session

---

### List Agents

**GET /api/agents**

List all active agent sessions.

**Query Parameters:**
- `status` - Filter by status (running, idle, error)
- `agent_type` - Filter by type (claude, droid, cursor, aider)

**Response:**
```json
{
  "agents": [
    {
      "session_id": "sess-claude-xyz",
      "agent_type": "claude",
      "status": "running",
      "created_at": "2025-01-10T11:00:00Z",
      "last_activity": "2025-01-10T12:00:00Z"
    }
  ],
  "total": 1
}
```

---

### Get Agent Details

**GET /api/agents/{session_id}**

Get details for specific agent session.

**Response:**
```json
{
  "session_id": "sess-droid-a1b2c3d4",
  "agent_type": "droid",
  "status": "running",
  "working_dir": "/workspace/project",
  "tmux_session": "agent-droid-a1b2c3d4",
  "tmux_pane": "%1",
  "created_at": "2025-01-10T12:00:00Z",
  "memory_mb": 250,
  "cpu_percent": 5.2
}
```

---

### Kill Agent

**DELETE /api/agents/{session_id}**

Terminate an agent session.

**Response:**
```json
{
  "session_id": "sess-droid-a1b2c3d4",
  "status": "terminated",
  "terminated_at": "2025-01-10T12:30:00Z"
}
```

**Status Codes:**
- `200` - Terminated successfully
- `404` - Session not found

---

### Delegate Task

**POST /api/delegate**

Delegate a task from primary agent to secondary agent.

**Request Body:**
```json
{
  "agent_type": "droid",
  "task": "Implement user authentication with JWT",
  "context": {
    "files": ["src/auth.py", "src/models.py"],
    "requirements": ["Use bcrypt for hashing"],
    "tests_required": true
  },
  "timeout_ms": 300000
}
```

**Response:**
```json
{
  "ticket_id": "ticket-uuid-1234",
  "session_id": "sess-droid-a1b2c3d4",
  "status": "pending",
  "created_at": "2025-01-10T12:00:00Z"
}
```

---

### Get Task Status

**GET /api/tasks/{ticket_id}**

Get status of delegated task.

**Response:**
```json
{
  "ticket_id": "ticket-uuid-1234",
  "status": "completed",
  "agent": "droid",
  "result": {
    "files_modified": ["src/auth.py", "src/models.py"],
    "tests_passed": true,
    "message": "Authentication module implemented with JWT"
  },
  "started_at": "2025-01-10T12:00:00Z",
  "completed_at": "2025-01-10T12:05:00Z",
  "duration_ms": 300000
}
```

**Status Values:**
- `pending` - Task queued, waiting for agent
- `running` - Agent is executing task
- `completed` - Task finished successfully
- `failed` - Task failed with error
- `timeout` - Task exceeded timeout

---

## WebSocket API

### Connection

**URL:** `wss://daemon/ws/observe?token=<JWT>`

**Connection Flow:**
1. Client opens WebSocket with JWT in query param
2. Server validates JWT
3. Server accepts connection or closes with policy violation
4. Client sends/receives JSON messages

---

### Message Types

#### Client → Server Messages

##### Subscribe to Terminal

```json
{
  "type": "subscribe_terminal",
  "session_id": "sess-droid-a1b2c3d4"
}
```

##### Unsubscribe from Terminal

```json
{
  "type": "unsubscribe_terminal",
  "session_id": "sess-droid-a1b2c3d4"
}
```

##### Send User Message

```json
{
  "type": "user_message",
  "content": "Build a REST API with authentication",
  "session_id": "sess-claude-primary"
}
```

##### Heartbeat Ping

```json
{
  "type": "ping"
}
```

---

#### Server → Client Messages

##### Terminal Output

```json
{
  "type": "terminal_output",
  "session_id": "sess-droid-a1b2c3d4",
  "data": "> droid\nAnalyzing task...\nCreating auth module...\n",
  "timestamp": 1704067200000
}
```

##### Claude Response

```json
{
  "type": "claude_response",
  "content": "I'll delegate this task to Droid for backend implementation.",
  "actions": [
    {
      "type": "approve_plan",
      "button_text": "Approve",
      "task_ids": [1, 2, 3]
    }
  ]
}
```

##### Task Update

```json
{
  "type": "task_update",
  "task_id": 1,
  "agent": "droid",
  "status": "running",
  "elapsed_ms": 45000
}
```

##### Agent Status Change

```json
{
  "type": "agent_status",
  "session_id": "sess-droid-a1b2c3d4",
  "status": "idle",
  "last_activity": "2025-01-10T12:00:00Z"
}
```

##### Error

```json
{
  "type": "error",
  "error_code": "AGENT_CRASHED",
  "message": "Agent session terminated unexpectedly",
  "session_id": "sess-droid-a1b2c3d4"
}
```

##### Heartbeat Pong

```json
{
  "type": "pong"
}
```

---

## Error Codes

### HTTP Status Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 400 | Bad Request | Invalid request body, missing required fields |
| 401 | Unauthorized | Invalid or expired JWT token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Session/ticket not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Daemon overloaded or restarting |

### Application Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `INVALID_TOKEN` | JWT validation failed | Refresh token and retry |
| `SESSION_NOT_FOUND` | Agent session doesn't exist | Check session_id |
| `AGENT_SPAWN_FAILED` | Failed to create tmux session | Check tmux availability |
| `AGENT_CRASHED` | Agent process terminated | Check agent logs |
| `TASK_TIMEOUT` | Task exceeded timeout | Increase timeout or optimize task |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait and retry with backoff |

---

## Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/agents/spawn` | 10 requests | 1 minute |
| `/api/delegate` | 100 requests | 1 minute |
| WebSocket messages | 600 messages | 1 minute (10/sec) |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704067260
```

---

## Code Examples

### Python Client

```python
import asyncio
import websockets
import json

async def connect_orchestra(token: str):
    uri = f"ws://localhost:8080/ws/observe?token={token}"
    
    async with websockets.connect(uri) as ws:
        # Subscribe to primary agent terminal
        await ws.send(json.dumps({
            "type": "subscribe_terminal",
            "session_id": "sess-claude-primary"
        }))
        
        # Receive terminal output
        async for message in ws:
            data = json.loads(message)
            
            if data["type"] == "terminal_output":
                print(f"[{data['session_id']}] {data['data']}")
            elif data["type"] == "error":
                print(f"Error: {data['message']}")

# Usage
token = "your_jwt_token_here"
asyncio.run(connect_orchestra(token))
```

### JavaScript/TypeScript Client

```typescript
class OrchestraClient {
  private ws: WebSocket;
  
  constructor(token: string) {
    this.ws = new WebSocket(`ws://localhost:8080/ws/observe?token=${token}`);
    
    this.ws.onopen = () => {
      console.log('Connected to Orchestra daemon');
      
      // Subscribe to terminal
      this.send({
        type: 'subscribe_terminal',
        session_id: 'sess-claude-primary'
      });
    };
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };
  }
  
  send(data: object) {
    this.ws.send(JSON.stringify(data));
  }
  
  private handleMessage(data: any) {
    switch (data.type) {
      case 'terminal_output':
        console.log(`[${data.session_id}] ${data.data}`);
        break;
      case 'claude_response':
        console.log(`Claude: ${data.content}`);
        break;
      case 'error':
        console.error(`Error: ${data.message}`);
        break;
    }
  }
}

// Usage
const client = new OrchestraClient('your_jwt_token_here');
```

---

## Changelog

### v0.1.0 (January 2025)
- Initial API specification
- WebSocket support for terminal streaming
- Basic agent lifecycle management
- Task delegation protocol

---

**Document Version:** 1.0  
**Last Updated:** January 2025  
**API Version:** v0.1.0
