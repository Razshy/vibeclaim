#!/usr/bin/env python3
"""
Windsurf Credit Claimer Automation
Automates the process of claiming credits on Windsurf using promotion codes.
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WindsurfCreditClaimer:
    def __init__(self, headless=False):
        """Initialize the credit claimer with Chrome driver."""
        self.driver = None
        self.wait = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise
    
    def check_and_handle_login(self):
        """Check if we're on login page and handle login if needed."""
        try:
            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Check if we're on login page
            if "login" in current_url.lower() or "account/login" in current_url:
                logger.info("Detected login page, attempting to log in...")
                return self.perform_login()
            else:
                logger.info("Not on login page, proceeding...")
                return True

        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False

    def perform_login(self):
        """Perform login with credentials."""
        try:
            logger.info("Performing login...")

            # Find email field
            email_selectors = [
                "//input[@type='email']",
                "//input[contains(@name, 'email')]",
                "//input[contains(@placeholder, 'email')]",
                "//input[contains(@id, 'email')]"
            ]

            email_field = None
            for selector in email_selectors:
                try:
                    email_field = self.wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    break
                except TimeoutException:
                    continue

            if not email_field:
                logger.error("Could not find email field")
                return False

            # Enter email
            email_field.clear()
            email_field.send_keys("emailhere")
            logger.info("Entered email")
            time.sleep(1)

            # Find password field
            password_selectors = [
                "//input[@type='password']",
                "//input[contains(@name, 'password')]",
                "//input[contains(@placeholder, 'password')]",
                "//input[contains(@id, 'password')]"
            ]

            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(By.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue

            if not password_field:
                logger.error("Could not find password field")
                return False

            # Enter password
            password_field.clear()
            password_field.send_keys("Passwordhere")
            logger.info("Entered password")
            time.sleep(1)

            # Find and click login button
            login_button_selectors = [
                "//button[contains(text(), 'Log in')]",
                "//button[contains(text(), 'Login')]",
                "//button[contains(text(), 'Sign in')]",
                "//button[@type='submit']",
                "//input[@type='submit']"
            ]

            for selector in login_button_selectors:
                try:
                    login_button = self.driver.find_element(By.XPATH, selector)
                    login_button.click()
                    logger.info("Clicked login button")
                    time.sleep(5)  # Wait for login to process
                    return True
                except NoSuchElementException:
                    continue

            logger.error("Could not find login button")
            return False

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    def navigate_to_windsurf(self):
        """Navigate to Windsurf usage page."""
        try:
            logger.info("Navigating to Windsurf usage page...")
            self.driver.get("https://windsurf.com/subscription/usage")
            time.sleep(3)

            # Check if we got redirected to login page
            if not self.check_and_handle_login():
                return False

            # If we were on login page, navigate to usage page again
            current_url = self.driver.current_url
            if "usage" not in current_url:
                logger.info("Navigating to usage page after login...")
                self.driver.get("https://windsurf.com/subscription/usage")
                time.sleep(3)

            return True
        except Exception as e:
            logger.error(f"Failed to navigate to Windsurf: {e}")
            return False
    
    def click_purchase_credit(self):
        """Click on the Purchase credits button."""
        try:
            logger.info("Looking for Purchase credits button...")

            # Store the current window handle (Windsurf tab)
            original_window = self.driver.current_window_handle
            logger.info(f"Original window handle: {original_window}")

            # Try multiple possible selectors for the purchase credits button
            selectors = [
                "//button[contains(text(), 'Purchase credits')]",
                "//a[contains(text(), 'Purchase credits')]",
                "//button[contains(text(), 'purchase credits')]",
                "//a[contains(text(), 'purchase credits')]",
                "//button[contains(text(), 'Purchase Credit')]",
                "//a[contains(text(), 'Purchase Credit')]",
                "//button[contains(@class, 'purchase') or contains(@class, 'credit')]",
                "//a[contains(@class, 'purchase') or contains(@class, 'credit')]"
            ]

            for selector in selectors:
                try:
                    element = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    element.click()
                    logger.info("Successfully clicked Purchase credits button")

                    # Wait for new tab to open
                    time.sleep(3)

                    # Check if a new tab opened
                    all_windows = self.driver.window_handles
                    logger.info(f"Number of windows after click: {len(all_windows)}")

                    if len(all_windows) > 1:
                        # Switch to the new tab (Stripe checkout)
                        for window in all_windows:
                            if window != original_window:
                                self.driver.switch_to.window(window)
                                logger.info(f"Switched to new tab: {window}")
                                logger.info(f"New tab URL: {self.driver.current_url}")
                                break

                        # Wait for Stripe page to fully load
                        time.sleep(5)
                        return True
                    else:
                        logger.info("No new tab opened, continuing on same page")
                        time.sleep(5)
                        return True

                except TimeoutException:
                    continue

            logger.error("Could not find Purchase credits button")
            return False
        except Exception as e:
            logger.error(f"Error clicking Purchase credits: {e}")
            return False
    
    def handle_stripe_page(self):
        """Handle the Stripe payment page."""
        try:
            logger.info("Handling Stripe payment page...")

            # Wait for Stripe page to load
            time.sleep(5)

            # Scroll down to make sure all elements are loaded
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
            except Exception as e:
                logger.warning(f"Could not scroll page: {e}")

            # Step 1: Look for and click "Add promotion code" link/button
            logger.info("Looking for 'Add promotion code' link...")

            # First, let's see what's on the page for debugging
            try:
                page_text = self.driver.find_element(By.TAG_NAME, "body").text
                logger.info(f"Page contains text: {page_text[:500]}...")  # First 500 chars
            except Exception as e:
                logger.warning(f"Could not get page text: {e}")

            promo_link_selectors = [
                "//button[contains(text(), 'Add promotion code')]",
                "//a[contains(text(), 'Add promotion code')]",
                "//span[contains(text(), 'Add promotion code')]",
                "//*[contains(text(), 'Add promotion code')]",
                "//button[contains(text(), 'promotion code')]",
                "//a[contains(text(), 'promotion code')]",
                "//*[contains(text(), 'promotion code')]",
                "//button[contains(text(), 'promo')]",
                "//a[contains(text(), 'promo')]",
                "//*[contains(text(), 'promo')]",
                # Try looking for elements that might be hidden or styled differently
                "//*[contains(@class, 'promo')]",
                "//*[contains(@id, 'promo')]",
                "//*[contains(@data-testid, 'promo')]",
                # Look for any clickable element near the subtotal area
                "//div[contains(text(), 'Subtotal')]/following-sibling::*//button",
                "//div[contains(text(), 'Subtotal')]/following-sibling::*//*[contains(text(), 'Add')]"
            ]

            promo_link_found = False
            for i, selector in enumerate(promo_link_selectors):
                try:
                    logger.info(f"Trying selector {i+1}: {selector}")
                    element = self.driver.find_element(By.XPATH, selector)
                    element_text = element.text.strip()
                    logger.info(f"Found element with text: '{element_text}'")

                    # Skip empty elements unless they have relevant attributes
                    if not element_text:
                        classes = element.get_attribute('class') or ''
                        if 'promo' not in classes.lower() and 'code' not in classes.lower():
                            logger.info(f"Skipping empty element without relevant classes")
                            continue

                    # Try to click the element
                    try:
                        element.click()
                        logger.info("Successfully clicked 'Add promotion code' button")
                        time.sleep(2)  # Wait for button to transform into input field

                        # Now look for the promotion code input field that should have appeared
                        promo_input_selectors = [
                            "//input[@id='promotionCode']",
                            "//input[@name='promotionCode']",
                            "//input[contains(@placeholder, 'Add promotion code')]",
                            "//input[contains(@placeholder, 'promotion')]"
                        ]

                        input_found = False
                        for input_selector in promo_input_selectors:
                            try:
                                promo_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, input_selector)))
                                logger.info(f"Found promotion code input field: {input_selector}")
                                promo_input.clear()
                                promo_input.send_keys("OPEN-SF")
                                logger.info("Entered promotion code: OPEN-SF")
                                promo_input.send_keys(Keys.RETURN)
                                logger.info("Pressed Enter to apply promotion code")
                                time.sleep(5)  # Wait for discount to be applied
                                input_found = True
                                promo_link_found = True
                                break
                            except TimeoutException:
                                continue

                        if input_found:
                            break
                        else:
                            logger.warning("Clicked promotion code button but input field did not appear")

                    except Exception as click_error:
                        logger.warning(f"Could not click element: {click_error}")
                        # Try JavaScript click as fallback
                        try:
                            self.driver.execute_script("arguments[0].click();", element)
                            logger.info("Successfully clicked 'Add promotion code' button using JavaScript")
                            time.sleep(2)

                            # Look for input field after JS click
                            promo_input_selectors = [
                                "//input[@id='promotionCode']",
                                "//input[@name='promotionCode']",
                                "//input[contains(@placeholder, 'Add promotion code')]"
                            ]

                            for input_selector in promo_input_selectors:
                                try:
                                    promo_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, input_selector)))
                                    promo_input.clear()
                                    promo_input.send_keys("OPEN-SF")
                                    promo_input.send_keys(Keys.RETURN)
                                    logger.info("Applied promotion code via JavaScript click")
                                    time.sleep(5)
                                    promo_link_found = True
                                    break
                                except TimeoutException:
                                    continue

                            if promo_link_found:
                                break

                        except Exception as js_error:
                            logger.warning(f"JavaScript click also failed: {js_error}")
                            continue

                except NoSuchElementException:
                    logger.info(f"Selector {i+1} not found")
                    continue

            if not promo_link_found:
                logger.error("Could not find or interact with 'Add promotion code' button/field")
                return False

            # Step 2: Enter promotion code "OPEN-SF" (if not already done above)
            if not promo_link_found:
                logger.info("Promotion code not entered yet, trying again...")
                promo_input_selectors = [
                    "//input[@id='promotionCode']",  # Exact ID from your screenshot
                    "//input[@name='promotionCode']",  # Exact name from your screenshot
                    "//input[contains(@placeholder, 'Add promotion code')]",  # Exact placeholder
                    "//input[contains(@placeholder, 'promotion') or contains(@placeholder, 'promo')]",
                    "//input[contains(@name, 'promotion') or contains(@name, 'promo')]",
                    "//input[contains(@id, 'promotion') or contains(@id, 'promo')]",
                    "//input[@type='text']"  # Generic text input as fallback
                ]

                promo_field_found = False
                for selector in promo_input_selectors:
                    try:
                        promo_field = self.wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                        promo_field.clear()
                        promo_field.send_keys("OPEN-SF")
                        logger.info("Entered promotion code: OPEN-SF")
                        time.sleep(1)
                        promo_field_found = True
                        break
                    except TimeoutException:
                        continue

                if not promo_field_found:
                    logger.error("Could not find promotion code input field")
                    return False

                # Step 3: Click "Apply" button
                apply_button_selectors = [
                    "//button[contains(text(), 'Apply')]",
                    "//input[contains(@value, 'Apply')]",
                    "//button[@type='submit']"
                ]

                apply_button_found = False
                for selector in apply_button_selectors:
                    try:
                        apply_button = self.driver.find_element(By.XPATH, selector)
                        apply_button.click()
                        logger.info("Clicked 'Apply' button for promotion code")
                        time.sleep(5)  # Wait for page to update with discount
                        apply_button_found = True
                        break
                    except NoSuchElementException:
                        continue

                if not apply_button_found:
                    logger.error("Could not find 'Apply' button")
                    return False
            else:
                logger.info("Promotion code already applied successfully")

            # Step 4: Fill in name field
            logger.info("Looking for name field...")
            name_selectors = [
                "//input[contains(@name, 'name') or contains(@placeholder, 'name') or contains(@placeholder, 'Name')]",
                "//input[contains(@autocomplete, 'name')]",
                "//input[contains(@id, 'name')]"
            ]

            name_field_found = False
            for selector in name_selectors:
                try:
                    name_field = self.driver.find_element(By.XPATH, selector)
                    current_value = name_field.get_attribute('value') or ""
                    if not current_value.strip():
                        name_field.send_keys("kendall")
                        logger.info("Filled name field with 'kendall'")
                    else:
                        logger.info(f"Name field already has value: {current_value}")
                    name_field_found = True
                    break
                except NoSuchElementException:
                    continue

            if not name_field_found:
                logger.warning("Could not find name field")

            # Step 5: Handle address field
            logger.info("Looking for address field...")

            # First check if we need to click "Enter address to calculate"
            try:
                address_trigger = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Enter address to calculate')]")
                address_trigger.click()
                logger.info("Clicked 'Enter address to calculate'")
                time.sleep(3)
            except NoSuchElementException:
                logger.info("No address trigger found, looking for address field directly")

            # Fill in address fields
            address_selectors = [
                "//input[contains(@name, 'address') or contains(@placeholder, 'address')]",
                "//input[contains(@autocomplete, 'address')]",
                "//input[contains(@id, 'address')]",
                "//input[contains(@placeholder, 'Address')]",
                "//input[contains(@placeholder, 'Enter address manually')]"
            ]

            address_field_found = False
            for selector in address_selectors:
                try:
                    address_field = self.driver.find_element(By.XPATH, selector)
                    address_field.clear()
                    address_field.send_keys("1200 market street")
                    logger.info("Filled address field with '1200 market street'")
                    # Press Enter after filling address
                    address_field.send_keys(Keys.RETURN)
                    logger.info("Pressed Enter after filling address")
                    time.sleep(3)  # Wait a bit longer for address processing
                    address_field_found = True
                    break
                except NoSuchElementException:
                    continue

            if not address_field_found:
                logger.warning("Could not find address field")

            # Step 5b: Fill in city field
            logger.info("Looking for city field...")
            city_selectors = [
                "//input[contains(@name, 'city') or contains(@placeholder, 'city') or contains(@placeholder, 'City')]",
                "//input[contains(@autocomplete, 'address-level2')]",
                "//input[contains(@id, 'city')]"
            ]

            city_field_found = False
            for selector in city_selectors:
                try:
                    city_field = self.driver.find_element(By.XPATH, selector)
                    city_field.clear()
                    city_field.send_keys("San Francisco")
                    logger.info("Filled city field with 'San Francisco'")
                    time.sleep(1)
                    city_field_found = True
                    break
                except NoSuchElementException:
                    continue

            if not city_field_found:
                logger.warning("Could not find city field")

            # Step 5c: Fill in state field
            logger.info("Looking for state field...")
            state_selectors = [
                "//input[contains(@name, 'state') or contains(@placeholder, 'state') or contains(@placeholder, 'State')]",
                "//select[contains(@name, 'state') or contains(@id, 'state')]",
                "//input[contains(@autocomplete, 'address-level1')]",
                "//input[contains(@id, 'state')]"
            ]

            state_field_found = False
            for selector in state_selectors:
                try:
                    state_field = self.driver.find_element(By.XPATH, selector)
                    if state_field.tag_name.lower() == 'select':
                        # Handle dropdown
                        select = Select(state_field)
                        try:
                            select.select_by_value("CA")
                        except:
                            try:
                                select.select_by_visible_text("California")
                            except:
                                select.select_by_visible_text("CA")
                        logger.info("Selected state 'CA' from dropdown")
                    else:
                        # Handle text input
                        state_field.clear()
                        state_field.send_keys("CA")
                        logger.info("Filled state field with 'CA'")
                    time.sleep(1)
                    state_field_found = True
                    break
                except NoSuchElementException:
                    continue

            if not state_field_found:
                logger.warning("Could not find state field")

            # Step 5d: Fill in zip code field
            logger.info("Looking for zip code field...")
            zip_selectors = [
                "//input[contains(@name, 'zip') or contains(@placeholder, 'zip') or contains(@placeholder, 'Zip')]",
                "//input[contains(@name, 'postal') or contains(@placeholder, 'postal')]",
                "//input[contains(@autocomplete, 'postal-code')]",
                "//input[contains(@id, 'zip') or contains(@id, 'postal')]"
            ]

            zip_field_found = False
            for selector in zip_selectors:
                try:
                    zip_field = self.driver.find_element(By.XPATH, selector)
                    zip_field.clear()
                    zip_field.send_keys("94102")
                    logger.info("Filled zip code field with '94102'")
                    time.sleep(1)
                    zip_field_found = True
                    break
                except NoSuchElementException:
                    continue

            if not zip_field_found:
                logger.warning("Could not find zip code field")

            # Step 6: Click "Complete order" button
            logger.info("Looking for Complete order button...")
            complete_order_selectors = [
                "//button[contains(text(), 'Complete order')]",
                "//button[contains(text(), 'Complete')]",
                "//button[contains(text(), 'Pay')]",
                "//button[@type='submit']",
                "//input[@type='submit']"
            ]

            complete_order_found = False
            for selector in complete_order_selectors:
                try:
                    complete_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    complete_button.click()
                    logger.info("Clicked 'Complete order' button")
                    time.sleep(5)  # Wait for order processing
                    complete_order_found = True
                    break
                except TimeoutException:
                    continue

            if not complete_order_found:
                logger.error("Could not find 'Complete order' button")
                return False

            return True
            
        except Exception as e:
            logger.error(f"Error handling Stripe page: {e}")
            return False
    
    def complete_purchase(self):
        """Click the complete purchase button."""
        try:
            logger.info("Looking for complete purchase button...")
            
            purchase_selectors = [
                "//button[contains(text(), 'Complete purchase')]",
                "//button[contains(text(), 'complete purchase')]",
                "//button[contains(text(), 'Purchase')]",
                "//button[contains(text(), 'Buy')]",
                "//button[contains(@type, 'submit')]"
            ]
            
            for selector in purchase_selectors:
                try:
                    button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    button.click()
                    logger.info("Clicked complete purchase button")
                    time.sleep(5)  # Wait for processing
                    return True
                except TimeoutException:
                    continue
            
            logger.error("Could not find complete purchase button")
            return False
            
        except Exception as e:
            logger.error(f"Error completing purchase: {e}")
            return False

    def close_stripe_tab_and_return(self):
        """Close the Stripe tab and return to the original Windsurf tab."""
        try:
            all_windows = self.driver.window_handles
            if len(all_windows) > 1:
                # Close current tab (should be Stripe)
                self.driver.close()
                logger.info("Closed Stripe tab")

                # Switch back to the first tab (Windsurf)
                self.driver.switch_to.window(all_windows[0])
                logger.info("Switched back to Windsurf tab")
                time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Error closing Stripe tab: {e}")
            return False

    def claim_credit_once(self):
        """Execute one complete credit claiming cycle."""
        try:
            logger.info("Starting credit claiming cycle...")
            
            if not self.navigate_to_windsurf():
                return False
            
            if not self.click_purchase_credit():
                return False
            
            # At this point we should be on the Stripe tab
            if not self.handle_stripe_page():
                return False

            # After successful purchase, close Stripe tab and return to Windsurf
            self.close_stripe_tab_and_return()

            logger.info("Credit claiming cycle completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error in credit claiming cycle: {e}")
            return False
    
    def claim_credits_multiple(self, count=1):
        """Claim credits multiple times using parallel Chrome instances."""
        import threading
        import queue

        successful_claims = 0
        results_queue = queue.Queue()

        def claim_worker(worker_id):
            """Worker function for parallel claiming."""
            try:
                # Create a new instance for this worker
                worker_claimer = WindsurfCreditClaimer(headless=self.headless)
                logger.info(f"Worker {worker_id}: Starting credit claim")

                if worker_claimer.claim_credit_once():
                    results_queue.put(('success', worker_id))
                    logger.info(f"Worker {worker_id}: Successfully claimed credit")
                else:
                    results_queue.put(('failure', worker_id))
                    logger.error(f"Worker {worker_id}: Failed to claim credit")

                # Clean up
                worker_claimer.close()

            except Exception as e:
                logger.error(f"Worker {worker_id}: Error - {e}")
                results_queue.put(('error', worker_id))

        # Create and start threads
        threads = []
        for i in range(count):
            thread = threading.Thread(target=claim_worker, args=(i + 1,))
            threads.append(thread)
            thread.start()
            logger.info(f"Started worker {i + 1} of {count}")

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Collect results
        while not results_queue.empty():
            result, worker_id = results_queue.get()
            if result == 'success':
                successful_claims += 1

        logger.info(f"Completed! Successfully claimed {successful_claims} out of {count} credits")
        return successful_claims
    
    def close(self):
        """Close the browser driver."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

def main():
    """Main function to run the credit claimer."""
    claimer = None
    try:
        # Initialize the claimer (set headless=True to run without GUI)
        claimer = WindsurfCreditClaimer(headless=False)
        
        # Ask user how many times to run
        try:
            count = int(input("How many times would you like to claim credits? (default: 1): ") or "1")
        except ValueError:
            count = 1
        
        # Run the credit claiming process
        successful_claims = claimer.claim_credits_multiple(count)
        
        print(f"\nProcess completed! Successfully claimed {successful_claims} credits.")
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if claimer:
            claimer.close()

if __name__ == "__main__":
    main()
