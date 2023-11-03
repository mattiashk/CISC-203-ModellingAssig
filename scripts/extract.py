import json

# Read the data from a JSON file
with open('data/reference/sections.json', 'r') as file:
    data = json.load(file)

# Filter and extract courses with "id" containing "CISC"
cisc_courses = [course for course in data if "CISC" in course["id"]]

# Create a new JSON file "other.json" with the filtered courses
with open("data/testing-2/sections.json", "w") as output_file:
    json.dump(cisc_courses, output_file, indent=4)

print("Filtered courses saved to 'other.json'.")