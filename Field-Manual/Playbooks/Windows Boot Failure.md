---
type: playbook
area: "Windows Administration"
tags: [windows, boot, uefi, bcd, bitlocker, winre, recovery, triage, incident]
status: working
---

# Windows Boot Failure

> **Area:** [[Windows Administration]]

Windows doesn't reach the login screen: it drops into the recovery environment (WinRE),
shows a boot error code, boots the wrong OS, or loops. Work through this playbook to
identify which stage of the boot chain failed and repair it — usually without reinstalling.

---

## The boot chain (know where it broke)

```
UEFI firmware → NVRAM boot entry ("Windows Boot Manager")
  → ESP: \EFI\Microsoft\Boot\bootmgfw.efi → BCD store
    → winload.efi → NT kernel + boot-critical drivers → session start
```

| Failure stage | Typical symptom |
|---|---|
| Firmware / NVRAM | Boots another OS (GRUB, old install), "no bootable device", drops to UEFI shell |
| Boot manager / BCD | `0xc000000e` / `0xc0000034` "Boot Configuration Data is missing", `Bootmgr is missing` (legacy) |
| winload / kernel | `0xc0000225`, `winload.efi missing or corrupt` |
| Boot-critical driver | `INACCESSIBLE_BOOT_DEVICE` blue screen |
| Later (session) | Spins, then falls into WinRE / Startup Repair; boot loop after update |

## Situation

- Machine drops into WinRE ("Startup Repair" / *Starthilfe*) and automatic repair does nothing
- A boot error code from the table above
- Wrong OS boots, or firmware says there is nothing to boot
- Often right after: attaching/removing disks, a firmware update, a Windows update, cloning, or a BIOS settings change

## Quick triage (first 3 checks)

1. **Firmware first.** Enter UEFI setup: is **Windows Boot Manager** present and first in
   the boot order? Attaching any other bootable disk (Linux, old installs, USB sticks)
   can reorder or replace NVRAM entries — this is the most common and cheapest fix.
2. **WinRE → Advanced options → Command Prompt**, then:

```bat
bcdedit                 :: does the store load? do entries show device=unknown?
diskpart
list disk               :: all disks Online? (Offline = signature collision, Fix C)
list vol                :: ESP present (FAT32, ~100-500 MB)? Windows volume healthy (NTFS)?
exit
```

3. **Find the real OS volume.** WinRE shifts drive letters — never assume `C:`:

```bat
dir C:\Windows          :: try D:, E: ... until you find the install
```

> **BitLocker:** if the volume is encrypted, have the recovery key ready *before* touching
> boot files — repairs change the measured boot chain and will trigger a key prompt.
> Unlock inside WinRE with `manage-bde -unlock C: -RecoveryPassword <key>`.

---

## Decision branches

| Observation | Likely cause | Go to |
|---|---|---|
| Another bootloader (GRUB etc.) or wrong Windows boots | Firmware boot order changed | Fix A |
| "Windows Boot Manager" gone from firmware, `0xc000000e`, `bcdedit` fails or shows `device=unknown` | Boot files / BCD / NVRAM entry lost | Fix B |
| `diskpart` shows a disk **Offline** | Disk signature collision (clone / old install attached) | Fix C |
| `INACCESSIBLE_BOOT_DEVICE` | SATA mode changed (AHCI↔RAID) or missing storage driver | Fix D |
| Boot loop after Windows/driver update | Bad update or driver | Fix E |
| Volume shows RAW / chkdsk errors / disk noises | Filesystem or hardware damage | Fix F |
| BitLocker recovery screen every boot | Measured boot changed / TPM issue | Fix G |
| Legacy BIOS/MBR machine | MBR / boot sector damage | Fix H |

---

## Fixes

### Fix A — Firmware boot order

1. Enter UEFI setup → Boot: move **Windows Boot Manager** to the top.
2. Remove or deprioritize other bootable disks/USB media.
3. If the Windows entry has *disappeared* entirely, go to Fix B — `bcdboot` recreates it.

> Field note: merely *attaching* an old bootable SATA/NVMe disk can silently rewrite the
> NVRAM boot order or clobber the default entry. If a machine stops booting right after
> disks were added or removed, start here — the Windows install is usually fine.

### Fix B — Rebuild boot files + BCD (UEFI)

From the WinRE command prompt:

```bat
diskpart
list vol                      :: find the ESP: FAT32, ~100-500 MB, no letter
sel vol <esp-number>
assign letter=S
exit

dir C:\Windows                :: confirm the OS volume letter (may not be C:)

bcdboot C:\Windows /s S: /f UEFI
```

`bcdboot` rewrites `\EFI\Microsoft\Boot\`, rebuilds the BCD, and registers a fresh
"Windows Boot Manager" NVRAM entry. Reboot, then re-check the firmware boot order (Fix A).

If the ESP itself is damaged or missing (destructive — only on unallocated space):

```bat
diskpart
sel disk <n>
create partition efi size=260
format quick fs=fat32 label=SYSTEM
assign letter=S
exit
bcdboot C:\Windows /s S: /f UEFI
```

### Fix C — Disk offline (signature collision)

Windows takes a disk offline when two disks share the same signature — typical after
attaching a clone or an old install of the same machine.

```bat
diskpart
list disk                     :: note the Offline disk
sel disk <n>
attributes disk clear readonly
online disk                   :: Windows writes a new signature if needed
exit
```

### Fix D — INACCESSIBLE_BOOT_DEVICE

The kernel started but can't reach its own boot volume — almost always the storage driver.

1. **BIOS setting changed?** If SATA mode was switched (AHCI ↔ RAID/RST/VMD), switch it
   back. That alone fixes it.
2. **Want to keep the new mode?** Force one boot into safe mode so Windows loads and
   installs the other driver:

```bat
bcdedit /set {default} safeboot minimal
:: boot once into safe mode, then remove the flag:
bcdedit /deletevalue {default} safeboot
```

3. **New hardware / missing driver:** inject it offline:

```bat
dism /image:C:\ /add-driver /driver:X:\drivers\<storage-driver>.inf
```

### Fix E — Boot loop after an update or driver

In escalating order:

```bat
:: 1. WinRE menu: Troubleshoot -> Uninstall Updates (try quality, then feature update)

:: 2. Roll back a stuck/pending update offline:
dism /image:C:\ /cleanup-image /revertpendingactions

:: 3. Repair the component store and system files offline:
dism /image:C:\ /cleanup-image /restorehealth
sfc /scannow /offbootdir=S:\ /offwindir=C:\Windows

:: 4. Suspect a specific third-party driver? Disable it offline:
dism /image:C:\ /get-drivers            :: find the oemNN.inf name
dism /image:C:\ /remove-driver /driver:oemNN.inf
```

Safe mode via WinRE: Startup Settings → Restart → 4, or the `safeboot` flag from Fix D.

### Fix F — Filesystem corruption / failing disk

```bat
chkdsk C: /f                  :: fix filesystem errors
chkdsk C: /r                  :: + surface scan (slow; stresses a dying disk)
```

**Stop and image first** if: the volume shows **RAW**, chkdsk finds massive errors, or
the disk clicks/times out. Boot a Linux live USB and take a full image
(`ddrescue /dev/sdX /path/to/image.img mapfile`) before any further writes — chkdsk on
failing hardware can destroy what's left. Check SMART (`smartctl -a /dev/sdX`) to decide.

### Fix G — BitLocker recovery prompt every boot

- Get the recovery key: Microsoft account (aka.ms/recoverykey), AD/Entra ID, or printout.
- One-time prompts after firmware/boot-file changes are expected. If it prompts *every*
  boot: boot in with the key, then re-seal the protectors:

```powershell
Suspend-BitLocker -MountPoint C: -RebootCount 1   # re-measures the boot chain on next boot
```

- Before planned firmware updates, always suspend BitLocker first — prevents the prompt.

### Fix H — Legacy BIOS / MBR machines

```bat
bootrec /fixmbr
bootrec /fixboot              :: "access denied" on some builds -> bootsect /nt60 SYS /mbr
bootrec /scanos
bootrec /rebuildbcd
```

---

## Workarounds & gotchas

- **Getting into WinRE** when the menu won't appear: power-cut the machine during boot
  three times in a row, or boot Windows install media → *Repair your computer*.
- **Startup Repair** rarely fixes more than trivial issues, but run it once — its log at
  `C:\Windows\System32\LogFiles\Srt\SrtTrail.txt` tells you what it *found*.
- **Drive letters lie in WinRE.** Always confirm with `dir <X>:\Windows` before running
  repair commands against a volume.
- **Fast Startup** means "shut down" is really hibernation: changing hardware or
  dual-booting against a fast-started Windows corrupts filesystems. Disable with
  `powercfg /h off` on dual-boot/multi-disk machines.
- **No restore points** is the norm, not the exception — System Restore is off by default
  on many installs. Don't burn time looking for one.

## Escalation / after-action

- Nothing above works but the install is intact → **in-place upgrade repair**: boot the
  running-or-repaired Windows, run `setup.exe` from a matching ISO, keep files and apps.
  Last resort before reinstall.
- Hardware suspect → image first (Fix F), replace disk, restore from image/backup.
- Afterwards: capture `SrtTrail.txt`, note the error code, and write down *what changed
  right before* (disks attached? BIOS touched? update installed?) — the trigger is almost
  always in the last 24 hours.
- Prevention: back up the BitLocker key now, keep a Windows install USB around, and
  detach other bootable disks before poking at firmware.

## See also

- [[windows-events]] — reading the event log once the system boots again
- [[powershell]] · [[powershell-cmdlets]] — for the online follow-up work
- Concepts in the IT-Dictionary: *UEFI*, *Secure Boot*, *Measured Boot*, *TPM*
