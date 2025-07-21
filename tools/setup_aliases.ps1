# Script de configuration des fonctions GESTIA
# A executer dans PowerShell : . .\tools\setup_aliases.ps1

Write-Host "Configuration des fonctions GESTIA..." -ForegroundColor Green

# Fonctions pour les commandes principales
function gestia-status { & python tools/manage_env.py status }
function gestia-migrate { & python tools/manage_env.py migrate }
function gestia-reset { & python tools/manage_env.py reset }
function gestia-run { & python tools/manage_env.py run }
function gestia-generate { & python tools/manage_env.py generate }

# Fonctions pour les outils de developpement
function gestia-explore { & python tools/tools/db/explore_db.py }
function gestia-create-migration { & python tools/tools/db/create_migration.py }

Write-Host "Fonctions configurees !" -ForegroundColor Green
Write-Host ""
Write-Host "Commandes disponibles :" -ForegroundColor Yellow
Write-Host "  gestia-status          - Voir le statut de l'environnement"
Write-Host "  gestia-migrate         - Appliquer les migrations"
Write-Host "  gestia-reset           - Reinitialiser la base de donnees"
Write-Host "  gestia-run             - Lancer l'application"
Write-Host "  gestia-generate        - Generer des donnees de test"
Write-Host "  gestia-explore         - Explorer la base de donnees"
Write-Host "  gestia-create-migration - Creer une nouvelle migration"
Write-Host ""
Write-Host "Pour recharger les fonctions : . .\tools\setup_aliases.ps1" -ForegroundColor Cyan 