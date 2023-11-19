# Stack or Queue?

print("\nBROWSER HISTORY -----------------------------------------------------------------------------------------------")
# Challenge 1: Browser Back Button
class BrowserHistory:
    def __init__(self):
        """ Initialize your data structure here """
        pass

    def visit(self, page):
        """ User visits a page """
        pass

    def back(self):
        """ User presses the back button """
        pass

def test_browser_history():
    browser = BrowserHistory()
    browser.visit("google.com")
    browser.visit("facebook.com")
    browser.visit("leetcode.com")
    print(browser.back())  # Should return the last visited page
    print(browser.back())  # Should return the second last visited page
    print(browser.back())  # Should return the first visited page

test_browser_history()

print("\nPRINT QUEUE -----------------------------------------------------------------------------------------------")
# Challenge 2: Printer Queue
class PrinterQueue:
    def __init__(self):
        """ Initialize your printer queue here """
        pass

    def add_job(self, job):
        """ Add a print job to the queue """
        pass

    def print_job(self):
        """ Print the next job in the queue """
        pass

def test_printer_queue():
    printer = PrinterQueue()
    printer.add_job("Job 1")
    printer.add_job("Job 2")
    printer.add_job("Job 3")
    print(printer.print_job())  # Should print "Job 1"
    print(printer.print_job())  # Should print "Job 2"
    print(printer.print_job())  # Should print "Job 3"

test_printer_queue()

print("\nTEXT EDITOR -----------------------------------------------------------------------------------------------")
# Challenge 3: Undo Functionality in a Text Editor
class TextEditor:
    def __init__(self):
        """ Initialize your data structure here """
        pass

    def write(self, text):
        """ User writes text """
        pass

    def undo(self):
        """ Undo the last write action """
        pass

def test_text_editor():
    editor = TextEditor()
    editor.write("Hello")
    editor.write(" World")
    editor.write("!")
    print(editor.undo())  # Should undo the last write action
    print(editor.undo())  # Should undo the second last write action
    print(editor.undo())  # Should undo the first write action

test_text_editor()

print("\nCUSTOMER SERVICE -----------------------------------------------------------------------------------------------")
# Challenge 4: Customer Service Line
class CustomerServiceLine:
    def __init__(self):
        """ Initialize your data structure here """
        pass

    def call_received(self, customer):
        """ A new customer call is received """
        pass

    def serve_customer(self):
        """ Serve the next customer """
        pass

def test_customer_service():
    customer_service = CustomerServiceLine()
    customer_service.call_received("Customer 1")
    customer_service.call_received("Customer 2")
    customer_service.call_received("Customer 3")
    print(customer_service.serve_customer())  # Should serve "Customer 1"
    print(customer_service.serve_customer())  # Should serve "Customer 2"
    print(customer_service.serve_customer())  # Should serve "Customer 3"

test_customer_service()

print("\nBALANCING PARENTHESES -----------------------------------------------------------------------------------------------")
# Challenge 5: Balancing Parentheses
def is_balanced(parentheses):
    """ Check if the parentheses string is balanced """
    pass

def test_balancing_parentheses():
    print(is_balanced("()()"))  # Should return True
    print(is_balanced("(()"))  # Should return False
    print(is_balanced("())"))  # Should return False
    print(is_balanced("((()))"))  # Should return True
    print(is_balanced("((())"))  # Should return False

test_balancing_parentheses()
