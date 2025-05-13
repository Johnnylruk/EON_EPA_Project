import os

class ApplicationLogServices():

    def create_exception_logs(self):
        os.mkdir("application_logs")
        
         

    def log_exceptions(self):
        """
            @params: None

            @returns: None

            @exception: Exception
                - logs exception message in application logs

        
            Logs exception in applications_logs.txt
        """
        self.create_exception_logs()
        