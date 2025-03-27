
TOLERANCE=1E-10
TMP_DIR=/tmp/test_laplacian
TMP_LOG=$TMP_DIR/test.log

mkdir -p $TMP_DIR

check_error() {

    values=($(cat $TMP_LOG | grep "||" | head -n 2 | cut -d "=" -f2 | sed 's/[\d0-\d127]*m//'))

    for value in "${values[@]}"; do
        value=$(echo "$value" | sed 's/e/E/g')
        if (( $(echo "$value > $TOLERANCE" | bc -l) )); then
            echo "Error: $value > $TOLERANCE"
            exit 1
        fi
    done
}

# Test 1
feelpp_qs_laplacian_3d --config-file tests/exact.cfg > $TMP_LOG
check_error

# Test 2
feelpp_qs_laplacian_3d --config-file tests/exact.cfg --case.discretization P2 --checker.solution x^2+y*z:x:y:z > $TMP_LOG
check_error
