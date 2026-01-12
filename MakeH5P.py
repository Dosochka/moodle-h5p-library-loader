#!/usr/bin/env python3
"""
make_h5p.py
To create .h5p (zip) from the H5P library directory so
that the archive contains the library's root directory (for example, H5P.InteractiveBook-1.11/...)
"""

import os
import zipfile
import argparse
import sys

def make_h5p(dir_path: str, out_path: str = None, skip_hidden=True):
    dir_path = os.path.abspath(dir_path)
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory not found: {dir_path}")

    base = os.path.basename(dir_path.rstrip(os.sep))
    parent = os.path.dirname(dir_path.rstrip(os.sep))

    if out_path is None:
        out_path = os.path.join(parent, base + '.h5p')
    out_path = os.path.abspath(out_path)

    # Try to use deflate; fallback to ZIP_STORED if zlib not available
    compression = zipfile.ZIP_DEFLATED if 'zlib' in sys.modules or hasattr(zipfile, 'ZIP_DEFLATED') else zipfile.ZIP_STORED

    with zipfile.ZipFile(out_path, 'w', compression=compression) as zf:
        # walk the folder and write files with arcname relative to parent,
        # so top-level entry in zip is base/
        for root, dirs, files in os.walk(dir_path):
            # optionally skip hidden dirs (like .git)
            if skip_hidden:
                # mutate dirs in-place to avoid walking them
                dirs[:] = [d for d in dirs if not d.startswith('.')]
            # write empty directory entry if there are no files and no subdirs
            rel_root = os.path.relpath(root, parent)  # starts with base/...
            if rel_root == '.':
                rel_root = base
            # ensure directory entry ends with '/'
            if not files and not dirs:
                zinfo = zipfile.ZipInfo(rel_root.rstrip('/') + '/')
                # mark as directory (external_attr) optional; not required for Moodle
                zf.writestr(zinfo, b'')
            for fname in files:
                if skip_hidden and fname.startswith('.'):
                    continue
                if fname.endswith('~') or fname.endswith('.bak'):
                    continue
                full_path = os.path.join(root, fname)
                arcname = os.path.join(rel_root, fname)
                # normalize to forward slashes (zip standard)
                arcname = arcname.replace(os.path.sep, '/')
                zf.write(full_path, arcname)
    return out_path

def list_top_level(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        entries = set()
        for n in zf.namelist():
            top = n.split('/', 1)[0]
            entries.add(top)
        return sorted(entries)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Create H5P (.h5p) from library folder preserving top-level dir')
    p.add_argument('folder', help='Path to library folder (e.g. H5P.InteractiveBook-1.11)')
    p.add_argument('-o','--out', help='Output path (.h5p). If omitted, creates <foldername>.h5p next to folder')
    p.add_argument('--no-skip-hidden', dest='skip', action='store_false', help='Do not skip hidden files/dirs')
    args = p.parse_args()

    out = make_h5p(args.folder, args.out, skip_hidden=args.skip)
    print(f"Created: {out}")
    tops = list_top_level(out)
    print("Top-level entries in archive:", tops)
    # Quick check: ensure the archive top-level contains exactly the base folder (recommended)
    base = os.path.basename(os.path.abspath(args.folder).rstrip(os.sep))
    if base not in tops:
        print("Warning: archive top-level does not contain expected root folder:", base)
    else:
        print("Archive root OK -> contains folder:", base)
