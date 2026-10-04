# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pycontacts/main.py:6-12` - the whole tool is built on the gdata Google Contacts API (`gdata.contacts.client.ContactsClient`), which Google shut down; every endpoint fails against the live service. `doc/TODO.txt:1-2` already says so. Port to the People API (`googleapiclient.discovery.build("people", "v1", ...)`, which `pygooglehelper` credentials already support) and drop `gdata-python3`.

## Medium

- `src/pycontacts/main.py:74-87` - `fix_phones` calls `contacts_client.update(entry)` once per changed number inside the loop over the same entry; after the first update the entry's etag is stale, so a second fix on the same contact fails (likely the "sometimes I get an exception when calling update" in `doc/TODO.txt:12`). Apply all phone fixes to the entry first, then update once (and use the returned entry).
- `src/pycontacts/main.py:86-87` - `except RequestError: print("failed to update")` throws away the status and reason; at least print the exception (`e.status`, `e.reason`) and the contact summary, or log via the logger.
- `src/pycontacts/main.py:143-148` - `unfilled_contacts_delete` deletes contacts with no dry-run and no confirmation, unlike `fix_phones`, which honours `ConfigFix.doit`; add `ConfigFix` to its configs and only call `delete` when `ConfigFix.doit` is set, printing what would be deleted otherwise.
- `src/pycontacts/configs.py:9-21` - `ConfigAuthFiles` (`client_secret`, `token`) is dead: nothing reads it, and `pygooglehelper` locates the secret itself (`~/.config/pycontacts/client_secret.json` or the packaged copy) and stores tokens under `~/.config/google_tokens/`, so these CLI options are shown on every endpoint but have no effect. Remove the class and its `configs=[ConfigAuthFiles]` uses; also drop the stale comment at `main.py:20` ("delete the file token.pickle").

## Low

- `src/pycontacts/main.py:176` - `get_summary` dereferences `entry.organization.name.text` without checking that `organization.name` is not `None` (which `unfilled_contact` at line 120 does check), so a contact with an organization but no organization name raises `AttributeError`; guard it the same way.
- `src/pycontacts/utils.py:23-36` - `flat_dump` and `dump` are identical and `flat_dump` is never called; delete it.
- `pyproject.toml:35` - `httplib2` is declared as a dependency but nothing in `src/` imports it; remove it.
- `rsconstruct.toml:28,32` - `hatch_build.py` (real Python with logic) is not covered by ruff or mypy, while `config/` (Lua only, no `.py` files) is listed in their `src_dirs`; drop `config` and add `src_files = ["hatch_build.py"]` to both.
- `README.md` - generated README has no usage section (no `tera.snippets/main.md.tera`); add a snippet listing the endpoints (`dump_contacts`, `fix_phones`, `show_bad_phones`, `unfilled_contacts_show`, `unfilled_contacts_delete`) and where `client_secret.json` must live.
