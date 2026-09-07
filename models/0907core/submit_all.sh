#!/bin/bash

# Submit all fresh TwoC3 jobs requested for the September 7 Kuma run.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
EXPECTED_SCRIPT_DIR="/scratch/pghosh/Working_AD_Honeycomb_September07"
J2_VALUES=(0.23 0.235)
failures=0
submitted=0

if [[ "${SCRIPT_DIR}" != "${EXPECTED_SCRIPT_DIR}" ]]; then
    echo "Run this script from its scratch copy: ${EXPECTED_SCRIPT_DIR}/submit_all.sh" >&2
    exit 1
fi

for REQUIRED_FILE in main_C3.py core_C3.py singleFileSbatchTwoC3.run; do
    if [[ ! -f "${SCRIPT_DIR}/${REQUIRED_FILE}" ]]; then
        echo "Missing required file: ${SCRIPT_DIR}/${REQUIRED_FILE}" >&2
        exit 1
    fi
done

submit_job() {
    local D="$1"
    local J2="$2"
    local REPLICA="$3"
    local J2_SHORT="${J2#0.}"

    if sbatch \
        --chdir="${SCRIPT_DIR}" \
        --job-name="${J2_SHORT}twoD${D}r${REPLICA}" \
        --export="ALL,D=${D},J2=${J2},REPLICA=${REPLICA}" \
        "${SCRIPT_DIR}/singleFileSbatchTwoC3.run"; then
        submitted=$((submitted + 1))
    else
        failures=$((failures + 1))
    fi
}

# Use the default chi schedule from main_C3.py.  Submit two independent
# replicas for every (J2, D) pair so their output files cannot collide.
for J2 in "${J2_VALUES[@]}"; do
    for D in {2..11}; do
        for REPLICA in 1 2; do
            submit_job "${D}" "${J2}" "${REPLICA}"
        done
    done
done

if (( failures > 0 )); then
    echo "Submitted ${submitted} jobs; ${failures} sbatch submission(s) failed." >&2
    exit 1
fi

echo "Submitted all ${submitted} fresh TwoC3 jobs."
