# `features/dialer.py`

**Purpose:** Dialer entry. Part import order, low to high:

## Routes
- `GET` `/api/state` → `get_state`
- `GET` `/api/leads` → `get_leads`
- `GET` `/api/live` → `get_live`
- `GET` `/api/voice-token` → `get_voice_token`
- `POST` `/api/voice/rejoin` → `post_voice_rejoin`
- `POST` `/api/timezone` → `post_timezone`
- `POST` `/api/caller-id-group` → `post_caller_id_group`
- `POST` `/api/start` → `post_start`
- `POST` `/api/pause` → `post_pause`
- `POST` `/api/stop` → `post_stop`
- `POST` `/api/hangup` → `post_hangup`
- `POST` `/api/skip` → `post_skip`
- `POST` `/api/next/skip` → `post_pass_next`
- `POST` `/api/advance` → `post_advance`
- `POST` `/api/dials/scan` → `post_scan_crm`
- `POST` `/api/dials/backfill-new-callbacks` → `post_backfill_new_dial_callbacks`
- `POST` `/api/dials/backfill-nov5-static-callbacks` → `post_backfill_nov5_static_callbacks`
- `GET` `/api/dials/export.csv` → `get_dials_export`
- `POST` `/api/dials/import` → `post_dials_import`
- `POST` `/api/dials/records/snapshot` → `post_dials_record_snapshot`
- `GET` `/api/dials/records/{id}` → `get_dials_record`
- `POST` `/api/leads/{id}/dial` → `post_dial`
- `POST` `/api/leads/{id}/status` → `post_status`
- `POST` `/api/leads/{id}/call-outcome` → `post_call_outcome`
- `GET` `/api/ai-agents` → `get_ai_agents`
- `POST` `/api/ai-agents/create` → `post_ai_agent_create`
- `POST` `/api/ai-agents/duplicate` → `post_ai_agent_duplicate`
- `POST` `/api/ai-agents/delete` → `post_ai_agent_delete`
- `POST` `/api/ai-agents/boot` → `post_ai_agent_boot`
- `POST` `/api/ai-agents/start` → `post_ai_agent_start`
- `POST` `/api/ai-agents/stop` → `post_ai_agent_stop`
- `POST` `/api/ai-agents/release-pool` → `post_ai_agent_release`
- `GET` `/api/ai-agents/playbook` → `get_ai_agent_playbook`
- `POST` `/api/ai-agents/playbook` → `post_ai_agent_playbook`
- `POST` `/api/ai-agents/sandbox/start` → `post_ai_sandbox_start`
- `POST` `/api/ai-agents/sandbox/turn` → `post_ai_sandbox_turn`
- `POST` `/api/ai-agents/sandbox/reset` → `post_ai_sandbox_reset`
- `GET` `/api/ai-agents/sandbox/sync` → `get_ai_sandbox_sync`
- `POST` `/api/ai-agents/sandbox/audio` → `post_ai_sandbox_audio`
- `POST` `/api/ai-agents/sandbox/playback-ready` → `post_ai_sandbox_playback_ready`

## Functions
### `read_values` (line 22)

**Pseudocode:**
- Return settings_feature.values(...).

**Calls →**
1. `features.settings.values`
2. `features.dialer.bool`

**Called by ←**
- `fn:features/dialer.py:read_settings`

### `read_settings` (line 25)

**Pseudocode:**
- Set current to self.read_values(...).
- Return a dict.

**Calls →**
1. `features.dialer.Dialer.read_values`
2. `features.settings.preferences`

**Called by ←**
- `fn:features/dialer.py:save_settings`

### `public_state` (line 29)

**Pseudocode:**
- Return projection.public_state(...).

**Calls →**
1. `features._dialer.projection.public_state`

### `leads_catalog` (line 32)

**Pseudocode:**
- Return projection.leads_catalog(...).

**Calls →**
1. `features._dialer.projection.leads_catalog`

### `maintain_crm` (line 35)

**Pseudocode:**
- Return queue.maintain_crm(...).

**Calls →**
1. `features._dialer.queue.maintain_crm`

### `live_state` (line 38)

**Pseudocode:**
- Return projection.live_state(...).

**Calls →**
1. `features._dialer.projection.live_state`

### `set_timezone_filter` (line 41)

**Pseudocode:**
- Return queue.set_timezone_filter(...).

**Calls →**
1. `features._dialer.queue.set_timezone_filter`

### `set_pool_filters` (line 44)

**Pseudocode:**
- Return queue.set_pool_filters(...).

**Calls →**
1. `features._dialer.queue.set_pool_filters`

### `set_caller_id_group` (line 49)

**Pseudocode:**
- Return queue.set_caller_id_group(...).

**Calls →**
1. `features._dialer.queue.set_caller_id_group`

### `scan_crm` (line 52)

**Pseudocode:**
- Return queue.scan_crm(...).

**Calls →**
1. `features._dialer.queue.scan_crm`

### `backfill_new_dial_callbacks` (line 55)

**Pseudocode:**
- Set count to queue.repair_total_dials_callbacks(...).
- If count:
-   Set noun to IfExp.
-   Call self.record_activity(...).
- Return count.

**Calls →**
1. `features._dialer.queue.repair_total_dials_callbacks`
2. `features.dialer.Dialer.record_activity`

### `start` (line 65)

**Pseudocode:**
- Return queue.start(...).

**Calls →**
1. `features._dialer.queue.start`

### `start_ai_agent` (line 68)

**Pseudocode:**
- Return ai_agents.start_agent(...).

**Calls →**
1. `features.ai_agents.start_agent`

### `stop_ai_agent` (line 71)

**Pseudocode:**
- Return ai_agents.stop_agent(...).

**Calls →**
1. `features.ai_agents.stop_agent`

### `boot_ai_agent_pool` (line 74)

**Pseudocode:**
- Return ai_agents.boot_agent_pool(...).

**Calls →**
1. `features.ai_agents.boot_agent_pool`

### `release_ai_agent_pool` (line 77)

**Pseudocode:**
- Return ai_agents.release_agent_pool(...).

**Calls →**
1. `features.ai_agents.release_agent_pool`

### `create_ai_agent` (line 80)

**Pseudocode:**
- Return ai_agents.create_agent(...).

**Calls →**
1. `features.ai_agents.create_agent`

### `duplicate_ai_agent` (line 83)

**Pseudocode:**
- Return ai_agents.duplicate_agent(...).

**Calls →**
1. `features.ai_agents.duplicate_agent`

### `delete_ai_agent` (line 86)

**Pseudocode:**
- Return ai_agents.delete_agent(...).

**Calls →**
1. `features.ai_agents.delete_agent`

### `ai_agent_playbook` (line 89)

**Pseudocode:**
- Set name to ai_agents._agent_name(...).
- Return ai_agent_playbook.get_playbook(...).

**Calls →**
1. `features.ai_agents._agent_name`
2. `features.ai_agent_playbook.get_playbook`

### `save_ai_agent_playbook` (line 93)

**Pseudocode:**
- Set name to ai_agents._agent_name(...).
- Return ai_agent_playbook.save_playbook(...).

**Calls →**
1. `features.ai_agents._agent_name`
2. `features.ai_agent_playbook.save_playbook`

### `ai_sandbox_start` (line 97)

**Pseudocode:**
- Return ai_agent_sandbox.start(...).

**Calls →**
1. `features.ai_agent_sandbox.start`

### `ai_sandbox_turn` (line 100)

**Pseudocode:**
- Return ai_agent_sandbox.turn(...).

**Calls →**
1. `features.ai_agent_sandbox.turn`

### `ai_sandbox_reset` (line 103)

**Pseudocode:**
- Return ai_agent_sandbox.reset(...).

**Calls →**
1. `features.ai_agent_sandbox.reset`

### `ai_sandbox_ingest` (line 106)

**Pseudocode:**
- Call ai_agent_sandbox.ingest_mulaw(...).

**Calls →**
1. `features.ai_agent_sandbox.ingest_mulaw`

### `ai_sandbox_sync` (line 109)

**Pseudocode:**
- Return ai_agent_sandbox.stream_sync(...).

**Calls →**
1. `features.ai_agent_sandbox.stream_sync`

### `ai_sandbox_playback_ready` (line 112)

**Pseudocode:**
- Return ai_agent_sandbox.mark_playback_ready(...).

**Calls →**
1. `features.ai_agent_sandbox.mark_playback_ready`

### `rejoin_browser_voice` (line 115)

**Pseudocode:**
- Return queue.rejoin_browser_voice(...).

**Calls →**
1. `features._dialer.queue.rejoin_browser_voice`

### `dial_lead` (line 123)

**Pseudocode:**
- Return queue.dial_lead(...).

**Calls →**
1. `features._dialer.queue.dial_lead`

### `pause` (line 126)

**Pseudocode:**
- Return queue.pause(...).

**Calls →**
1. `features._dialer.queue.pause`

### `stop` (line 129)

**Pseudocode:**
- Return queue.stop(...).

**Calls →**
1. `features._dialer.queue.stop`

### `fill_slots` (line 132)

**Pseudocode:**
- Return slots.fill_slots(...).

**Calls →**
1. `features._dialer.slots.fill_slots`

### `advance_now` (line 135)

**Pseudocode:**
- Return timing.advance_now(...).

**Calls →**
1. `features._dialer.timing.advance_now`

### `handle_webhook` (line 138)

**Pseudocode:**
- Return call_events.handle_webhook(...).

**Calls →**
1. `features._dialer.call_events.handle_webhook`

### `handle_client_voice` (line 141)

**Pseudocode:**
- Return call_events.handle_client_voice(...).

**Calls →**
1. `features._dialer.call_events.handle_client_voice`

### `hangup_active` (line 144)

**Pseudocode:**
- Return call_events.hangup_active(...).

**Calls →**
1. `features._dialer.call_events.hangup_active`

### `skip_active` (line 147)

**Pseudocode:**
- Return call_events.skip_active(...).

**Calls →**
1. `features._dialer.call_events.skip_active`

### `pass_next` (line 150)

**Pseudocode:**
- Return queue.pass_next(...).

**Calls →**
1. `features._dialer.queue.pass_next`

### `update_status` (line 165)

**Pseudocode:**
- Return outcomes.update_status(...).

**Calls →**
1. `features._dialer.outcomes.update_status`

### `tag_call` (line 168)

**Pseudocode:**
- Return outcomes.tag_call(...).

**Calls →**
1. `features._dialer.outcomes.tag_call`

### `log_booking` (line 171)

**Pseudocode:**
- Return outcomes.log_booking(...).

**Calls →**
1. `features._dialer.outcomes.log_booking`

### `validate_webhook` (line 174)

**Pseudocode:**
- Return twilio.validate_webhook(...).

**Calls →**
1. `features._dialer.twilio.validate_webhook`

### `voice_access_token` (line 177)

**Pseudocode:**
- Return twilio.voice_access_token(...).

**Calls →**
1. `features._dialer.twilio.voice_access_token`

### `settings_state` (line 180)

**Pseudocode:**
- Return settings_feature.settings_state(...).

**Calls →**
1. `features.settings.settings_state`
2. `features.dialer.getattr`
3. `features.dialer.getattr`
4. `features.dialer.bool`

**Called by ←**
- `fn:features/dialer.py:save_settings`

### `save_settings` (line 189)

**Pseudocode:**
- Set save_remote to None.
- Set saver to getattr(...).
- If saver:
- Set parsed to settings_feature.save_settings(...).
- With self.lock:
-   Set self.settings to self.read_settings(...).
- Return self.settings_state(...).

**Calls →**
1. `features.dialer.getattr`
2. `features.dialer.saver`
3. `features.settings.save_settings`
4. `features.dialer.Dialer.read_settings`
5. `features.dialer.Dialer.settings_state`

### `save_goal` (line 202)

**Pseudocode:**
- Set save_remote to None.
- Set saver to getattr(...).
- If saver:
- Set parsed to settings_feature.save_goal(...).
- With self.lock:
-   Call self.settings.update(...).
- Return settings_feature.daily_goal(...).

**Calls →**
1. `features.dialer.getattr`
2. `features.dialer.saver`
3. `features.settings.save_goal`
4. `datetime.date.today`
5. `features.dialer.Dialer.settings.update`
6. `features.settings.daily_goal`

### `_maybe_run_nov5_static_callback_migration` (line 217)

**Pseudocode:**
- Set dialer to request.account.dialer.
- If getattr(...):
-   Return nothing.
- Set dialer._nov5_static_callback_migration_checked to True.
- Set archive to a boolean condition.
- Call queue.ensure_nov5_static_callback_migration(...).

**Calls →**
1. `features.dialer.getattr`
2. `features.dialer.getattr`
3. `features._dialer.queue.ensure_nov5_static_callback_migration`

**Called by ←**
- `fn:features/dialer.py:get_leads`
- `fn:features/dialer.py:get_state`

### `get_state` (line 226)

**Pseudocode:**
- Try:
-   Call _maybe_run_nov5_static_callback_migration(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC2B3E10>:
-   Call request.report_storage_error(...).

**Calls →**
1. `features.dialer._maybe_run_nov5_static_callback_migration`
2. `request.send_json`
3. `request.account.dialer.public_state`
4. `request.report_storage_error`

### `get_leads` (line 234)

**Pseudocode:**
- Try:
-   Call _maybe_run_nov5_static_callback_migration(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC2B1710>:
-   Call request.report_storage_error(...).

**Calls →**
1. `features.dialer._maybe_run_nov5_static_callback_migration`
2. `request.send_json`
3. `request.account.dialer.leads_catalog`
4. `request.report_storage_error`

### `get_live` (line 242)

**Pseudocode:**
- Try:
-   Set dialer to request.account.dialer.
-   Set payload to dialer.live_state(...).
-   Call team.maybe_record_presence(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC181A50>:
-   Call request.report_storage_error(...).

**Calls →**
1. `dialer.live_state`
2. `team.maybe_record_presence`
3. `request.send_json`
4. `request.report_storage_error`

### `get_voice_token` (line 254)

**Pseudocode:**
- Try:
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC185010>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.voice_access_token`
3. `features.dialer.str`
4. `request.send_json`
5. `features.dialer.str`

### `post_timezone` (line 262)

**Pseudocode:**
- Set timezone to IfExp.
- Set pool_status to IfExp.
- Set business_type to IfExp.
- Try:
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC1B49D0>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).

**Calls →**
1. `data.get`
2. `data.get`
3. `data.get`
4. `request.send_json`
5. `request.account.dialer.set_pool_filters`
6. `features.dialer.str`
7. `request.send_json`
8. `features.dialer.str`

### `post_caller_id_group` (line 275)

**Pseudocode:**
- Try:
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC28A150>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.set_caller_id_group`
3. `data.get`
4. `features.dialer.str`
5. `request.send_json`
6. `features.dialer.str`

### `post_start` (line 283)

**Pseudocode:**
- Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.start`

### `post_voice_rejoin` (line 287)

**Pseudocode:**
- Try:
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC267E50>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.rejoin_browser_voice`
3. `features.dialer.str`
4. `request.send_json`
5. `features.dialer.str`

### `post_pause` (line 295)

**Pseudocode:**
- Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.pause`

### `post_stop` (line 299)

**Pseudocode:**
- Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.stop`

### `post_hangup` (line 303)

**Pseudocode:**
- Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.hangup_active`

### `post_skip` (line 307)

**Pseudocode:**
- Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.skip_active`

### `post_pass_next` (line 311)

**Pseudocode:**
- Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.pass_next`
3. `data.get`

### `post_advance` (line 315)

**Pseudocode:**
- Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.advance_now`

### `post_scan_crm` (line 319)

**Pseudocode:**
- Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `request.account.dialer.scan_crm`

### `post_backfill_new_dial_callbacks` (line 323)

**Pseudocode:**
- Set count to request.account.dialer.backfill_new_dial_callbacks(...).
- Try:
-   Set state to request.ctx.state(...).
- On <ast.Name object at 0x00000242BC22A790>:
-   Call request.ctx.log(...).
-   Set state to request.account.dialer.public_state(...).
- Call request.send_json(...).

**Calls →**
1. `request.account.dialer.backfill_new_dial_callbacks`
2. `request.ctx.state`
3. `request.ctx.log`
4. `request.account.dialer.public_state`
5. `request.send_json`

### `post_backfill_nov5_static_callbacks` (line 333)

**Pseudocode:**
- Set dialer to request.account.dialer.
- Set archive to a boolean condition.
- Set count to queue.ensure_nov5_static_callback_migration(...).
- Try:
-   Set state to request.ctx.state(...).
- On <ast.Name object at 0x00000242BC2CE0D0>:
-   Call request.ctx.log(...).
-   Set state to dialer.public_state(...).

**Calls →**
1. `features.dialer.getattr`
2. `features._dialer.queue.ensure_nov5_static_callback_migration`
3. `request.ctx.state`
4. `request.ctx.log`
5. `dialer.public_state`
6. `request.send_json`

### `post_dial` (line 345)

**Pseudocode:**
- Set lead_id to urllib.parse.unquote(...).
- Call request.send_json(...).

**Calls →**
1. `urllib.parse.parse.unquote`
2. `request._trace_path.removeprefix`
3. `request.send_json`
4. `request.account.dialer.dial_lead`

### `post_status` (line 350)

**Pseudocode:**
- Set lead_id to urllib.parse.unquote(...).
- Set dialer to request.account.dialer.
- Call dialer.update_status(...).
- Set state to dialer.public_state(...).
- Set lead to next(...).
- If lead compared to ...:
-   Raise an error.
- Call request.send_json(...).

**Calls →**
1. `urllib.parse.parse.unquote`
2. `request._trace_path.removeprefix`
3. `dialer.update_status`
4. `data.get`
5. `data.get`
6. `data.get`
7. `features.dialer.bool`
8. `data.get`
9. `dialer.public_state`
10. `features.dialer.next`
11. `dialer.crm.snapshot`
12. `item.get`
13. `features.dialer.KeyError`
14. `request.send_json`

### `get_dials_export` (line 364)

**Pseudocode:**
- Try:
-   Set archive to request.account.dial_archive.snapshot(...).
-   Set content to dials_csv_bytes_for(...).
-   Call request.send_bytes(...).
- On <ast.Name object at 0x00000242BC2BABD0>:
-   Call request.report_storage_error(...).

**Calls →**
1. `request.account.dial_archive.snapshot`
2. `features.dialer.dials_csv_bytes_for`
3. `request.account.crm.snapshot`
4. `request.send_bytes`
5. `request.report_storage_error`

### `post_dials_import` (line 377)

**Pseudocode:**
- Try:
-   Set result to request.account.dial_archive.import_csv_bytes(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC2811D0>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC271190>:
-   Call request.report_storage_error(...).

**Calls →**
1. `request.account.dial_archive.import_csv_bytes`
2. `request.send_json`
3. `request.ctx.state`
4. `features.dialer.str`
5. `request.send_json`
6. `features.dialer.str`
7. `request.report_storage_error`

### `post_dials_record_snapshot` (line 388)

**Pseudocode:**
- Try:
-   Set saved to snapshot_active_dials(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC12F650>:
-   Set request._trace_error to str(...).
-   Call request.send_json(...).
- On <ast.Name object at 0x00000242BC12B390>:
-   Call request.report_storage_error(...).

**Calls →**
1. `features.dialer.snapshot_active_dials`
2. `request.send_json`
3. `request.ctx.state`
4. `features.dialer.str`
5. `request.send_json`
6. `features.dialer.str`
7. `request.report_storage_error`

### `get_dials_record` (line 406)

**Pseudocode:**
- Set record_id to urllib.parse.unquote(...).
- Set record to request.account.dial_records.get_record(...).
- If record compared to ...:
-   Set request._trace_error to 'Record not found'.
-   Call request.send_json(...).
-   Return nothing.
- Call request.send_json(...).

**Calls →**
1. `urllib.parse.parse.unquote`
2. `request._trace_path.removeprefix`
3. `request.account.dial_records.get_record`
4. `request.send_json`
5. `request.send_json`

### `post_call_outcome` (line 418)

**Pseudocode:**
- Set lead_id to urllib.parse.unquote(...).
- Set dialer to request.account.dialer.
- Set lead to dialer.tag_call(...).
- Call request.send_json(...).

**Calls →**
1. `urllib.parse.parse.unquote`
2. `request._trace_path.removeprefix`
3. `dialer.tag_call`
4. `data.get`
5. `request.send_json`
6. `dialer.public_state`

### `get_ai_agents` (line 425)

**Pseudocode:**
- Call request.send_json(...).

**Calls →**
1. `request.send_json`
2. `features.ai_agents.agents_public_view`

### `post_ai_agent_create` (line 429)

**Pseudocode:**
- Set dialer to request.account.dialer.
- Set result to dialer.create_ai_agent(...).
- Call request.send_json(...).

**Calls →**
1. `dialer.create_ai_agent`
2. `data.get`
3. `data.get`
4. `request.send_json`

### `post_ai_agent_duplicate` (line 435)

**Pseudocode:**
- Set dialer to request.account.dialer.
- Set source_id to a boolean condition.
- Set result to dialer.duplicate_ai_agent(...).
- Call request.send_json(...).

**Calls →**
1. `data.get`
2. `data.get`
3. `dialer.duplicate_ai_agent`
4. `data.get`
5. `request.send_json`

### `post_ai_agent_delete` (line 442)

**Pseudocode:**
- Set dialer to request.account.dialer.
- Set agent_id to str(...).strip(...).
- Set result to dialer.delete_ai_agent(...).
- Call request.send_json(...).

**Calls →**
1. `features.dialer.str`
2. `data.get`
3. `dialer.delete_ai_agent`
4. `request.send_json`

### `post_ai_agent_boot` (line 449)

**Pseudocode:**
- Set agent_id to a boolean condition.
- Set dialer to request.account.dialer.
- Set result to dialer.boot_ai_agent_pool(...).
- Call request.send_json(...).

**Calls →**
1. `data.get`
2. `urllib.parse.parse.unquote`
3. `request._trace_path.removeprefix`
4. `dialer.boot_ai_agent_pool`
5. `request.send_json`
6. `dialer.public_state`

### `post_ai_agent_start` (line 458)

**Pseudocode:**
- Set agent_id to a boolean condition.
- Set dialer to request.account.dialer.
- Set view to dialer.start_ai_agent(...).
- Call request.send_json(...).

**Calls →**
1. `data.get`
2. `urllib.parse.parse.unquote`
3. `request._trace_path.removeprefix`
4. `dialer.start_ai_agent`
5. `request.send_json`

### `post_ai_agent_stop` (line 467)

**Pseudocode:**
- Set agent_id to a boolean condition.
- Set dialer to request.account.dialer.
- Set view to dialer.stop_ai_agent(...).
- Call request.send_json(...).

**Calls →**
1. `data.get`
2. `urllib.parse.parse.unquote`
3. `request._trace_path.removeprefix`
4. `dialer.stop_ai_agent`
5. `request.send_json`

### `post_ai_agent_release` (line 476)

**Pseudocode:**
- Set agent_id to a boolean condition.
- Set dialer to request.account.dialer.
- Set result to dialer.release_ai_agent_pool(...).
- Call request.send_json(...).

**Calls →**
1. `data.get`
2. `urllib.parse.parse.unquote`
3. `request._trace_path.removeprefix`
4. `dialer.release_ai_agent_pool`
5. `request.send_json`
6. `dialer.public_state`

### `get_ai_agent_playbook` (line 485)

**Pseudocode:**
- Set query to urllib.parse.parse_qs(...).
- Set agent_id to a boolean condition[...].
- Set dialer to request.account.dialer.
- Set playbook to dialer.ai_agent_playbook(...).
- Call request.send_json(...).

**Calls →**
1. `urllib.parse.parse.parse_qs`
2. `urllib.parse.parse.urlsplit`
3. `query.get`
4. `query.get`
5. `dialer.ai_agent_playbook`
6. `request.send_json`
7. `features.dialer.str`

### `post_ai_agent_playbook` (line 493)

**Pseudocode:**
- Set agent_id to a boolean condition.
- Set dialer to request.account.dialer.
- Set playbook to dialer.save_ai_agent_playbook(...).
- Call request.send_json(...).

**Calls →**
1. `data.get`
2. `dialer.save_ai_agent_playbook`
3. `data.get`
4. `request.send_json`
5. `features.dialer.str`

### `post_ai_sandbox_start` (line 500)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set dialer to request.account.dialer.
- Set prospect to IfExp.
- Set payload to dialer.ai_sandbox_start(...).
- Call request.send_json(...).

**Calls →**
1. `features.dialer.str`
2. `data.get`
3. `features.dialer.isinstance`
4. `data.get`
5. `data.get`
6. `dialer.ai_sandbox_start`
7. `request.send_json`

### `post_ai_sandbox_turn` (line 508)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set dialer to request.account.dialer.
- Set payload to dialer.ai_sandbox_turn(...).
- Call request.send_json(...).

**Calls →**
1. `features.dialer.str`
2. `data.get`
3. `dialer.ai_sandbox_turn`
4. `data.get`
5. `data.get`
6. `request.send_json`

### `post_ai_sandbox_reset` (line 515)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set dialer to request.account.dialer.
- Set payload to dialer.ai_sandbox_reset(...).
- Call request.send_json(...).

**Calls →**
1. `features.dialer.str`
2. `data.get`
3. `dialer.ai_sandbox_reset`
4. `request.send_json`

### `get_ai_sandbox_sync` (line 522)

**Pseudocode:**
- Set query to urllib.parse.parse_qs(...).
- Set agent_id to a boolean condition[...].
- Set dialer to request.account.dialer.
- Call request.send_json(...).

**Calls →**
1. `urllib.parse.parse.parse_qs`
2. `urllib.parse.parse.urlsplit`
3. `query.get`
4. `query.get`
5. `request.send_json`
6. `dialer.ai_sandbox_sync`

### `post_ai_sandbox_audio` (line 529)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set dialer to request.account.dialer.
- Set payloads to list(...).
- If data.get(...):
-   Call payloads.insert(...).
- For each item in payloads:
-   If item:
-     Call dialer.ai_sandbox_ingest(...).

**Calls →**
1. `features.dialer.str`
2. `data.get`
3. `features.dialer.list`
4. `data.get`
5. `data.get`
6. `payloads.insert`
7. `data.get`
8. `dialer.ai_sandbox_ingest`
9. `request.send_json`
10. `dialer.ai_sandbox_sync`

### `post_ai_sandbox_playback_ready` (line 541)

**Pseudocode:**
- Set agent_id to str(...).strip(...).
- Set dialer to request.account.dialer.
- Call request.send_json(...).

**Calls →**
1. `features.dialer.str`
2. `data.get`
3. `request.send_json`
4. `dialer.ai_sandbox_playback_ready`
