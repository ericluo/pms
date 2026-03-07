@echo off
REM PMS 测试运行脚本 (Windows)

echo ==========================================
echo PMS 系统测试套件
echo ==========================================
echo.

REM 颜色定义（需要 Windows 10+）
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do     rem"') do (
  set "DEL=%%a"
  set "COLOR_GREEN=%%b[32m"
  set "COLOR_RED=%%b[31m"
  set "COLOR_YELLOW=%%b[33m"
  set "COLOR_RESET=%%b[0m"
)

REM 测试计数
set TOTAL_TESTS=0
set PASSED_TESTS=0
set FAILED_TESTS=0

REM 检查参数
if "%1"=="backend" goto backend_tests
if "%1"=="frontend" goto frontend_tests
if "%1"=="e2e" goto e2e_tests
if "%1"=="" goto all_tests
echo 用法：%0 {backend^|frontend^|e2e^|all}
exit /b 1

:backend_tests
echo %COLOR_YELLOW%[1/3] 运行后端单元测试...%COLOR_RESET%
echo.

REM 检查 pytest 是否安装
where pytest >nul 2>nul
if %errorlevel% neq 0 (
    echo %COLOR_RED%错误：pytest 未安装，请先安装依赖%COLOR_RESET%
    echo 运行：pip install -r requirements.txt
    goto backend_failed
)

REM 运行后端测试
pytest tests\test_backend.py -v --tb=short
if %errorlevel% equ 0 (
    echo %COLOR_GREEN%✓ 后端测试通过%COLOR_RESET%
    set /a PASSED_TESTS+=1
    goto backend_passed
)

:backend_failed
echo %COLOR_RED%✗ 后端测试失败%COLOR_RESET%

:backend_passed
set /a TOTAL_TESTS+=1
echo.
if "%1"=="" goto frontend_tests
goto show_summary

:frontend_tests
echo %COLOR_YELLOW%[2/3] 运行前端组件测试...%COLOR_RESET%
echo.

REM 检查 npm 是否安装
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo %COLOR_RED%错误：npm 未安装%COLOR_RESET%
    goto frontend_failed
)

REM 运行前端测试
call npm run test:unit
if %errorlevel% equ 0 (
    echo %COLOR_GREEN%✓ 前端测试通过%COLOR_RESET%
    set /a PASSED_TESTS+=1
    goto frontend_passed
)

:frontend_failed
echo %COLOR_RED%✗ 前端测试失败%COLOR_RESET%

:frontend_passed
set /a TOTAL_TESTS+=1
echo.
if "%1"=="" goto e2e_tests
goto show_summary

:e2e_tests
echo %COLOR_YELLOW%[3/3] 运行 E2E 测试...%COLOR_RESET%
echo.

REM 运行 E2E 测试
call npm run test:e2e
if %errorlevel% equ 0 (
    echo %COLOR_GREEN%✓ E2E 测试通过%COLOR_RESET%
    set /a PASSED_TESTS+=1
    goto e2e_passed
)

:e2e_failed
echo %COLOR_RED%✗ E2E 测试失败%COLOR_RESET%

:e2e_passed
set /a TOTAL_TESTS+=1
echo.

:show_summary
echo ==========================================
echo 测试总结
echo ==========================================
echo 总测试数：%TOTAL_TESTS%
echo %COLOR_GREEN%通过：%PASSED_TESTS%%COLOR_RESET%
echo %COLOR_RED%失败：%FAILED_TESTS%%COLOR_RESET%
echo.

if %FAILED_TESTS% equ 0 (
    echo %COLOR_GREEN%所有测试通过！%COLOR_RESET%
    exit /b 0
) else (
    echo %COLOR_RED%部分测试失败，请检查错误信息%COLOR_RESET%
    exit /b 1
)

:all_tests
call :backend_tests
call :frontend_tests
call :e2e_tests
goto show_summary
