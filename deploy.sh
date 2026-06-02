#!/bin/bash
# ============================================================
# SCIENCE-APPS DEPLOY-SKRIPT
# Führt Commit + Push auf main & gh-pages aus
# Autor: Licht und Schatten
# Datum: 02.06.2026 - Loop R2.31
# ============================================================
set -e

cd "$(dirname "$0")"
echo "🔍 Aktuelles Verzeichnis: $(pwd)"

# 1. Status prüfen
echo ""
echo "📋 Git Status:"
git status --short

# 2. Alles adden und committen
echo ""
echo "📦 Commit erstellen..."
git add -A
git commit -m "Blog #37 + #38: KI für Autoren & Schriftsteller + Nachhaltige Geldanlage & ETFs | Sitemap + Blog-Index aktualisiert (36→38) | Autor: Licht und Schatten"

# 3. Remote auf HTTPS setzen (für CI/cron ohne SSH)
REMOTE=$(git remote get-url origin)
if [[ "$REMOTE" == git@* ]]; then
    echo "🔄 Remote auf HTTPS umstellen..."
    git remote set-url origin https://github.com/affirmationpositiv-sudo/science-apps.git
fi

# 4. Auf main pushen (braucht GH_TOKEN oder gh auth)
echo ""
echo "🚀 Push zu main (HTTPS)..."

if [ -n "$GH_TOKEN" ]; then
    echo "GH_TOKEN gefunden – pushen..."
    git push "https://$GH_TOKEN@github.com/affirmationpositiv-sudo/science-apps.git" main
    echo "🚀 Push zu gh-pages..."
    git push "https://$GH_TOKEN@github.com/affirmationpositiv-sudo/science-apps.git" main:gh-pages
elif command -v gh &>/dev/null && gh auth status &>/dev/null; then
    echo "gh CLI authentifiziert – pushen..."
    git push origin main
    echo "🚀 Push zu gh-pages..."
    git push origin main:gh-pages
else
    echo "❌ KEINE AUTHENTIFIZIERUNG GEFUNDEN!"
    echo "   SSH-Key: nicht in GitHub autorisiert"
    echo "   GH_TOKEN: nicht gesetzt"
    echo "   gh CLI: nicht eingeloggt"
    echo ""
    echo "📋 Zum Deployen benötigst du:"
    echo "   Option 1: SSH-Key auf GitHub registrieren:"
    echo "     cat ~/.ssh/github_ed25519.pub"
    echo "     → Auf https://github.com/settings/keys hinzufügen"
    echo "   Option 2: GH_TOKEN setzen:"
    echo "     export GH_TOKEN=ghp_..."
    echo "   Option 3: gh auth login"
    echo ""
    echo "📦 Content ist bereit zum Deploy. Führe aus:"
    echo "   cd $(pwd) && bash deploy.sh"
    exit 1
fi

echo ""
echo "✅ DEPLOY KOMPLETT!"
echo "   Live: https://affirmationpositiv-sudo.github.io/science-apps/"
echo "   Blog #37: https://affirmationpositiv-sudo.github.io/science-apps/blog/ki-autoren-schriftsteller-2026.html"
echo "   Blog #38: https://affirmationpositiv-sudo.github.io/science-apps/blog/nachhaltige-geldanlage-etf-2026.html"

# 6. Prüfen ob Seiten live sind
echo ""
echo "⏳ Warte auf Deployment..."
sleep 10
echo "   Main: $(curl -sI https://affirmationpositiv-sudo.github.io/science-apps/ | head -1)"
echo "   Blog #37: $(curl -sI https://affirmationpositiv-sudo.github.io/science-apps/blog/ki-autoren-schriftsteller-2026.html | head -1)"
echo "   Blog #38: $(curl -sI https://affirmationpositiv-sudo.github.io/science-apps/blog/nachhaltige-geldanlage-etf-2026.html | head -1)"
