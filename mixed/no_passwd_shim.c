/* LD_PRELOAD shim for SpiceBind. libngspice's ngSpice_Init() dereferences
 * getpwuid(getuid()) without checking it, to find ~/.spiceinit. In this
 * container the user (uid 1000) has no /etc/passwd entry, so it crashes with
 * a bus error or segfault before printing anything. Not needed where the
 * user has a passwd entry. */
#include <pwd.h>
#include <stdlib.h>
#include <sys/types.h>

struct passwd *getpwuid(uid_t uid) {
  static struct passwd p;
  const char *home = getenv("HOME");
  p.pw_name = "user";
  p.pw_passwd = "x";
  p.pw_uid = uid;
  p.pw_gid = uid;
  p.pw_gecos = "";
  p.pw_dir = (char *)(home ? home : "/tmp");
  p.pw_shell = "/bin/sh";
  return &p;
}
