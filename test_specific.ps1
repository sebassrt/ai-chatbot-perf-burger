# Test chat endpoint with very specific questions
$registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email": "testuser6@example.com", "password": "password123", "first_name": "Test", "last_name": "User6"}'

$token = $registerResponse.access_token
Write-Output "Testing very specific questions..."

# Test very specific menu question
$chatResponse1 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "What is the price of the Classic PerfBurger?"}'

Write-Output "`nClassic PerfBurger Price Question:"
Write-Output $chatResponse1.message

# Test delivery hours question
$chatResponse2 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "What are your delivery hours?"}'

Write-Output "`nDelivery Hours Question:"
Write-Output $chatResponse2.message

# Test vegetarian options with specific name
$chatResponse3 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Tell me about the Veggie Supreme burger"}'

Write-Output "`nVeggie Supreme Question:"
Write-Output $chatResponse3.message
