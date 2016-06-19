Title: Git Ignorin'
Slug: git-ignorin
Date: 2015-06-26 10:07
Modified: 2015-07-03 13:25
Authors: Daniel Rothenberg
 
It gets really old having to create a site-specific `.gitignore` anytime I start a new project. It's especially troublesome since I tend to access the same repository when it's mounted on different filesystems, creating all sorts of superfluous, useless files (I'm talking about you, **.DS_Store**). Luckily, [gitignore.io](https://www.gitignore.io) has your back, and can quickly generate lists of ignorable files from many different operating systems, editors, and programming languages. Very useful!

**OSX .gitignore**
``` bash
### OSX ###
.DS_Store
.AppleDouble
.LSOverride

# Icon must end with two \r
Icon


# Thumbnails
._*

# Files that might appear in the root of a volume
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns

# Directories potentially created on remote AFP share
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk
```
