# Alert catalog

Official source: [Alerts overview](https://concentrate.ai/docs/alerts/overview).

| Need | Alert | Mode | Official guide |
|---|---|---|---|
| Balance is below a fixed dollar threshold | Low balance | Reactive | [Guide](https://concentrate.ai/docs/alerts/low-balance) |
| Balance is trending toward zero | Balance depletion | Scheduled | [Guide](https://concentrate.ai/docs/alerts/balance-depletion) |
| A key crossed a percentage of its usage cap | Key limit | Reactive | [Guide](https://concentrate.ai/docs/alerts/key-limit) |
| A key is forecast to exhaust its cap | Key exhaustion | Scheduled | [Guide](https://concentrate.ai/docs/alerts/key-exhaustion) |
| Spend deviated suddenly from normal | Anomalous spend | Scheduled | [Guide](https://concentrate.ai/docs/alerts/anomalous-spend) |
| Error rate climbed above a threshold | Error rate spike | Scheduled | [Guide](https://concentrate.ai/docs/alerts/error-rate-spike) |
| A long-inactive key resumed activity | Dormant key | Scheduled | [Guide](https://concentrate.ai/docs/alerts/dormant-key) |
| Recurring model/provider cost breakdown | Model usage report | Scheduled | [Guide](https://concentrate.ai/docs/alerts/model-usage-report) |
| Recurring account summary | Dashboard snapshot | Scheduled | [Guide](https://concentrate.ai/docs/alerts/dashboard-snapshot) |

Alerts are per user. Personal alerts cover that user's account; organization alerts cover an organization the user belongs to, subject to role visibility. Organization configuration subscribes only the configuring user.

Delivery is email and/or SMS, selected in notification settings. Scheduled frequencies differ by alert; the official overview says most default to daily at 2:00 AM in the user's local timezone when no custom schedule is set. Reactive low-balance and key-limit alerts fire when their conditions are met instead of using a schedule.
