# Load project env vars into the current shell:  source scripts/load-env.sh
# (Python code does NOT need this — ms408.env loads .env automatically.)
_env_file="$(cd "$(dirname "${BASH_SOURCE:-$0}")/.." && pwd)/.env"
if [ -f "$_env_file" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$_env_file"
  set +a
  echo "loaded $(grep -cE '^[A-Za-z_]+=' "$_env_file") variable(s) from .env"
else
  echo "no .env at $_env_file" >&2
  return 1 2>/dev/null || exit 1
fi
unset _env_file
