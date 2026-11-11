#!/usr/bin/env python3
"""Replace the default rendezvous server and public key in hbb_common with the
values from the RENDEZVOUS_SERVER and RS_PUB_KEY environment variables."""
import os
import re
import sys

PATH = "libs/hbb_common/src/config.rs"
server = os.environ.get("RENDEZVOUS_SERVER", "").strip()
key = os.environ.get("RS_PUB_KEY", "").strip()
if not server or not key:
    sys.exit("RENDEZVOUS_SERVER and RS_PUB_KEY secrets must both be set")
if not re.fullmatch(r"[A-Za-z0-9.:\-\[\]]+", server) or not re.fullmatch(r"[A-Za-z0-9+/=]+", key):
    sys.exit("RENDEZVOUS_SERVER or RS_PUB_KEY contains unexpected characters")

with open(PATH, encoding="utf-8") as f:
    src = f.read()
src, n1 = re.subn(
    r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];',
    'pub const RENDEZVOUS_SERVERS: &[&str] = &["%s"];' % server,
    src,
)
src, n2 = re.subn(
    r'pub const RS_PUB_KEY: &str = "[^"]*";',
    'pub const RS_PUB_KEY: &str = "%s";' % key,
    src,
)
if n1 != 1 or n2 != 1:
    sys.exit("config.rs layout changed: servers=%d key=%d replacements" % (n1, n2))
with open(PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write(src)
print("Baked custom server and key into", PATH)
