---
name: concentrate-alerts
description: Choose and configure Concentrate AI account alerts for spend anomalies, error spikes, key limits or exhaustion, dormant keys, low or depleting balance, model usage reports, and dashboard snapshots. Use for operational notifications, scheduled reports, alert scope, email/SMS delivery, or cooldown behavior.
---

# Concentrate Alerts

Map the user's operational question to the narrowest documented alert, then configure it in the Concentrate alerts UI at the correct personal or organization scope.

## Workflow

1. Identify whether the user needs an immediate threshold, a forecast/trend, an anomaly, a health signal, a security signal, or a recurring report.
2. Choose the alert from [references/alert-catalog.md](references/alert-catalog.md).
3. Confirm personal versus organization scope and that the user's role can see the underlying data.
4. Configure delivery channels in **Settings → Notifications**. SMS requires a verified phone number.
5. For scheduled alerts, use only frequencies supported by that alert's official page. For reactive alerts, do not invent a schedule.
6. Explain that subscriptions are per user; coworkers must opt in separately even for the same organization.

## Boundaries

- Alerts are configured in the app, not through a documented public alerts API.
- Do not assume one user's organization alert enrolls other members.
- Do not promise exact evaluation timing beyond the official page. Cooldowns prevent repeated notifications for the same persistent condition.
- Do not treat a forecast alert and an immediate threshold alert as interchangeable.
