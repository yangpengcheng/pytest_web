"""
Command line
"""


class Command:
    def __init__(self, comm, arg):
        self.comm = comm
        self.r_arg = arg.r_arg
        self.p_arg = arg.p_arg
        self.d_arg = arg.d_arg
        self.output = []
        self.output = self._execute()

    def _execute(self):
        import os

        args = filter(lambda x: True if x else False,
                      [self.r_arg, self.p_arg, self.d_arg])
        args = ' '.join(args)

        cmd = '{} {}'.format(self.comm, args) if args else self.comm
        print('执行指令', cmd)

        lines = os.popen(cmd=cmd).readlines()

        return [line.strip('\n').encode('gbk').decode('utf-8') for line in lines]
