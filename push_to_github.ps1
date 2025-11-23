# PowerShell script to push to GitHub
# Replace YOUR_USERNAME with your actual GitHub username

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Multi-Agent Tourism System" -ForegroundColor Cyan
Write-Host "GitHub Push Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$username = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter repository name (default: multi-agent-tourism-system)"

if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "multi-agent-tourism-system"
}

Write-Host ""
Write-Host "Creating remote and pushing to GitHub..." -ForegroundColor Yellow

# Remove existing remote if any
git remote remove origin 2>$null

# Add remote
git remote add origin "https://github.com/$username/$repoName.git"

# Set branch to main
git branch -M main

Write-Host ""
Write-Host "IMPORTANT: First create the repository on GitHub:" -ForegroundColor Red
Write-Host "1. Go to: https://github.com/new" -ForegroundColor Yellow
Write-Host "2. Repository name: $repoName" -ForegroundColor Yellow
Write-Host "3. DO NOT initialize with README, .gitignore, or license" -ForegroundColor Yellow
Write-Host "4. Click 'Create repository'" -ForegroundColor Yellow
Write-Host ""
$continue = Read-Host "Have you created the repository? (y/n)"

if ($continue -eq "y" -or $continue -eq "Y") {
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Green
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
        Write-Host "Repository: https://github.com/$username/$repoName" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "Error pushing to GitHub. Please check:" -ForegroundColor Red
        Write-Host "1. Repository exists on GitHub" -ForegroundColor Yellow
        Write-Host "2. You have access to push" -ForegroundColor Yellow
        Write-Host "3. Your GitHub credentials are correct" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "Please create the repository first, then run this script again." -ForegroundColor Yellow
    Write-Host "Or run these commands manually:" -ForegroundColor Yellow
    Write-Host "  git remote add origin https://github.com/$username/$repoName.git" -ForegroundColor Cyan
    Write-Host "  git branch -M main" -ForegroundColor Cyan
    Write-Host "  git push -u origin main" -ForegroundColor Cyan
}

