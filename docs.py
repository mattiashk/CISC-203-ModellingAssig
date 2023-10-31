import sys
from contextlib import redirect_stdout
import datalayer

docs = ''

# Redirect stdout to the file
with open("documentation.txt", "w") as text_file:
    with redirect_stdout(text_file):
        docs += str(help(datalayer.Course))
        docs += str(help(datalayer.Courses))
        docs += str(help(datalayer.Section))
        docs += str(help(datalayer.SectionDates))
        docs += str(help(datalayer.SectionDate))
        docs += str(help(datalayer.Sections))
        docs += str(help(datalayer.Student))
        docs += str(help(datalayer.Students))

# After this block, the stdout is restored to the console

# Optionally, print the documentation to the console
print(docs)
