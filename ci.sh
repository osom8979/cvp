#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)

USAGE="
Usage: ${BASH_SOURCE[0]} [options] command

Available command are:
  create-cache
  extract-cache
  install-packages
  test
  build
  deploy

Available options are:
  -h, --help       Print this message.
  --               Stop handling options.
"

cd "$ROOT_DIR" || exit 1

CI_PYPI_REPOSITORY_URL="${CI_SERVER_URL}/api/v4/projects/${CI_PROJECT_ID}/packages/pypi"
CACHE_ARCHIVE=$ROOT_DIR/cache.tar.gz
CACHES=(
    "$ROOT_DIR/.venv/"
    "$ROOT_DIR/.mypy_cache/"
    "$ROOT_DIR/.pytest_cache/"
)

function print_error
{
    # shellcheck disable=SC2145
    echo -e "\033[31m$@\033[0m" 1>&2
}

function print_message
{
    # shellcheck disable=SC2145
    echo -e "\033[32m$@\033[0m"
}

function print_line
{
    printf -v line '%*s' "$(tput cols)" '' && echo "${line// /-}"
}

function on_interrupt_trap
{
    print_error "An interrupt signal was detected."
    exit 1
}

trap on_interrupt_trap INT

function print_usage
{
    echo "$USAGE"
}

function exit_on_error
{
    local code=$?
    if [[ $code -ne 0 ]]; then
        exit $code
    fi
}

function run_create_cache
{
    if [[ -f "$CACHE_ARCHIVE" ]]; then
        rm -v "$CACHE_ARCHIVE"
    fi

    local files
    for f in "${CACHES[@]}"; do
        if [[ -e "$f" ]]; then
            files+=("$f")
        fi
    done

    print_message "Creating cache ..."
    for f in "${files[@]}"; do
        print_message " - Cache '$f'"
    done

    tar -czf "$CACHE_ARCHIVE" "${files[@]}"
    print_message "Cache creation complete!"
}

function run_extract_cache
{
    if [[ ! -f "$CACHE_ARCHIVE" ]]; then
        return
    fi

    print_message "Extracting cache ..."
    tar -xzf "$CACHE_ARCHIVE"
    print_message "Cache extraction complete!"
}

function run_install_packages
{
    print_message "Install python packages"

    bash "$ROOT_DIR/python" -m pip install -U pip
    exit_on_error

    bash "$ROOT_DIR/python" -m pip install -r "$ROOT_DIR/requirements.txt"
    exit_on_error
}

_TEMP_FILES=()

function _remove_temp_files
{
    if [[ ${#_TEMP_FILES[@]} -gt 0 ]]; then
        rm "${_TEMP_FILES[@]}"
    fi
}

function run_test
{
    print_message "Run python tests"

    local script_names=("black" "flake8" "isort" "mypy" "pytest")
    local script_length=${#script_names[@]}
    local script_pids=()
    local temp_files=()
    local exit_codes=()

    local script_name
    local temp_file
    local script_pid
    local exit_code

    trap _remove_temp_files EXIT

    for script_name in "${script_names[@]}"; do
        temp_file=$(mktemp || exit)
        temp_files+=("$temp_file")
        _TEMP_FILES+=("$temp_file")
    done

    for (( i = 0; i < script_length; i++ )); do
        script_name="${script_names[$i]}"
        temp_file=${temp_files[$i]}

        print_message "Executes script '$script_name'"

        bash "$ROOT_DIR/${script_name}.sh" &> "$temp_file" &
        script_pids+=($!)
    done

    for (( i = 0; i < script_length; i++ )); do
        script_name="${script_names[$i]}"
        script_pid=${script_pids[$i]}

        print_message "Waiting for completion of script '$script_name' with PID ${script_pid} ..."
        wait "${script_pid}"
        exit_codes+=($?)
    done

    for (( i = 0; i < script_length; i++ )); do
        script_name="${script_names[$i]}"
        temp_file=${temp_files[$i]}
        exit_code=${exit_codes[$i]}

        if [[ $exit_code -eq 0 ]]; then
            print_message "Script '$script_name' completed successfully."
        else
            print_error "$(print_line)"
            print_error "Error ${exit_code} occurred in script '$script_name'."
            cat "$temp_file"
        fi
    done

    for exit_code in "${exit_codes[@]}"; do
        if [[ $exit_code -ne 0 ]]; then
            exit 1
        fi
    done
}

function run_build
{
    print_message "Build the backend"
    bash "$ROOT_DIR/build.sh"
    exit_on_error
}

function run_deploy_pypi
{
    local repository
    local username
    local password

    repository="${PYPI_REPOSITORY_URL:-$CI_PYPI_REPOSITORY_URL}"

    # GitLab > User Settings > Personal Access Tokens
    # Name is {PYPI_USERNAME}
    # Token is {PYPI_PASSWORD}
    # Scopes is api
    username="${PYPI_USERNAME}"
    password="${PYPI_PASSWORD}"

    if [[ -z $username ]]; then
        print_error "Undefined repository username"
        exit 1
    fi
    if [[ -z $password ]]; then
        print_error "Undefined repository password"
        exit 1
    fi

    print_message "Deploy to '${repository}'"
    bash "$ROOT_DIR/python" -m twine upload \
        --repository-url "${repository}" \
        --username "${username}" \
        --password "${password}" \
        "$ROOT_DIR/dist/*"
    exit_on_error
}

function run_deploy_gitlab_package
{
    local repository="${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/pypi"
    local username="gitlab-ci-token"
    local password="${CI_JOB_TOKEN}"

    print_message "Deploy to '${repository}'"
    bash "$ROOT_DIR/python" -m twine upload \
        --repository-url "${repository}" \
        --username "${username}" \
        --password "${password}" \
        "$ROOT_DIR/dist/*"
    exit_on_error
}

while [[ -n $1 ]]; do
    case $1 in
    -h|--help)
        print_usage
        exit 0
        ;;
    --)
        shift
        break
        ;;
    *)
        break
        ;;
    esac
done

if [[ -z $1 ]]; then
    print_error "Empty 'command' argument"
    exit 1
fi

COMMAND=$1
shift

case "$COMMAND" in
    create-cache|create_cache)
        run_create_cache
        ;;
    extract-cache|extract_cache)
        run_extract_cache
        ;;
    install-packages|install_packages)
        run_install_packages
        ;;
    test)
        run_test
        ;;
    build)
        run_build
        ;;
    deploy)
        # run_deploy_pypi
        # run_deploy_gitlab_package
        ;;
    *)
        print_error "Unknown command '$COMMAND'"
        exit 1
        ;;
esac
