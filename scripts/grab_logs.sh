#!/bin/bash

set -e


export PATH=$PATH:/snap/bin



units=$(juju status elasticsearch --format json | jq -r '.applications | map_values(.units) | .[] | keys | .[]')

for unit in $units; do
    juju scp $unit:/var/log/juju/unit-*.log .
done
