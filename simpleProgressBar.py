
import sys

'''========================== Progress Bar fantasticó ======================'''

def progressBar(prgrs, prgrsTot, n=2, elapsedTime=None):
    '''
    A very simple progress bar fit for command line printing.
    Has an option to decide the length and detail of the bar
    as well as option to show estimated time of finishing. Also
    has a cute little ASCII spinning wheel for "extra annoyance".
    
    :param  prgrs: The value representing the current progress of
            the program the progress bar represents. 
    :type   prgrs: int 
    :param  prgrsTot: The value representing the end of the progress
            (100%). The parameter 'prgrs' will be compared to this
            with equation *prgrs/prgrsTot* to calculate how much of 
            the progress is done.
    :type   prgrsTot: int
    :param  n: The divider deciding how long the progress bar will
            be on the screen. I.e. the number of characters the bar
            consists of. (Calculated by: *num_of_char = 100/n*). 
            Defaults to 2.
    :type   n: int
    :param  elapsedTime: Time since the program started running.
            Note that a timer should be initiated for this to be
            used. If omitted, the progress bar won't update the
            eta/elapsed time fields.
    :type   elapsedTime: int
    :returns: Nothing
    ''' 
    
    # Also has a rudimentary spin wheel for extra annoyance!
    spinList = ["\\","|", "/", "-"]
    progress = prgrs/prgrsTot*100
    
    # Average based calculation that of the estimated time
    # when program finishes. 
    if elapsedTime == None:
        etaAppr = ''
    else:
        avgRt = elapsedTime/(prgrs + 1)
        etaAppr_s = (prgrsTot-prgrs)*avgRt
        hs, rem = divmod(etaAppr_s, 3600)
        mins = rem/60
        if not min and not hs:
            etaAppr = "Less than a minute "
        else:
            etaAppr = ''.join(['Time Left appr:', str(int(hs)), \
                               'h ', str(int(mins)), 'm '])
    
    # Updating the progress bar
    sys.stdout.write ( '\r[{0}{1}] {2} {3:.2f}%  {4}'.format(\
                        '|'*int((progress/n)), \
                        ' '*int(100/n-int(progress/n)),\
                        spinList[int(prgrs)%4], \
                        progress, etaAppr) )
    sys.stdout.flush()


