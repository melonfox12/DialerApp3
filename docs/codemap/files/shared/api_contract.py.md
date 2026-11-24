# `shared/api_contract.py`

**Purpose:** Canonical top-level JSON keys for public HTTP responses.

## Functions
### `assert_top_level_keys` (line 311)
_Raise AssertionError when payload keys differ from the contract tuple._

**Pseudocode:**
- If isinstance(...):
-   Raise an error.
- Set expected to tuple(...).
- Set actual to tuple(...).
- If actual compared to ...:
-   Set missing to sorted(...).
-   Set extra to sorted(...).
-   Set detail to a list.

**Calls →**
1. `shared.api_contract.isinstance`
2. `shared.api_contract.AssertionError`
3. `shared.api_contract.type`
4. `shared.api_contract.tuple`
5. `shared.api_contract.sorted`
6. `shared.api_contract.tuple`
7. `shared.api_contract.sorted`
8. `shared.api_contract.sorted`
9. `shared.api_contract.set`
10. `shared.api_contract.set`
11. `shared.api_contract.sorted`
12. `shared.api_contract.set`
13. `shared.api_contract.set`
14. `detail.append`
15. `detail.append`
16. `shared.api_contract.AssertionError`
