# Test chat endpoint
$registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email": "testuser4@example.com", "password": "password123", "first_name": "Test", "last_name": "User4"}'

$token = $registerResponse.access_token
Write-Output "Token received: $($token.Substring(0, 50))..."

$chatResponse = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Hello, I would like to know about your burgers"}'

Write-Output "Chat Response:"
$chatResponse | ConvertTo-Json -Depth 3
