
# Define Django app names
$apps = @("activity", "ap2v_courses", "ap2v_e_store","batches", "blogs" ,"bluejeans","chats", "classroom", "communication", "core", "courses", "demo", "enquiries", "enrolls", "events", "feedback", "followups", "gallery", "home", "instructors", "landing_page", "learning_paths", "payment", "promotions", "recording_sessions", "reporting", 
"seo", "sitemaps", "django_chatter", "testimonials", "users", "website")

# Loop through each app and remove __pycache__ and migrations folders
foreach ($app in $apps) {
    # Remove __pycache__ folders
    Get-ChildItem -Path $app -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

    # Remove migrations folders (but keep __init__.py if it exists)
    if (Test-Path "$app\migrations") {
        Get-ChildItem -Path "$app\migrations" -Exclude "__init__.py" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Deleted __pycache__ and migrations folders from all apps."
