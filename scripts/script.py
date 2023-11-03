def course_requriement_extracter():
    input_file = "requirements.txt"
    output_file = "requirements-cisc.txt"

    with open(input_file, "r") as input_file, open(output_file, "w") as output_file:
        for line in input_file:
            if "CISC-" in line:
                output_file.write(line + "\n")
                                
course_requriement_extracter()