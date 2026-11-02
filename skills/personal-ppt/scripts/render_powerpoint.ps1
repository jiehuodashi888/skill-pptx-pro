<#
Render a PPTX through installed desktop PowerPoint, opened read-only.
Usage: powershell -File render_powerpoint.ps1 -Pptx FILE -Output NEW_DIRECTORY
Requires Windows, PowerPoint, and an interactive desktop account.
See ../references/production.md. Never treats rendering as visual approval.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Pptx,
    [Parameter(Mandatory=$true)][string]$Output,
    [ValidateRange(640,3840)][int]$Width = 1600
)
$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $Pptx).Path
if ([IO.Path]::GetExtension($sourcePath) -ine '.pptx') { throw 'Input must be a PPTX file.' }
$outputPath = [IO.Path]::GetFullPath($Output)
if (Test-Path -LiteralPath $outputPath) { throw 'Output exists; use a new directory to avoid stale images.' }
$app = $null
$deck = $null
$ownedSession = $false
try {
    $app = New-Object -ComObject PowerPoint.Application
    $ownedSession = ($app.Presentations.Count -eq 0)
    $deck = $app.Presentations.Open($sourcePath, -1, 0, 0)
    New-Item -ItemType Directory -Path $outputPath | Out-Null
    $height = [int][Math]::Round($Width * $deck.PageSetup.SlideHeight / $deck.PageSetup.SlideWidth)
    $pages = @()
    for ($i = 1; $i -le $deck.Slides.Count; $i++) {
        $name = 'slide-{0:D2}.png' -f $i
        $imagePath = Join-Path $outputPath $name
        $slide = $deck.Slides.Item($i)
        try { $slide.Export($imagePath, 'PNG', $Width, $height) }
        finally { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($slide) }
        if (!(Test-Path -LiteralPath $imagePath) -or (Get-Item -LiteralPath $imagePath).Length -eq 0) {
            throw "Rendering failed for slide $i"
        }
        $pages += @{page=$i; file=$name; sha256=(Get-FileHash -LiteralPath $imagePath -Algorithm SHA256).Hash.ToLower()}
    }
    $manifest = @{
        schema_version=1; renderer='Microsoft PowerPoint'; renderer_version=$app.Version
        pptx_sha256=(Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLower()
        width=$Width; height=$height; pages=$pages; visual_review='pending'
    }
    $json = $manifest | ConvertTo-Json -Depth 6
    [IO.File]::WriteAllText((Join-Path $outputPath 'render-manifest.json'), $json, (New-Object Text.UTF8Encoding($false)))
    Write-Output $json
} finally {
    if ($null -ne $deck) {
        $deck.Close()
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($deck)
    }
    if ($null -ne $app) {
        if ($ownedSession -and $app.Presentations.Count -eq 0) { $app.Quit() }
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
    }
}
