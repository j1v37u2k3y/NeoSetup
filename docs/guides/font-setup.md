# Nerd Font Setup for Terminal Icons

## Installed Fonts

NeoSetup has installed the following Nerd Fonts:

- MesloLGS Nerd Font (recommended for Powerlevel10k)
- Fira Code Nerd Font (alternative option)

## Terminal.app Configuration

1. Open Terminal.app
2. Go to **Terminal → Settings** (or Preferences on older macOS)
3. Select your profile (e.g., "Basic", "Pro", or custom)
4. Click the **Text** tab
5. Click **Change...** next to Font
6. Search for one of these fonts:

- **MesloLGS NF** (recommended)
- **MesloLGS Nerd Font**
- **MesloLGSDZ Nerd Font**

7. Select the font and set size to 12-14pt
8. Click **Select**
9. Close and restart Terminal

## iTerm2 Configuration

1. Open iTerm2
2. Go to **iTerm2 → Settings** (⌘,)
3. Select **Profiles** → **Text**
4. Click **Change Font**
5. Select **MesloLGS NF** or **MesloLGS Nerd Font**
6. Set size to 12-14pt

## Troubleshooting

### Icons Still Not Showing

If icons still appear as question marks:

1. **Restart font service:**

   ```bash
   killall -HUP fontd
   ```

2. **Clear font cache (if needed):**

   ```bash
   sudo atsutil databases -remove
   sudo atsutil server -shutdown
   sudo atsutil server -ping
   ```

3. **Verify font installation:**

   ```bash
   ls ~/Library/Fonts/ | grep -i meslo
   ```

4. **Restart Terminal.app completely:**

- Quit Terminal (⌘Q)
- Reopen Terminal

### Alternative: Manual Font Installation

If Homebrew fonts aren't working:

1. Download directly from Nerd Fonts:

   ```bash
   curl -fLo ~/Downloads/Meslo.zip https://github.com/ryanoasis/nerd-fonts/releases/download/v3.1.1/Meslo.zip
   unzip ~/Downloads/Meslo.zip -d ~/Downloads/Meslo
   ```

2. Open Font Book.app
3. Drag the .ttf files from ~/Downloads/Meslo to Font Book
4. Click "Install"

## Testing Icons

After configuring your terminal font, test with:

```bash
echo " Git branch icon"
echo " Folder icon"
echo " Home icon"
echo "󰊢 GitHub icon"
echo " Docker icon"
```

If you see the icons correctly, your font is properly configured!
