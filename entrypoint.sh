#!/usr/bin/env sh

set -o errexit
set -o nounset

cmd="$*"

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
