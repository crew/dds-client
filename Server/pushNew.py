import os, sys
pipe_name = 'dds-pipe'

if __name__ == '__main__':
    pipeout = os.open(pipe_name, os.O_WRONLY)
    os.write(pipeout, sys.argv[1] + '\n')
    os.close(pipeout)
