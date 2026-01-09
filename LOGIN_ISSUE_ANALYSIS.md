# Login Issue Analysis and Fix

## Problem Description
Tests that log into the platform were getting stuck because they navigate directly to the login page `/auth/realms`, but sometimes the application redirects them back to the main/landing page (that has the Login button).

## Root Cause Analysis

### The Issue Flow:
1. **Test tries to navigate directly to OIDC URL**: `https://www.openbraininstitute.org/auth/realms/SBO/protocol/openid-connect/auth?...`
2. **Sometimes the application redirects back to landing page** instead of showing the login form
3. **Original fallback mechanism was flawed**:
   - Only looked for one specific login button selector: `//a[@href='/app/virtual-lab']`
   - No retry mechanism for different button variations
   - Poor error handling when fallback failed
   - Tests would get stuck waiting for login form that never appeared

### Why This Happens:
- **Session state**: Sometimes existing cookies/sessions cause redirects
- **Application routing logic**: The app might redirect unauthenticated direct OIDC requests to landing page
- **Timing issues**: Race conditions between navigation and page load

## The Fix

### Enhanced `navigate_to_login_direct` Fixture:

#### 1. **Clear Session State**
```python
# Clear any existing cookies/session first
browser.delete_all_cookies()
```

#### 2. **Multiple Login Button Selectors**
Instead of just one selector, now tries multiple variations:
```python
login_selectors = [
    (By.XPATH, "//a[@href='/app/virtual-lab']"),
    (By.XPATH, "//a[@href='/app/virtual-lab/sync']"),
    (By.XPATH, "//a[contains(@href, 'virtual-lab')]"),
    (By.XPATH, "//button[contains(text(), 'Go to Lab')]"),
    (By.XPATH, "//a[contains(text(), 'Go to Lab')]")
]
```

#### 3. **Robust Error Handling**
- Better logging at each step
- Screenshots for debugging when things fail
- Clear error messages indicating what went wrong
- Proper URL validation

#### 4. **Enhanced `navigate_to_login` Fixture**
- Added retry mechanism for landing page load
- Added retry mechanism for login button click
- Better error handling and debugging

## Key Improvements

### Before:
```python
try:
    login_btn = WebDriverWait(browser, 25).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/app/virtual-lab']"))
    )
    login_btn.click()
except TimeoutException:
    browser.save_screenshot("/tmp/failed_login.png")
    raise RuntimeError("Cannot reach OIDC login page from CI/CD")
```

### After:
```python
# Try multiple login button selectors
login_selectors = [...]
login_clicked = False
for selector in login_selectors:
    try:
        login_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(selector)
        )
        logger.info(f"Found login button with selector: {selector}")
        login_btn.click()
        login_clicked = True
        break
    except TimeoutException:
        logger.debug(f"Login button not found with selector: {selector}")
        continue

if not login_clicked:
    logger.error("Could not find any login button on landing page")
    browser.save_screenshot("/tmp/landing_page_no_login.png")
    raise RuntimeError("Cannot find login button on landing page")
```

## Results

### Test Results After Fix:
✅ **All CI/CD stability tests passing**
✅ **Login stability test passing consistently**
✅ **Better error messages and debugging**
✅ **Robust fallback mechanisms**

### Benefits:
1. **Eliminates stuck tests** - Multiple fallback strategies prevent hanging
2. **Better debugging** - Clear logs and screenshots when issues occur
3. **More reliable CI/CD** - Handles various application states gracefully
4. **Faster failure detection** - Quick identification of actual issues vs transient problems

## Usage

The fixes are automatically applied to all tests using these fixtures:
- `navigate_to_login_direct` - For direct OIDC navigation
- `navigate_to_login` - For landing page → login flow
- `login_direct_complete` - Complete login process

## Monitoring

To monitor login stability:
```bash
# Run stability tests
make ci-cd-stability

# Debug specific login issues
make debug-explore-headless
```

The enhanced logging will show exactly which login path was taken and any fallback mechanisms that were triggered.