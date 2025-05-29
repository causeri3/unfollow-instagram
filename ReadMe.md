# Unfollow Instagram Scripts

--- 
See who doesn't follow you back and unfollow them manually.

---

## You got two alternatives:

### 1. Download your data from instagram:
   * **You need to:**
       * Request your data from Instagram in JSON format. [Click here.](https://www.instagram.com/accounts/login/?next=https%3A%2F%2Faccountscenter.instagram.com%2Finfo_and_permissions%2Fdyi%2F%3F__coig_login%3D1)
       * Put the folder *followers_and_following* inside the directory of this repository (the folder will be somewhere in the folder structure of the data you downloaded, depending on what you clicked.)
       * Install dependencies (see below)
       * Run
         * with uv
          `uv run unfollow_manual_download.py -d 7`

         * standard
          `python unfollow_manual_download.py -d 7`
   * **Pros:**
     * This way you can choose how recent the followed accounts to be compared with shall be
### 2. Extract with an instagram account:
(optimally not your main important account)
   * **You need to:**
     * Have or make an unimportant instagram profile
     * Install dependencies (see below)
     * Run
       * with uv
        `uv run unfollow_with_account.py -t target_account -u username_scrap_account -p password_scrap_account`

       * standard
        `python unfollow_with_account.py  -t target_account -u username_scrap_account -p password_scrap_account`
  * **Pros:**
    * Automisable (Once extended with login to the actual account, the unfollowing could be automated as well and the whole thing could be scheduled by a cron job)
    * No waiting for instagram to give you your data


## Dependencies
### Python
I tried it with python 3.8 & 3.13  - you could peg it with `uv venv --python 3.13` but properly not necessary

### Python packages 
You can install them via

`pip install -r requirements.txt`

Or even better if you use [uv](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1), run in the directory of this repo:
```sh
uv venv
uv pip install -r requirements.txt
```

### Args
See all arguments:
* `python unfollow_with_account.py --help`
* `python unfollow_manual_download.py --help`

---
Note: Make sure you don't unfollow too many accounts in one go. You can google the limits.