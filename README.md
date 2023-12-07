# ReadMe

<br/>
<p align="center">
  <a>
    <img src="/documentation/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Schedule Sensi</h3>

  <p align="center">Optimize course schedules by leveraging our SAT solver's logical model</p>
  <p align="center"> CISC-204 Modelling Project</p>
  <p align="center">
    <a href="https://github.com/mattiashk/CISC-204-ModellingAssig/blob/main/documents/final/Modelling-Report.pdf">Explore the Report</a>
  </p>
</p>

# CISC/CMPE 204 Modelling Project

The aim of this project is to create a logical model that allows a student to input a tentative course schedule and assess its feasibility. The model will consider various factors, including course prerequisites, and time conflicts. By applying principles of natural deduction, the model will attempt to evaluate a feasible solution satisfying all constraints and ensuring all necessary requirements are met.

## Table Of Contents
- [Features](#features)
- [Structure](#structure)
- [Installation](#installation)
	- [Running With Docker](#running-with-docker)
	- [Configuration](#configuration)
- [Usage](#usage)
    - [Overview](#overview)
	- [Custom Test Cases](#custom-test-cases)
- [Contents](#contents)
- [Uninstall](#uninstall)
- [Acknowledgements](#acknowledgements)

## Features
- Student-Course Matching
- Conflict Resolution
- Prerequisite, Corequisite Tracking
- Course Exclusion
- Friendship Considerations
- Flexible Term Enrollment
- Time Conflict Avoidance
- Maximized Course Enrollment

## Structure

***Folders***

- `documents` Contains both draft and final submissions.
- `data` Contains both test and main data sets from [qmulus](https://github.com/queens-qmulus/datasets).
- `webapp` Contains a Nextjs web app to view and interact with generated timetable solutions.

***Files***

- `run.py`General wrapper script to execute the sat solver.
- `sat_solver.py` The Python SAT solver constraint and proposition models, as well as compile and solve functions.
- `datalayer.py` Defines classes for representing Queens courses, departments, requirements, and sections, as well as collections of these elements.
- `timetable.py` Defines timetable classes and JSON Serialization functions.
- `webapp_api.py` Defines a Flask API for parsing requested SAT solver test cases.
- `utils.py` Contains utility classes and functions for the timetable scheduling SAT solver.
- `test.py` Submission requirements and theory size checks.

## Installation
### Running With Docker

By far the most reliable way to get this project running is with [Docker](https://www.docker.com/). This section runs through the steps.

1. First, download Docker https://www.docker.com/get-started
2. Navigate to your project folder on the command line.
3. We have created a bash script `model.sh` to help you build and run the project given your desired preferences. **(Web App and Console modes)**
- This script is just a simple wrapper that executes commands in your docker containers to prevent blocking or terminal tie ups.
- [This section](#alternative-install) outlines the steps without using `model.sh`.
4. Our script **requires jq**, a json processor. It can be installed by running `sudo apt install jq` in your console.
    
    ### **Using the Web App**
    
    If you would like to run the *Python SAT Solver* and use the *Nextjs Web App* for interaction with the Solver: 
	
    *From the project folder run to following commands.*
	a. Ensure the model.sh has execute permission.
	```sh
		chmod +x model.sh
	```
	
    b. Build both the Sat Solver and the Web App containers.
	```sh
		./model.sh --build
	```
    c. Start both the Sat Solver and the Web App
	```sh
		./model.sh --start
	```
    d. The Web App can be accessed at [http://localhost:3000/](http://localhost:3000/)
    e. To stop both the Web App and the Sat Solver, you can `Ctrl+C` in the terminal to interrupt and shut down both containers. Running the following command is also an option if your terminal is not tied up.
	```sh
		./model.sh --shutdown
	```
    f. From the shutdown state both the Sat Solver and the Web APP containers can be restarted with `./model.sh --start` followed by `./model.sh --run` to run both programs.
    
    ### **Using the Console**
    
    If you would like to run the *Python SAT Solver* and use the *Console* for interaction: 
    
    *From the project folder run to following commands.*
    
    a. Build the Sat Solver container*
	```sh
		./model.sh --build --console
	```
    b. Starts the Sat Solver
	```sh
		./model.sh --start --console
	```
    c. The Sat Solver can then be used through the terminal.
    d. To stop the Sat Solver, you can `Ctrl+C` in the terminal to interrupt and shut down the container. Running the following is also an option if your terminal is not tied up.
	```sh
		./model.sh --shutdown
	```
    e. From the shutdown state the Sat Solver container can be restarted with `./model.sh --start --console` followed by `./model.sh --run --console` to run the program.
    
    <a id="alternative-install"></a>**Alternative Using Docker Compose**
    
    *More complicated*
    
    1. Running `docker-compose up -d`  will build the Python SAT Solver image `sat_solver_204` as well as the Nextjs Web App `web_app_204` image as well as create and start both containers.
        
        Note that the -d option is important as it runs the command in the background to avoid tying up the terminal, preventing further commands from being run.
        
    2. From there the two containers should be connected. Both containers share a local network `webapp_network` for HTTP communications. The SAT Solver container project directory is also linked to the local project folder so that everything you do in one automatically updates in the other.
    3. **IMPORTANT** You must ensure your desired preferences exist in the `config.json` file if using this method, otherwise the app may run in console mode as a background process, or vise versa.
    4. **Web App Mode**
        1. To start the Nextjs Web App you must run
	```sh
	docker exec -d $(docker-compose ps -q web_app_204) npm start
	```
 *This executes `npm start` in the web_app_204 container as a background process*
            
2. To start the Python Sat Solver you must run
	```sh
	docker exec -d $(docker-compose ps -q sat_solver_204) python3 run.py
	```
*This executes `python3 run.py` in the sat_colver_204 container*
            
3. The Web App can be accessed at [http://localhost:3000/](http://localhost:3000/)
4. To stop both the Web App and the Sat Solver, you must shutdown the containers using the Docker Desktop GUI or by running:
	```sh
	docker-compose stop $(docker-compose ps -q web_app_204)
	```
*stops the Web App*
	```sh
	docker-compose stop $(docker-compose ps -q sat_solver_204)
	```
*stops the SAT Solver*
            
5. **Console Mode**
   1. To start the Python Sat Solver you must run
	```sh
	docker exec -it $(docker-compose ps -q sat_solver_204) python3 run.py
	```
   *This executes `python3 run.py)` in the sat_colver_204 container*
            
    2. To stop the Sat Solver, you can enter `e` as input, to shutdown the containers you can use the Docker Desktop GUI or run:
	```sh
	docker-compose stop $(docker-compose ps -q sat_solver_204)
	```
    *stops the SAT Solver*

### Configuration
Please read the [configuration overview]()
            
## Usage
### Overview
**Web App Mode**

After running the project in the Web App Mode and visiting the home page [http://localhost:3000/](http://localhost:3000/) you will be greeted with a blank page with no student data, as no tests have been ran.

![schedule-sense-capture-01](/documentation/schedule-sense-capture-01.png)

Selecting the drop-down reveals pre-configured test cases, that can be selected and ran in the Sat Solver using the *“Generate New Data button”*.

![schedule-sense-capture-02](/documentation/schedule-sense-capture-02.png)

After generating the solution the page will refresh and a table containing students and there enrolled terms will appear. A students term schedule can then be viewed using the *“view”* button located in the table.

![schedule-sense-capture-03](/documentation/schedule-sense-capture-03.png)

A specific students time table may resemble the following

![schedule-sense-capture-04](/documentation/schedule-sense-capture-04.png)

**Console Mode**

After running the project in Console Mode the following message will be displayed in the console

![schedule-sense-capture-05](/documentation/schedule-sense-capture-05.png)

This prompt accepts user input for a *test case id*. After entering a case the solution is directed to the console.

![schedule-sense-capture-06](/documentation/schedule-sense-capture-06.png)

The Console Mode remains in a while loop repeatedly asking for user input until the `e` key is entered closing the program.

### Custom Test Cases
Please read the [creating custom test cases overview](https://github.com/mattiashk/CISC-204-ModellingAssig/blob/main/data/README.md)

## Contents
- [Web App Overview](https://github.com/mattiashk/CISC-204-ModellingAssig/tree/main/nextjs_app#readme)
- [Data Set Overview](https://github.com/mattiashk/CISC-204-ModellingAssig/blob/main/data/reference/README.md)
- [Creating Custom Test Cases](https://github.com/mattiashk/CISC-204-ModellingAssig/blob/main/data/README.md)

## Uninstall

To remove all docker containers, volumes, and networks used by this project you can run
```sh
./model.sh —uninstall
```
*if you wish to use our script*
OR
```sh
docker-compose down --volumes --rmi all
```

## Acknowledgements
- [bauhaus](https://github.com/QuMuLab/bauhaus)
- [qmulus](https://github.com/queens-qmulus/datasets)
- [syncfusion](https://www.syncfusion.com/)
