# Test chat endpoint with menu question
$registerResponse = Invoke-RestMethod -Uri "http://localhost:5000/users/register" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email": "testuser5@example.com", "password": "password123", "first_name": "Test", "last_name": "User5"}'

$token = $registerResponse.access_token
Write-Output "Testing specific menu questions..."

# Test menu question
$chatResponse1 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "What burgers do you have and what are the prices?"}'

Write-Output "`nMenu Question Response:"
Write-Output $chatResponse1.message

# Test another question
$chatResponse2 = Invoke-RestMethod -Uri "http://localhost:5000/chat/" -Method POST -Headers @{"Content-Type"="application/json"; "Authorization"="Bearer $token"} -Body '{"message": "Do you have vegetarian options?"}'

Write-Output "`nVegetarian Options Response:"
Write-Output $chatResponse2.message
