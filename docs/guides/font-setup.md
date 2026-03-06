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
   curl -fLo ~/Downloads/Meslo.zip https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Meslo.zip
   unzip ~/Downloads/Meslo.zip -d ~/Downloads/Meslo
   ```

2. Open Font Book.app
3. Drag the .ttf files from ~/Downloads/Meslo to Font Book
4. Click "Install"

## Testing Icons

After configuring your terminal font, test with these commands using Nerd Font Unicode codepoints:

```bash
# Powerline symbols
printf "\ue0a0 Git branch icon\n"
printf "\ue0b0 Powerline arrow\n"

# Font Awesome icons
printf "\uf115 Folder icon\n"
printf "\uf015 Home icon\n"

# Dev icons
printf "\ue709 Docker icon\n"
printf "\ue702 Linux (Tux) icon\n"

# Material Design icons
printf "\U000f02a2 GitHub icon\n"
```

If each line shows a small icon before the label, your Nerd Font is properly configured!

**What to expect:**

- If you see distinct icons/symbols, your font is working
- If you see empty boxes, question marks, or nothing, your terminal font is not set to a Nerd Font
