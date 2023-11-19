#                                     Stack or Queue?

# Challenge 1: Browser Back Button
# Scenario: You're writing a simple web browser. Implement a feature to keep track of the pages visited, so that when the 'Back' button is pressed, the browser goes back to the previously visited page.

# Hint: Think about the order in which web pages are visited and how the 'Back' button should work. Does it follow a Last-In-First-Out (LIFO) or a First-In-First-Out (FIFO) approach?

class BrowserHistory:
    def __init__(self):
        # Initialize your data structure here
        # TODO: Implement this

    def visit(self, page):
        # User visits a page
        # TODO: Implement this

    def back(self):
        # User presses the back button
        # TODO: Implement this
        pass

# Test the BrowserHistory class
def test_browser_history():
    # TODO: Create a BrowserHistory instance and test visiting pages and going back

test_browser_history()

#----------------------------------------------------------------------------------------------

# Challenge 2: Printer Queue
# Scenario: Create a system for a printer to manage print jobs. Each new print request should be added to the printer's list of jobs, and jobs should be printed in the order they were received.

# Hint: Consider how a printer processes print jobs. Should it print the most recently added job first or the first job that was added?

class PrinterQueue:
    def __init__(self):
        # Initialize your printer queue here
        # TODO: Implement this

    def add_job(self, job):
        # Add a print job to the queue
        # TODO: Implement this

    def print_job(self):
        # Print the next job in the queue
        # TODO: Implement this
        pass

# Test the PrinterQueue class
def test_printer_queue():
    # TODO: Create a PrinterQueue instance and test adding and printing jobs

test_printer_queue()


#----------------------------------------------------------------------------------------------

# Challenge 3: Undo Functionality in a Text Editor
# Scenario: Implement an 'Undo' feature in a text editor. This feature should allow users to undo their last action, and each subsequent undo should reverse the previous action in reverse order.

# Hint: Reflect on how the undo functionality should work. When a user undoes an action, should it be the most recent one or the oldest one?

class TextEditor:
    def __init__(self):
        # Initialize your data structure here
        # TODO: Implement this

    def write(self, text):
        # User writes text
        # TODO: Implement this

    def undo(self):
        # Undo the last write action
        # TODO: Implement this
        pass

# Test the TextEditor class
def test_text_editor():
    # TODO: Create a TextEditor instance and test writing and undoing

test_text_editor()


#----------------------------------------------------------------------------------------------

# Challenge 4: Customer Service Line
# Scenario: Design a system to manage a customer service line. Customers call and are put on hold until a representative is available. The system should ensure that the customers are served in the order they called.

# Hint: Think about the order in which customers should be served. Is it fair to serve the last caller first, or should it be the first caller?

class CustomerServiceLine:
    def __init__(self):
        # Initialize your data structure here
        # TODO: Implement this

    def call_received(self, customer):
        # A new customer call is received
        # TODO: Implement this

    def serve_customer(self):
        # Serve the next customer
        # TODO: Implement this
        pass

# Test the CustomerServiceLine class
def test_customer_service():
    # TODO: Create a CustomerServiceLine instance and test receiving and serving calls

test_customer_service()


#----------------------------------------------------------------------------------------------

# Challenge 5: Balancing Parentheses
# Scenario: Write a program that checks if a string of parentheses is balanced. Every opening parenthesis should have a corresponding closing parenthesis in the correct order.

# Hint: Analyze how parentheses open and close. When checking for balance, do you need to consider the most recent parenthesis first, or the first parenthesis that was opened?

def is_balanced(parentheses):
    # Check if the parentheses string is balanced
    # TODO: Implement this function
    pass

# Test the is_balanced function
def test_balancing_parentheses():
    # TODO: Test the function with different parentheses strings

test_balancing_parentheses()
