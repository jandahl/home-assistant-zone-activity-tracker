#!/usr/bin/env bash

#
# A script to automate the version bump and release process for a Home Assistant custom component.
#
# This script performs the following actions:
# 1. Updates the version in the manifest.json file.
# 2. Commits all changes to git.
# 3. Pushes the commit to the 'master' branch.
# 4. Creates a new git tag for the specified version.
# 5. Pushes the new tag to the remote repository.
#
# After running, the user must go to GitHub to publish the release from the newly pushed tag.
#

# --- Configuration ---
MANIFEST_PATH="custom_components/zone_activity_tracker/manifest.json"
GIT_REMOTE="origin"
GIT_BRANCH="master"

# --- Functions ---

show_help() {
    echo "Usage: $(basename "$0") --version <version>"
    echo ""
    echo "Automates the process of bumping the version and creating a release tag."
    echo ""
    echo "  --version   The new version number (e.g., 1.0.4)."
    echo "  -h, --help  Show this help message."
}

show_examples() {
    echo "Examples:"
    echo "  $(basename "$0") --version 1.0.4"
}


# --- Main Script ---

# Exit immediately if a command exits with a non-zero status.
set -e

# Check if any arguments were provided
if [ "$#" -eq 0 ]; then
    show_help
    exit 1
fi

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --version)
            if [[ -z "$2" || "$2" == -* ]]; then
                echo "Error: --version requires a value." >&2
                exit 1
            fi
            VERSION="$2"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        --examples)
            show_examples
            exit 0
            ;;
        *)
            echo "Error: Unknown parameter passed: $1" >&2
            show_help
            exit 1
            ;;
    esac
    shift
done

# Check if version is set
if [ -z "$VERSION" ]; then
  echo "Error: --version argument is required." >&2
  show_help
  exit 1
fi

# Check if manifest file exists
if [ ! -f "$MANIFEST_PATH" ]; then
    echo "Error: manifest.json not found at $MANIFEST_PATH" >&2
    exit 1
fi

echo "Bumping version to $VERSION..."
# Use sed to update the version in manifest.json. The .bak extension is for macOS compatibility.
sed -i.bak 's/"version": ".*"/"version": "'''$VERSION'''"/' "$MANIFEST_PATH"
rm "${MANIFEST_PATH}.bak" # Clean up the backup file

echo "Staging and committing changes..."
git add .
git commit -m "feat: Release version $VERSION"

echo "Pushing commit to $GIT_BRANCH..."
git push "$GIT_REMOTE" "$GIT_BRANCH"

echo "Creating and pushing tag $VERSION..."
git tag -a "$VERSION" -m "Version $VERSION"
git push "$GIT_REMOTE" "$VERSION"

echo ""
echo "✅ Done."
echo "🚀 Next step: Go to GitHub and publish the release for tag $VERSION."
