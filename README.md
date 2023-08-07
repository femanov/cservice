## control service helpers classes

UNIX daemons adapted to control system services

- pid, log and err files in /var/tmp
- prints are redirected to log with automatic timestaps.
- "-not-daemonize" to run as console app
- can interact with systemd in order to start/stop with it correctly
- can run Qt main loop, Qt main loop with cothread if catools needed, CX scheduler main loop
- In case of CX main loop services can be controlled with Lord-service.
