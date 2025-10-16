# Function to initialize repository with master and develop branches
function Initialize-GitBranches {
    $branches = git branch | ForEach-Object { $_.TrimStart('* ') } | Where-Object { $_ }
    
    if ($branches.Count -eq 0) {
        Write-Host "`nNo branches found. Initializing repository with master and develop branches..."
        
        # Create and switch to master branch
        git checkout -b master
        # Create initial commit if needed if remote only has main
        git fetch
        if (git remote show origin | Select-String -Pattern "main") {
            Write-Host "Creating initial commit..."
            git commit --allow-empty -m "Initial commit"
        }
        # Create and push develop branch
        git checkout -b develop
        
        # Push both branches to remote
        git push -u origin master
        git push -u origin develop
        
        Write-Host "Repository initialized with master and develop branches"
        return $true
    }
    return $false
}

# Fetch latest changes from remote
Write-Host "Fetching latest changes from remote..."
git fetch
Write-Host "Fetch completed`n"

# Check and initialize branches if needed
$initialized = Initialize-GitBranches
if ($initialized) {
    Write-Host "`nPlease run the script again to commit your changes."
    exit
}

# Function to select branch
function Select-GitBranch {
    Write-Host "Available branches (local and remote):"
    $branches = git branch -a | ForEach-Object { $_.TrimStart('* ').TrimStart('remotes/origin/') } | Where-Object { $_ -and $_ -ne 'HEAD' } | Sort-Object -Unique
    $branches | ForEach-Object { Write-Host "  $_" }
    
    do {
        $selection = Read-Host "Enter branch name"
        $branch = $branches | Where-Object { $_ -eq $selection }
        if (-not $branch) {
            Write-Host "Invalid branch name. Please try again."
        }
    } until ($branch)
    
    Write-Host "Selected branch: $branch"
    return $branch
}

# Get current branch
$current_branch = git branch --show-current
Write-Host "Current branch: $current_branch"

# Ask for commit message
do {
    $commit_message = Read-Host "Enter commit message"
} until ($commit_message)

# Show status and ask for confirmation
git status
$confirm = Read-Host "`nCommit these changes? (y/n)"

if ($confirm -ne "y") {
    Write-Host "Commit cancelled"
    exit
}

# Select target branch
Write-Host "`nSelect target branch:"
$branch = Select-GitBranch

# Commit and push
git add .
git commit -m $commit_message

# If current branch is different from target, ask to switch
if ($branch -ne $current_branch) {
    $switch_confirm = Read-Host "`nSwitch to $branch and merge changes? (y/n)"
    
    if ($switch_confirm -eq "y") {
        git checkout $branch
        git merge $current_branch
    }
}

# Ask to push
$push_confirm = Read-Host "`nPush changes to remote? (y/n)"

if ($push_confirm -eq "y") {
    git push origin $branch
    Write-Host "Changes pushed successfully"
} 