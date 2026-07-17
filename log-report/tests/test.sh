#!/bin/bash

mkdir -p /logs/verifier

pytest /tests/test_outputs.py

STATUS=$?

# Always create a CTRF file so Harbor finds it.
cat > /logs/verifier/ctrf.json <<EOF
{
  "results": {
    "summary": {
      "passed": $([ "$STATUS" -eq 0 ] && echo 3 || echo 0),
      "failed": $([ "$STATUS" -eq 0 ] && echo 0 || echo 1)
    }
  }
}
EOF

if [ "$STATUS" -eq 0 ]; then
    echo "1" > /logs/verifier/reward.txt
else
    echo "0" > /logs/verifier/reward.txt
fi

exit $STATUS