@echo off
:LoopStart
For /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
SET var=0430 PM
IF "%var%"=="%mytime%" (
    ECHO Scraping Started
	C:\Anaconda3\Python.exe G:\MyWorks\JA\TripAdvisor.py https://www.tripadvisor.com.sg https://www.tripadvisor.com.sg/Hotel_Review-g293974-d1604061-Reviews-White_House_Hotel_Istanbul-Istanbul.html#REVIEWS 10
	ECHO Scraping completed
)
GOTO LoopStart
pause
CLS
EXIT