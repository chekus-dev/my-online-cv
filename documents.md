---
title: "The MySQL bug that turned out to be AppArmor"
date: 2026-10-04
summary: "A process I couldn't kill, even as root, and what the kernel log said about it."
---

I started my budget tracker with the smallest possible piece: one Go file that connects to a local MySQL database and prints `connected to database`. Nothing else. That step took longer than the rest of the first version combined, and none of the delay was Go.

## It started with a missing service

The install had left `mysql-common` in a "removed but not purged" state. `systemctl` couldn't find a `mysql.service` unit at all, so there was nothing to start.

I reinstalled. Root authentication then failed over and over. MySQL 8.4 no longer enables the `mysql_native_password` plugin by default, and the setup instructions I was following assumed it did. I switched to `caching_sha2_password`.

## The process that wouldn't die

While recovering, I had started `mysqld` in `--skip-grant-tables` mode. Then I couldn't stop it. Not even root could kill it.

A process that ignores root isn't normally a permissions problem in the usual sense. So I looked at the kernel log:

```bash
sudo dmesg | grep -i apparmor
```

AppArmor was actively denying the kill signal, at the kernel level. That's why root made no difference. It's an easy detail to overlook when all you see is a process that simply won't die.

## What fixed it

A full reinstall from a clean state:

1. Purge MySQL completely.
2. Remove its data directory.
3. Reinitialize with `mysqld --initialize-insecure`.
4. Reset the root password, and confirm each step worked before moving to the next.

That last point is the real lesson. Each step was verified before I built on it, so when something failed I knew exactly which step had caused it.

## What I took from it

- **Read the kernel log when something is impossible.** If a process ignores root, ask what is above root.
- **Check the defaults of the version you installed.** Instructions age. MySQL 8.4 changed an authentication default that older guides still assume.
- **Prove the connection before writing application code.** I tested the database from the command line before adding any HTTP code, so database problems and web problems never got tangled together.

I later moved the app off local MySQL to hosted PostgreSQL, which meant translating the SQL as well. That's a separate post. The app is live at [budget-tracker-1-svws.onrender.com](https://budget-tracker-1-svws.onrender.com/), and the source is on [GitHub](https://github.com/chekus-dev/budget-tracker).