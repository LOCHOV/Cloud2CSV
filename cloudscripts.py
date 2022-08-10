import argparse

import AWS

#from GCP import *
#from AZR import *
#aws_s3_inventory_csv.main()

class user_selection:
    def __init__(self, csp, script):
        self.csp = csp
        self.script = script

    def aws_selected(self):
        print("Importing the AWS modules")
        print(self.csp + self.script)



print(dir(AWS))
user = user_selection("AWS","S3")
user.aws_selected()





print("done")