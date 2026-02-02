# Security Policy

DONGOL takes security seriously. Made in Indonesia 🇮🇩 for the world.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

## Reporting a Vulnerability

We appreciate your efforts to responsibly disclose your findings.

### Reporting Process

1. **Email**: security@dongol.io
2. **Subject**: `[SECURITY] Brief description`
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **24 hours**: Acknowledgment
- **72 hours**: Initial assessment
- **7 days**: Detailed response with plan
- **30 days**: Fix released (critical)
- **90 days**: Fix released (non-critical)

### What to Expect

- Confidential treatment of your report
- Credit in security advisories (if desired)
- No legal action for good-faith reports

## Security Best Practices

### When Using DONGOL

1. **Keep Updated** - Always use the latest version
2. **Validate Input** - Sanitize data before processing
3. **Use Virtual Environments** - Isolate dependencies
4. **Review Plugins** - Only use trusted plugins
5. **Monitor Resources** - Set appropriate limits

### For Contributors

1. **No Secrets** - Never commit credentials
2. **Dependency Scanning** - Keep dependencies updated
3. **Code Review** - All changes require review
4. **Testing** - Include security tests

## Known Security Considerations

### File System Access

DONGOL can access the file system. Use with caution:

```python
# Safe: Only access allowed directories
engine.configure(allowed_paths=["/safe/path"])

# Use dry-run mode
organizer = DriveOrganizer(dry_run=True)
```

### Code Execution

The `run` command can execute code:

```bash
# Safe: Use restricted types only
dongol run "print('hello')" --type python --safe-mode
```

### Network Access

API server listens on network interfaces:

```bash
# Production: Bind to localhost only
dongol-server --host 127.0.0.1

# Use HTTPS in production
```

## Vulnerability Disclosure Policy

We follow a 90-day disclosure timeline:

1. Report received
2. Issue confirmed (within 7 days)
3. Fix developed and tested
4. Fix released
5. Public disclosure (after 90 days or sooner with mutual agreement)

## Hall of Fame

We thank the following security researchers:

- *Your name could be here*

## Contact

- **Security Team**: security@dongol.io
- **PGP Key**: [Download](https://dongol.io/security-key.asc)
- **Maintainer**: Ardellio Satria Anindito

---

*Secure by design. Made with ❤️ in Indonesia.*
