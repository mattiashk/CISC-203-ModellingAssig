#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' #no color

# Edit config.json and set parameters
update_json() {
    key=$1
    value=$2
    CONFIG_FILE="config.json"

    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}WARNING jq is not installed. Please install jq to use this script.${NC}"
        echo "using -> sudo apt install jq"
        exit 1
    fi

    # Using jq to update the JSON file
    jq ".$key = $value" "$CONFIG_FILE" > temp.json && mv temp.json "$CONFIG_FILE"
}
 

build_and_start_all() {
    docker-compose up -d

}

build_and_start_sat() {
    echo "Building the SAT solver service..."
    docker-compose up -d sat_solver_204
}


start_sat_solver_solo(){
    docker exec $SAT_SOLVER_CONTAINER_ID python3 run.py
}

start_sat_solver() {
    docker exec $SAT_SOLVER_CONTAINER_ID python3 run.py > /dev/null 2>&1
}

start_nextjs_app() {
    docker exec $WEB_APP_CONTAINER_ID npm start > /dev/null 2>&1
}

get_docker_containers() {
    WEB_APP_CONTAINER_ID=$(docker-compose ps -q web_app_204)
    SAT_SOLVER_CONTAINER_ID=$(docker-compose ps -q sat_solver_204)
}

is_web_app_running() {
    docker ps -q -f name=web_app_204
}

is_sat_solver_running() {
    docker ps -q -f name=sat_solver_204
}

# Clean up processes on exit
cleanup() {
    get_docker_containers
    echo 'Stopping all processes...'

    if is_web_app_running; then
        docker stop $WEB_APP_CONTAINER_ID 2> /dev/null &
    fi
    docker stop $SAT_SOLVER_CONTAINER_ID 2> /dev/null
    exit
}
trap cleanup SIGINT SIGTERM

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --build) build_flag=true; shift ;;
        --start) start_flag=true; shift ;;
        --console) console_flag=true; shift ;;
        --run) run_flag=true; shift ;;
        --stop) stop_flag=true; shift;;
    esac
done


if [[ $build_flag == true && $console_flag == true ]]; then
    update_json "use_web_app" "false"
    build_and_start_sat
    get_docker_containers
    docker exec -it $SAT_SOLVER_CONTAINER_ID python3 run.py

elif [[ $start_flag ]]; then
    if [[ $console_flag ]]; then
        build_and_start_sat
        get_docker_containers
        docker exec -it $SAT_SOLVER_CONTAINER_ID python3 run.py
    else
        build_and_start_all

    fi


elif [[ $build_flag == true ]]; then
    echo "Building the Python Sat Solver and the Nextjs Web App"
    update_json "use_web_app" "true"
    build_and_start_all

elif [[ $run_flag == true ]]; then
    runmode=true
    get_docker_containers

    #SAT
    if [[ $console_flag == true ]]; then
        echo -e "${GREEN}Success!${NC}"
        docker exec -it $SAT_SOLVER_CONTAINER_ID python3 run.py

    #WEBAPP
    else
        start_sat_solver &
        echo -e "${GREEN}Success!${NC}"
        echo -e "${GREEN}The Web App is available: http://localhost:3000/${NC}"
        start_nextjs_app
        if [ $? -eq 1 ]; then
            echo -e "${RED}WARNING An Error has occured starting the Web App!${NC}"
        fi
        
    fi

elif [[ $stop_flag == true ]]; then
    cleanup

else
    echo "Invalid option: -$OPTARG" >&2
    echo "Please specify a build or run option"
    exit 1
fi