APPENDIX OF TERMS
====================

This document will hold common jargon/acronyms found through out the code base, and their meanings.

A
--


B
--


C
--
 > child-table: for each Module (Tasks, Tickets, Documents, etc) there is the main Master table, symbolizing a single Master (i.e. Task, Ticket, etc.) records. And then several children-tables which carry additional data pertaining to the master-record.
 > CT: abbreviation for child-table (see above)

D
--


E
--


F
--


G
--


H
--


I
--


J
--


K
--


L
--


M
--
 > Module: the module is a nearly stand alone section of the CRM. The originally conceptualized modules for the DotzCRM were: 
  1. Tasks Module
  2. Tickets Module (refers to customer queries/requests)
  3. Documents Module
  4. Customers Module

 > mt (or MT): stands for Master Table: usually refers to the paraent table for a module that all children tables relate to. In Tasks module, this would be the 'tasks_task' table (unless configured differently).
 > Master Table: see mt above.

 > Model: a Model with a capital M, refers not to the default django models found in each module's codebase. But the the core.Models directory. Please see README.md of that directory for more info.

N
--


O
--


P
--


Q
--
 > QuerySets: querysets hold special meaning to DotzCRM, as we rely heavily on raw queries. These queryset classes can be found in core.Models.querysets. Please see README.md in core.Models for details.


R
--



S
--
 > space: may be used in CRUD operations. Space is another term for a module. See Module above for further info.

 > settings: the settings found in core.settings. These are system-wide configurations referenced is various classes for all CRM operations.

T
--


U
--



V
--



X
--


Y
--


Z
--

