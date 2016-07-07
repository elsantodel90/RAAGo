#! /bin/bash
set -u

cd $(dirname $0)/..

find aago_ranking -not -path "*/migrations/*" -name "*.py" -exec echo "Checking" {} \; -exec yapf --style .style.yapf -d {} \;
