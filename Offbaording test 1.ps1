# Function to prompt for user email
function Get-UserEmail {
  Write-Host "Enter the email address of the user to be offboarded:"
  $userEmail = Read-Host
  return $userEmail
}

# Get user email from function
$userEmail = Get-UserEmail

# Activate User, some commands needs accounts to be 'active' to be able to work
# User will be suspended again after commands have completed 

Write-Host "Unsuspending $userEmail..."
gam unsuspend user $userEmail 

# Prompt to delete all calendar events
$confirmDeleteEvents = Read-Host "Delete all calendar events for $userEmail? (y/n)"
if ($confirmDeleteEvents -eq "y" -or $confirmDeleteEvents -eq "Y") {
    gam calendar $userEmail wipe events 
}  else { 
    Write-host "Keeping calendar events for $userEmail"
}

# Reset users password
Write-Host "Ressetting the users password..."
gam update user $userEmail password blocklogin

Start-Sleep -Seconds 3 

# Sign the user out of all web and device sessions
Write-Host "Signing the user out of all sessions"
gam user $userEmail signout

# Suspend user from google 
Write-Host "Suspending $userEmail..."
gam suspend user $userEmail 

Start-Sleep -Seconds 3

# Prompt remove user from all groups 
$confirmRemoveGroups = Read-Host "Remove $userEmail from all groups? (y/n): "
if ($confirmRemoveGroups -eq "y" -or $confirmRemoveGroups -eq "Y") {
    gam user $userEmail delete groups
    Write-Host "All groups removed from $userEmail"
}  else {
    Write-Host "Keeping $userEmail's groups"
}

# Backup user email using GYB
Write-Host "Backing up emails for $userEmail to admin..."
gyb --email $userEmail --service-account --local-folder "H:\My Drive\Ex-Employee Email Backups\$userEmail"

# Transfer user's Google Drive using GAM
Write-Host "Transferring user's Google Drive..."
gam user $userEmail transfer drive admin@tripadeal.com.au 

# Prompt deletion of user 
$confirmDeleteUser = Read-Host "Do you wish to delete this user? (y/n)"
if ($confirmDeleteUser -eq 'y' -or $confirmDeleteUser -eq 'Y') {
    Write-Host "Deleting the user... licence made avaialble. Account will be permanatley deleted in 20 days"
    gam delete user $userEmail
} else {
    Write-Host "User will NOT be deleted"
}

Start-Sleep -Seconds 2

# Confirmation message
Write-Host "Offboarding process for $userEmail completed!"