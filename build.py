#!/usr/bin/env python3
import json
import os
import html as html_lib
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "errors.json").read_text())

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — UnitCore API errors</title>
<meta name="description" content="{summary}">
<link rel="canonical" href="https://docs.unitcore.app/errors/{slug}">
<link rel="stylesheet" href="/style.css">
</head>
<body class="error-page">
<header class="site-header">
  <div class="container">
    <a class="logo" href="/">UnitCore <span>docs</span></a>
    <nav>
      <a href="/">Errors</a>
      <a href="{source_url}">Source</a>
    </nav>
  </div>
</header>

<main class="container">
  <p class="breadcrumb"><a href="/">Errors</a> &nbsp;/&nbsp; {group_title}</p>
  <div class="header-row">
    <h1>{title}</h1>
    <span class="badge badge-status-{status}">{status}</span>
  </div>
  <p class="code-text"><code>{code}</code></p>
  <p class="summary">{summary}</p>

  <h2>Common causes</h2>
  <ul>
{causes}
  </ul>

  <h2>How to resolve</h2>
  <ul>
{resolution}
  </ul>

  <p class="source-link">
    Canonical definition: <a href="{source_url}"><code>ApiErrorCodes.{const_name}</code></a> in <code>unitcore-crm/backend/src/Kernel/Api/ErrorCodes/ApiErrorCodes.cs</code>.
  </p>
</main>

<footer class="site-footer">
  <div class="container">
    <p>Source of truth: <a href="{source_url}">ApiErrorCodes.cs</a></p>
  </div>
</footer>
</body>
</html>
"""

CONST_MAP = {
    "validation.failed": "ValidationFailed",
    "validation.field_required": "ValidationFieldRequired",
    "validation.field_invalid": "ValidationFieldInvalid",
    "validation.argument": "ValidationArgument",
    "resource.not_found": "NotFound",
    "resource.duplicate": "Duplicate",
    "resource.constraint_violation": "ConstraintViolation",
    "resource.concurrency_conflict": "ConcurrencyConflict",
    "resource.invalid_state_transition": "InvalidStateTransition",
    "auth.unauthorized": "AuthUnauthorized",
    "auth.forbidden": "AuthForbidden",
    "auth.invalid_credentials": "AuthInvalidCredentials",
    "auth.token_expired": "AuthTokenExpired",
    "auth.token_invalid": "AuthTokenInvalid",
    "auth.account_locked": "AuthAccountLocked",
    "auth.mfa_required": "AuthMfaRequired",
    "auth.site_required": "AuthSiteRequired",
    "auth.session_invalid": "AuthSessionInvalid",
    "auth.invalid_password": "AuthInvalidPassword",
    "auth.same_password": "AuthSamePassword",
    "auth.registration_disabled": "AuthRegistrationDisabled",
    "auth.registration_failed": "AuthRegistrationFailed",
    "site.context_mismatch": "SiteContextMismatch",
    "operation.invalid": "InvalidOperation",
    "service.unavailable": "ServiceUnavailable",
    "service.database_error": "DatabaseError",
    "service.internal_error": "InternalError",
    "cluster.at_capacity": "ClusterAtCapacity",
    "billing.payment_required": "PaymentRequired",
    "backup.in_progress": "BackupInProgress",
    "backup.not_found": "BackupNotFound",
    "backup.file_not_found": "BackupFileNotFound",
    "backup.test_failed": "BackupTestFailed",
    "backup.insufficient_space": "BackupInsufficientSpace",
    "backup.invalid_status": "BackupInvalidStatus",
    "backup.restore_failed": "BackupRestoreFailed",
    "backup.pg_restore_error": "BackupPgRestoreError",
    "backup.sql_restore_error": "BackupSqlRestoreError",
    "backup.db_connection_error": "BackupDbConnectionError",
    "auth.apikey_insufficient_permissions": "AuthApiKeyInsufficientPermissions",
    "auth.agent_key_unavailable": "AuthAgentKeyUnavailable",
    "auth.agent_key_invalid": "AuthAgentKeyInvalid",
    "auth.agent_key_no_site": "AuthAgentKeyNoSite",
    "auth.agent_key_path_forbidden": "AuthAgentKeyPathForbidden",
    "auth.portal_audience_not_allowed": "AuthPortalAudienceNotAllowed",
    "auth.endpoint_requires_permission_config": "AuthEndpointRequiresPermissionConfig",
    "rate.limit_exceeded": "RateLimitExceeded",
    "cors.origin_not_allowed": "CorsOriginNotAllowed",
    "network.invalid_host": "NetworkInvalidHost",
    "network.websocket_required": "NetworkWebSocketRequired",
    "service.too_many_connections": "ServiceTooManyConnections",
    "feature.not_implemented": "FeatureNotImplemented",
    "validation.invalid_dev_bypass": "ValidationInvalidDevBypass",
    "validation.locale_required": "ValidationLocaleRequired",
    "validation.site_required": "ValidationSiteRequired",
    "scraping.missing_idempotency_key": "ScrapingMissingIdempotencyKey",
    "scraping.body_too_large": "ScrapingBodyTooLarge",
    "scraping.missing_tenant_id": "ScrapingMissingTenantId",
    "scraping.invalid_tenant_id": "ScrapingInvalidTenantId",
    "scraping.missing_tenant_header": "ScrapingMissingTenantHeader",
    "scraping.malformed_payload": "ScrapingMalformedPayload",
    "scraping.empty_payload": "ScrapingEmptyPayload",
    "scraping.invalid_signature": "ScrapingInvalidSignature",
    "scraping.unknown_job": "ScrapingUnknownJob",
}

def escape(s):
    return html_lib.escape(s, quote=True)

def li_list(items):
    return "\n".join("    <li>" + escape(i) + "</li>" for i in items)

count = 0
for g in DATA["groups"]:
    for c in g["codes"]:
        slug = c["code"].replace(".", "/")
        out_dir = ROOT / "errors" / Path(slug)
        out_dir.mkdir(parents=True, exist_ok=True)
        body = TEMPLATE.format(
            title=escape(c["title"]),
            summary=escape(c["summary"]),
            slug=slug,
            group_title=escape(g["title"]),
            status=c["status"],
            code=escape(c["code"]),
            causes=li_list(c["causes"]),
            resolution=li_list(c["resolution"]),
            source_url=DATA["sourceUrl"],
            const_name=CONST_MAP.get(c["code"], "Unknown"),
        )
        (out_dir / "index.html").write_text(body)
        count += 1

print(f"Generated {count} error pages.")
