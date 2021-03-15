#/bin/sh

mongoexport --db=finance --collection=mystocks \
            --fields=platform,exchange_rate,code,name,risk,market_value,hold_gain,mv_rmb,hg_rmb \
            --type=csv --out=mystocks.csv
