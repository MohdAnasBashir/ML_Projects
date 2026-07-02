##Imports Python's sys module.
import sys
#function named error_message_details.
#It accepts:
#error → the actual exception (e.g., ZeroDivisionError)
#error_detail → the sys module
def error_message_details(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    #returns
    #Exception type
    #Exception object
    #Traceback object

    #Extracts the filename where the error occurred.
    file_name = exc_tb.tb_frame.f_code.co_filename


    #Starts creating a string that will hold the final error message.
    #Creates a template.
    #Starts replacing the placeholders with real values.
    error_message = (
        "Error occurred in python script "
        "name [{0}] line number [{1}] error message [{2}]"
    ).format(
        file_name,
        exc_tb.tb_lineno,
        str(error)
    )
    #Returns the completed error message to the code that called this function.
    return error_message

#Creates your own custom exception.
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        #Calls the parent (Exception) constructor.
        super().__init__(error_message)
        self.error_message=error_message_details(error_message,error_detail=error_detail)
    def __str__(self):
        return self.error_message
    





