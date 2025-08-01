# Diagnostic test for OpenAI API integration
Write-Output "=== OpenAI API Diagnostic Test ==="

# Check if the health endpoint works
Write-Output "1. Testing health endpoint:"
try {
    $health = Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET
    Write-Output "✅ Health endpoint working: $($health.status)"
} catch {
    Write-Output "❌ Health endpoint failed: $($_.Exception.Message)"
}

# Register user and get token
Write-Output "`n2. Registering user:"
$registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email": "diagnostic@example.com", "password": "password123", "first_name": "Diagnostic", "last_name": "Test"}'
$token = $registerResponse.access_token
Write-Output "✅ User registered successfully"

# Test simple chat message
Write-Output "`n3. Testing simple chat message:"
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Hello"}'
    Write-Output "✅ Chat response received:"
    Write-Output "   Message: $($response.message)"
    Write-Output "   Session ID: $($response.session_id)"
    Write-Output "   Timestamp: $($response.timestamp)"
} catch {
    Write-Output "❌ Chat failed: $($_.Exception.Message)"
}

# Test very specific menu question to see if knowledge base is working
Write-Output "`n4. Testing knowledge base retrieval:"
try {
    $response2 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Classic PerfBurger price ingredients"}'
    Write-Output "✅ Knowledge base test response:"
    Write-Output "   $($response2.message)"
    
    # Check if response contains specific information
    if ($response2.message -match "12\.99|grass-fed|brioche") {
        Write-Output "✅ Knowledge base appears to be working - specific details found"
    } else {
        Write-Output "⚠️  Knowledge base may not be working - generic response detected"
    }
} catch {
    Write-Output "❌ Knowledge base test failed: $($_.Exception.Message)"
}

Write-Output "`n=== Diagnostic Complete ==="
