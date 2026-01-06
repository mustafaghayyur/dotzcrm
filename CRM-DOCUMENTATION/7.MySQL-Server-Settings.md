## MYSQL Server Settings

While every project, and organization has their own guidelines on database servers, we require the following settings to ensure Dotz CRM runs smoothely.

### In the my.cnf file:
Please add these conditions under:
[mysqld]
default-time-zone = "+00:00"


### Timezone-settings:

Timezones on the following elements should be UTC for Dotz CRM + PM software to function correctly:

1) MySQL Server -> should be explicitly set to UTC timezone (+00:00). As we stipulated with the above my.cnf file setting.

2) MySQL Client -> the mysql client(s) interacting with the database should ideally also be set to UTC timezone, though since we use DateTime columns, client's settings should not impact the end result much.

3) The Web server -> Django's timezone aware settings have been set to UTC timezone, please do not change these settings, so Django and MySQL work within the same timezone.

4) The User interacting with the Dotz CRM + PM Software. The user's activities and timestamps will be automatically converted on the front-end by our application. What the user sees, interms of timestamps, will always be in local time.

MySQL server, (ideally) MySQL client, and Django's timezone aware settings found in settings.py are most critical to keep the system's records accurate.

To check what your mysql server timezones are set to, you can login to the mysql server with an appropriate privilaged account and run:
 > SELECT @@GLOBAL.time_zone, @@SESSION.time_zone;

 The results will verify if your MySQL server is set to operate with the data correctly.
