# Test OpenAI API integration with specific knowledge base questions
Write-Output "=== Testing OpenAI API Integration ==="
Write-Output "Registering new user and testing chat with knowledge base..."

$registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email": "openaitest@example.com", "password": "password123", "first_name": "OpenAI", "last_name": "Test"}'

$token = $registerResponse.access_token
Write-Output "User registered successfully"

# Test 1: Specific menu item with price
Write-Output "`n1. Testing specific menu question (Classic PerfBurger price):"
$response1 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "What is the price of the Classic PerfBurger and what ingredients does it have?"}'
Write-Output $response1.message

# Test 2: Vegetarian options
Write-Output "`n2. Testing vegetarian options:"
$response2 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Do you have any vegetarian burgers? What vegetarian options are available?"}'
Write-Output $response2.message

# Test 3: Delivery hours from FAQ
Write-Output "`n3. Testing delivery hours (FAQ knowledge):"
$response3 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "What are your delivery hours and how long does delivery take?"}'
Write-Output $response3.message

# Test 4: Specific burger details
Write-Output "`n4. Testing specific burger details (BBQ Bacon Deluxe):"
$response4 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Tell me about the BBQ Bacon Deluxe burger - price, ingredients, and calories"}'
Write-Output $response4.message

Write-Output "`n=== Test Complete ==="
