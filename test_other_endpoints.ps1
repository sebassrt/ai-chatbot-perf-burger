# Test other endpoints to see if they work
$registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email": "testuser7@example.com", "password": "password123", "first_name": "Test", "last_name": "User7"}'

$token = $registerResponse.access_token
Write-Output "Testing other endpoints..."

# Test orders endpoint
try {
    $ordersResponse = Invoke-RestMethod -Uri "http://localhost:5000/orders" -Method GET -Headers @{"Authorization"="Bearer $token"}
    Write-Output "`nOrders Response:"
    $ordersResponse | ConvertTo-Json -Depth 2
} catch {
    Write-Output "`nOrders Error: $($_.Exception.Message)"
}

# Test user profile
try {
    $profileResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/profile" -Method GET -Headers @{"Authorization"="Bearer $token"}
    Write-Output "`nProfile Response:"
    $profileResponse | ConvertTo-Json -Depth 2
} catch {
    Write-Output "`nProfile Error: $($_.Exception.Message)"
}
