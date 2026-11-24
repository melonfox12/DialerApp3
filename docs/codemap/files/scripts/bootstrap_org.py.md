# `scripts/bootstrap_org.py`

**Purpose:** Create an organization and attach an owner, optionally invite reps by email.

## Functions
### `main` (line 19)

**Pseudocode:**
- Set parser to argparse.ArgumentParser(...).
- Call parser.add_argument(...).
- Call parser.add_argument(...).
- Call parser.add_argument(...).
- Call parser.add_argument(...).
- Set args to parser.parse_args(...).
- Call sys.path.insert(...).
- Set values to read_env(...).

**Calls →**
1. `argparse.ArgumentParser`
2. `parser.add_argument`
3. `parser.add_argument`
4. `parser.add_argument`
5. `parser.add_argument`
6. `parser.parse_args`
7. `sys.path.insert`
8. `scripts.bootstrap_org.str`
9. `scripts.bootstrap_org.read_env`
10. `SupabaseClient.from_env`
11. `scripts.bootstrap_org.print`
12. `scripts.bootstrap_org.str`
13. `values.get`
14. `values.get`
15. `values.get`
16. `os.path.exists`
17. `hints.append`
18. `hints.append`
19. `hints.append`
20. `scripts.bootstrap_org.print`
21. `scripts.bootstrap_org.str`
22. `scripts.bootstrap_org.print`
23. `org_storage.get_active_membership`
24. `org_storage.get_organization`
25. `scripts.bootstrap_org.print`
26. `org.get`
27. `existing.get`
28. `org_storage.create_organization`
29. `org_storage.add_member`
30. `scripts.bootstrap_org.print`
