RejseplanenCLI
==============

A CLI version of Rejseplanen

usage: rp [-h] [-t TTIME] [-d TDATE] [-s {depart,arrive}] From Destination

Rejseplanen CLI.

positional arguments:
  From                  The station to travel from
  Destination           The destination.

optional arguments:
  -h, --help            show this help message and exit
  -t TTIME, --time TTIME
                        Time of journey in the format H:M
  -d TDATE, --date TDATE
                        Date of journey in the format H:M
  -s {depart,arrive}, --sort {depart,arrive}
                        Selects time after arrive
