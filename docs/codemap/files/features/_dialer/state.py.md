# `features/_dialer/state.py`

**Purpose:** Dialer state and the call record shape.

## Functions
### `__init__` (line 20)

**Pseudocode:**
- Set self.crm to crm.
- Set self.env_path to env_path.
- Set self.metrics to metrics.
- Set self.storage_name to 'local JSON files'.
- Set self.account_values to a dict.
- Set self.account_user_id to None.
- Set self.account_email to ''.
- Set self.token_index to None.

**Calls →**
1. `threading.RLock`
2. `threading.Lock`
3. `shared.vocabulary.caller_ids_for_group`

### `record_activity` (line 76)

**Pseudocode:**
- With self.lock:
-   Update self.activity_sequence with Add 1.
-   Call self.activity_log.append(...).
- If source compared to ...:
-   Call debug_event(...).

**Calls →**
1. `features._dialer.state.DialerState.activity_log.append`
2. `datetime.datetime.now`
3. `features._dialer.state.str`
4. `shared.infra.debug_event`
