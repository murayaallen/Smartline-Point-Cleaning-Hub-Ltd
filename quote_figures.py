# -*- coding: utf-8 -*-
"""Smartline website engagement - the money, in one place.
Quotation AMM-Q-2026-187 (16/11/2026) and the final invoice AMM-I-2026-187 both read these.
verify() runs on import, so a wrong figure stops both documents from building."""

BUILD      = 35000          # website: full build + Google setup + profile
DOMAIN     = 2000           # .co.ke, 1 year
HOSTING    = 3000           # server space + business email, 1 year
DEPOSIT_PC = 0.40

BUILD_DEPOSIT = int(round(BUILD * DEPOSIT_PC))        # 14,000
TOTAL         = BUILD + DOMAIN + HOSTING              # 40,000
DUE_NOW       = BUILD_DEPOSIT + DOMAIN + HOSTING      # 19,000  deposit to start
DUE_LIVE      = BUILD - BUILD_DEPOSIT                 # 21,000  balance on go-live
RENEWAL       = 3000                                  # flat 3,000 / yr from yr 2 (domain + hosting)

QUOTE_NO   = "AMM-Q-2026-187"
QUOTE_DATE = "16/11/2026"
INVOICE_NO = "AMM-I-2026-187"


def verify():
    assert BUILD_DEPOSIT == 14000, BUILD_DEPOSIT
    assert TOTAL == 40000, TOTAL
    assert DUE_NOW == 19000, DUE_NOW
    assert DUE_LIVE == 21000, DUE_LIVE
    assert DUE_NOW + DUE_LIVE == TOTAL
    assert BUILD_DEPOSIT + DUE_LIVE == BUILD
    assert TOTAL - DUE_NOW == DUE_LIVE          # what the final invoice asks for
    assert RENEWAL == 3000
    return True


verify()


def ksh(n):
    return "{:,}".format(n)
