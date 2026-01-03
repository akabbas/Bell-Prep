#!/bin/bash

# Add repository description using GitHub CLI
# Requires: gh cli to be installed and authenticated

DESCRIPTION="Production-grade procurement automation system for Bell Textron with SAP Ariba integration, ITAR compliance, and AS9100 certification tracking"

echo "Adding description to Bell-Prep repository..."
gh repo edit akabbas/Bell-Prep --description "$DESCRIPTION" --visibility public

if [ $? -eq 0 ]; then
    echo "✅ Description added successfully!"
else
    echo "❌ Failed to add description. Make sure you have 'gh' CLI installed and are authenticated."
    echo "Install: https://cli.github.com/"
fi


