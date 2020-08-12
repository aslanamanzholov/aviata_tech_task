#!/bin/bash
wait_for () {
    for _ in `seq 0 100`; do
        (echo > /dev/tcp/$1/$2) >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            echo "$1:$2 accepts connections"
            break
        fi
        sleep 1
    done
}
populate_env_variables () {
  set -o allexport
  [[ -f core/.env ]] && source core/.env
  set +o allexport
  echo "env variables are populated"
}
populate_env_variables
wait_for "${DB_HOST}" "${DB_PORT}"
#wait_for "${BROKER_HOST}" "${BROKER_PORT}"
case "$MODE" in
"TEST")
    python manage.py migrate && \
    pytest -v --cov . --cov-report term-missing --cov-fail-under=100 \
    --flake8 --color=yes -n 4 --no-migrations --reuse-db -W error
    ;;
"PROD")
    python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    gunicorn -c gunicorn.conf.py core.wsgi
    ;;
"DEV")
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000
    ;;
"CELERY")
    celery -A core worker --beat --loglevel=INFO
    ;;
*)
    echo "NO MODE SPECIFIED!"
    exit 1
    ;;
esac
