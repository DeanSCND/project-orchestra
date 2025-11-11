# Security Model & Threat Analysis

## Security Architecture

Project Orchestra implements defense-in-depth security with multiple layers:

### Layer 1: Authentication (Auth0)
- **Google OAuth 2.0** via Auth0
- **PKCE flow** for web applications
- **JWT access tokens** (1 hour expiry)
- **Refresh tokens** (httpOnly cookies)

### Layer 2: Network Security (Twingate)
- **Zero-trust network access** (no public ports)
- **Encrypted tunnels** (WireGuard-based)
- **Identity-based routing** (user → specific daemon)
- **Device posture checks** (optional MDM integration)

### Layer 3: Application Security (FastAPI)
- **JWT signature validation** (Auth0 public key)
- **Rate limiting** (10 msg/sec per connection)
- **Input validation** (Pydantic models)
- **CORS restrictions** (whitelist origins)

### Layer 4: Process Isolation (tmux)
- **Separate tmux sessions** per agent
- **Non-privileged user** (no root access)
- **File system permissions** (restricted to workspace)
- **Process tree monitoring** (detect escapes)

## Threat Model

### Threat 1: Unauthorized Access to Daemon
**Attack Vector:** Attacker obtains valid JWT token

**Mitigations:**
- Short token expiry (1 hour)
- Refresh token rotation
- IP whitelist (Twingate subnet only)
- Audit logging (all access attempts)

**Detection:**
- Unusual login patterns (geolocation)
- Multiple concurrent sessions
- High message rate

**Response:**
- Revoke refresh token
- Force re-authentication
- Alert security team

### Threat 2: Tmux Session Hijacking
**Attack Vector:** Attacker gains access to tmux socket

**Mitigations:**
- Non-privileged user runs tmux
- Socket permissions (0700)
- No shared sockets between users
- Session-specific environment isolation

**Detection:**
- Process tree anomalies
- Unexpected tmux attach attempts
- File permission changes

**Response:**
- Kill affected tmux sessions
- Audit system for compromise
- Rotate credentials

### Threat 3: Agent Escape from Tmux
**Attack Vector:** Malicious agent breaks out of tmux

**Mitigations:**
- Read-only file system (future)
- cgroup resource limits (future)
- AppArmor/SELinux profiles (future)
- Network egress filtering (future)

**Detection:**
- Process spawning outside tmux
- Unexpected network connections
- File system modifications outside workspace

**Response:**
- Kill agent process tree
- Quarantine affected workspace
- Forensic analysis

### Threat 4: Credential Leakage in Logs
**Attack Vector:** API keys logged in plain text

**Mitigations:**
- Structured logging with redaction
- Environment variables only (no hardcoded keys)
- Log rotation with encryption
- Access controls on log files

**Detection:**
- Grep logs for patterns (API_KEY, SECRET, PASSWORD)
- Automated scanning in CI/CD
- SIEM alerts on sensitive patterns

**Response:**
- Rotate leaked credentials immediately
- Purge logs containing secrets
- Review all recent commits

### Threat 5: Man-in-the-Middle Attack
**Attack Vector:** Attacker intercepts WebSocket traffic

**Mitigations:**
- HTTPS/WSS only (TLS 1.3)
- Certificate pinning (future)
- HSTS headers
- Twingate encryption layer

**Detection:**
- Certificate validation errors
- TLS handshake failures
- Unexpected certificate changes

**Response:**
- Terminate suspicious connections
- Investigate certificate authority
- Check for compromised CA certificates

## Security Best Practices

### For Developers

**DO:**
- ✅ Use environment variables for secrets
- ✅ Validate all user input with Pydantic
- ✅ Log security-relevant events
- ✅ Run with least privilege
- ✅ Keep dependencies updated

**DON'T:**
- ❌ Hardcode API keys in code
- ❌ Log sensitive data (tokens, passwords)
- ❌ Run daemon as root
- ❌ Disable security features for convenience
- ❌ Trust user input without validation

### For Operators

**DO:**
- ✅ Rotate JWT signing keys quarterly
- ✅ Review audit logs weekly
- ✅ Update Twingate connector regularly
- ✅ Monitor for anomalous behavior
- ✅ Backup audit logs offsite

**DON'T:**
- ❌ Share Auth0 credentials
- ❌ Disable audit logging
- ❌ Expose daemon on public IP
- ❌ Ignore security alerts
- ❌ Grant unnecessary permissions

## Compliance Considerations

### GDPR (EU Data Protection)
- **User consent:** Required for Auth0 Google OAuth
- **Data minimization:** Only store necessary user data (email, name)
- **Right to erasure:** Provide user data export/deletion
- **Data retention:** Delete audit logs after 30 days (configurable)

### SOC 2 (Security Controls)
- **Access controls:** JWT + Twingate + RBAC
- **Audit logging:** All security events logged
- **Encryption:** TLS in transit, encrypted logs at rest
- **Change management:** GitHub audit trail, PR reviews

### HIPAA (Healthcare Data)
⚠️ **Not currently compliant** - Would require:
- Business Associate Agreement (BAA) with Auth0
- Encrypted storage of all data at rest
- Additional access controls (MFA required)
- Enhanced audit logging (6+ year retention)

## Security Checklist

### Before Production Deployment

- [ ] Auth0 tenant configured with MFA
- [ ] Twingate connector deployed and healthy
- [ ] JWT signing keys rotated
- [ ] Secrets stored in environment (not code)
- [ ] Rate limiting enabled and tested
- [ ] Audit logging enabled
- [ ] Log rotation configured
- [ ] Security scan passed (no critical vulns)
- [ ] Penetration test completed
- [ ] Incident response plan documented

### Regular Security Maintenance

**Weekly:**
- [ ] Review audit logs for anomalies
- [ ] Check for dependency vulnerabilities (Dependabot)
- [ ] Verify backup integrity

**Monthly:**
- [ ] Review Auth0 user list (remove inactive)
- [ ] Check Twingate access logs
- [ ] Update dependencies (patch versions)

**Quarterly:**
- [ ] Rotate JWT signing keys
- [ ] Update major dependencies
- [ ] Security training for team
- [ ] Review/update threat model

**Annually:**
- [ ] Full security audit
- [ ] Penetration testing
- [ ] Review compliance requirements
- [ ] Update disaster recovery plan

## Incident Response Plan

### P0: Critical Security Incident
**Examples:** Credential leak, unauthorized access, data breach

**Response:**
1. **Immediate** (0-15 min):
   - Revoke all refresh tokens in Auth0
   - Disable affected user accounts
   - Kill all active daemon sessions
   - Notify security team

2. **Short-term** (15 min - 2 hours):
   - Rotate all credentials (API keys, JWT keys)
   - Review audit logs for scope
   - Isolate affected systems
   - Document timeline of events

3. **Long-term** (2+ hours):
   - Forensic analysis of logs
   - Patch vulnerabilities
   - Notify affected users (if applicable)
   - Post-mortem and remediation plan

### P1: Non-Critical Security Issue
**Examples:** Outdated dependency, misconfiguration

**Response:**
1. Create security issue in GitHub (private)
2. Assess severity and impact
3. Schedule fix in next sprint
4. Apply workaround if available
5. Monitor for exploitation attempts

## Security Contacts

**Report Security Issues:**
- Email: security@project-orchestra.dev (to be setup)
- PGP Key: [TBD]
- Expected response: 24 hours

**Do NOT:**
- Open public GitHub issues for security vulnerabilities
- Discuss security issues in public channels
- Attempt to exploit vulnerabilities in production

---

**Document Version:** 1.0  
**Last Security Review:** January 2025  
**Next Review Due:** April 2025
