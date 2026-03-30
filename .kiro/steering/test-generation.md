---
inclusion: manual
---

# Test Generation from Spec Files

When the user asks to generate tests from a spec file in `specs/`, follow these rules:

## Input
- Read the spec file (plain text) from `specs/<name>.txt`
- The spec defines: page name, entry point, URL pattern, steps, recordings, timeouts

## Spec File Format
```
Page: <PageName>
Entry: <navigation path>
URL: <url pattern>

Steps:
1. <step description>
2. <step description>
...

Recordings: <comma-separated section types>
Timeout: <element> <seconds>, <element> <seconds>
Exclude rows: <creator> <date>
```

## Output — Generate 3 files

### 1. Locators: `locators/<snake_name>_locators.py`
- Class named `<PageName>Locators`
- Use triple-quoted docstrings as section headers (no `#` comment blocks)
- All selectors as class-level tuples: `(By.XPATH, "...")` or `(By.CSS_SELECTOR, "...")`
- Sub-element selectors (used with `parent.find_element()`) go in a "Reusable sub-element selectors" section
- Reference `#[[file:locators/simulate_mem_locators.py]]` for pattern

### 2. Page Object: `pages/<snake_name>_page.py`
- Class extends `HomePage` (which extends `CustomBasePage`)
- Constructor: `def __init__(self, browser, wait, logger, base_url)`
- Always use base_page wrapper methods: `find_element`, `element_visibility`, `find_all_elements`, `element_to_be_clickable`, `wait_for_long_load`
- Never use raw `WebDriverWait`/`EC` — use the wrappers from `#[[file:pages/base_page.py]]`
- Never hard-code selectors — always reference the locators class
- Use `ActionChains` with JS fallback for clicks
- Row filtering: `click_random_row(exclude_date, exclude_creator)` with dynamic column index lookup
- Morphology canvas wait wrapped in try/except (non-blocking)
- Use `Cmd+A` + `Backspace` to clear React controlled inputs
- Reference `#[[file:pages/simulate_mem_page.py]]` for pattern

### 3. Test: `tests/test_<snake_name>.py`
- Class named `Test<PascalName>`
- Single test method with all steps in sequence
- Use `@pytest.mark.simulate` and `@pytest.mark.run(order=N)`
- Class docstring lists the flow steps
- Helper: `_get_page(self, setup, logger)` returns page object + lab_id + project_id
- Fixtures: `setup, login, logger, test_config`
- Non-blocking checks use `logger.warning()`, blocking checks use `assert`
- Reference `#[[file:tests/test_simulate_mem.py]]` for pattern

## Conventions
- Copyright header on all files (Blue Brain Project/EPFL + Open Brain Institute)
- `time.sleep()` after clicks (1-3s depending on expected load)
- Log every step with `logger.info()`
- Disabled items must be filtered out before random selection
- Performance-sensitive waits (3D viewer, plots) get longer timeouts (60-120s)
- Simulation completion polling: 300s timeout, 10s interval
