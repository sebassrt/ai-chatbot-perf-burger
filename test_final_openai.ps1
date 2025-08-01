# Simple OpenAI integration test
Write-Output "=== Testing OpenAI API Integration ==="

# Generate a unique email
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$email = "test$timestamp@example.com"

Write-Output "Registering user: $email"
$registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body "{`"email`": `"$email`", `"password`": `"password123`", `"first_name`": `"Test`", `"last_name`": `"User`"}"

$token = $registerResponse.access_token
Write-Output "Registration successful, testing chat..."

# Test specific questions that should use knowledge base
Write-Output "`n1. Testing Classic PerfBurger price:"
try {
    $response1 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "What is the price of the Classic PerfBurger?"}'
    Write-Output $response1.message
} catch {
    Write-Output "Error: $($_.Exception.Message)"
}

Write-Output "`n2. Testing delivery hours:"
try {
    $response2 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "What are your delivery hours?"}'
    Write-Output $response2.message
} catch {
    Write-Output "Error: $($_.Exception.Message)"
}

Write-Output "`n3. Testing vegetarian options:"
try {
    $response3 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Do you have vegetarian burgers?"}'
    Write-Output $response3.message
} catch {
    Write-Output "Error: $($_.Exception.Message)"
}

Write-Output "`n=== Test Complete ==="
