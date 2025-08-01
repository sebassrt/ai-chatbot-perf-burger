# Test chat memory and conversation context
Write-Output "=== Testing Chat Memory & Conversation Context ==="

# Generate a unique email
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$email = "memory_test$timestamp@example.com"

Write-Output "Registering user: $email"
$registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body "{`"email`": `"$email`", `"password`": `"password123`", `"first_name`": `"Memory`", `"last_name`": `"Test`"}"

$token = $registerResponse.access_token
Write-Output "Registration successful, testing conversation memory..."

# Message 1: Ask about a specific burger
Write-Output "`n1. First message - Ask about Classic PerfBurger:"
$response1 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Tell me about the Classic PerfBurger - price and ingredients please"}'
Write-Output "Response: $($response1.message)"
$sessionId = $response1.session_id
Write-Output "Session ID: $sessionId"

# Message 2: Ask a follow-up question that references the previous burger
Write-Output "`n2. Second message - Follow-up question:"
$response2 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Is that burger you just mentioned customizable? Can I add bacon to it?"}'
Write-Output "Response: $($response2.message)"

# Message 3: Ask about something different
Write-Output "`n3. Third message - Ask about delivery:"
$response3 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "What are your delivery hours?"}'
Write-Output "Response: $($response3.message)"

# Message 4: Reference both previous topics
Write-Output "`n4. Fourth message - Reference previous topics:"
$response4 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Great! So if I order that burger with bacon during those delivery hours, how much would it cost total?"}'
Write-Output "Response: $($response4.message)"

# Check conversation history
Write-Output "`n5. Checking conversation history via API:"
try {
    $history = Invoke-RestMethod -Uri "http://localhost:5000/chat/sessions/$sessionId/messages" -Method GET -Headers @{"Authorization"="Bearer $token"}
    Write-Output "Total messages in session: $($history.messages.Count)"
    Write-Output "Messages:"
    foreach ($msg in $history.messages) {
        Write-Output "  [$($msg.message_type)]: $($msg.content.Substring(0, [Math]::Min(100, $msg.content.Length)))..."
    }
} catch {
    Write-Output "Could not retrieve conversation history: $($_.Exception.Message)"
}

Write-Output "`n=== Memory Test Complete ==="
