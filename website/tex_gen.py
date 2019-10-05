import sys, os
from subprocess import call
import hashlib

class TexGenerator(object):
    def __init__(self, expression):
        self.expression = expression
        self.fileHased  = self.generateUniqueID(expression)
        
        self.generateTexFile(expression)
        self.tex_to_pdf()
        
    def generatePath(self, extension):
        return os.path.join("tmp/", self.fileHased + extension)
    
    def generateUniqueID(self, expression):
        return hashlib.sha256(expression.encode("utf-8")).hexdigest()[:16]

    def generateTexFile(self, expression):
        result = self.generatePath(".tex")
        if not os.path.exists(result):
            with open("template.tex", "r") as latex:
                body = latex.read()

            body = body.replace("REPLACE_ME", expression)

            with open(str(self.generatePath(".tex")), "w") as outfile:
                outfile.write(body)
    
    def tex_to_pdf(self):
        result = self.generatePath(".div")
        if not os.path.exists(result):
            command = ["pdflatex", "-interaction=batchmode", "-output-directory=" + "tmp/", str(self.generatePath(".tex")), ">", "/dev/null"]
            exitCode = os.system(" ".join(command))
