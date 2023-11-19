#                                     Stack or Queue?


print("\nBROWSER HISTORY -----------------------------------------------------------------------------------------------")
# Challenge 1: Browser Back Button
# Scenario: You're writing a simple web browser. Implement a feature to keep track of the pages visited, so that when the 'Back' button is pressed, the browser goes back to the previously visited page.

# Hint: Think about the order in which web pages are visited and how the 'Back' button should work. Does it follow a Last-In-First-Out (LIFO) or a First-In-First-Out (FIFO) approach?

class BrowserHistory:
    def __init__(self):
        """ Initialize your data structure here"""
        self.history = []

    def visit(self, page):
        """ User visits a page """
        self.history.append(page)

    def back(self):
        """ User presses the back button """
        if self.history:
            self.history.pop()
        return "No pages visited"


# Test the BrowserHistory class
def test_browser_history():
    """ Test the BrowserHistory class"""
    browser = BrowserHistory()
    browser.visit("google.com")
    browser.visit("facebook.com")
    browser.visit("leetcode.com")
    print(browser.history)
    print(browser.back())  # "leetcode.com"
    print(browser.back())  # "facebook.com"
    print(browser.back())  # "google.com"
    print(browser.back())  # "No pages visited"


test_browser_history()

print("\nPRINT QUEUE -----------------------------------------------------------------------------------------------")
# ----------------------------------------------------------------------------------------------

# Challenge 2: Printer Queue
# Scenario: Create a system for a printer to manage print jobs. Each new print request should be added to the printer's list of jobs, and jobs should be printed in the order they were received.

# Hint: Consider how a printer processes print jobs. Should it print the most recently added job first or the first job that was added?

class PrinterQueue:
    def __init__(self):
        """# Initialize your printer queue here """
        self.queue = []

    def add_job(self, job):
        """ # Add a print job to the queue """
        self.queue.append(job)

    def print_job(self):
        """ Print the next job in the queue """
        if self.queue:
            return self.queue.pop(0)
        return "No more jobs to print"


# Test the PrinterQueue class
def test_printer_queue():
    """ Test the PrinterQueue class"""
    printer = PrinterQueue()
    printer.add_job("Job 1")
    printer.add_job("Job 2")
    printer.add_job("Job 3")
    print(printer.print_job())  # "Job 1"
    print(printer.print_job())  # "Job 2"
    print(printer.print_job())  # "Job 3"
    print(printer.print_job())  # "No more jobs to print"


test_printer_queue()

print("\nTEXT EDITOR -----------------------------------------------------------------------------------------------")
# ----------------------------------------------------------------------------------------------

# Challenge 3: Undo Functionality in a Text Editor
# Scenario: Implement an 'Undo' feature in a text editor. This feature should allow users to undo their last action, and each subsequent undo should reverse the previous action in reverse order.

# Hint: Reflect on how the undo functionality should work. When a user undoes an action, should it be the most recent one or the oldest one?

class TextEditor:
    def __init__(self):
        """ Initialize your data structure here """
        self.content = ""
        self.history = []

    def write(self, text):
        """ User writes text """
        self.history.append(self.content)
        self.content += text

    def undo(self):
        """ Undo the last write action """
        if self.history:
            self.content = self.history.pop()
            return self.content
        return "Nothing to undo"


# Test the TextEditor class
def test_text_editor():
    """ Test the TextEditor class"""
    editor = TextEditor()
    editor.write("Hello")
    editor.write(" World")
    editor.write("!")
    print(editor.undo())  # "Hello World"
    print(editor.undo())  # "Hello"
    print(editor.undo())  # ""
    print(editor.undo())  # "Nothing to undo"


test_text_editor()

print("\nCUSTOMER SERVICE -----------------------------------------------------------------------------------------------")
# ----------------------------------------------------------------------------------------------

# Challenge 4: Customer Service Line
# Scenario: Design a system to manage a customer service line. Customers call and are put on hold until a representative is available. The system should ensure that the customers are served in the order they called.

# Hint: Think about the order in which customers should be served. Is it fair to serve the last caller first, or should it be the first caller?

class CustomerServiceLine:
    def __init__(self):
        """ Initialize your data structure here """
        self.queue = []

    def call_received(self, customer):
        """ A new customer call is received """
        self.queue.append(customer)

    def serve_customer(self):
        """ Serve the next customer """
        if self.queue:
            return self.queue.pop(0)
        return "No customers waiting"


# Test the CustomerServiceLine class
def test_customer_service():
    """ Test the CustomerServiceLine class"""
    customer_service = CustomerServiceLine()
    customer_service.call_received("Customer 1")
    customer_service.call_received("Customer 2")
    customer_service.call_received("Customer 3")
    print(customer_service.serve_customer())  # "Customer 1"
    print(customer_service.serve_customer())  # "Customer 2"
    print(customer_service.serve_customer())  # "Customer 3"
    print(customer_service.serve_customer())  # "No customers waiting"


test_customer_service()

print("\nBALANCING PARENTHESES -----------------------------------------------------------------------------------------------")
# ----------------------------------------------------------------------------------------------

# Challenge 5: Balancing Parentheses
# Scenario: Write a program that checks if a string of parentheses is balanced. Every opening parenthesis should have a corresponding closing parenthesis in the correct order.

# Hint: Analyze how parentheses open and close. When checking for balance, do you need to consider the most recent parenthesis first, or the first parenthesis that was opened?

def is_balanced(parentheses):
    """ Check if the parentheses string is balanced """
    stack = []
    for p in parentheses:
        if p == "(":
            stack.append(p)
        elif p == ")":
            if stack:
                stack.pop()
            else:
                return False
    return len(stack) == 0


# Test the is_balanced function
def test_balancing_parentheses():
    """ Test the is_balanced function """
    print(is_balanced("()()"))  # True
    print(is_balanced("(()"))  # False
    print(is_balanced("())"))  # False
    print(is_balanced("((()))"))  # True
    print(is_balanced("((())"))  # False


test_balancing_parentheses()
