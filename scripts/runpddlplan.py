
class PDDLPlanOutputIterator:

    def __init__(self, planfilename):
        self.iter=0
        f = open(planfilename,'r')
        self.line = f.read()
        i = self.line.find('(output)')
        if i>=0:
            self.line = self.line[i+8:] # remove heading text

        print(self.line)
        f.close()

    def next(self):
        i1 = self.line[self.iter:].find('(')
        i2 = self.line[self.iter:].find(')')
        if (i1<0 or i2<0):
            return ''
        r = self.line[self.iter+i1:self.iter+i2+1]
        self.iter += i2+1
        return r



def executeAction(a,p):
    # Implement exection of action a with parameters p
    print("Execute: action %s with parameters %s" %(a,p))


if __name__=='__main__':

    planfilename = '../plans/plan1.pddloutput' # name of file containing the plan output

    pit = PDDLPlanOutputIterator(planfilename)

    pp = '' # Python program
    r = '*'
    while (r!=''):
        r = pit.next() # get next PDDL action (A p1 p2 ... pn) from plan file
        if r!='':
            a = r[1:len(r)-1] # remove parenthesis
            v = a.split(' ') # split parameters
            if (v[0]==':action'): # remove final stuff in the file
                break
            p = '' # build parameters list separated by _ -> p1_p2_..._pn
            if (len(v)>1):
                for i in range(1,len(v)-1):
                    p = p + v[i] + "_";
                p = p + v[-1];
            pp += "executeAction('%s','%s')\n" %(v[0],p)  # add Python statement

    print('Python program:')
    print(pp)
    exec(pp)


