# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
"""
Test recorder utility to generate test code from user interactions.
Captures clicks, inputs, and navigation to generate Selenium test code.
"""
import json
from datetime import datetime
from typing import List, Dict, Any


class TestRecorder:
    """Records user interactions and generates test code."""
    
    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.actions = []
        self.recording = False
    
    def start_recording(self, test_name: str):
        """Start recording user interactions."""
        self.test_name = test_name
        self.recording = True
        self.actions = []
        self.logger.info(f"Started recording test: {test_name}")
        
        # Inject JavaScript to capture events
        self._inject_event_listeners()
    
    def stop_recording(self):
        """Stop recording and return captured actions."""
        self.recording = False
        self.logger.info(f"Stopped recording. Captured {len(self.actions)} actions")
        return self.actions
    
    def _inject_event_listeners(self):
        """Inject JavaScript to capture user interactions."""
        script = """
        window.testRecorderActions = window.testRecorderActions || [];
        
        // Capture clicks
        document.addEventListener('click', function(e) {
            var target = e.target;
            var selector = getSelector(target);
            window.testRecorderActions.push({
                type: 'click',
                selector: selector,
                text: target.innerText?.substring(0, 50),
                timestamp: Date.now()
            });
        }, true);
        
        // Capture input changes
        document.addEventListener('input', function(e) {
            var target = e.target;
            if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
                var selector = getSelector(target);
                window.testRecorderActions.push({
                    type: 'input',
                    selector: selector,
                    value: target.value,
                    inputType: target.type,
                    timestamp: Date.now()
                });
            }
        }, true);
        
        // Helper to generate CSS selector
        function getSelector(element) {
            if (element.id) {
                return '#' + element.id;
            }
            if (element.className && typeof element.className === 'string') {
                var classes = element.className.trim().split(/\\s+/).join('.');
                if (classes) return element.tagName.toLowerCase() + '.' + classes;
            }
            if (element.name) {
                return element.tagName.toLowerCase() + '[name="' + element.name + '"]';
            }
            // Fallback to xpath-like path
            var path = [];
            while (element.parentElement) {
                var index = Array.from(element.parentElement.children).indexOf(element) + 1;
                path.unshift(element.tagName.toLowerCase() + ':nth-child(' + index + ')');
                element = element.parentElement;
                if (element.id) {
                    path.unshift('#' + element.id);
                    break;
                }
            }
            return path.join(' > ');
        }
        """
        self.browser.execute_script(script)
    
    def capture_actions(self):
        """Retrieve captured actions from the browser."""
        if not self.recording:
            return []
        
        try:
            actions = self.browser.execute_script("""
                var actions = window.testRecorderActions || [];
                window.testRecorderActions = [];
                return actions;
            """)
            
            if actions:
                self.actions.extend(actions)
                self.logger.info(f"Captured {len(actions)} new actions")
            
            return actions
        except Exception as e:
            self.logger.error(f"Failed to capture actions: {e}")
            return []
    
    def generate_test_code(self, class_name: str = None) -> str:
        """Generate Python test code from recorded actions."""
        if not class_name:
            class_name = f"Test{self.test_name.replace(' ', '').replace('_', '')}"
        
        # Capture any remaining actions
        self.capture_actions()
        
        code_lines = [
            "# Auto-generated test code",
            f"# Generated: {datetime.now().isoformat()}",
            f"# Test: {self.test_name}",
            "",
            "import pytest",
            "from selenium.webdriver.common.by import By",
            "from selenium.webdriver.support import expected_conditions as EC",
            "",
            "",
            f"class {class_name}:",
            f'    """Auto-generated test for {self.test_name}"""',
            "",
            f"    def test_{self.test_name.lower().replace(' ', '_')}(self, login_direct_complete, logger):",
            f'        """Test generated from recorded user interactions."""',
            "        browser, wait, base_url, lab_id, project_id = login_direct_complete",
            ""
        ]
        
        # Generate code for each action
        for i, action in enumerate(self.actions):
            action_type = action.get('type')
            selector = action.get('selector', '')
            
            if action_type == 'click':
                text = action.get('text') or ''
                # Clean text: remove newlines, tabs, and limit length
                text_clean = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                text_display = text_clean[:30] if text_clean else 'element'
                code_lines.append(f"        # Click: {text_display}")
                code_lines.append(f"        element = wait.until(")
                code_lines.append(f"            EC.element_to_be_clickable((By.CSS_SELECTOR, '{selector}'))")
                code_lines.append(f"        )")
                code_lines.append(f"        element.click()")
                code_lines.append(f"        logger.info('Clicked element: {text_display}')")
                code_lines.append("")
                
            elif action_type == 'input':
                value = action.get('value') or ''
                input_type = action.get('inputType', 'text')
                # Clean value: escape quotes and newlines
                value_clean = value.replace("'", "\\'").replace('\n', '\\n').replace('\r', '\\r')
                # Mask password fields
                display_value = '***' if input_type == 'password' else value_clean[:30]
                code_lines.append(f"        # Input: {display_value}")
                code_lines.append(f"        element = wait.until(")
                code_lines.append(f"            EC.presence_of_element_located((By.CSS_SELECTOR, '{selector}'))")
                code_lines.append(f"        )")
                if input_type == 'password':
                    code_lines.append(f"        element.send_keys(os.getenv('OBI_PASSWORD'))")
                else:
                    code_lines.append(f"        element.send_keys('{value_clean}')")
                code_lines.append(f"        logger.info('Entered text in: {selector[:30]}')")
                code_lines.append("")
        
        code_lines.append("        # Add assertions here")
        code_lines.append("        assert browser.current_url, 'Page should be loaded'")
        
        return "\n".join(code_lines)
    
    def save_test_file(self, filename: str = None):
        """Save generated test code to a file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tests/test_recorded_{timestamp}.py"
        
        test_code = self.generate_test_code()
        
        try:
            with open(filename, 'w') as f:
                f.write(test_code)
            self.logger.info(f"Test code saved to {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Failed to save test file: {e}")
            return None
    
    def save_actions_json(self, filename: str = None):
        """Save raw actions to JSON for later analysis."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recorded_actions_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'test_name': self.test_name,
                    'recorded_at': datetime.now().isoformat(),
                    'actions': self.actions
                }, f, indent=2)
            self.logger.info(f"Actions saved to {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Failed to save actions: {e}")
            return None
