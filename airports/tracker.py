#!/usr/bin/env python3
"""Compatibility entry point for the free Airports.ru cancellation collector."""
import sys
from collect_cancellations import main

if __name__ == '__main__':
    # Existing manual collect commands now use completed-day source totals.
    if len(sys.argv) > 1 and sys.argv[1] == 'collect':
        del sys.argv[1]
    if '--hours' in sys.argv:
        i = sys.argv.index('--hours')
        del sys.argv[i:i + 2]
        print('Airports.ru refreshes the last seven completed days; --hours is ignored.', file=sys.stderr)
    main()
