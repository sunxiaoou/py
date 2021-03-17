#!/bin/sh

mongoexport --db=finance --collection=myfunds \
            --query='{"date": {"$gte": {"$date": "2021-03-11T00:00:00.000Z"}}}' \
            --fields=platform,code,name,risk,market_value,hold_gain \
            --type=csv --out=myfunds.csv
exit

mongoexport --db=finance --collection=mystocks \
            --fields=platform,exchange_rate,code,name,risk,market_value,hold_gain,mv_rmb,hg_rmb \
            --type=csv --out=mystocks.csv
