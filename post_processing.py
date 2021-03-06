import json
import sys

# The DOT Allocation Indicator only has 3 decimals representation, but we want 12. So we add 9 more.
# We do this in Python because the JS JSON serializer will not allow us to write numbers larger than 2^53.
DECIMALS = 1 * 10**9

print("Performing post-processing on", sys.argv[1])

with open(sys.argv[1], encoding='utf-8') as f:
    chain_spec = json.loads(f.read())
    bal_array = chain_spec['genesis']['runtime']['balances']['balances']
    for i in range(len(bal_array)):
        bal_item = chain_spec['genesis']['runtime']['balances']['balances'][i]
        bal_w_decimals = bal_item[1] * DECIMALS
        chain_spec['genesis']['runtime']['balances']['balances'][i] =[bal_item[0], bal_w_decimals]

    claimers_array = chain_spec['genesis']['runtime']['claims']['claims']
    for i in range(len(claimers_array)):
        claims_item = chain_spec['genesis']['runtime']['claims']['claims'][i]
        claims_w_decimals = claims_item[1] * DECIMALS
        chain_spec['genesis']['runtime']['claims']['claims'][i] = [claims_item[0], claims_w_decimals, claims_item[2], claims_item[3]]

    vested_claimers = chain_spec['genesis']['runtime']['claims']['vesting']
    for i in range(len(vested_claimers)):
        item = vested_claimers[i]
        w_decimals = item[1][0] * DECIMALS
        chain_spec['genesis']['runtime']['claims']['vesting'][i] = [item[0], [w_decimals, item[1][1], item[1][2]]]

    vesting_array = chain_spec['genesis']['runtime']['vesting']['vesting']
    for i in range(len(vesting_array)):
        vesting_item = chain_spec['genesis']['runtime']['vesting']['vesting'][i]
        vesting_w_decimals = vesting_item[3] * DECIMALS
        chain_spec['genesis']['runtime']['vesting']['vesting'][i] = [ vesting_item[0], vesting_item[1], vesting_item[2], vesting_w_decimals]

    with open ('polkadot.json', 'w', encoding='utf-8') as f2:
        json.dump(chain_spec, f2, ensure_ascii=False, indent=2)
