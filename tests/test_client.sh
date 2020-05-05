#!/bin/bash

echo
echo "************** START: test_client.sh **********************"

# Create temporary testing directory
echo "Creating temporary directory to work in."
here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

. $here/helpers.sh

# Make sure it's installed
if which gridtest >/dev/null; then
    printf "gridtest is installed\n"
else
    printf "gridtest is not installed\n"
    exit 1
fi

# Create temporary testing directory
tmpdir=$(mktemp -d)
output=$(mktemp ${tmpdir:-/tmp}/gridtest_test.XXXXXX)
printf "Creatied temporary directory to work in. ${output}\n"

echo "#### Testing basic tests"
runTest 0 $output gridtest test $here/modules/basic-tests.yml
runTest 0 $output gridtest test $here/modules/basic-tests.yml --serial
runTest 0 $output gridtest check $here/modules/basic-tests.yml

echo
echo "#### Testing temp file and directory tests"
runTest 0 $output gridtest test $here/modules/temp-tests.yml
runTest 0 $output gridtest test $here/modules/temp-tests.yml --serial

echo
echo "#### Testing report generation"
runTest 0 $output gridtest test $here/modules/metrics.yml --save $tmpdir/results.json
cat $tmpdir/results.json
runTest 0 $output gridtest test $here/modules/metrics.yml --save-web $tmpdir/web
ls $tmpdir/web
rm -rf ${tmpdir}
