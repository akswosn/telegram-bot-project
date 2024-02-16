# Atherneswap Bot
import json
import string
from math import trunc

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sched

import logging

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log를 console에 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

################################################
#  변수 선언
################################################
# TEST
atheneswapBotKey = '5935756403:AAH2-rk9pNUQ4yWPfpufQ-eKDcuPm2Jl1o4'
domain = 'https://api.atheneswap.io'
estimateOutAPI = domain + '/v1/swap/estimate-out'
reserveAPI = domain + "/v1/support/pair/reserve"
unit = 10000000


################################################
#  API (외부 & 아테네스왑)
################################################
def call_estimate_out(tokenA: string, tokenB: string):
    data = {
        'input_amount': 1,
        'tokenA': tokenA,
        'tokenB': tokenB
    }
    # 데이터를 JSON 문자열로 변환
    json_data = json.dumps(data)

    # POST 요청을 보냄 (JSON 형식으로 body에 데이터를 넣음)
    headers = {'Content-Type': 'application/json'}

    response = requests.post(estimateOutAPI, data=json_data, headers=headers)

    return response.json()['output_value']

def call_reserve(tokenA: string, tokenB: string):
    headers = {'Content-Type': 'application/json'}
    response = requests.get(f"{reserveAPI}/{tokenA}/{tokenB}", headers=headers)
    return response.json()

def get_binance_balance():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8'
    }
    api_url = "https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-product-by-symbol?symbol=ETHUSDT"
    response = requests.get(api_url, headers=headers)
    res = json.loads(response.text)
    data = res.get("data")
    binance_eth_value = 0
    for i in data:
        if i == "c":
            binance_eth_value = float(data[i])

    return binance_eth_value

def get_lbank_ksta_usdt():
    apiUrl = 'https://api.lbkex.com/v1/ticker.do?symbol=ksta_usdt'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.get(apiUrl, headers=headers)
    return response.json()['ticker']

def get_lbank_loui_usdt():
    apiUrl = 'https://api.lbkex.com/v1/ticker.do?symbol=loui_usdt'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.get(apiUrl, headers=headers)
    return response.json()['ticker']


################################################
#  이벤트 등록 (start)
################################################
def start() -> None:
    application = Application.builder().token(atheneswapBotKey).build()
    # add event
    application.add_handler(CommandHandler("Price", help_command))
    application.add_handler(CommandHandler("ETH", binance))
    application.add_handler(CommandHandler("LBANK_Price", lbankPrice))


    application.add_handler(CommandHandler("Ratio_KSTA", ratio_ksta))
    application.add_handler(CommandHandler("Ratio_ksETH", ratio_kseth))
    application.add_handler(CommandHandler("Ratio_ksETH", ratio_kseth))
    application.add_handler(CommandHandler("Ratio_ksUSDT", ratio_ksusdt))
    application.add_handler(CommandHandler("Ratio_LOUI", ratio_loui))
    application.add_handler(CommandHandler("Ratio_inKSTA", ratio_inksta))
    application.add_handler(CommandHandler("Ratio_NST", ratio_nst))
    application.add_handler(CommandHandler("Ratio_DLT", ratio_dlt))
    application.add_handler(CommandHandler("Ratio_XABT", ratio_xabt))


    application.add_handler(CommandHandler("Price_KSTA", price_ksta))
    # application.add_handler(CommandHandler("Price_ksETH", priceksETH))
    # application.add_handler(CommandHandler("Price_ksUSDT", priceksUSDT))
    application.add_handler(CommandHandler("Price_LOUI", price_loui))
    application.add_handler(CommandHandler("Price_inKSTA", price_inksta))
    application.add_handler(CommandHandler("Price_NST", price_nst))
    application.add_handler(CommandHandler("Price_DLT", price_dlt))
    application.add_handler(CommandHandler("Price_XABT", price_xabt))


    application.add_handler(CommandHandler("Youtube", link_youtube))
    application.add_handler(CommandHandler("Discord", link_discord))
    application.add_handler(CommandHandler("Forum", link_forum))
    application.add_handler(CommandHandler("X", link_x))
    application.add_handler(CommandHandler("Medium", link_medium))
    application.add_handler(CommandHandler("Telegram", link_telegram))
    application.add_handler(CommandHandler("Website", link_website))
    application.add_handler(CommandHandler("Explorer", link_explorer))
    application.add_handler(CommandHandler("Bridge", link_bridge))
    application.add_handler(CommandHandler("Helpcenter", link_helpcenter))




    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

################################################
#  command
################################################
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    text = (
        # '/ETH : balance of eth(usdt) \n'
        '[Need You Help?] \n \n'
        '/Price : Command list\n'
        '/ETH : Binance ETH value\n'
        '/LBANK_Price : LBank KSTA Price\n'
        '======= Command Ratio \n'
        '/Ratio_KSTA : KSTA Current Ratio (LOUI, ksETH, ksUSDT, inKSTA, NST, DLT, XABT) \n'
        '/Ratio_ksETH : ksETH Current Ratio (KSTA, LOUI) \n'
        # '/Ratio_ksUSDT : ksUSDT Current Ratio (KSTA, LOUI)\n'
        '/Ratio_LOUI : LOUI Current Ratio (KSTA)\n'
        '/Ratio_inKSTA : inKSTA Current Ratio (KSTA)\n'
        '/Ratio_NST : NST Current Ratio (KSTA)\n'
        '/Ratio_DLT : DLT Current Ratio (KSTA)\n'
        '/Ratio_XABT : XABT Current Ratio (KSTA)\n'
        '======= Command price \n'
        '/Price_KSTA : KSTA Current Price \n'
        # '/Price_ksETH : ksETH Current Price \n'
        # '/Price_ksUSDT : ksUSDT Current Price\n'
        '/Price_LOUI : LOUI Current Price\n'
        '/Price_inKSTA : inKSTA Current Price\n'
        '/Price_NST : NST Current Price\n'
        '/Price_DLT : DLT Current Price\n'
        '/Price_XABT : XABT Current Price\n'
        '======= Command Link \n'
        '/Youtube : Link for Youtube\n'
        '/Discord : Link for Discord\n'
        '/Forum : Link for Forum\n'
        '/X : Link for X\n'
        '/Medium : Link for Medium\n'
        '/Telegram : Link for Telegram \n'
        '/Website : Link for Website \n'
        '/Explorer : Link for Explorer \n'
        '/Bridge : Link for Bridge \n'
        '/Helpcenter : Link for Helpcenter \n')
    await update.message.reply_text(text)

#>>>>>>>>>>>>>>> Start of link
async def link_youtube(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://www.youtube.com/@kstadium_official')
async def link_discord(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://discord.gg/qpUx25T9')
async def link_forum(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://forum.kstadium.io/')
async def link_x(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://x.com/KStadium_Offl?s=20')
async def link_medium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://medium.com/@KSTADIUM_Offl')

async def link_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://t.me/K_STADIUM_Official')
async def link_website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://kstadium.io/')
async def link_explorer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://explorer.kstadium.io/')
async def link_bridge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://bridge.kstadium.io/bridge')
async def link_helpcenter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('https://help.kstadium.io/hc/en-us')
#>>>>>>>>>>>>>>>>> end of link

#>>>>>>>>>>>>>>>>>> start of Ratio
async def ratio_ksta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    louiBalance = call_estimate_out('KSTA', 'LOUI')
    if louiBalance > 0:
        louiBalance = louiBalance / unit

    ksETHBalance = call_estimate_out('KSTA', 'ksETH')
    if ksETHBalance > 0:
        ksETHBalance = ksETHBalance / unit
        logger.info(f'ksETHBalance : {ksETHBalance}')

    ksUSDTBalance = call_estimate_out('KSTA', 'ksUSDT')
    if ksUSDTBalance > 0:
        ksUSDTBalance = ksUSDTBalance / unit

    inKSTABalance = call_estimate_out('KSTA', 'inKSTA')
    if inKSTABalance > 0:
        inKSTABalance = inKSTABalance / unit

    nstBalance = call_estimate_out('KSTA', 'NST')
    if nstBalance > 0:
        nstBalance = nstBalance / unit

    dltBalance = call_estimate_out('KSTA', 'DLT')
    if dltBalance > 0:
        dltBalance = dltBalance / unit

    xabtBalance = call_estimate_out('KSTA', "XABT")
    if xabtBalance > 0:
        xabtBalance = xabtBalance / unit

    text = (f"KSTA balance to tokens \n \n "
            f"1 KSTA = {format(louiBalance, 'f')} LOUI \n "
            f"1 KSTA = {format(ksETHBalance, 'f')} ksETH  \n "
            f"1 KSTA = {format(ksUSDTBalance, 'f')} ksUSDT \n "
            f"1 KSTA = {format(inKSTABalance, 'f')} inKSTA \n "
            f"1 KSTA = {format(nstBalance, 'f')} NST \n "
            f"1 KSTA = {format(dltBalance, 'f')} DLT \n"
            f" 1 KSTA = {format(xabtBalance, 'f')} XABT")
    await update.message.reply_text(text)

async def ratio_kseth(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kstaBalance = call_estimate_out('ksETH', 'KSTA')
    if kstaBalance > 0:
        kstaBalance = kstaBalance / unit
    louiBalance = call_estimate_out('ksETH', 'LOUI')
    if louiBalance > 0:
        louiBalance = louiBalance / unit

    text = (f"ksETH balance \n \n "
            f"1 ksETH = {kstaBalance} KSTA \n "
            f"1 ksETH = {louiBalance} LOUI")
    await update.message.reply_text(text)

async def ratio_ksusdt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kstaBalance = call_estimate_out('ksUSDT', 'KSTA')
    if kstaBalance > 0:
        kstaBalance = kstaBalance / unit
    louiBalance = call_estimate_out('ksUSDT', 'LOUI')
    if louiBalance > 0:
        louiBalance = louiBalance / unit

    text = (f"ksUSDT balance \n \n "
            f"1 ksUSDT = {kstaBalance} KSTA \n "
            f"1 ksUSDT = {louiBalance} LOUI")
    await update.message.reply_text(text)
async def ratio_loui(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kstaBalance = call_estimate_out('LOUI', 'KSTA')
    if kstaBalance > 0:
        kstaBalance = kstaBalance / unit

    text = (f"LOUI balance \n \n "
            f"1 LOUI = {kstaBalance} KSTA")
    await update.message.reply_text(text)
async def ratio_inksta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kstaBalance = call_estimate_out('inKSTA', 'KSTA')
    if kstaBalance > 0:
        kstaBalance = kstaBalance / unit
    # louiBalance = call_estimate_out('inKSTA', 'LOUI')
    # if louiBalance > 0:
    #     louiBalance = louiBalance / unit

    text = (f"inKSTA balance \n \n "
            f"1 inKSTA = {kstaBalance} KSTA \n ")
    await update.message.reply_text(text)
async def ratio_nst(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kstaBalance = call_estimate_out('NST', 'KSTA')
    if kstaBalance > 0:
        kstaBalance = kstaBalance / unit

    text = f"NST balance \n \n 1 NST = {kstaBalance} KSTA "
    await update.message.reply_text(text)
async def ratio_dlt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kstaBalance = call_estimate_out('DLT', 'KSTA')
    if kstaBalance > 0:
        kstaBalance = kstaBalance / unit

    text = f"DLT balance \n \n 1 DLT = {kstaBalance} KSTA "
    await update.message.reply_text(text)

async def ratio_xabt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kstaBalance = call_estimate_out('XABT', 'KSTA')
    if kstaBalance > 0:
        kstaBalance = kstaBalance / unit

    text = f"XABT balance \n \n 1 XABT = {kstaBalance} KSTA "
    await update.message.reply_text(text)
# >>>>>>>>>>>>>>>> end of Ratio
async def binance(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    binanceBalance = get_binance_balance()

    text = f"binance ETH balance \n \n {binanceBalance}  "
    await update.message.reply_text(text)
async def lbankPrice(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    kstaLbank = get_lbank_ksta_usdt()
    louiLbank = get_lbank_loui_usdt()
    text = (f"LBank KSTA-USDT Price \n"
           f"$ {kstaLbank['latest']}\n"
            f"High : {kstaLbank['high']}\n"
            f"Low : {kstaLbank['low']}\n"
            f"24h Vol : {format(float(kstaLbank['turnover'])/1000, 'f')} \n\n"
            f"---------------------\n\n"
            f"LBank LOUI-USDT Price \n"
            f"$ {louiLbank['latest']} \n"
            f"High : {louiLbank['high']}\n"
            f"Low : {louiLbank['low']}\n"
            f"24h Vol : {format(float(louiLbank['turnover']) / 1000, 'f')}"
            )
    await update.message.reply_text(text)


###########################################################################################
# >>>>>>>>>>>>>>>>> price
###########################################################################################
async def price_ksta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kstaKsETH = calc_ksta_kseth()
    # kstaKsUSDT = calc_ksta_ksusdt()
    lbankKsta = get_lbank_ksta_usdt()

    # text = (f"[KSTA-ksETH Pool] \n"
    #         f"1 KSTA : ${format(kstaKsETH, 'f')} \n\n"
    #         # f"[KSTA-ksUSDT Pool] \n"
    #         # f"1 KSTA : ${format(kstaKsUSDT, 'f')} \n"
    #         )

    text = (
        f"Atheneswap_KSTA : ${kstaKsETH} \n\n"
        f"L Bank_KSTA : ${lbankKsta['latest']}"
    )
    await update.message.reply_text(text)

# async def priceksETH(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text('price ksETH')
# async def priceksUSDT(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text('price ksUSDT')
async def price_loui(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    priceLouiKsta = calc_loui_ksta()
    # priceLouiKseth = calc_loui_kseth()
    lbankLoui = get_lbank_loui_usdt()
    # priceLouiKsusdt = calc_loui_ksusdt()

    text = (
        f"Atheneswap_LOUI : ${priceLouiKsta} \n\n"
        f"L Bank_LOUI : ${lbankLoui['latest']}"
    )

    # text = (f"[LOUI-KSTA Pool] \n"
    #         f"1 LOUI : ${format(priceLouiKsta, 'f')} \n\n"
    #         f"[LOUI-ksETH Pool]\n"
    #         f"1 LOUI : ${format(priceLouiKseth, 'f')} \n\n"
    #         # f"[LOUI-ksUSDT Pool]\n"
    #         # f"1 LOUI : ${format(priceLouiKsusdt, 'f')} \n\n"
    #         )
    await update.message.reply_text(text)
async def price_inksta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    priceInkstaKsta = calc_inksta_ksta()

    text = (f"[inKSTA-KSTA Pool] \n"
            f"1 inKSTA : ${format(priceInkstaKsta, 'f')} \n\n")
    await update.message.reply_text(text)
async def price_nst(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    priceNstKsta = calc_nst_ksta()
    text = (f"[NST-KSTA Pool] \n"
            f"1 NST : ${format(priceNstKsta, 'f')} \n\n")
    await update.message.reply_text(text)
async def price_dlt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    priceDltKsta = calc_dlt_ksta()
    text = (f"[DLT-KSTA Pool] \n"
            f"1 DLT : ${format(priceDltKsta, 'f')} \n\n")
    await update.message.reply_text(text)

async def price_xabt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    priceXABTKsta = calc_xabt_ksta()
    text = (f"[XABT-KSTA Pool] \n"
            f"1 XABT : ${format(priceXABTKsta, 'f')} \n\n")
    await update.message.reply_text(text)

###########################################################################################
# >>>>>>>>> Calc
###########################################################################################
# calcKsETH : ksETH * binanceETH / KSTA
def calc_ksta_kseth():
    binanceBalance = get_binance_balance()
    reserveETH = call_reserve('KSTA', 'ksETH')
    kstaRevers = reserveETH['reserveA']
    ksEthRevers = reserveETH['reserveB']
    logger.info(f"KSTA : {format(float(kstaRevers) / 1000000000000000000, 'f')}")
    logger.info(f"ksETH : {format(float(ksEthRevers) / 1000000000000000000, 'f')}")

    kstaKsETH = 0
    if kstaRevers and ksEthRevers:
        kstaKsETH = float(ksEthRevers) * binanceBalance / float(kstaRevers)
    return kstaKsETH

# ksUSDTr / KSTAr
def calc_ksta_ksusdt():
    reserveksUSDT = call_reserve('KSTA', 'ksUSDT')
    kstaReserve = reserveksUSDT['reserveA']
    ksUsdtReserve = reserveksUSDT['reserveB']
    logger.info(f"KSTA : {format(float(kstaReserve) / 1000000000000000000, 'f')}")
    logger.info(f"ksUSDT : {format(float(ksUsdtReserve) / 1000000000000000000, 'f')}")

    kstaKsUSDT = 0
    if kstaReserve and ksUsdtReserve:
        kstaKsUSDT = float(ksUsdtReserve) / float(kstaReserve)
    return kstaKsUSDT

# KSTAr * ksETH(price) / LOUIr
def calc_loui_ksta():
    kstaKsETH = calc_ksta_kseth()

    reserveLOUI = call_reserve('LOUI', 'KSTA')
    louiReserve = reserveLOUI['reserveA']
    kstaReserve = reserveLOUI['reserveB']
    logger.info(f"KSTA : {format(float(louiReserve) / 1000000000000000000, 'f')}")
    logger.info(f"ksETH : {format(float(kstaReserve) / 1000000000000000000, 'f')}")

    kstaLoui = 0
    if louiReserve and kstaReserve:
        kstaLoui = float(kstaReserve) * kstaKsETH / float(louiReserve)
    return kstaLoui

# KSTAr * binance / LOUIr
def calc_loui_kseth():
    binanceBalance = get_binance_balance()
    reserveLOUI = call_reserve('LOUI', 'ksETH')
    louiReserve = reserveLOUI['reserveA']
    ksethReserve = reserveLOUI['reserveB']

    result = 0
    if louiReserve and ksethReserve:
        result = float(ksethReserve) * binanceBalance / float(louiReserve)
    return result

#ksUSDTr / LOUI
def calc_loui_ksusdt():
    reserveLOUI = call_reserve('LOUI', 'ksUSDT')
    louiReserve = reserveLOUI['reserveA']
    ksusdtReserve = reserveLOUI['reserveB']

    result = 0
    if louiReserve and ksusdtReserve:
        result = float(ksusdtReserve) / float(louiReserve)
    return result

# KSTAr * ksETH(price) / inKSTAr
def calc_inksta_ksta():
    kstaKsETH = calc_ksta_kseth()
    reserveInksta = call_reserve('inKSTA', 'KSTA')
    inkstaReserve = reserveInksta['reserveA']
    kstaReserve = reserveInksta['reserveB']
    result = 0
    if inkstaReserve and kstaReserve:
        result = float(kstaReserve) * kstaKsETH / float(inkstaReserve)
    return result

def calc_nst_ksta():
    kstaKsETH = calc_ksta_kseth()
    reserveNst = call_reserve('NST', 'KSTA')
    nstReserve = reserveNst['reserveA']
    kstaReserve = reserveNst['reserveB']
    result = 0
    if nstReserve and kstaReserve:
        result = float(kstaReserve) * kstaKsETH / float(nstReserve)
    return result

def calc_dlt_ksta():
    kstaKsETH = calc_ksta_kseth()
    reserveDLT = call_reserve('DLT', 'KSTA')
    dltReserve = reserveDLT['reserveA']
    kstaReserve = reserveDLT['reserveB']
    result = 0
    if dltReserve and kstaReserve:
        result = float(kstaReserve) * kstaKsETH / float(dltReserve)
    return result

def calc_xabt_ksta():
    kstaKsETH = calc_ksta_kseth()
    reserveDLT = call_reserve('XABT', 'KSTA')
    xabtReserve = reserveDLT['reserveA']
    kstaReserve = reserveDLT['reserveB']
    logger.info(f"xabtReserve : {xabtReserve}")
    logger.info(f"kstaReserve : {kstaReserve}")
    logger.info(f"kstaKsETH : {kstaKsETH}")

    result = 0
    if xabtReserve and kstaReserve:
        result = float(kstaReserve) * kstaKsETH / float(xabtReserve)
    return result
