# `features/_dialer/projection.py`

**Purpose:** Public and live snapshots.

## Functions
### `crm_catalog` (line 11)
_Lead rows plus derived pool, timezone counts, and summary counts._

**Pseudocode:**
- Set leads to IfExp.
- Set pool_status to resolve_pool_status(...).
- Set business_type to a boolean condition.
- Set groups to state.crm.timezone_groups(...).
- Set pool to calls._pool_leads(...).
- Set busy to calls._busy_lead_ids(...).
- Set dialer_pool to global_dialer_pool(...).
- Set pipeline_revision to getattr(...).

**Calls →**
1. `state.crm.snapshot`
2. `shared.dial_policy.resolve_pool_status`
3. `features._dialer.projection.getattr`
4. `features._dialer.projection.getattr`
5. `state.crm.timezone_groups`
6. `shared.dial_policy.leads_for_timezone_counts`
7. `shared.infra.utc_now`
8. `features._dialer.calls._pool_leads`
9. `features._dialer.calls._busy_lead_ids`
10. `shared.dial_policy.global_dialer_pool`
11. `features._dialer.projection.getattr`
12. `features._dialer.projection.getattr`
13. `features._dialer.projection.getattr`
14. `state.crm.pipeline_steps_for_catalog`
15. `shared.dial_policy.unique_business_types`
16. `features._dialer.projection.len`
17. `features._dialer.projection.sum`
18. `features._dialer.projection.sum`

**Called by ←**
- `fn:features/_dialer/projection.py:leads_catalog`
- `fn:features/_dialer/projection.py:public_state`

### `leads_catalog` (line 46)
_Full CRM table payload for GET /api/leads._

**Pseudocode:**
- Set catalog to crm_catalog(...).
- Set archive to getattr(...).
- If archive compared to ...:
-   Set catalog[...] to archive.snapshot(...).
-   Set catalog[...] to archive.revision.
- Else:
-   Set catalog[...] to a list.
-   Set catalog[...] to 0.

**Calls →**
1. `features._dialer.projection.crm_catalog`
2. `features._dialer.projection.getattr`
3. `archive.snapshot`
4. `features._dialer.projection.getattr`
5. `records.list_summaries`
6. `features._dialer.projection.len`
7. `state.in_flight.values`

**Called by ←**
- `fn:features/dialer.py:leads_catalog`

### `public_state` (line 69)

**Pseudocode:**
- Set leads to state.crm.snapshot(...).
- With state.lock:
-   Set active_call to clear_stale_active(...).
-   Set active_id to IfExp.
-   Set prospect_calls to ListComp.
-   Set transcript_call to a boolean condition.
-   Set current_call to a boolean condition.
- Set by_id to DictComp.

**Calls →**
1. `state.crm.snapshot`
2. `features._dialer.rules.clear_stale_active`
3. `active_call.get`
4. `state.in_flight.values`
5. `features._dialer.projection.next`
6. `call.get`
7. `shared.prospect_schema.display_name`
8. `call.get`
9. `call.get`
10. `call.get`
11. `call.get`
12. `features._dialer.projection.list`
13. `features._dialer.voice_session.voice_profile`
14. `features._dialer.voice_session.requires_browser_voice`
15. `features._dialer.projection.list`
16. `transcript_call.get`
17. `features._dialer.projection.list`
18. `transcript_call.get`
19. `features._dialer.projection.list`
20. `transcript_call.get`
21. `features._dialer.projection.bool`
22. `transcript_call.get`
23. `features._dialer.projection.dict`
24. `active_call.get`
25. `state.taggable_call.get`
26. `state.taggable_call.get`
27. `state.taggable_call.get`
28. `by_id.get`
29. `by_id.get`
30. `features._dialer.projection.crm_catalog`

**Called by ←**
- `fn:features/_dialer/call_events.py:hangup_active`
- `fn:features/_dialer/call_events.py:skip_active`
- `fn:features/_dialer/projection.py:live_state`
- `fn:features/_dialer/queue.py:_pin_manual_dial`
- `fn:features/_dialer/queue.py:pass_next`
- `fn:features/_dialer/queue.py:pause`
- `fn:features/_dialer/queue.py:rejoin_browser_voice`
- `fn:features/_dialer/queue.py:scan_crm`
- `fn:features/_dialer/queue.py:set_caller_id_group`
- `fn:features/_dialer/queue.py:set_pool_filters`
- `fn:features/_dialer/queue.py:start`
- `fn:features/_dialer/queue.py:stop`
- `fn:features/_dialer/timing.py:advance_now`
- `fn:features/dialer.py:public_state`

### `live_state` (line 183)

**Pseudocode:**
- Set view to public_state(...).
- Call view.pop(...).
- Return view.

**Calls →**
1. `features._dialer.projection.public_state`
2. `view.pop`

**Called by ←**
- `fn:features/dialer.py:live_state`
