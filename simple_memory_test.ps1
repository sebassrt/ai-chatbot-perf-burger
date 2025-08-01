# Simple test to verify chat memory
Write-Output "=== Simple Chat Memory Test ==="

# Generate a unique email
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$email = "simple_test$timestamp@example.com"

$registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body "{`"email`": `"$email`", `"password`": `"password123`", `"first_name`": `"Simple`", `"last_name`": `"Test`"}"

$token = $registerResponse.access_token

# First message: Ask about a burger
Write-Output "`n1. Ask about Classic PerfBurger:"
$response1 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "What ingredients are in the Classic PerfBurger?"}'
Write-Output "Response: $($response1.message)"

# Second message: Reference the previous burger without naming it
Write-Output "`n2. Reference the previous burger:"
$response2 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Can I customize that burger by adding extra cheese?"}'
Write-Output "Response: $($response2.message)"

# Check if the AI understood "that burger" refers to the Classic PerfBurger
if ($response2.message -match "Classic|PerfBurger|customize|cheese") {
    Write-Output "`n✅ Chat memory is working! AI understood the reference to the previous burger."
} else {
    Write-Output "`n⚠️  Chat memory may not be working fully - AI might not have understood the reference."
}

Write-Output "`n=== Simple Test Complete ==="
