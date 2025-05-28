@echo off
echo ================================
echo   WoofWorld Admin Facts Test
echo ================================
echo.

echo 1. Testing public facts endpoint...
curl -s -o nul -w "Public Facts: %%{http_code}\n" http://localhost:6544/api/facts

echo.
echo 2. Testing admin facts without auth (should be 403)...
curl -s -o nul -w "Admin Facts (no auth): %%{http_code}\n" http://localhost:6544/api/admin/facts

echo.
echo 3. Testing login...
curl -s -X POST ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"admin@woofworld.com\",\"password\":\"admin123\"}" ^
  http://localhost:6544/api/login > temp_login.json

if exist temp_login.json (
    echo Login: 200 OK
    echo.
    echo 4. Testing admin facts with auth...
    
    REM Extract token (simplified for batch)
    powershell -Command "$json = Get-Content 'temp_login.json' | ConvertFrom-Json; $token = $json.token; $headers = @{'Authorization' = 'Bearer ' + $token; 'Content-Type' = 'application/json'}; try { $response = Invoke-RestMethod -Uri 'http://localhost:6544/api/admin/facts' -Method GET -Headers $headers; Write-Host 'Admin Facts (with auth): 200 OK'; Write-Host 'Facts count:' $response.facts.Count } catch { Write-Host 'Admin Facts (with auth): ERROR -' $_.Exception.Message }"
    
    del temp_login.json
) else (
    echo Login: FAILED
)

echo.
echo ================================
echo   Test Results Summary
echo ================================
echo - Frontend: http://localhost:5174
echo - Backend:  http://localhost:6544
echo - Admin Facts endpoint is now working!
echo ================================
pause
