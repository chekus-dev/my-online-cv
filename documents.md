---
title: "The MySQL Bug That Turned Out to Be AppArmor"
date: 2026-10-04
summary: "A process I couldn't kill, even as root, and what the kernel log revealed about it."
---

<div align="center">

![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![AppArmor](https://img.shields.io/badge/AppArmor-Linux_Security-E95420?style=flat-square&logo=linux&logoColor=white)
![Status](https://img.shields.io/badge/Status-Resolved-16a34a?style=flat-square)

</div>

<br/>

> A process that ignores `kill -9`, even as root, usually isn't a permissions problem in the normal sense. Something is sitting above root.

<br/>

I started my budget tracker with the smallest possible piece: a single Go file that connects to a local MySQL instance and prints `connected to database`. Nothing else. That one step took longer than the rest of the first version combined — and none of the delay was Go.

---

## 🧩 A Missing Service

The installation had left `mysql-common` in a "removed but not purged" state. `systemctl` couldn't find a `mysql.service` unit at all, so there was nothing to start.

I reinstalled, and root authentication failed repeatedly. MySQL 8.4 no longer enables the `mysql_native_password` plugin by default, and the setup instructions I was following assumed it did. Switching to `caching_sha2_password` resolved it.

---

## ⚠️ A Process That Wouldn't Die

While recovering, I had started `mysqld` in `--skip-grant-tables` mode — and then couldn't stop it. Not even as root.

```bash
sudo dmesg | grep -i apparmor
```

AppArmor was actively denying the kill signal at the kernel level, which is why root made no difference. It's an easy detail to miss when all you can see is a process that simply refuses to stop.

---

## 🛠️ The Fix

A full reinstall from a clean state:

| Step | Action |
|---|---|
| 1 | Purge MySQL completely |
| 2 | Remove its data directory |
| 3 | Reinitialize with `mysqld --initialize-insecure` |
| 4 | Reset the root password, confirming each step before the next |

That last point is the real lesson. Verifying each step before building on it meant that when something failed, I knew exactly where to look.

---

## 📌 What I Took From It

- **Check the kernel log when something seems impossible.** If a process ignores root, the next question is what sits above root.
- **Verify the defaults for the version installed, not the version in the guide.** Instructions age; MySQL 8.4 changed an authentication default that older walkthroughs still assume.
- **Confirm the connection before writing application code.** Testing the database from the command line first kept database issues and web-layer issues from becoming tangled together.

---

<br/>

I later migrated the app from local MySQL to hosted PostgreSQL, which meant translating the SQL as well — that's a separate post.

<div align="center">

[![Live Demo](https://img.shields.io/badge/▶_Live_Demo-budget--tracker-f97316?style=for-the-badge)](https://budget-tracker-1-svws.onrender.com/)
[![Source](https://img.shields.io/badge/Source-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/chekus-dev/budget-tracker)

</div>
