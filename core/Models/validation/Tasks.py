import re
from tasks.models import *
from core.Models import Tasks


class Standard:
    record = {}


    def __init__(self, pk):
        # some logic
        records = CRUD.read(['all'], {id: pk})

        if records:
            record = records[0]
            self.record['tid'] = record.tid
            self.record['did'] = record.idd
            self.record['lid'] = record.lid
            self.record['sid'] = record.sid
            self.record['vid'] = record.vid
            self.record['aid'] = record.aid

            self.record['description'] = record.description
            self.record['deadline'] = record.deadline
            self.record['status'] = record.status
            self.record['visibility'] = record.visibility
            self.record['assignor'] = record.assignor
            self.record['assignee'] = record.assignee



    def validate(self, record):

        pattern = r"^[a-zA-Z]{3,10}$" # Using a raw string is a common Python practice

        test_strings = ["abc", "python", "toolongword", "ab", "abc1", "fine"]

        for s in test_strings:
            if re.fullmatch(pattern, s):
                print(f"'{s}' is a valid string.")
            else:
                print(f"'{s}' is NOT a valid string.")