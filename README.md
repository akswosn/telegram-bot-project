# python 3 bot program
## 설치 모듈
brew install python (for mac)
pip3 install python-telegram-bot


## 환경 (pip3 23.3.1)
Package (Version)
------------------- --------
anyio               (4.0.0)  
certifi             (2023.5.7)  
charset-normalizer  (3.1.0)  
exceptiongroup      (1.1.3)  
h11                 (0.14.0)  
httpcore            (0.18.0)  
httpx               (0.25.0)  
idna                (3.4)  
pip                 (23.3.1)  
python-telegram-bot (20.6)  
requests            (2.30.0)  
setuptools          (65.5.0)  
sniffio             (1.3.0)  
telegram            (0.0.1)  
urllib3             (2.0.2)  


## 기능
- [main.py](main.py) 모듈 실행
- [AtheneSwapBot.py](bot%2FAtheneSwapBot.py) atheneswap 기능 모듈
  - ETH : 바이넨스 이더 가격
  - LBANK_Price : KSTA/USDT 가격 (LBANK)
  - swap 비율
    - Ratio_KSTA : KSTA Pair 모든 비율 조회
    - Ratio_ksETH : ksETH Pair 모든 비율 조회
    - Ratio_ksUSDT : ksUSDT Pair 모든 비율 조회
    - Ratio_LOUI : LOUI Pair 모든 비율 조회
    - Ratio_inKSTA : inKSTA Pair 모든 비율 조회
    - Ratio_NST : NST Pair 모든 비율 조회
    - Ratio_DLT : DLT Pair 모든 비율 조회
  - Price 가격
    - Price_KSTA : 
      - calc_ksta_kseth : ksETH(ratio) * binanceETH / KSTA(ratio), 
      - calc_ksta_ksusdt : ksUSDT(ratio) / KSTA(ratio)
    - Price_LOUI : 
      - calc_loui_ksta : KSTA(ratio) * ksETH(price) / LOUI(ratio)
      - calc_loui_kseth :  KSTA(ratio) * binance / LOUI(ratio)
      - calc_loui_ksusdt : ksUSDT(ratio) / LOUI
    - Price_inKSTA :
      - calc_inksta_ksta : KSTA(ratio) * ksETH(price) / inKSTA(ratio)
    - Price_NST :
      - calc_nst_ksta : KSTA(ratio) * ksETH(price) / NST(ratio)
    - Price_DLT
      - calc_dlt_ksta : KSTA(ratio) * ksETH(price) / DLT(ratio)
  - 기타 링크
    - Youtube
    - Discord
    - Forum
    - X
    - Medium
    - Telegram
    - Website
    - Explorer
    - Bridge
    - Helpcenter


실행 스크립트
python3 telegram-bot.py &
